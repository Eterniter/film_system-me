import pymysql
import json


class DB:
    def __init__(
        self, host="localhost", user="root", password="root", database="film_system"
    ):
        self.db = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        self.database = database
        self.cursor = self.db.cursor()
        self.get_score_sql = "SELECT score FROM `film_statistic` WHERE film_id='%s'"

    def search(self, keyword):
        sql = f"SELECT * FROM `film_item` WHERE (film_name LIKE '%{keyword}%' or director LIKE '%{keyword}%') AND tf_idf_keywords IS NOT NULL AND similarity_film IS NOT NULL"
        res = []
        try:
            cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            cursor2 = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(sql)
            results = cursor.fetchone()
            while results:
                cursor2.execute(self.get_score_sql % results["film_id"])
                results.update(cursor2.fetchone())
                res.append(
                    {
                        "film_id": results["film_id"],
                        "film_name": results["film_name"],
                        "film_poster": results["film_poster"],
                        "score": results["score"],
                    }
                )
                results = cursor.fetchone()
            return res
        except Exception:
            pass

    def category(self, **args):
        film_type = args["film_type"]
        film_producer = args["film_producer"]
        start = args["start"]
        limit = args["limit"]
        sql = f"SELECT * FROM `film_item` WHERE film_type LIKE '%{film_type}%' and film_producer LIKE '%{film_producer}%' LIMIT {start},{limit}"
        sql_get_sum = f"SELECT count(*) FROM `film_item` WHERE film_type LIKE '%{film_type}%' and film_producer LIKE '%{film_producer}%'"
        res = []
        try:
            cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            cursor2 = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(sql)
            results = cursor.fetchone()
            while results:
                cursor2.execute(self.get_score_sql % results["film_id"])
                results.update(cursor2.fetchone())
                res.append(
                    {
                        "film_id": results["film_id"],
                        "film_name": results["film_name"],
                        "film_poster": results["film_poster"],
                        "score": results["score"],
                    }
                )
                results = cursor.fetchone()
            data_sum = self.__select(sql_get_sum)[0][0]
            return data_sum, res
            return {"data_sum": data_sum, "film_show": res}
        except Exception:
            pass

    def preference(self, area_name):
        sql = f"""
            SELECT DISTINCT
                film_id 
            FROM
                `comment` 
            WHERE
                user_id IN (
                SELECT
                    user_id 
                FROM
                    `comment_user_item` 
            WHERE
                residence = '{area_name}')
        """
        try:
            res = self.__select(sql)
            res = [item[0] for item in res]
            area_films = {}
            for film_id in res:
                area_films[film_id] = self.get_film_item(film_id)
            sql = """
            SELECT
                film_id,
                SUM( rating )/ COUNT( film_id ) AS tmp 
            FROM
                `comment` 
            WHERE
                user_id IN ( SELECT user_id FROM `comment_user_item` WHERE residence = '%s' ) 
            GROUP BY
                film_id 
            HAVING
                COUNT( film_id )> %d 
            ORDER BY
                tmp DESC
            """
            for cnt in range(8, -1, -1):
                res = self.__select(sql % (area_name, cnt))
                res = [item[0] for item in res]
                if len(res) > 0:
                    break
                else:
                    print(res)
            return area_films, res
        except Exception:
            pass

    def store_film_item_one_field(self, field_name, film_id, json_data):
        sql = "UPDATE `film_item` SET %s = '%s' WHERE film_id='%s'" % (
            field_name,
            pymysql.converters.escape_string(json_data),
            film_id,
        )
        try:
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            print(err)

    def get_film_keywords(self, film_id):
        sql = "SELECT tf_idf_keywords FROM `film_item` WHERE film_id =%s " % film_id
        res = self.__select(sql)
        return json.loads(res[0][0])

    def get_film_item(self, film_id, extra_info=True):
        sql = "SELECT * FROM `film_item` WHERE film_id =%s " % film_id
        try:
            cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(sql)
            results = cursor.fetchone()
            if extra_info:
                cursor.execute(self.get_score_sql % film_id)
                results.update(cursor.fetchone())
            return results
        except Exception:
            pass

    def get_user_info(self, film_id):
        sql = (
            "SELECT residence,register_time FROM `comment_user_item` WHERE EXISTS (SELECT * FROM `comment` WHERE film_id ='%s' AND comment_user_item.user_id=user_id)"
            % film_id
        )
        res = self.__select(sql)
        return [item[0] for item in res], [item[1] for item in res]

    def get_film_comment_rating(self, film_id):
        sql = f"""
            SELECT
                rating,
                residence 
            FROM
                `comment`,
                `comment_user_item` 
            WHERE
                film_id = '{film_id}' 
                AND COMMENT.user_id = comment_user_item.user_id
            """
        res = self.__select(sql)
        return [{"rating": item[0], "residence": item[1]} for item in res]

    def get_film_id(self):
        sql = "SELECT film_id FROM `film_item`"
        res = self.__select(sql)
        return [item[0] for item in res]

    def get_film_id_without_tf_idf_keywords(self):
        sql = "SELECT film_id FROM `film_item` WHERE tf_idf_keywords is NULL"
        res = self.__select(sql)
        return [item[0] for item in res]

    def get_film_id_name(self):
        sql = "SELECT film_id,film_name FROM `film_item`"
        res = self.__select(sql)
        return [{"film_id": item[0], "film_name": item[1]} for item in res]

    def select_user_id(self, film_id):
        sql = "SELECT user_id FROM `comment` WHERE film_id='%s'" % film_id
        res = self.__select(sql)
        return [item[0] for item in res]

    def select_comment_num(self, film_id):
        sql = "SELECT COUNT(*) FROM `comment` WHERE film_id='%s'" % film_id
        res = self.__select(sql)
        return res[0][0]

    def select_comment_content(self, film_id):
        sql = "SELECT comment_content FROM `comment` WHERE film_id='%s'" % film_id
        res = self.__select(sql)
        return [item[0] for item in res]

    def rank(self):
        sql = "SELECT film_id,short_comment_num FROM `film_statistic` ORDER BY short_comment_num DESC LIMIT 5"
        short_comment_num_rank = self.__select(sql, True)
        for item in short_comment_num_rank:
            film_item = self.get_film_item(item["film_id"], False)
            del film_item["similarity_film"]
            del film_item["tf_idf_keywords"]
            item.update(film_item)
        sql = "SELECT film_id,question_num FROM `film_statistic` ORDER BY question_num DESC LIMIT 5"
        question_num_rank = self.__select(sql, True)
        for item in question_num_rank:
            film_item = self.get_film_item(item["film_id"], False)
            del film_item["similarity_film"]
            del film_item["tf_idf_keywords"]
            item.update(film_item)
        sql = "SELECT film_id,score FROM `film_statistic` ORDER BY score DESC LIMIT 5"
        score_rank = self.__select(sql, True)
        for item in score_rank:
            film_item = self.get_film_item(item["film_id"], False)
            del film_item["similarity_film"]
            del film_item["tf_idf_keywords"]
            item.update(film_item)
        sql = "SELECT film_id,topic_num FROM `film_statistic` ORDER BY topic_num DESC LIMIT 5"
        topic_num_rank = self.__select(sql, True)
        for item in topic_num_rank:
            film_item = self.get_film_item(item["film_id"], False)
            del film_item["similarity_film"]
            del film_item["tf_idf_keywords"]
            item.update(film_item)
        return {
            "short_comment_num_rank": short_comment_num_rank,
            "question_num_rank": question_num_rank,
            "score_rank": score_rank,
            "topic_num_rank": topic_num_rank,
        }

    def select_common_username(self):
        sql = "SELECT username FROM `user` WHERE authority is NULL"
        res = self.__select(sql)
        return [item[0] for item in res]

    def select_user_history(self, username):
        sql = f"SELECT film_id FROM `user_history` WHERE username='{username}'"
        film_id_ls = self.__select(sql)
        res = []
        for film_id in film_id_ls:
            item = self.get_film_item(film_id)
            res.append(
                {
                    "film_id": item["film_id"],
                    "film_name": item["film_name"],
                    "film_poster": item["film_poster"],
                    "score": item["score"],
                }
            )
        return res

    def user_is_exist(self, username, password, is_admin=False):
        sql = f"SELECT count(*) FROM `user` WHERE username='{username}' AND password='{password}'"
        if is_admin:
            sql += " AND authority='admin'"
        res = self.__select(sql)
        return res[0][0]

    def insert_user(self, username, password):
        sql = f"INSERT INTO `{self.database}`.`user` (`username`, `password`) VALUES ('{username}', '{password}');"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as err:
            self.db.rollback()
            print(err)
            return False

    def delete_user(self, username):
        sql = f"DELETE FROM `user` WHERE username='{username}'"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def delete_film(self, film_id):
        sql = f"DELETE FROM `film_item` WHERE film_id='{film_id}'"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def insert_history(self, username, film_id):
        # 记录用户浏览过的电影页面
        sql = f"INSERT INTO `{self.database}`.`user_history` (`username`, `film_id`) VALUES ('{username}', '{film_id}');"
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as err:
            self.db.rollback()
            if "Duplicate entry" in str(err):
                return True
            print(err)
            return False

    def __select(self, sql, dict_form=False):
        try:
            cursor = (
                self.db.cursor(cursor=pymysql.cursors.DictCursor)
                if dict_form
                else self.cursor
            )
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception:
            return None

    def insert_table(self, table_name, data):
        """
        专门为film_system2的数据插入
        """
        for key in data.keys():
            if isinstance(data[key], str):
                data[key] = pymysql.converters.escape_string(data[key])
        data["database_name"] = self.database
        if table_name == "film_item":
            sql = "INSERT INTO `{database_name}`.`film_item` \
(`film_id`, `film_name`, `film_chinese_name`, `director`, \
`screen_writer`, `starring`, `film_type`, `film_producer`, \
`film_language`, `release_date`, `film_duration`, `film_intro`, `film_poster`) \
VALUES ('{film_id}', '{film_name}', '{film_chinese_name}', \
'{director}', '{screen_writer}', '{starring}', '{film_type}', \
'{film_producer}', '{film_language}', '{release_date}', \
'{film_duration}', '{film_intro}', '{film_poster}');"
        elif table_name == "film_statistic":
            sql = "INSERT INTO `{database_name}`.`film_statistic` \
(`film_id`, `comment_num`, `short_comment_num`, `vote_num`, `question_num`, \
`topic_num`, `seen_num`, `want_num`, `score`, `percent_stars5`, `percent_stars4`, \
`percent_stars3`, `percent_stars2`, `percent_stars1`) VALUES \
('{film_id}', {comment_num}, {short_comment_num}, {vote_num}, \
{question_num}, {topic_num}, {seen_num}, {want_num}, \
{score}, {percent_stars5}, {percent_stars4}, \
{percent_stars3}, {percent_stars2}, {percent_stars1});"
        elif table_name == "comment_user_item":
            sql = "INSERT INTO `{database_name}`.`comment_user_item` \
(`user_id`, `user_name`, `register_time`, `residence`, `follower_num`, `concern_num`, `user_poster_url`) VALUES \
('{user_id}', '{user_name}', '{register_time}', '{residence}', {follower_num}, {concern_num}, '{user_poster_url}');"
        elif table_name == "comment":
            sql = "INSERT INTO `{database_name}`.`comment` \
(`film_id`, `user_id`, `comment_content`, `comment_time`, `useful_num`,`rating`) VALUES \
('{film_id}', '{user_id}', '{comment_content}', '{comment_time}', {useful_num},{rating});"
        else:
            print("The name of table is wrong!")
            return
        try:
            self.cursor.execute(sql.format(**data))
            self.db.commit()
            return True
        except Exception as err:
            self.db.rollback()
            if "Duplicate entry" in str(err):
                return False
            print(table_name, " INSERT ERROR! ", str(err))
            print(sql.format(**data))
            print(data)
            return False

    def __del__(self):
        self.db.close()


if __name__ == "__main__":
    db = DB()

    a, b = db.get_user_info("10437779")
    res = db.select_comment_content("10437779")
    res = db.select_comment_num("10437779")
    res = db.select_user_id("10437779")
    res = db.get_film_id()
    res = db.get_user_info("10437779")
    res = db.get_film_keywords("10437779")
    res = db.search("哈利")
    res = db.category(film_type="剧情", film_producer="中国", start=20, limit=20)
    res = db.rank()
    res = db.user_is_exist("1234", "1")
    res = db.select_user_history("hesitater")
    # res = db.delete_user("2342324")
    res = db.get_film_id_name()
    # res = db.delete_film("1")
    res = db.get_film_comment_rating("10437779")
    res = db.preference("山西")

    print(res)
    print(type(res))
    print(len(res))
