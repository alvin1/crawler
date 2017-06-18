import urllib
import urllib2
import httplib
import re
import socket
from bs4 import BeautifulSoup

from .settings import Settings
from .logger import Logger
from .file_helper import FileHelper
from database.models.failed_page import FailedPage


class HtmlLoader(object):
    def __init__(self):
        self.logger = Logger()
        self.file_helper = FileHelper()

    def save_failed_grab(self, url, page):
        info_id_pattarn = re.compile(u'.+InfoID=(?P<INFOID>.+)&.+')
        match = info_id_pattarn.match(url)

        if match:
            failed_page = FailedPage(tender_id=match.group('INFOID'), page_url=url, failed_type='grab', page_num=page,
                                     page_type='detail')
        else:
            failed_page = FailedPage(tender_id=None, page_url=url, failed_type='grab', page_num=page, page_type='list')
        failed_page.save()

    def get_page_content(self, url, page=1):
        print("%s -> %s" % (page, url))
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
            self.logger.error("urllib2.URLError")
            self.save_failed_grab(url, page)
        except httplib.BadStatusLine, e:
            self.logger.error("httplib.BadStatusLine")
            self.save_failed_grab(url, page)
        except socket.timeout as e:
            self.logger.error("Socket time out")
            self.save_failed_grab(url, page)
        except Exception, e:
            self.logger.error("Load web page %s failed" % (page))
            self.save_failed_grab(url, page)

    def beautiful_page_content(self, content):
        return BeautifulSoup(content, "html.parser")

    def get_page_soup(self, url, page=1):
        page_content = self.get_page_content(url, page)
        if page_content is None:
            self.save_failed_grab(url, page)
            return None
        
        return self.beautiful_page_content(page_content)
