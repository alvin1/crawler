from datetime import datetime
import re
import json

from .settings import Settings
from .file_helper import FileHelper

from database.models.tender_info import TrenderInfo
from database.models.candidate import Candidate
from database.models.candidate_incharge import CandidateIncharge
from database.models.candidate_incharge_projects import CandidateInChargeProjects
from database.models.candidate_projects import CandidateProjects
from database.models.other_tenderer_review import OtherTendererReview
from database.models.review_board_member import ReviewBoardMember
from database.models.failed_page import FailedPage
from database.models.grab_status import GrabStatus

class Extracter(object):
    def __init__(self):
        self.extracter_status_file = 'var/status/last_extract.json'
        self.file_helper = FileHelper()
        self.file_helper.poke_dir(self.file_helper.get_dir_from_path(self.extracter_status_file))

    def clean_content(self, content):
        if content is None:
            return None

        new_content = content.replace('\r\n', '').replace('\t', '').lstrip()
        return re.sub(r'\t.+', '', re.sub(r'\n.+', '', new_content))

    def extract_list(self, soup, page):
        list = []

        tender_id_pattarn = re.compile(u'.+InfoID=(?P<INFOID>.+)&.+')
        for item in soup.select('#MoreInfoList1_tdcontent tr'):
            a = item.select('a')[0]
            match = tender_id_pattarn.match(a['href'])
            date = self.clean_content(item.select('td')[2].string)

            list.append({
                'title': self.convert_type('string', a['title']),
                'pubdate': date,
                'page_url': "%s%s" % (Settings.DOMAIN, a['href']),
                'page_num': page,
                'tender_id': match.group('INFOID') if match else ''
            })
        return list

    def extract_record_status(self, soup):
        record_status = soup.select('#MoreInfoList1_Pager td b')
        return {
            'total_records': int(record_status[0].string),
            'total_pages': int(record_status[1].string)
        }

    def get_last_extract_status(self):
        status = GrabStatus()
        return status.get()

    def save_extract_status(self, page_num, total_pages):
        status = GrabStatus(page_num=page_num, total_pages=total_pages)
        status.save()

    def get_content(self, soup):
        if soup.string is not None:
            return soup.string if soup.string != '\n' else u''

        if len(soup.contents) == 0:
            return u''

        values = []
        for item in soup.contents:
            values.extend(self.get_content(item))
        return values

    def get_cell_content(self, td_soup):
        if td_soup.string is not None:
            return td_soup.string if td_soup.string != '\n' else u''

        values = []
        for item in td_soup.contents:
            values.extend(self.get_content(item))
        return self.clean_content(u"".join(values))

    def convert_type(self, data_type, value):
        if value is None:
            return None

        if data_type == 'string':
            return value.replace(u'\xa0', u' ').replace(u'\u2022', '.').encode('utf8')
        elif data_type == 'int':
            return int(value)
        elif data_type == 'datetime':
            if len(value.replace(u'\xa0', '')) == 0:
                return None
            try:
                value = value.replace(u'\xa0', '').replace(u'\u5e74', '-').replace(u'\u6708', '-').replace(
                    u'\u65e5', '').replace("/", "-")
                if len(value) > 10:
                    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                else:
                    return datetime.strptime(value.replace(' ',''), '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S")
            except:
                return value
            # return value
        elif data_type == 'decimal':
            try:
                return float(value)
            except:
                return None

    def find_row_number_by_key(self, key, rows):
        start_line = 0

        for row in rows:
            for item in [self.get_cell_content(item).replace('\t', '').replace('\n', '').replace(' ', '') for item in row.select('td')]:
                for key_item in key:
                    # if item and key_item in item:
                    if item and key_item == item:
                        return start_line
            start_line += 1
        return None

    def extract_field_value(self, row, field, data):
        value_of_key = self.get_cell_content(row.select('td')[field['extract']['column']])
        if value_of_key and 'remove' in field['extract']:
            for remove_key in field['extract']['remove']:
                value_of_key = value_of_key.replace(remove_key, u'')
        if 'split_pattern' in field['extract']:
            match = field['extract']['split_pattern'].match(value_of_key)
            if match:
                for split_field in field['extract']['split_result']:
                    split_data = match.group(split_field['key'])
                    data[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
        else:
            data[field['field_name']] = self.convert_type(field['data_type'], value_of_key)

    def check_all_keys_blank(self, row):
        for k,v in row.items():
            if v is not None and v != ' ':
                return False
        return True

    def extract_detail(self, soup):
        details = {}

        rows = soup.select('#_Sheet1 tr')
        if len(rows) == 0:
            rows = soup.select('table .MsoNormalTable [width=675] tr')
            if len(rows) == 0:
                rows = soup.select('#ivs_content table tr')
        # 1. extract tender info
        details['tender_info'] = []
        tender_name_config = Settings.DETAIL_COORDINATE['tender_name']
        start_row = self.find_row_number_by_key(tender_name_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        tender_info = {}
        tender_info['pubdate'] = self.convert_type('datetime',
                                                   soup.select("font.webfont")[0].contents[0].split('\n')[1].replace(
                                                       ' ', ''))
        for field in tender_name_config['fields']:
            self.extract_field_value(rows_of_range, field, tender_info)

        owner_config = Settings.DETAIL_COORDINATE['owner']
        start_row = self.find_row_number_by_key(owner_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        for field in owner_config['fields']:
            self.extract_field_value(rows_of_range, field, tender_info)

        owner_phone_config = Settings.DETAIL_COORDINATE['owner_phone']
        start_row = self.find_row_number_by_key(owner_phone_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        for field in owner_phone_config['fields']:
            self.extract_field_value(rows_of_range, field, tender_info)

        tenderee_config = Settings.DETAIL_COORDINATE['tenderee']
        start_row = self.find_row_number_by_key(tenderee_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        for field in tenderee_config['fields']:
            self.extract_field_value(rows_of_range, field, tender_info)

        tenderee_phone_config = Settings.DETAIL_COORDINATE['tenderee_phone']
        start_row = self.find_row_number_by_key(tenderee_phone_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        for field in tenderee_phone_config['fields']:
            self.extract_field_value(rows_of_range, field, tender_info)

        tenderee_proxy_config = Settings.DETAIL_COORDINATE['tenderee_proxy']
        start_row = self.find_row_number_by_key(tenderee_proxy_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        for field in tenderee_proxy_config['fields']:
            self.extract_field_value(rows_of_range, field, tender_info)

        tenderee_proxy_phone_config = Settings.DETAIL_COORDINATE['tenderee_proxy_phone']
        start_row = self.find_row_number_by_key(tenderee_proxy_phone_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        for field in tenderee_proxy_phone_config['fields']:
            self.extract_field_value(rows_of_range, field, tender_info)

        publicity_config = Settings.DETAIL_COORDINATE['publicity']
        publicity_row = self.find_row_number_by_key(publicity_config['title_row_key'], rows)
        if publicity_row is not None:
            rows_of_range = rows[publicity_row]
            for field in publicity_config['fields']:
                self.extract_field_value(rows_of_range, field, tender_info)

        tender_openning_location_config = Settings.DETAIL_COORDINATE['tender_openning_location']
        start_row = self.find_row_number_by_key(tender_openning_location_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        field = tender_openning_location_config['fields'][0]
        if publicity_row is not None:
            field['extract']['column'] = 1
        else:
            field['extract']['column'] = 3
        self.extract_field_value(rows_of_range, field, tender_info)

        tender_openning_time_config = Settings.DETAIL_COORDINATE['tender_openning_time']
        start_row = self.find_row_number_by_key(tender_openning_time_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        field = tender_openning_time_config['fields'][0]
        if publicity_row is not None:
            field['extract']['column'] = 3
        else:
            field['extract']['column'] = 1
        self.extract_field_value(rows_of_range, field, tender_info)

        tender_ceil_price_config = Settings.DETAIL_COORDINATE['tender_ceil_price']
        start_row = self.find_row_number_by_key(tender_ceil_price_config['title_row_key'], rows)
        rows_of_range = rows[start_row]
        for field in tender_ceil_price_config['fields']:
            if self.find_row_number_by_key(publicity_config['title_row_key'], rows) is not None:
                value_of_key = rows_of_range.select('td')[field['extract']['column']].string
            else:
                value_of_key = self.get_cell_content(rows_of_range.select('td')[1])
            if value_of_key and 'remove' in field['extract']:
                for remove_key in field['extract']['remove']:
                    value_of_key = value_of_key.replace(remove_key, u'')
            if 'split_pattern' in field['extract']:
                match = field['extract']['split_pattern'].match(value_of_key)
                if match:
                    for split_field in field['extract']['split_result']:
                        split_data = match.group(split_field['key'])
                        tender_info[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
            else:
                tender_info[field['field_name']] = self.convert_type(field['data_type'], value_of_key)

        details['tender_info'].append(tender_info)

        # 2. extract candidate list
        candidate_config = Settings.DETAIL_COORDINATE['candidate']
        details['candidate'] = []
        start_row = self.find_row_number_by_key(candidate_config['title_row_key'], rows)
        next_start_row = self.find_row_number_by_key(candidate_config['next_title_row_key'], rows)
        rows_of_range = rows[start_row + 2:next_start_row]

        tmp_row_index = 0
        incharge_in_same_line = False
        title_row = rows[start_row ]
        for col in title_row.select('td'):
            col_value = self.get_cell_content(col)
            if u'\u62df\u4efb\u9879\u76ee\u8d1f\u8d23\u4eba' == col_value:
                incharge_in_same_line = True
                break

        for row_data in rows_of_range:
            tmp_row_index += 1
            columns = row_data.select('td')
            if len(columns) == 1:
                break
            candidate = {}
            for field in candidate_config['fields']:
                self.extract_field_value(row_data, field, candidate)
            details['candidate'].append(candidate)
        # 2.1 extract candidate_incharge list
        if not incharge_in_same_line:
            for candidate in details['candidate']:
                candidate['incharge_start'] = tmp_row_index + 2
                tmp_row_index += 2
                for row_data in rows_of_range[tmp_row_index:]:
                    columns = row_data.select('td')
                    if len(columns) != len(candidate_config['inchage_fields']):
                        candidate['incharge_end'] = tmp_row_index
                        tmp_row_index += 1
                        break
                    tmp_row_index += 1
            for candidate in details['candidate']:
                candidate['incharge'] = []
                incharge_rows = rows_of_range[candidate['incharge_start']:candidate['incharge_end']]
                for incharge_row in incharge_rows:
                    incharge = {}
                    for field in candidate_config['inchage_fields']:
                        self.extract_field_value(incharge_row, field, incharge)
                    candidate['incharge'].append(incharge)
        else:
            index = 0
            for candidate in details['candidate']:
                candidate['incharge'] = []
                for incharge_row in rows_of_range[index: index + 1]:
                    incharge = {
                        'incharge_type': u'\u9879\u76ee\u8d1f\u8d23\u4eba'
                    }
                    fields = [
                        {
                            'field_name': 'incharge_name',
                            'data_type': 'string',
                            'extract': {
                                'column': 5
                            }
                        },
                        {
                            'field_name': 'incharge_certificate_name',
                            'data_type': 'string',
                            'extract': {
                                'column': 6
                            }
                        },
                        {
                            'field_name': 'incharge_certificate_no',
                            'data_type': 'string',
                            'extract': {
                                'column': 7
                            }
                        }
                    ]
                    for field in fields:
                        self.extract_field_value(incharge_row, field, incharge)
                    candidate['incharge'].append(incharge)
                    break
                index += 1
        # 2.2 extract the candidate projects and candidate incharge projects
        break_time = 0
        candidate_index = -1
        for candidate in details['candidate']:
            candidate['project_start'] = tmp_row_index + 1
            if len(rows_of_range[tmp_row_index:]) == 0:
                break
            candidate_index += 1
            for row_data in rows_of_range[tmp_row_index:]:
                columns = row_data.select('td')
                if len(columns) == 1:
                    break_time += 1
                    if break_time == 1:
                        candidate['project_end'] = tmp_row_index
                        tmp_row_index += 1
                        candidate['incharge_project_start'] = tmp_row_index + 1
                    else:
                        candidate['incharge_project_end'] = tmp_row_index
                        break_time = 0
                        tmp_row_index += 1
                        break
                else:
                    tmp_row_index += 1

        if len(details['candidate']) > 0:
            details['candidate'][candidate_index]['incharge_project_end'] = tmp_row_index

        for candidate in details['candidate']:
            candidate['projects'] = []
            candidate['incharge_projects'] = []
            if 'project_start' not in candidate or 'project_end' not in candidate:
                continue
            for project_row in rows_of_range[candidate['project_start']:candidate['project_end']]:
                project = {}
                fields = candidate_config['project_fields']
                if len(project_row.select('td')) == 7:
                    fields = [
                        {
                            'field_name': 'owner',
                            'field_title': u'\u9879\u76ee\u4e1a\u4e3b',
                            'data_type': 'string',
                            'extract': {
                                'column': 0
                            }
                        },
                        {
                            'field_name': 'name',
                            'field_title': u'\u9879\u76ee\u540d\u79f0 ',
                            'data_type': 'string',
                            'extract': {
                                'column': 1
                            }
                        },
                        {
                            'field_name': 'kick_off_date',
                            'field_title': u'\u5f00\u5de5\u65e5\u671f ',
                            'data_type': 'datetime',
                            'extract': {
                                'column': 2
                            }
                        },
                        {
                            'field_name': 'finish_date',
                            'field_title': u'\u7ae3\u5de5\u65e5\u671f',
                            'data_type': 'datetime',
                            'extract': {
                                'column': 3
                            }
                        },
                        {
                            'field_name': 'scale',
                            'field_title': u'\u5efa\u8bbe\u89c4\u6a21',
                            'data_type': 'string',
                            'extract': {
                                'column': 4
                            }
                        },
                        {
                            'field_name': 'contract_price',
                            'field_title': u'\u5408\u540c\u4ef7\u683c\uff08\u5143\uff09',
                            'data_type': 'decimal',
                            'extract': {
                                'column': 5
                            }
                        },
                        {
                            'field_name': 'project_incharge_name',
                            'field_title': u'\u9879\u76ee\u8d1f\u8d23\u4eba',
                            'data_type': 'string',
                            'extract': {
                                'column': 6
                            }
                        }
                    ]
                for field in fields:
                    self.extract_field_value(project_row, field, project)
                if not self.check_all_keys_blank(project):
                    candidate['projects'].append(project)

            for project_row in rows_of_range[candidate['incharge_project_start']:candidate['incharge_project_end']]:
                project = {}
                fields = candidate_config['inchage_project_fields']
                if len(project_row.select('td')) == 1:
                    break
                if len(project_row.select('td')) == 7:
                    fields = [
                        {
                            'field_name': 'owner',
                            'field_title': u'\u9879\u76ee\u4e1a\u4e3b',
                            'data_type': 'string',
                            'extract': {
                                'column': 0
                            }
                        },
                        {
                            'field_name': 'name',
                            'field_title': u'\u9879\u76ee\u540d\u79f0 ',
                            'data_type': 'string',
                            'extract': {
                                'column': 1
                            }
                        },
                        {
                            'field_name': 'kick_off_date',
                            'field_title': u'\u5f00\u5de5\u65e5\u671f ',
                            'data_type': 'datetime',
                            'extract': {
                                'column': 2
                            }
                        },
                        {
                            'field_name': 'finish_date',
                            'field_title': u'\u7ae3\u5de5\u65e5\u671f',
                            'data_type': 'datetime',
                            'extract': {
                                'column': 3
                            }
                        },
                        {
                            'field_name': 'scale',
                            'field_title': u'\u5efa\u8bbe\u89c4\u6a21',
                            'data_type': 'string',
                            'extract': {
                                'column': 4
                            }
                        },
                        {
                            'field_name': 'contract_price',
                            'field_title': u'\u5408\u540c\u4ef7\u683c\uff08\u5143\uff09',
                            'data_type': 'decimal',
                            'extract': {
                                'column': 5
                            }
                        },
                        {
                            'field_name': 'tech_incharge_name',
                            'field_title': u'\u6280\u672f\u8d1f\u8d23\u4eba',
                            'data_type': 'string',
                            'extract': {
                                'column': 6
                            }
                        }
                    ]
                for field in fields:
                    self.extract_field_value(project_row, field, project)
                if not self.check_all_keys_blank(project):
                    candidate['incharge_projects'].append(project)

        # 3 extract other tenders list
        other_tenders_config = Settings.DETAIL_COORDINATE['other_tenderer_review']
        start_row = self.find_row_number_by_key(other_tenders_config['title_row_key'], rows)
        next_start_row = self.find_row_number_by_key(other_tenders_config['next_title_row_key'], rows)
        rows_of_range = rows[start_row + 2:next_start_row]
        details['other_tenderer_review'] = []
        for row in rows_of_range:
            other_tender = {}
            if len(row.select('td')) == 3:
                fields = other_tenders_config['fields'][0:2]
                fields.append(other_tenders_config['fields'][3])
                fields[-1]['extract']['column'] = 2
                for field in fields:
                    self.extract_field_value(row, field, other_tender)
            else:
                for field in other_tenders_config['fields']:
                    self.extract_field_value(row, field, other_tender)
            details['other_tenderer_review'].append(other_tender)

        # 4 extract other_description
        other_desc_config = Settings.DETAIL_COORDINATE['other_description']
        start_row = self.find_row_number_by_key(other_desc_config['title_row_key'], rows)
        next_start_row = self.find_row_number_by_key(other_desc_config['next_title_row_key'], rows)
        rows_of_range = rows[start_row + 2:next_start_row]
        details['other_description'] = []
        for row in rows_of_range:
            other_desc = {}
            for field in other_desc_config['fields']:
                self.extract_field_value(row, field, other_desc)
            details['other_description'].append(other_desc)

        # 5 extract review_board_member
        review_member_config = Settings.DETAIL_COORDINATE['review_board_member']
        start_row = self.find_row_number_by_key(review_member_config['title_row_key'], rows)
        if start_row is not None:
            next_start_row = self.find_row_number_by_key(review_member_config['next_title_row_key'], rows)
            rows_of_range = rows[start_row + 2:next_start_row]
            details['review_board_member'] = []
            for row in rows_of_range:
                review_member = {}
                for field in review_member_config['fields']:
                    self.extract_field_value(row, field, review_member)
                details['review_board_member'].append(review_member)

        # 6 extract review_department
        review_depart_config = Settings.DETAIL_COORDINATE['review_department']
        start_row = self.find_row_number_by_key(review_depart_config['title_row_key'], rows)
        next_start_row = self.find_row_number_by_key(review_depart_config['next_title_row_key'], rows)
        rows_of_range = rows[start_row:next_start_row]
        details['review_department'] = []
        for row in rows_of_range:
            review_depart = {}
            for field in review_depart_config['fields']:
                self.extract_field_value(row, field, review_depart)
            details['review_department'].append(review_depart)

        # 7 extract administration_department
        admin_depart_config = Settings.DETAIL_COORDINATE['administration_department']
        start_row = self.find_row_number_by_key(admin_depart_config['title_row_key'], rows)
        next_start_row = self.find_row_number_by_key(admin_depart_config['next_title_row_key'], rows)
        rows_of_range = rows[start_row:next_start_row]
        details['administration_department'] = []
        for row in rows_of_range:
            admin_depart = {}
            for field in admin_depart_config['fields']:
                self.extract_field_value(row, field, admin_depart)
            details['administration_department'].append(admin_depart)
            break

        return details

    def get_data_from_dict(self, dict, key, default=''):
        if key in dict:
            return dict[key]
        return default

    def save_extracted_data(self, list_item, item_detail):
        tender_info = TrenderInfo(tender_id=self.get_data_from_dict(list_item, 'tender_id'),
                                   tender_name=self.get_data_from_dict(item_detail['tender_info'][0], 'tender_name'),
                                   pubdate=self.get_data_from_dict(item_detail['tender_info'][0], 'pubdate'),
                                   page_url=self.get_data_from_dict(list_item, 'page_url'),
                                   owner=self.get_data_from_dict(item_detail['tender_info'][0], 'owner'),
                                   owner_phone=self.get_data_from_dict(item_detail['tender_info'][0], 'owner_phone'),
                                   tenderee=self.get_data_from_dict(item_detail['tender_info'][0], 'tenderee'),
                                   tenderee_phone=self.get_data_from_dict(item_detail['tender_info'][0], 'tenderee_phone'),
                                   tenderee_proxy=self.get_data_from_dict(item_detail['tender_info'][0], 'tenderee_proxy'),
                                   tenderee_proxy_phone=self.get_data_from_dict(item_detail['tender_info'][0], 'tenderee_proxy_phone'),
                                   tender_openning_location=self.get_data_from_dict(item_detail['tender_info'][0], 'tender_openning_location'),
                                   tender_openning_time=self.get_data_from_dict(item_detail['tender_info'][0], 'tender_openning_time'),
                                   tender_ceil_price=self.get_data_from_dict(item_detail['tender_info'][0], 'tender_ceil_price'),
                                   publicity_start=self.get_data_from_dict(item_detail['tender_info'][0], 'publicity_start', None),
                                   publicity_end=self.get_data_from_dict(item_detail['tender_info'][0], 'publicity_end', None),
                                   other_description=self.get_data_from_dict(item_detail['other_description'][0], 'other_description') if len(item_detail['other_description']) == 1 else '',
                                   review_department=self.get_data_from_dict(item_detail['review_department'][0], 'review_department'),
                                   review_department_phone=self.get_data_from_dict(item_detail['review_department'][0], 'review_department_phone'),
                                   administration_department=self.get_data_from_dict(item_detail['administration_department'][0], 'administration_department'),
                                   administration_department_phone=self.get_data_from_dict(item_detail['administration_department'][0], 'administration_department_phone'),
                                   page_num=self.get_data_from_dict(list_item, 'page_num')
                                   )
        tender_info.save()

        # candidate_index = 1
        for item in item_detail['candidate']:
            candidate = Candidate(tender_id=self.get_data_from_dict(list_item, 'tender_id'),
                                  ranking=self.get_data_from_dict(item, 'ranking'),
                                  candidate_name=self.get_data_from_dict(item, 'candidate_name'),
                                  tender_price=self.get_data_from_dict(item, 'tender_price'),
                                  tender_price_review=self.get_data_from_dict(item, 'tender_price_review'),
                                  review_score=self.get_data_from_dict(item, 'review_score'))
            candidate_id = candidate.save()
            item['candidate_id'] = candidate_id
            # identity_key = "candidate_%s" % candidate_index
            for incharge_item in item['incharge']:
                candidate_incharge = CandidateIncharge(tender_id=self.get_data_from_dict(list_item, 'tender_id'),
                                                       candidate_id=candidate_id,
                                                       incharge_id='',
                                                       incharge_type=self.get_data_from_dict(incharge_item, 'incharge_type'),
                                                       incharge_name=self.get_data_from_dict(incharge_item, 'incharge_name'),
                                                       incharge_certificate_name=self.get_data_from_dict(incharge_item, 'incharge_certificate_name'),
                                                       incharge_certificate_no=self.get_data_from_dict(incharge_item, 'incharge_certificate_no'),
                                                       professional_grade=self.get_data_from_dict(incharge_item, 'professional_grade', None),
                                                       professional_titles=self.get_data_from_dict(incharge_item, 'professional_titles', None))
                incharge_id = candidate_incharge.save()
                incharge_item['incharge_id'] = incharge_id
            for project_item in item['projects']:
                candidate_projects = CandidateProjects(tender_id=self.get_data_from_dict(list_item, 'tender_id'),
                                                       candidate_id=candidate_id,
                                                       owner=self.get_data_from_dict(project_item, 'owner'),
                                                       name=self.get_data_from_dict(project_item, 'name'),
                                                       kick_off_date=self.get_data_from_dict(project_item, 'kick_off_date'),
                                                       deliver_date=self.get_data_from_dict(project_item, 'deliver_date', None),
                                                       finish_date=self.get_data_from_dict(project_item, 'finish_date'),
                                                       scale=self.get_data_from_dict(project_item, 'scale'),
                                                       contract_price=self.get_data_from_dict(project_item, 'contract_price'),
                                                       project_incharge_name=self.get_data_from_dict(project_item, 'project_incharge_name'))
                candidate_projects.save()
            for project_item in item['incharge_projects']:
                candidate_incharge_projects = CandidateInChargeProjects(tender_id=self.get_data_from_dict(list_item, 'tender_id'),
                                                                        candidate_id=candidate_id,
                                                                        incharge_id=incharge_id,
                                                                        owner=self.get_data_from_dict(project_item, 'owner'),
                                                                        name=self.get_data_from_dict(project_item, 'name'),
                                                                        kick_off_date=self.get_data_from_dict(project_item, 'kick_off_date'),
                                                                        deliver_date=self.get_data_from_dict(project_item, 'deliver_date', None),
                                                                        finish_date=self.get_data_from_dict(project_item, 'finish_date'),
                                                                        scale=self.get_data_from_dict(project_item, 'scale'),
                                                                        contract_price=self.get_data_from_dict(project_item, 'contract_price'),
                                                                        tech_incharge_name=self.get_data_from_dict(project_item,
                                                                            'tech_incharge_name'))
                candidate_incharge_projects.save()

        for item in item_detail['other_tenderer_review']:
            other_tenderer_review = OtherTendererReview(tender_id=self.get_data_from_dict(list_item, 'tender_id'),
                                                        tenderer_name=self.get_data_from_dict(item, 'tenderer_name'),
                                                        price_or_vote_down=self.get_data_from_dict(item, 'price_or_vote_down'),
                                                        price_review_or_vote_down_reason=self.get_data_from_dict(item, 'price_review_or_vote_down_reason', None),
                                                        review_score_or_description=self.get_data_from_dict(item, 'review_score_or_description'))
            tenderer_id = other_tenderer_review.save()
            item['tenderer_id'] = tenderer_id
        if 'review_board_member' in item_detail:
            for item in item_detail['review_board_member']:
                review_board_member = ReviewBoardMember(tender_id=self.get_data_from_dict(list_item, 'tender_id'),
                                                        name=self.get_data_from_dict(item, 'member_name'),
                                                        company=self.get_data_from_dict(item, 'member_company'))
                review_board_member.save()

    def save_failed_page(self, tender_id, page_url, failed_type, page_num, page_type, pubdate):
        if failed_type not in ['grab', 'extract']:
            return

        failed_page = FailedPage(tender_id, page_url, failed_type, page_num, page_type, pubdate)
        failed_page.save()

    def get_trenders_by_page_num(self, page_num):
        tender_info = TrenderInfo(page_num=page_num)
        trenders = tender_info.get_tenders_by_page_num()
        return [item['tender_id'] for item in trenders['data']]

    def update_tender_page_num(self, page_num):
        tender_info = TrenderInfo(page_num=page_num)
        tender_info.update_page_num()

    def get_failed_grab_pages(self):
        failed_page = FailedPage(failed_type='grab')
        return failed_page.get_failed_pages()

    def get_failed_extract_pages(self):
        failed_page = FailedPage(failed_type='extract')
        return failed_page.get_failed_pages()

    def save_reprocess_status(self, page_url, page_num, status):
        failed_page = FailedPage(page_url=page_url, page_num=page_num, reprocessed=(1 if status else 0))
        failed_page.update_reprocess_status()
