import os
from modules.file_helper import FileHelper
from modules.html_loader import HtmlLoader
from modules.extracter import Extracter


if __name__ == '__main__':
    file_helper = FileHelper()
    html_loader = HtmlLoader()
    extracter = Extracter()

    page_dir = "debug_pages/"
    page_path = os.path.join(page_dir, '1f46cabd-204a-4309-90d2-759b912da047' + '.html')

    soup = html_loader.beautiful_page_content(file_helper.read(page_path))
    detail = extracter.extract_detail(soup)
    print(detail)