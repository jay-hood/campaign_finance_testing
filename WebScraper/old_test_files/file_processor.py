import os
import attr
from datetime import datetime 
import time
import logging.config
loginipath = os.path.join(os.path.dirname(__file__), 'logging_config.ini')
logging.config.fileConfig(loginipath)
logger = logging.getLogger('sLogger')


@attr.s
class FileProcessor:
    csv_location = attr.ib(init=False, default=os.path.join(os.path.dirname(__file__), 'csv', 'StateEthicsReport.csv'))
   
    def process(self):
        while not os.path.isfile(self.csv_location):
            time.sleep(1)
        with open(self.csv_location, 'r') as f:
            try:
                content = f.read()
                f.close()
                return (content, datetime.now())
            except Exception as e:
                logging.info(e)

    def delete_csv(self):
        if os.path.isfile(self.csv_location):
            try:
                os.remove(self.csv_location)
                return True
            except Exception as e:
                logging.info(e)
                return False

if __name__ == '__main__':
    print(os.path.join(os.path.dirname(__file__), 'csv', 'StateEthicsReport.csv'))
