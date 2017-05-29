import threadpool
import json

from modules.settings import Settings
from modules.html_loader import HtmlLoader
from modules.file_helper import FileHelper
from modules.logger import Logger
from modules.extracter import Extracter
from modules.extract_helper import ExtractHelper

if __name__ == '__main__':
    html_loader = HtmlLoader()
    logger = Logger()
    file_helper = FileHelper()
    extracter = Extracter()
    extract_helper = ExtractHelper()

    last_extract_status = extracter.get_last_extract_status()

    # get first page
    soup = html_loader.get_page_soup(url=Settings.URL, page=1)
    record_status = extracter.extract_record_status(soup)
    bid_list = extracter.extract_list(soup, page=1)

    new_list = []

    records_need_to_extract = record_status['total_records'] - last_extract_status['total_records']
    pages = int(records_need_to_extract / Settings.PAGE_SIZE)

    if records_need_to_extract % Settings.PAGE_SIZE != 0:
        pages += 1
    """
    data = []
    pool = threadpool.ThreadPool(num_workers=1)

    thread_request = threadpool.makeRequests(callable_=extract_helper.extract_lists,
                                             args_list=[([current_page, data], None) for current_page in
                                                        range(2, 4)])
    [pool.putRequest(req) for req in thread_request]
    pool.wait()
    """
    soup = html_loader.get_page_soup(url=Settings.DETAIL_URL, page=1)
    detail = extracter.extract_detail(soup)
    print json.dumps(detail, sort_keys=True, indent=2)
