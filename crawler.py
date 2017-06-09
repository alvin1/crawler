from modules.settings import Settings
from modules.html_loader import HtmlLoader
from modules.logger import Logger
from modules.extracter import Extracter


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

    # get last extract status
    last_extract_status = extracter.get_last_extract_status()

    # get first page
    print('Get data of page 1')
    soup = html_loader.get_page_soup(url=Settings.URL, page=1)
    if soup is None:
        print("Get page 1 data failed. Exit data process.")
        exit(100)

    record_status = extracter.extract_record_status(soup)
    tender_list = extracter.extract_list(soup, page=1)

    records_need_to_extract = record_status['total_records'] - last_extract_status['total_records']
    pages = int(records_need_to_extract / Settings.PAGE_SIZE)

    if records_need_to_extract % Settings.PAGE_SIZE != 0:
        pages += 1

    page_array = range(1, pages + 1)

    # get data from earlier to current
    for page in page_array.reverse():
        print('Get data of page %s' % page)
        soup = html_loader.get_page_soup(url=Settings.URL, page=page)
        if soup is None:
            continue
        lists = extracter.extract_list(soup, page)
        for item in lists:
            soup = html_loader.get_page_soup(url=item['page_url'], page=1)
            if soup is None:
                continue
            detail = extracter.extract_detail(soup)
            extracter.save_extracted_data(item, detail)
