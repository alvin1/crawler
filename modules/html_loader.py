import urllib
import urllib2
import httplib
import time
from bs4 import BeautifulSoup

from .settings import Settings
from .logger import Logger
from .file_helper import FileHelper


class HtmlLoader(object):
    def __init__(self):
        self.logger = Logger()
        self.file_helper = FileHelper()

    def save_failed_grab(self, url, page):
        failed_path = 'var/status/failed_grab.json'
        failed_grabs = self.file_helper.get_json(failed_path)
        if failed_grabs is None:
            failed_grabs = []
        failed_grabs.append({
            'url': url,
            'page': page
        })
        self.file_helper.write_json(failed_path, failed_grabs)

    def get_page_content(self, url, page=1, retry_times = 0):
        print(url)
        data = urllib.urlencode({
            '__VIEWSTATEGENERATOR': Settings.VIEWSTATEGENERATOR,
            '__EVENTTARGET': Settings.EVENTTARGET,
            '__VIEWSTATE': Settings.VIEWSTATE,
            '__EVENTARGUMENT': str(page)
        })
        headers = {  
           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
           'Connection':'Keep-Alive',
           'Referer': url
        }

        req = urllib2.Request(url=url, headers=headers)

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        try:
            response = opener.open(req, data, Settings.PAGE_WAIT_TIMEOUT)
            return response.read()
        except urllib2.URLError, e:
            print("urllib2.URLError")
            print("Load web page %s failed. message: %s" % (page, e))
            print('retry_times = %s --> retry_times + 1 = %s' % (retry_times, retry_times + 1))
            retry_times += 1
            if Settings.RETRY_TIMES != 0 and retry_times > Settings.RETRY_TIMES:
                print("Reached the max retry times, will record to error log")

            print("Sleep 3 seconds")
            time.sleep(3)
            print("Trying to get content again. Tried times: %s" % retry_times)
            self.get_page_content(url, page, retry_times)
        except httplib.BadStatusLine, e:
            print("httplib.BadStatusLine")
            print("Load web page %s failed. message: %s" % (page, e))
            print('retry_times = %s --> retry_times + 1 = %s' % (retry_times, retry_times + 1))
            retry_times += 1
            if Settings.RETRY_TIMES != 0 and retry_times > Settings.RETRY_TIMES:
                print("Reached the max retry times, will record to error log")
                self.save_failed_grab(url, page)

            print("Sleep 3 seconds")
            time.sleep(3)
            print("Trying to get content again. Tried times: %s" % retry_times)
            self.get_page_content(url, page, retry_times)

    def beautiful_page_content(self, content):
        return BeautifulSoup(content, "html.parser")

    def get_page_soup(self, url, page=1):
        page_content = self.get_page_content(url, page)
        if page_content is None:
            self.save_failed_grab(url, page)
            return None
        
        return self.beautiful_page_content(page_content)
