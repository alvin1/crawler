import threadpool
import time
import traceback

from modules.settings import Settings
from modules.html_loader import HtmlLoader
from modules.logger import Logger
from modules.extracter import Extracter


def worker(page, retry_times = 0):
    html_loader = HtmlLoader()
    extracter = Extracter()
    logger = Logger()

    logger.warning('page=%s' % page)

    try:
        soup = html_loader.get_page_soup(url=Settings.URL, page=page)
        lists = extracter.extract_list(soup, page)
    except Exception, e:
        retry_times += 1
        if Settings.RETRY_TIMES == 0:
            logger.warning(
                'Load page failed. Retrying: %s.\n%s.\n%s' % (retry_times, e.message, traceback.print_stack()))
            time.sleep(2)
            worker(page, retry_times)
        else:
            if retry_times <= Settings.RETRY_TIMES:
                logger.warning('Load page failed. Retrying: %s.\n%s.\n%s' % (retry_times, e.message, traceback.print_stack()))
                time.sleep(2)
                worker(page, retry_times)
            else:
                logger.error('Max retry time reached. Not retry any more. page: %s' % page)
    time.sleep(1)

if __name__ == '__main__':
    html_loader = HtmlLoader()
    extracter = Extracter()

    last_extract_status = extracter.get_last_extract_status()

    # get first page
    soup = html_loader.get_page_soup(url=Settings.URL, page=1)
    record_status = extracter.extract_record_status(soup)
    tender_list = extracter.extract_list(soup, page=1)

    records_need_to_extract = record_status['total_records'] - last_extract_status['total_records']
    pages = int(records_need_to_extract / Settings.PAGE_SIZE)

    if records_need_to_extract % Settings.PAGE_SIZE != 0:
        pages += 1

    page_array = range(2, pages + 1)
    """
    for item in tender_list:
        soup = html_loader.get_page_soup(url=item['page_url'], page=1)
        detail = extracter.extract_detail(soup)
        # print json.dumps(detail, sort_keys=True, indent=2)
    """

    # pool = threadpool.ThreadPool(num_workers=Settings.MAX_CLIENTS)
    pool = threadpool.ThreadPool(num_workers=100)
    thread_request = threadpool.makeRequests(callable_=worker,
                                             args_list=[([current_page], None) for current_page in
                                                        range(2, pages + 1)])
    [pool.putRequest(req) for req in thread_request]
    pool.poll()
    pool.wait()
