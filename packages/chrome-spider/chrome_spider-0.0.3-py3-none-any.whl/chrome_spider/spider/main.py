from os import sep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager import chrome
from selenium import webdriver
import time
import json
import subprocess
from chrome_spider.common.sql import DB
from chrome_spider.common.config import config
from chrome_spider.spider.cookie import CookieManager



class Spider(CookieManager):
    def __init__(self,debug=False):
        self.debug = debug
        self.debugger_port = 9222


    def get_options(self):
        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-features=EnableEphemeralFlashPermission")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if self.debug == True:
            options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.debugger_port}")
        return options

    def open_debugger_port(self,debugger_port = 9222):
        shell = f'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port={debugger_port} --user-data-dir="{config.chrome_data}"'
        subprocess.Popen(shell,shell=True)
        self.debugger_port = debugger_port
        time.sleep(3) # wait for chrome start

    def get_driver(self):

        self.driver = webdriver.Chrome(
            chrome.ChromeDriverManager().install(), options=self.get_options()
        )
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(10)
        # self.driver.maximize_window()
        return self.driver

    




if __name__ == "__main__":
    # spider = ChromeSpider(debug=True)
    # spider.open_debugger_port()

    spider = ChromeSpider() 

    driver = spider.get_driver()
    driver.get("http://d.weidian.com")
    time.sleep(3)
    # spider.save_cookie("weidian.com","15233200179")
    
    spider.login_by_cookie("weidian.com","15233200179")
    driver.get("https://d.weidian.com/weidian-pc/weidian-loader/#/pc-vue-micro-index/index")
