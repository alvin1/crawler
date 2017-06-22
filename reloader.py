import sys
from modules.html_loader import HtmlLoader
from modules.extracter import Extracter
from modules.logger import Logger

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s <url>" % sys.argv[0])
        exit -1

    html_loader = HtmlLoader()
    extracter = Extracter()
    logger = Logger()

    path = sys.argv[1]
    soup = html_loader.get_page_soup(url=path, page=1)
    detail = extracter.extract_detail(soup)

    list_item = {
        'tender_id': '',
        'pubdate': '2013-10-28 00:00:00',
        'page_url': path,
        'page_num': 0
    }

    extracter.save_extracted_data(list_item, detail)
