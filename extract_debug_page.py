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
    page_path = os.path.join(page_dir, '1f46cabd-204a-4309-90d2-759b912da047' + '.html')
    # page_path = os.path.join(page_dir, 'a3b7960e-287a-47fe-9beb-db2495a7a9f0' + '.html')

    soup = html_loader.beautiful_page_content(file_helper.read(page_path))
    detail = extracter.extract_detail(soup)
    format_print(detail)
    list_item = {
        'info_id': '1f46cabd-204a-4309-90d2-759b912da047',
        'publish_date': '2017-06-01 00:00:00',
        'page_url': 'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=1f46cabd-204a-4309-90d2-759b912da047&CategoryNum=005001003'
    }
    extracter.save_extracted_data(list_item, detail)
