import re
import os
from modules.file_helper import FileHelper
from modules.html_loader import HtmlLoader


if __name__ == '__main__':
    loader = HtmlLoader()
    file_helper = FileHelper()

    debug_pages = [
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=a9e29e7b-da58-47cc-a9a4-0d9340a62282&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=22890968-fc9b-44e3-bc5f-1440e62e0428&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=1f46cabd-204a-4309-90d2-759b912da047&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=6bb1dbcc-134b-4bc1-9e85-4ac114d2f81b&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=a3b7960e-287a-47fe-9beb-db2495a7a9f0&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=4679b8f1-f5a4-44b2-bde2-f70872076b8d&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=b5e20669-a119-4da6-b7ca-ccb97456fbe3&CategoryNum=005001003'
    ]

    page_path = "debug_pages/"

    info_id_pattarn = re.compile(u'.+InfoID=(?P<INFOID>.+)&.+')
    for page in debug_pages:
        match = info_id_pattarn.match(page)
        if match:
            page_id = match.group('INFOID')
            page_file_name = os.path.join(page_path, page_id + '.html')
            file_helper.write(page_file_name, loader.get_page_content(page, 1, 3))
