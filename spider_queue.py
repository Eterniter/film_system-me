import re
from time import time, sleep
from random import random, sample
import queue, threading
import json
import requests
from lxml import etree
from collections import defaultdict
from mysql_query import DB


class Request:
    cookies_path = "film_system-me/douban_cookies.txt"
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Accept-Encoding": "gzip, deflate, br",
        # 这条信息代表本地可以接收压缩格式的数据，而服务器在处理时就将大文件压缩再发回客户端，
        # IE在接收完成后在本地对这个文件又进行了解压操作。
        # 出错的原因是因为你的程序没有解压这个文件，所以删掉这行就不会出现问题了
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": 'bid=u3L9LkrHrK8; douban-fav-remind=1; _vwo_uuid_v2=D658FDAD2B07A23FB825384DF0694E89D|416ab8d942edaf85a1fef3b556c60525; __utmv=30149280.23325; _ga=GA1.1.1378090368.1631590510; ll="118254"; __gads=ID=0095ba28a4991dbd-2210b6a4c9cc0072:T=1634884872:RT=1634884872:S=ALNI_Mbn6n5F80LMoGOF__x0E4YaTVSfqA; gr_user_id=9c10b13d-7987-405f-8abf-590c5bb39fe0; _ga_RXNMP372GL=GS1.1.1636696073.2.1.1636696311.0; viewed="30701505_1035318_3603080_1752607_26931513_26311122"; dbcl2="233257236:rXjpJ2WJk14"; push_noty_num=0; push_doumail_num=0; ck=s2oB; __utmc=30149280; __utmz=30149280.1643425913.104.72.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __utmz=223695111.1643425913.62.38.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1643465782%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DbouPwKi2b2t3xDYaV7gq5sB1AnPDYTpnN3sKDyd8B_x7JjHj2g2QZA4whOoArEWttBg0J1AApFpoZClnU-TjUa%26wd%3D%26eqid%3D94279dc200079c900000000661f4b073%22%5D; _pk_id.100001.4cf6=53955f53524a91c0.1631672030.77.1643465782.1643460358.; _pk_ses.100001.4cf6=*; __utma=30149280.1378090368.1631590510.1643460073.1643465782.109; __utmb=30149280.1.10.1643465782; __utma=223695111.1826932903.1631672030.1643460073.1643465782.67; __utmb=223695111.0.10.1643465782',
        "Host": "movie.douban.com",
        "Pragma": "no-cache",
        "Referer": "https://movie.douban.com/top250?start=50&filter=",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }
    get_json_header = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "m.douban.com",
        "Origin": "https://movie.douban.com",
        "Pragma": "no-cache",
        "Referer": "https://www.douban.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }

    def __init__(self, url, headers=header) -> None:
        self.req = self.get(url, headers)
        self.status_code = self.req.status_code
        self.text = self.req.text
        self.url = self.req.url
        self.html = etree.HTML(self.text)
        self.start_time = time()

    @staticmethod
    def init_cookie(retry=2):
        cookie_ls = []
        try:
            with open(Request.cookies_path, "r", encoding="utf-8") as f:
                listcookies = json.loads(f.read())
                for item in listcookies:
                    item = dict(item)
                    cookie_ls.append(item["name"] + "=" + item["value"])
            Request.header["Cookie"] = "; ".join(cookie_ls)
        except Exception:
            from selenium import webdriver
            from selenium.webdriver.support.wait import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation", "enable-logging"]
            )
            try:
                driver = webdriver.Chrome(options=chrome_options)
                wait = WebDriverWait(driver, 60)
                driver.get("https://www.douban.com/")
                wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//iframe[@src="//accounts.douban.com/passport/login_popup?login_source=anony"]',
                        )
                    )
                )
                iframe = driver.find_element(
                    By.XPATH,
                    '//iframe[@src="//accounts.douban.com/passport/login_popup?login_source=anony"]',
                )
                driver.switch_to.frame(iframe)
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//a[@title="用微信登录"]'))
                )
                driver.find_element(By.XPATH, '//a[@title="用微信登录"]').click()
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//a[@class="bn-more"]'))
                )
                cookies = driver.get_cookies()
                driver.quit()
                with open(Request.cookies_path, "w") as f:
                    f.write(json.dumps(cookies))
                for item in cookies:
                    item = dict(item)
                    cookie_ls.append(item["name"] + "=" + item["value"])
                    Request.header["Cookie"] = "; ".join(cookie_ls)
            except Exception:
                if retry > 0:
                    return Request.init_cookie(retry - 1)

    @staticmethod
    def get(url, headers):
        if url.startswith("https://www.douban.com/people/"):
            headers = headers.copy()
            headers["Host"] = "www.douban.com"
        try:
            req = requests.get(url, headers=headers)
            return req
        except Exception:
            pass

    @staticmethod
    def get_json(url):
        req = requests.get(url, headers=Request.get_json_header)
        return json.loads(req.text)

    @staticmethod
    def get_city_name(city_name):
        url = "http://lspengine.map.sogou.com/tips/tip"
        req = requests.get(url, params={"key": city_name})
        data = json.loads(req.text)
        if data["code"] == 0:
            loc = data["response"]["results"][0]
            loc = loc.split(",")
            if len(loc) < 4 or loc[0] == "p":
                return None
            loc = loc[-1] if loc[-2] == "中国" else loc[-2]
            loc = loc.replace("省", "")
            loc = loc.replace("市", "")
            loc = loc.replace("特别行政区", "")
            loc = loc.replace("壮族", "")
            loc = loc.replace("回族", "")
            loc = loc.replace("维吾尔", "")
            loc = loc.replace("自治区", "")
            return loc
        return None

    def get_item(self, exp):
        res = self.html.xpath(exp)
        # print(res)
        if isinstance(res, list):
            if len(res) >= 1:
                return res[0]
            else:
                return None
        return res

    def get_items(self, exp):
        return self.html.xpath(exp)

    def get_items_text(self, exp):
        items = self.get_items(exp)
        return "".join([item.xpath("string(.)") for item in items])

    def get_current_item_text(self, current_item):
        return str(current_item.xpath("string(.)"))

    def element_exist(self, exp):
        if int(self.html.xpath(f"count({exp})")) == 0:
            return False
        if len(self.html.xpath(exp)) == 0:
            return False
        return True

    def __del__(self):
        # return
        if self.status_code != 200:
            print(
                f"{self.__class__.__name__} DONE! {self.url} COST:{time()-self.start_time}"
            )


class MySpider:
    def __init__(self, thread_num=2) -> None:
        self.start_time = time()
        self.block_time = 0
        self.queue = queue.LifoQueue()
        self.thread_ls = []
        self.current_state = "NOTWORKING"
        for _ in range(thread_num):
            self.thread_ls.append(threading.Thread(target=self.run, daemon=True))

    def run(self):
        while not self.queue.empty():
            try:
                # print(
                #     f"\r队列数量:{self.queue.qsize()} COST:{time()-self.start_time}", end=""
                # )
                url, parse = self.queue.get(timeout=2)
                self.handle(url, parse)
                self.queue.task_done()
            except Exception:
                import traceback

                traceback.print_exc()
                sleep(0.5)

    def start_urls(self):
        """
        needed to be overrided
        """
        pass

    def handle(self, url, parse):
        try:
            sleep(1 + random())
            html = Request(url)
            return parse(html)
        except Exception:
            print("当前出错URL:", url)
            import traceback

            traceback.print_exc()

    def follow(self, urls, parse):
        if type(urls) != list:
            assert type(urls) == str
            self.queue.put([urls, parse])
        else:
            for url in urls:
                self.queue.put([url, parse])

    def start_work(self):
        for threading in self.thread_ls:
            threading.start()
        self.current_state = "WORKING"
        for threading in self.thread_ls:
            threading.join()
        self.current_state = "NOTWORKING"

    def display(self, data):
        for k, v in data.items():
            print(f"{k} : {v}")

    def stop(self):
        assert False

    def __del__(self):
        print(f"{self.__class__.__name__} DONE! Total_cost:{time()-self.start_time}")


class DoubanMovieSpider(MySpider):
    def __init__(self) -> None:
        super().__init__()

    def test(self):
        Request.init_cookie()
        urls = ["https://movie.douban.com/subject/1291571/"]
        self.follow(urls, self.parse_subject_page)
        super().start_work()

    def start_urls(self):
        urls = [
            f"https://movie.douban.com/top250?start={index}&filter="
            for index in range(0, 250, 25)
        ]
        return urls

    def display(self, data):
        return
        # super().display(data)

    def start(self):
        Request.init_cookie()
        urls = self.start_urls()
        self.follow(urls, self.parse_douban_top250)
        super().start_work()

    def add_one(self, url):
        Request.init_cookie()
        urls = url
        self.follow(urls, self.parse_subject_page)
        super().start_work()

    def parse_douban_top250(self, response):
        if response.status_code != 200:
            print("\033[31mstatus_code error\033[0m")
            return
        urls = response.get_items('//ol/li//div[@class="pic"]/a/@href')
        film_id_ls = DB().get_film_id()
        target_urls = []
        for url in urls:
            if url.split("/")[-2] not in film_id_ls:
                target_urls.append(url)
        if len(target_urls) > 0:
            self.follow(target_urls, self.parse_subject_page)

    def parse_subject_page(self, response):
        if response.status_code != 200:
            print("\033[31mstatus_code error\033[0m")
            return
        db = DB()
        info_map = {
            "导演": "director",
            "编剧": "screen_writer",
            "主演": "starring",
            "类型": "film_type",
            "制片国家/地区": "film_producer",
            "语言": "film_language",
            "上映日期": "release_date",
            "片长": "film_duration",
            "官方网站": "film_website",
        }
        film_item = {}
        for name in [
            "film_id",
            "film_name",
            "film_chinese_name",
            "film_intro",
        ] + list(info_map.values()):
            film_item[name] = "None"
        # film_item
        film_item["film_id"] = response.url.split("/")[-2]
        film_item["film_chinese_name"] = (
            response.get_item("//title/text()").strip().rstrip(" (豆瓣)")
        )
        film_item["film_name"] = response.get_item(
            '//span[@property="v:itemreviewed"]/text()'
        ).strip()
        info = response.get_item('string(//div[@id="info"])')
        info = info.split("\n")
        info = [line.strip() for line in info if len(line.strip()) > 0]
        for line in info:
            line = line.split(":")
            l, r = line[0].strip(), "".join(line[1:]).strip()
            if l in info_map.keys():
                film_item[info_map[l]] = r
        if response.element_exist('//span[@class="all hidden"]'):
            film_item["film_intro"] = response.get_item(
                '//span[@class="all hidden"]/text()'
            ).strip()
        else:
            film_item["film_intro"] = response.get_item(
                '//span[@property="v:summary"]/text()'
            ).strip()
        film_item["film_poster"] = response.get_item(
            '//*[@id="mainpic"]/a/img/@src'
        ).strip()
        self.display(film_item)
        db.insert_table("film_item", film_item)
        # film_statistic
        film_statistic = {}
        film_statistic["film_id"] = film_item["film_id"]
        statistic_text = response.get_items_text("//h2/span/a[@href]/../..")
        statistic_text = "".join(statistic_text.split())

        res = re.findall(r"影评······\(全部(\d+)条\)", statistic_text)
        film_statistic["comment_num"] = int(res[0]) if len(res) == 1 else 0

        res = re.findall(r"短评······\(全部(\d+)条\)", statistic_text)
        film_statistic["short_comment_num"] = int(res[0]) if len(res) == 1 else 0

        film_statistic["vote_num"] = int(
            response.get_item('//span[@property="v:votes"]/text()')
        )

        res = re.findall(r"问题······\(全部(\d+)个\)", statistic_text)
        film_statistic["question_num"] = int(res[0]) if len(res) == 1 else 0

        film_statistic["topic_num"] = response.get_json(
            f'https://m.douban.com/rexxar/api/v2/gallery/subject_feed?start=0&count=4&subject_id={film_item["film_id"]}&ck=ciK0'
        )["total"]
        seen_want_text = response.get_items_text(
            '//div[@class="subject-others-interests-ft"]'
        )
        seen_want_text = "".join(seen_want_text.split())
        res = re.findall(r"(\d+)人看过", seen_want_text)
        film_statistic["seen_num"] = int(res[0]) if len(res) == 1 else 0
        res = re.findall(r"(\d+)人想看", seen_want_text)
        film_statistic["want_num"] = int(res[0]) if len(res) == 1 else 0
        film_statistic["score"] = float(
            response.get_item('//strong[@property="v:average"]/text()')
        )
        percent_stars_text = response.get_items_text('//span[@class="rating_per"]')
        percent_stars_text = percent_stars_text.split("%")[:5]
        for index in range(5, 0, -1):
            film_statistic[f"percent_stars{index}"] = percent_stars_text[5 - index]
        self.display(film_statistic)
        db.insert_table("film_statistic", film_statistic)


class DoubanCommentSpider(MySpider):
    def __init__(self) -> None:
        super().__init__()
        self.target_comment_num = 100
        self.increment = 100

    def __test(self, response):
        comment_ls = self.parse_douban_comment(response)
        for comment in comment_ls:
            self.handle(
                f"https://www.douban.com/people/{comment['user_id']}/",
                self.parse_people_page,
            )

    def test(self):
        Request.init_cookie()
        urls = [
            f"https://movie.douban.com/subject/1292720/comments?start={index*100}&limit=100&status=P&sort=new_score"
            for index in range(5)
        ]
        self.follow(urls, self.__test)
        super().start_work()

    def start_urls(self):
        urls = []
        db = DB()
        film_id_ls = db.get_film_id()
        for film_id in film_id_ls:
            current_comment_num = db.select_comment_num(film_id)
            if current_comment_num < self.target_comment_num:
                urls.append(
                    f"https://movie.douban.com/subject/{film_id}/comments?start=0&limit={self.target_comment_num}&status=P&sort=new_score"
                )
        return urls

    def start(self):
        Request.init_cookie()
        urls = self.start_urls()
        self.follow(urls, self.__parse)
        super().start_work()

    def __parse(self, response):
        db = DB()
        current_comment_num = None
        film_id, comment_ls = self.parse_douban_comment(response)
        current_comment_num = db.select_comment_num(film_id)
        current_user_ls = db.select_user_id(film_id)
        print(
            f"{film_id} {db.get_film_item(film_id,False)['film_name']} has {current_comment_num} comment(s)"
        )
        for comment in comment_ls:
            if current_comment_num >= self.target_comment_num:
                return
            if comment["user_id"] not in current_user_ls:
                comment_user_item = self.handle(
                    f"https://www.douban.com/people/{comment['user_id']}/",
                    self.parse_people_page,
                )
                if comment_user_item is None:
                    continue
                db.insert_table("comment_user_item", comment_user_item)
                if db.insert_table(
                    "comment", comment
                ):  # user先插入，comment表有外键，user不存在comment插入会出错
                    current_comment_num += 1
                    current_user_ls.append(comment["user_id"])
        if current_comment_num < self.target_comment_num:
            start = int(re.findall(r"start=(\d+)", response.url)[0])
            if start > self.target_comment_num * 10:
                return
            self.follow(
                f"https://movie.douban.com/subject/{film_id}/comments?start={start+self.increment}&limit={self.target_comment_num}&status=P&sort=new_score",
                self.__parse,
            )

    def parse_douban_comment(self, response):
        # comment
        comment = {}
        comment_ls = []
        comment["film_id"] = response.url.split("/")[-2]
        comment_items = response.get_items('//div[@class="comment-item "]')
        for comment_item in comment_items:
            try:
                user_href = comment_item.xpath('./div[@class="avatar"]/a/@href')[0]
                comment["user_id"] = user_href.split("/")[-2]
                user_comment = comment_item.xpath(
                    './/p[@class=" comment-content"]/span[@class="short"]/text()'
                )[0].strip()
                if len(user_comment) > 0:
                    comment["comment_content"] = user_comment
                else:
                    continue
                comment["comment_time"] = comment_item.xpath(
                    './/span[@class="comment-time "]/@title'
                )[0]
                comment["useful_num"] = int(
                    comment_item.xpath('.//span[@class="votes vote-count"]/text()')[0]
                )
                user_rating = comment_item.xpath(
                    './/span[@class="comment-info"]/span[contains(@class,"rating")]/@class'
                )[0]
                comment["rating"] = int(
                    user_rating.lstrip("allstar").rstrip("0 rating")
                )
                comment_ls.append(comment.copy())
            except Exception:
                pass
        return comment["film_id"], comment_ls
        # self.follow(user_hrefs[:3], self.parse_people_page)

    def parse_people_page(self, response):
        # 用户不存在 或者 用户账号状态异常
        if (
            response.get_item('//div[@class="mn"]') is not None
            or response.get_item("//title/text()").strip() == "该用户帐号状态异常"
        ):
            return None
        # comment_user_item
        comment_user_item = {}
        comment_user_item["user_id"] = response.url.split("/")[-2]
        comment_user_item["user_name"] = str(
            response.get_item('//div[@class="pic"]//img/@alt')
        ).strip()
        if comment_user_item["user_name"] is None:
            return None
        user_info_text = response.get_items_text(
            '//div[@class="user-info"]/div[@class="pl"]'
        )
        user_info_text = user_info_text.split()
        comment_user_item["register_time"] = user_info_text[-1].rstrip("加入").strip()
        residence = response.get_item('//div[@class="user-info"]/a/text()')
        residence = (
            Request.get_city_name(residence.strip()) if residence is not None else None
        )
        if residence is None:
            return None
        comment_user_item["residence"] = residence

        follower_num_text = response.get_item('//p[@class="rev-link"]/a/text()')
        res = re.findall(r"被(\d+)人关注", follower_num_text)
        comment_user_item["follower_num"] = int(res[0]) if len(res) == 1 else 0

        concern_num = response.get_item('//div[@id="friend"]//a/text()')
        comment_user_item["concern_num"] = (
            int(concern_num.lstrip("成员").strip()) if concern_num is not None else 0
        )
        comment_user_item["user_poster_url"] = response.get_item(
            '//div[@class="pic"]//img/@src'
        )
        return comment_user_item


if __name__ == "__main__":
    obj = DoubanMovieSpider()
    obj.start()
    obj = DoubanCommentSpider()
    obj.start()
    from TF_IDF import TfIdf

    TfIdf().calculate()
