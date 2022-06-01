from flask import Flask, request, render_template, url_for, redirect, jsonify
import json
import math
import jwt
import time
import hashlib
import datetime
import queue
import spider_queue
from TF_IDF import TfIdf
from mysql_query import DB
from collections import defaultdict

app = Flask(__name__, static_url_path="", static_folder="../")
app.config["ENV"] = "development"
app.config["DEBUG"] = True
app.config["KEY"] = "SECRET"
film_ls_queue = queue.Queue()
queue_is_free = True


@app.route("/")
def redirect_function():
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/preference")
def preference():
    return render_template("preference.html")


@app.route("/manage")
def manage():
    return render_template("manage.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/custom_recommendation", methods=["POST"])
def custom_recommendation():
    db = DB()
    token = request.form.get("token").strip()
    payload = jwt.decode(token, app.config["KEY"], algorithms=["HS256"])
    username = payload["data"]["username"]
    history_film_id = [item["film_id"] for item in db.select_user_history(username)]
    if len(history_film_id) == 0:
        return jsonify({"status": "error", "reason": "无浏览历史"})
    film_id_ls = db.get_film_id()
    film_keywords = []
    res = []
    for film_id in history_film_id:
        film_keywords.append(db.get_film_keywords(film_id))
    for film_id in film_id_ls:
        if film_id in history_film_id:
            continue
        tmp_keyword = db.get_film_keywords(film_id)
        res.append(
            {
                "film_id": film_id,
                "similarity": sum(
                    [
                        TfIdf.compute_cosine_similarity(tmp_keyword, keyword)
                        for keyword in film_keywords
                    ]
                )
                / len(film_keywords),
            }
        )
    res.sort(key=lambda tmp: tmp["similarity"], reverse=True)
    data = []
    for film_id in [item["film_id"] for item in res[:12]]:
        item = db.get_film_item(film_id)
        data.append(
            {
                "film_id": item["film_id"],
                "film_name": item["film_name"],
                "film_poster": item["film_poster"],
                "score": item["score"],
            }
        )
    return jsonify({"status": "success", "data": data})


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/record", methods=["POST"])
def record():
    token = request.form.get("token").strip()
    film_id = request.form.get("film_id").strip()
    payload = jwt.decode(token, app.config["KEY"], algorithms=["HS256"])
    username = payload["data"]["username"]
    if DB().insert_history(username, film_id):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "reason": "已存过"})


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username").strip()
    password = request.form.get("password").strip()
    authority = request.form.get("authority")
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if authority is not None and authority == "admin":
        if DB().user_is_exist(username, password, is_admin=True) != 1:
            return jsonify({"status": "error", "reason": "用户名或密码不正确 或 用户权限不够"})
    else:
        if DB().user_is_exist(username, password) != 1:
            return jsonify({"status": "error", "reason": "用户名或密码不正确"})
    dic = {
        "exp": datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
        "data": {"username": username},  # 内容，一般存放该用户id和开始时间
    }
    return jsonify(
        {
            "status": "success",
            "token": jwt.encode(dic, app.config["KEY"], algorithm="HS256"),
            "username": username,
        }
    )


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username").strip()
    password = request.form.get("password").strip()
    if len(username) < 4 or len(username) > 12:
        return jsonify({"status": "error", "reason": "用户名长度不符合规范"})
    if len(password) < 6 or len(password) > 12:
        return jsonify({"status": "error", "reason": "密码长度不符合规范"})
    for letter in username:
        if not letter.isdigit() and not letter.isalpha():
            return jsonify({"status": "error", "reason": "用户名不符合规范"})
    for letter in password:
        if not letter.isdigit() and not letter.isalpha():
            return jsonify({"status": "error", "reason": "密码不符合规范"})
    db = DB()
    username_ls = db.select_common_username()
    if username in username_ls:
        return jsonify({"status": "error", "reason": "用户名已存在"})
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    db.insert_user(username, password)
    dic = {
        "exp": datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
        "data": {"username": username},  # 内容，一般存放该用户id和开始时间
    }
    return jsonify(
        {
            "status": "success",
            "token": jwt.encode(dic, app.config["KEY"], algorithm="HS256"),
            "username": username,
        }
    )


@app.route("/rank")
def rank():
    db = DB()
    res = db.rank()
    return render_template("rank.html", data_json=json.dumps(res, ensure_ascii=False))


@app.route("/search")
def search():
    db = DB()
    keyword = request.args.get("keyword")
    data_json = db.search(keyword)
    data_json = json.dumps(data_json, ensure_ascii=False)
    # print(data_json)
    return render_template("search.html", data_json=data_json)


@app.route("/test")
def test():
    import time

    return jsonify(time.time())


@app.route("/category")
def category():
    db = DB()
    film_type = request.args.get("film_type")
    film_producer = request.args.get("film_producer")
    current_page = int(request.args.get("current_page"))
    if current_page <= 0:
        current_page = 1
    limit = 24
    if film_type == "全部类型":
        film_type = ""
    if film_producer == "全部地区":
        film_producer = ""
    data_sum, res = db.category(
        film_type=film_type,
        film_producer=film_producer,
        start=(current_page - 1) * limit,
        limit=limit,
    )
    page_num = math.ceil(data_sum / limit)
    if current_page > page_num:
        current_page = page_num
        tmp = db.category(
            film_type=film_type,
            film_producer=film_producer,
            start=(current_page - 1) * limit,
            limit=limit,
        )
        if tmp is None:
            data_sum = 0
            res = []
        else:
            data_sum, res = db.category(
                film_type=film_type,
                film_producer=film_producer,
                start=(current_page - 1) * limit,
                limit=limit,
            )
    return render_template(
        "category.html",
        data=res,
        page_num=page_num,
        current_page=current_page,
        film_type=film_type,
        film_producer=film_producer,
    )


@app.route("/film/<option>")
def film_item(option):
    default_film_id = "10437779"
    db = DB()
    print(option)
    film_id = (
        request.args.get("film_id")
        if request.args.get("film_id")
        else default_film_id
    )
    context = db.get_film_item(film_id)
    if context is None:
        context = db.get_film_item(default_film_id)
    if option == "introduction":
        return render_template("film_introduction.html", **context)
    elif option == "user_analysis":
        return render_template("film_user_analysis.html", **context)
    elif option == "comment_analysis":
        return render_template("film_comment_analysis.html", **context)
    return render_template("404.html")


@app.route("/get/<option>")
def get_data(option):
    db = DB()
    if option == "film_user_analysis":
        film_id = request.args.get("film_id")
        residence, register_time = db.get_user_info(film_id)
        residence_count = defaultdict(int)
        register_time_count = defaultdict(int)
        for region in residence:
            residence_count[region] += 1
        for t in register_time:
            t = t.split("-")[0]
            register_time_count[t] += 1
        return jsonify(
            {
                "residence": residence_count,
                "register_time": register_time_count,
            }
        )
    elif option == "history":
        token = request.args.get("token").strip()
        payload = jwt.decode(token, app.config["KEY"], algorithms=["HS256"])
        username = payload["data"]["username"]
        return jsonify(db.select_user_history(username))
    elif option == "preference":
        area_name = request.args.get("area_name")
        area_films, favor_films = db.preference(area_name)
        if len(favor_films) > 20:
            favor_films = favor_films[:20]
        film_type = defaultdict(int)
        for film_id, film_item in area_films.items():
            for item in film_item["film_type"].split("/"):
                film_type[item.strip()] += 1
        favor_films= [
                    area_films[favor_film] for favor_film in favor_films
                ]
        favor_films.sort(key=lambda item: item["score"],reverse=True)
        return jsonify(
            {
                "film_type": film_type,
                "favor_films":favor_films,
            }
        )
    elif option == "film_comment_analysis":
        film_id = request.args.get("film_id")
        ls = [0, 0, 0, 0, 0, 0]
        items = db.get_film_comment_rating(film_id)
        area_rating_data = defaultdict(
            lambda: {
                "1星": 0,
                "2星": 0,
                "3星": 0,
                "4星": 0,
                "5星": 0,
            }
        )
        for item in items:
            ls[item["rating"] - 1] += 1
            area_rating_data[item["residence"]][str(item["rating"]) + "星"] += 1
        return jsonify(
            {
                "rating_data": [
                    {"name": str(index + 1) + "星", "value": ls[index]}
                    for index in range(len(ls) - 1)
                ],
                "area_rating_data": area_rating_data,
                "film_keywords": db.get_film_keywords(film_id),
            }
        )
    elif option == "similarity_film":
        film_id = request.args.get("film_id")
        film_item = db.get_film_item(film_id, extra_info=False)
        if film_item is None:
            return jsonify({})
        similarity_film = json.loads(film_item["similarity_film"])
        for index in range(len(similarity_film)):
            try:
                similarity_film_item = db.get_film_item(
                    similarity_film[index]["film_id"], extra_info=True
                )
                similarity_film[index]["film_poster"] = similarity_film_item[
                    "film_poster"
                ]
                similarity_film[index]["score"] = similarity_film_item["score"]
            except Exception:
                pass
        return jsonify(similarity_film)
    elif option == "common_username":
        return jsonify(db.select_common_username())
    elif option == "film":
        return jsonify(db.get_film_id_name())
    return jsonify("nothing")


@app.route("/delete", methods=["POST"])
def delete():
    data_type = request.form.get("type")
    if data_type == "user":
        username = request.form.get("username")
        DB().delete_user(username)
        return jsonify({"status": "success"})
    elif data_type == "film":
        film_id = request.form.get("film_id")
        DB().delete_film(film_id)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})


@app.route("/add_film", methods=["POST"])
def add_film():
    global queue_is_free
    film_url = request.form.get("film_url").strip()
    if not film_url.startswith("https://movie.douban.com/subject/"):
        return jsonify({"status": "error", "reason": "URL错误"})
    # queue_is_free全局变量控制爬虫开启
    film_ls_queue.put(film_url)
    if queue_is_free:
        queue_is_free = False
        while True:
            if not film_ls_queue.empty():
                url = film_ls_queue.get()
                spider_queue.DoubanMovieSpider().add_one(url)
                spider_queue.DoubanCommentSpider().start()
            else:
                TfIdf().calculate()
                if film_ls_queue.empty():  # 防止有新的URL加入
                    queue_is_free = True
                    break
    return jsonify({"status": "success"})


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.template_filter("fun1")
def tmp(val, val2):
    return val + "tmp" + val2


if __name__ == "__main__":
    # print(app.url_map)
    app.run(
        host="127.0.0.1",
    )
