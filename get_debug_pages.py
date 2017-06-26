import re
import os
from modules.file_helper import FileHelper
from modules.html_loader import HtmlLoader


if __name__ == '__main__':
    loader = HtmlLoader()
    file_helper = FileHelper()

    debug_pages = [
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=1b5686fc-3633-4187-a9e6-cfc609e7c3ee&CategoryNum=005001003'
    ]

    page_path = "debug_pages/"

    info_id_pattarn = re.compile(u'.+InfoID=(?P<INFOID>.+)&.+')
    for page in debug_pages:
        match = info_id_pattarn.match(page)
        if match:
            page_id = match.group('INFOID')
            page_file_name = os.path.join(page_path, page_id + '.html')
            content = loader.get_detail_page(page, 1)
            print(content)
            file_helper.write(page_file_name, content)
