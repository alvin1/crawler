import re
import os
from modules.file_helper import FileHelper
from modules.html_loader import HtmlLoader


if __name__ == '__main__':
    loader = HtmlLoader()
    file_helper = FileHelper()

    debug_pages = [
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=2662e52d-e5f3-4685-b27f-7273609b2cdf&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=e72af24e-6328-468e-a9e3-6f2412cd3dc8&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=94537ee2-d01f-4756-8aea-8bb42b1ca07e&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=bc53ab8f-6981-48d7-a739-6701eed1d36a&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=da1098a8-0655-4748-b7de-ebfa003ec9a0&CategoryNum=005001003', # need fix
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=c00d2e22-2636-4646-8792-5d5e93d662e2&CategoryNum=005001003', # need fix
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=8b1371c4-ede1-4547-a15c-50540c2b3be0&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=1857d004-fdb3-4909-9ef6-f01382300bb7&CategoryNum=005001003',
        'http://www.spprec.com/sczw/InfoDetail/Default.aspx?InfoID=3f0a2dd7-1e13-4929-961b-a07808811650&CategoryNum=005001003'
    ]

    page_path = "debug_pages/"

    info_id_pattarn = re.compile(u'.+InfoID=(?P<INFOID>.+)&.+')
    for page in debug_pages:
        match = info_id_pattarn.match(page)
        if match:
            page_id = match.group('INFOID')
            page_file_name = os.path.join(page_path, page_id + '.html')
            content = loader.get_detail_page(page, 1)
            file_helper.write(page_file_name, content.decode('utf8'))
