from modules.settings import Settings
from modules.html_loader import HtmlLoader
from modules.logger import Logger
from modules.extracter import Extracter
from modules.file_helper import FileHelper


def worker(page):
    html_loader = HtmlLoader()
    extracter = Extracter()
    logger = Logger()

    logger.warning('page=%s' % page)

    soup = html_loader.get_page_soup(url=Settings.URL, page=page)
    lists = extracter.extract_list(soup, page)
    for item in lists:
        soup = html_loader.get_page_soup(url=item['page_url'], page=1)
        detail = extracter.extract_detail(soup)
        extracter.save_extracted_data(item, detail)

if __name__ == '__main__':
    html_loader = HtmlLoader()
    extracter = Extracter()
    logger = Logger()
    file_helper = FileHelper()

    # get last extract status
    last_extract_page = extracter.get_last_extract_status()
    # TODO: need process when last page is 1
    last_page_data_in_db = extracter.get_trenders_by_page_num(page_num=last_extract_page)

    # get first page
    print('Get total records from first page')
    soup = html_loader.get_page_soup(url=Settings.URL, page=1)
    if soup is None:
        print("Get total records from first page. Exit data process.")
        exit(100)

    record_status = extracter.extract_record_status(soup)

    last_page_need_grab = False
    if last_extract_page is None:
        last_extract_page = record_status['total_pages']
    else:
        # check the last page need to grab or not
        if len(last_page_data_in_db) != Settings.PAGE_SIZE:
            last_page_need_grab = True
    print('Grab data from page: %s' % last_extract_page)
    # records_need_to_extract = last_extract_page
    pages = last_extract_page

    # if records_need_to_extract % Settings.PAGE_SIZE != 0:
    #     pages += 1

    page_array = range(1, pages + (1 if last_page_need_grab else 0))
    page_array.reverse()

    # get data from earlier to current
    for page in page_array:
        print('Get data of page %s' % page)
        logger.info("Grab data of page: %s" % page)
        extracter.save_extract_status(page_num=page)
        soup = html_loader.get_page_soup(url=Settings.URL, page=page)
        if soup is None:
            continue
        lists = extracter.extract_list(soup, page)
        if page == last_extract_page:
            lists = [item for item in lists if item['info_id'] not in last_page_data_in_db]
        for item in lists:
            soup = html_loader.get_page_soup(url=item['page_url'], page=page)
            if soup is None:
                logger.error("The page content is blank, may have some issues when grab")
                extracter.save_failed_page(item['info_id'], item['page_url'], 'grab')
                continue
            try:
                detail = extracter.extract_detail(soup)
                print('extract done')
                extracter.save_extracted_data(item, detail)
                print('saved')
                logger.info("Grab data of page success")
            except:
                print('extract failed')
                extracter.save_failed_page(item['info_id'], item['page_url'], 'extract')
                logger.error('Grab data of page failed')
