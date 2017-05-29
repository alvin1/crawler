import urllib
import urllib2
from bs4 import BeautifulSoup

from .settings import Settings


class HtmlLoader(object):
    def get_page_content(self, url, page=1):
        req = urllib2.Request(url)
        data = urllib.urlencode({
            '__VIEWSTATEGENERATOR': Settings.VIEWSTATEGENERATOR,
            '__EVENTTARGET': Settings.EVENTTARGET,
            '__VIEWSTATE': Settings.VIEWSTATE,
            '__EVENTARGUMENT': str(page)
        })

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        return response.read()

    def beautiful_page_content(self, content):
        return BeautifulSoup(content, "html.parser")

    def get_page_soup(self, url, page=1):
        return self.beautiful_page_content(self.get_page_content(url, page))