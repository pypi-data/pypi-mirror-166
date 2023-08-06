import os


class Config:
    
    db_name = None
    chrome_data = None
    log_path = None

    def __init__(self):
        self.get_path()

    def get_path(self):
        home_path = os.environ["HOME"]
        if not os.path.exists(f"{home_path}/.chrome-spider"):
            os.mkdir(f"{home_path}/.chrome-spider")
        if not os.path.exists(f"{home_path}/.chrome-spider/logs/"):
            os.mkdir(f"{home_path}/.chrome-spider/logs/")

        self.db_name = f"{home_path}/.chrome-spider/spider.db"
        self.chrome_data = f"{home_path}/.chrome-spider/chrome-data"
        self.log_path = f"{home_path}/.chrome-spider/logs/logging.log"


config = Config()
