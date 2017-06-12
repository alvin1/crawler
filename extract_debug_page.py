import os
import json
from modules.file_helper import FileHelper
from modules.html_loader import HtmlLoader
from modules.extracter import Extracter


def format_print(json_string):
    print(json.dumps(json_string, indent=2, encoding='gbk'))

if __name__ == '__main__':
    file_helper = FileHelper()
    html_loader = HtmlLoader()
    extracter = Extracter()

    page_dir = "debug_pages/"
    # page_path = os.path.join(page_dir, 'a9e29e7b-da58-47cc-a9a4-0d9340a62282' + '.html')
    page_path = os.path.join(page_dir, 'a3b7960e-287a-47fe-9beb-db2495a7a9f0' + '.html')

    soup = html_loader.beautiful_page_content(file_helper.read(page_path))
    detail = extracter.extract_detail(soup)
    format_print(detail)
    list_item = {
        'info_id': 'a9e29e7b-da58-47cc-a9a4-0d9340a62282',
        'publish_date': '2013-10-28 00:00:00',
        'page_url': 'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=a9e29e7b-da58-47cc-a9a4-0d9340a62282&CategoryNum=005001003'
    }
    extracter.save_extracted_data(list_item, detail)
