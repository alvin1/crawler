from modules.settings import Settings
from modules.html_loader import HtmlLoader
from modules.logger import Logger
from modules.extracter import Extracter
from modules.file_helper import FileHelper

def process_detail_page(item):
    soup = html_loader.get_page_soup(url=item['page_url'], page=item['page_num'])
    if soup is None:
        extracter.save_failed_page(item['tender_id'], item['page_url'], 'grab', page, 'detail',
                                   item['publish_date'])
        return

    try:
        detail = extracter.extract_detail(soup)
        extracter.save_extracted_data(item, detail)
        logger.info("Grab data of page success")
    except:
        extracter.save_failed_page(item['tender_id'], item['page_url'], 'extract', page, 'detail',
                                   item['publish_date'])
        logger.error('Grab data of page failed')

def process_list_page(lists):
    for item in lists:
        process_detail_page(item)

if __name__ == '__main__':
    html_loader = HtmlLoader()
    extracter = Extracter()
    logger = Logger()
    file_helper = FileHelper()

    # get last extract status
    last_status = extracter.get_last_extract_status()
    last_extract_page = last_status['page']
    total_pages_last_status = last_status['total_pages']

    # get first page
    logger.info('Get total records from first page')
    soup = html_loader.get_page_soup(url=Settings.URL, page=1)
    if soup is None:
        logger.info("Get total records from first page. Exit data process.")
        exit(100)

    record_status = extracter.extract_record_status(soup)
    if last_extract_page == 1:
        new_pages = record_status['total_pages'] - total_pages_last_status
        last_extract_page = new_pages
        extracter.update_tender_page_num(page_num=new_pages)
    last_page_data_in_db = extracter.get_trenders_by_page_num(page_num=last_extract_page)

    last_page_need_grab = False
    if last_extract_page is None:
        last_extract_page = record_status['total_pages']
    else:
        # check the last page need to grab or not
        if len(last_page_data_in_db) != Settings.PAGE_SIZE:
            last_page_need_grab = True
    logger.info('Grab data from page: %s' % last_extract_page)
    pages = last_extract_page

    page_array = range(1, pages + (1 if last_page_need_grab else 0))
    page_array.reverse()

    # get data from earlier to current
    for page in page_array:
        logger.info("Grab data of page: %s" % page)
        extracter.save_extract_status(page_num=page)
        soup = html_loader.get_page_soup(url=Settings.URL, page=page)
        if soup is None:
            continue
        lists = extracter.extract_list(soup, page)
        if page == last_extract_page:
            lists = [item for item in lists if item['tender_id'] not in last_page_data_in_db]
        process_list_page(lists)

    # trying to process the failed grab
    logger.info("Start to process the grab failed pages")
    for retry_times in range(1, Settings.RETRY_TIMES + 1):
        failed_pages = extracter.get_failed_grab_pages()
        for page in failed_pages['data']:
            if page['page_type'] == 'list':
                soup = html_loader.get_page_soup(url=page['page_url'], page=page['page_num'])
                if soup is None:
                    extracter.save_reprocess_status(page['page_url'], page['page_num'], False)
                    continue
                extracter.save_reprocess_status(page['page_url'], page['page_num'], True)
                lists = extracter.extract_list(soup, page['page_num'])
                process_list_page(lists)
            else:
                process_detail_page(page)
