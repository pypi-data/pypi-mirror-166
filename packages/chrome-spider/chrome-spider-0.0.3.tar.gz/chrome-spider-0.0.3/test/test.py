from chrome_spider import Spider
import time

if __name__ == "__main__":
    spider = Spider()
    driver = spider.get_driver()
    driver.get("https://baidu.com")
    time.sleep(5)
    driver.quit()