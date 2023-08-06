from chrome_spider.common.config import config
from chrome_spider.common.sql import DB
import json
import time

class CookieManager(object):
    def __init__(self, driver):
        self.driver = driver

    def save_cookie(self, host, name, cookies=None):
        """
        保存/更新 cookie 到数据库

        """
        if cookies == None:
            # 1. 由selenium 直接获取 cookie 保存 - 推荐使用
            cookies = self.driver.get_cookies()
        elif type(cookies) == str:
            # 2. 存储通过 document.cookies 获取的cookie - 有时候不能恢复登录态
            cookie_dic = dict([l.split("=", 1) for l in cookies.split("; ")])
            cookies = []
            for key, value in cookie_dic.items():
                cookies.append({"name": key, "value": value})

        cookies = json.dumps(cookies)

        with DB() as cursor:
            cursor.execute(
                "select cookie from account where host = ? and name = ?", (host, name)
            )
            if cursor.fetchone():
                print("update cookies")
                cursor.execute(
                    "update account set cookie = ? where name = ? and host = ?",
                    (cookies, name, host),
                )
            else:
                print("insert cookies")
                cursor.execute(
                    "insert into account (host,name,cookie) values (?,?,?)",
                    (host, name, cookies),
                )

    def login_by_cookie(self, host, name):
        """
        基于数据库存储的cookie进行登录
        @param host: 要登录的账号所在域名 示例: "weidian.com"
        @param name: 要登录的账号名称 示例: "kirito or 15233200000"
        """
        with DB() as cursor:
            cursor.execute(
                "select cookie from account where host = ? and name = ?", (host, name)
            )
            cookies = json.loads(cursor.fetchone()[0])
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        time.sleep(0.5)
        self.driver.refresh()

    def get_cookie(self):
        """
        从数据库中获取 cookies
        """
        with DB() as cursor:
            cursor.execute(
                "select cookie from account where host = ? and name = ?", (host, name)
            )
            cookies = json.loads(cursor.fetchone()[0])
        return cookies
