import os
import json
import sys
from modules.file_helper import FileHelper
from modules.html_loader import HtmlLoader
from modules.extracter import Extracter


def format_print(json_string):
    print(json.dumps(json_string, indent=2, encoding='utf8'))

def get_content(soup):
    if soup.string is not None:
        return soup.string if soup.string != '\n' else u''

    if len(soup.contents) == 0:
        return u''

    values = []
    for item in soup.contents:
        values.extend(get_content(item))
    return values

def get_cell_content(td_soup):
    if td_soup.string is not None:
        return td_soup.string if td_soup.string != '\n' else u''

    values = []
    for item in td_soup.contents:
        values.extend(get_content(item))
    return u"".join(values).replace('\n', '').replace(u' ', u'')

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print("Usage: %s <info_id>" % sys.argv[0])
    #     exit(-1)
    info_id = '3f0a2dd7-1e13-4929-961b-a07808811650'  # sys.argv[1]

    file_helper = FileHelper()
    html_loader = HtmlLoader()
    extracter = Extracter()

    page_dir = "debug_pages/"
    # page_path = os.path.join(page_dir, 'a9e29e7b-da58-47cc-a9a4-0d9340a62282' + '.html')
    page_path = os.path.join(page_dir, info_id + '.html')

    if not os.path.exists(page_path) or not os.path.isfile(page_path):
        print("info id not exists")
        exit(-2)

    soup = html_loader.beautiful_page_content(file_helper.read(page_path))
    detail = extracter.extract_detail(soup)
    format_print(detail)
    list_item = {
        'tender_id': info_id,
        'pubdate': '2013-10-28 00:00:00',
        'page_url': 'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=' + info_id + '&CategoryNum=005001003',
        'page_num': 0
    }
    extracter.save_extracted_data(list_item, detail)
