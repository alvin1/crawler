from .html_loader import HtmlLoader
from .extracter import Extracter
from .settings import Settings
from .logger import Logger


class ExtractHelper(object):
    def __init__(self):
        self.extracter = Extracter()
        self.html_loader = HtmlLoader()
        self.logger = Logger()

    def extract_lists(self, page, data):
        soup = self.html_loader.get_page_soup(url=Settings.URL, page=page)
        for item in self.extracter.extract_list(soup, page):
            self.logger.warning("title=%s, date=%s, page=%s" % (item['title'].decode('utf8'), item['publish_date'], item['page_index']))
