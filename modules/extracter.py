from datetime import datetime
import json
import re
import uuid

from .settings import Settings
from .file_helper import FileHelper

from database.models.tender_info import TrenderInfo
from database.models.candidate import Candidate
from database.models.candidate_incharge import CandidateIncharge
from database.models.candidate_incharge_projects import CandidateInChargeProjects
from database.models.candidate_projects import CandidateProjects
from database.models.other_tenderer_review import OtherTendererReview
from database.models.review_board_member import ReviewBoardMember

class Extracter(object):
    def __init__(self):
        self.extracter_status_file = 'var/status/last_extract.json'
        self.file_helper = FileHelper()
        self.file_helper.poke_dir(self.file_helper.get_dir_from_path(self.extracter_status_file))

    def clean_content(self, content):
        return content.replace('\r\n', '').replace('\t', '')

    def extract_list(self, soup, page):
        list = []

        info_id_pattarn = re.compile(u'.+InfoID=(?P<INFOID>.+)&.+')
        for item in soup.select('#MoreInfoList1_tdcontent tr'):
            a = item.select('a')[0]
            match = info_id_pattarn.match(a['href'])
            # date = self.clean_content(item.select('td[width=80]')[0].string)
            date = self.clean_content(item.select('td')[2].string)

            list.append({
                'title': a['title'].encode("utf8"),
                'publish_date': date,
                'page_url': "%s%s" % (Settings.DOMAIN, a['href']),
                'page_index': page,
                'info_id': match.group('INFOID') if match else ''
            })
        return list

    def extract_record_status(self, soup):
        record_status = soup.select('#MoreInfoList1_Pager font[color=blue]')
        return {
            'total_records': int(record_status[0].string),
            'total_pages': int(record_status[1].string)
        }

    def get_last_extract_status(self):
        status = self.file_helper.get_json(self.extracter_status_file)
        if not status:
            status = {
                'info_id': '',
                'total_records': 0,
                'total_pages': 0
            }
        return status

    def convert_type(self, data_type, value):
        if not value:
            return None

        if data_type == 'string':
            return value.encode('utf8')
        elif data_type == 'int':
            return int(value)
        elif data_type == 'datetime':
            # return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return value
        elif data_type == 'decimal':
            return float(value)

    def find_row_number_by_key(self, key, rows):
        start_line = 0
        for row in rows:
            for item in [item.string for item in row.select('td')]:
                for key_item in key:
                    if item and key_item in item:
                        return start_line
            start_line += 1
        return None
    
    def extract_detail(self, soup):
        detail = {}
        rows = soup.select('#_Sheet1 tr')
        if len(soup.select('#_Sheet1')) == 0:
          print soup

        for item in Settings.DETAIL_COORDINATE:
            target_table = item['target_table']
            multiple_lines = item['multiple_lines']

            if target_table not in detail:
                detail[target_table] = []
            if not multiple_lines:
                data = {}
                if 'identity' in item:
                    data['identity'] = item['identity']
                for field in item['fields']:
                    field_name  = field['field_name']
                    data_type = field['data_type']
                    extract_rule = field['extract']
                    if 'row' in extract_rule:
                        row = extract_rule['row']
                    else:
                        row = self.find_row_number_by_key(title_row_key, rows)
                    value_of_key = rows[row + 1].select('td')[extract_rule['column']].string

                    if 'split_pattern' in extract_rule:
                        match = extract_rule['split_pattern'].match(value_of_key)
                        if match:
                            for split_field in extract_rule['split_result']:
                                split_data = match.group(split_field['key'])
                                data[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                    else:
                        data[field_name] = self.convert_type(data_type, value_of_key)
                detail[target_table].append(data)
            else:
                title_row_key = item['title_row_key']
                next_title_row_key = item['next_title_row_key']

                start_line = self.find_row_number_by_key(title_row_key, rows)
                next_start_line = self.find_row_number_by_key(next_title_row_key, rows)

                if not start_line or not next_start_line:
                    continue

                title_row_offset = 0
                if 'title_row_offset' in item:
                    title_row_offset = item['title_row_offset']

                data_of_range = rows[start_line + title_row_offset+ 1 : next_start_line]

                for data in data_of_range:
                    cells = data.select('td')
                    if len(cells) == 0:
                        continue
                    row_data = {}
                    if 'identity' in item:
                        row_data['identity'] = item['identity']
                    for field in item['fields']:
                        print(field)
                        print(item)
                        content = cells[field['extract']['column']].contents
                        field_value = None
                        if len(content) > 0:
                            field_value = content[0]
                        if 'field_title' in field and field['field_title'] == field_value:
                            continue

                        if 'split_pattern' in field['extract']:
                            match = field['extract']['split_pattern'].match(field_value)
                            if match:
                                for split_field in field['extract']['split_result']:
                                    split_data = match.group(split_field['key'])
                                    row_data[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                        else:
                            row_data[field['field_name']] = self.convert_type(field['data_type'], field_value)
                    if ('identity' in item and len(row_data.items()) > 1) or ('identity' not in item and len(row_data.items()) > 0):
                        detail[target_table].append(row_data)

        return detail

    def save_extracted_data(self, list_item, item_detail):
        trender_info = TrenderInfo(tender_id=list_item['info_id'],
                                   tender_name=item_detail['tender_info'][0]['tender_name'],
                                   pubdate=list_item['publish_date'],
                                   page_url=list_item['page_url'],
                                   owner=item_detail['tender_info'][0]['owner'],
                                   owner_phone=item_detail['tender_info'][0]['owner_phone'],
                                   tenderee=item_detail['tender_info'][0]['tenderee'],
                                   tenderee_phone=item_detail['tender_info'][0]['tenderee_phone'],
                                   tenderee_proxy=item_detail['tender_info'][0]['tenderee_proxy'],
                                   tenderee_proxy_phone=item_detail['tender_info'][0]['tenderee_proxy_phone'],
                                   tender_openning_location=item_detail['tender_info'][0]['tender_openning_location'],
                                   tender_openning_time=item_detail['tender_info'][0]['tender_openning_time'],
                                   tender_ceil_price=item_detail['tender_info'][0]['tender_ceil_price'],
                                   publicity_start=item_detail['tender_info'][0]['publicity_start'],
                                   publicity_end=item_detail['tender_info'][0]['publicity_end'],
                                   other_description=item_detail['other_description'][0]['other_description'],
                                   review_department=item_detail['review_department'][0]['review_department'],
                                   review_department_phone=item_detail['review_department'][0]['review_department_phone'],
                                   administration_department=item_detail['administration_department'][0]['administration_department'],
                                   administration_department_phone=item_detail['administration_department'][0]['administration_department_phone']
                                   )
        trender_info.save()

        candidate_index = 1
        for item in item_detail['candidate']:
            candidate = Candidate(tender_id=list_item['info_id'],
                                  ranking=item['ranking'],
                                  candidate_name=item['candidate_name'],
                                  tender_price=item['tender_price'],
                                  tender_price_review=item['tender_price_review'],
                                  review_score=item['review_score'])
            candidate_id = candidate.save()
            item['candidate_id'] = candidate_id
            identity_key = "candidate_%s" % candidate_index
            for incharge_item in [incharge_item for incharge_item in item_detail['candidate_incharge'] if
                                  incharge_item['identity'] == identity_key]:
                candidate_incharge = CandidateIncharge(tender_id=list_item['info_id'],
                                                       candidate_id=candidate_id,
                                                       incharge_id='',
                                                       incharge_type=incharge_item['incharge_type'],
                                                       incharge_name=incharge_item['incharge_name'],
                                                       incharge_certificate_name=incharge_item['incharge_certificate_name'],
                                                       incharge_certificate_no=incharge_item['incharge_certificate_no'],
                                                       professional_grade=incharge_item['professional_grade'],
                                                       professional_titles=incharge_item['professional_titles'])
                incharge_id = candidate_incharge.save()
                incharge_item['incharge_id'] = incharge_id

                if u'\u9879\u76ee\u8d1f\u8d23\u4eba' in incharge_item['incharge_type'].decode('utf8'):
                    for project_item in [project_item for project_item in item_detail['candidate_incharge_projects'] if
                                         project_item['identity'] == identity_key]:

                        candidate_incharge_projects = CandidateInChargeProjects(tender_id=list_item['info_id'],
                                                                                candidate_id=candidate_id,
                                                                                incharge_id=incharge_id,
                                                                                owner=project_item['owner'],
                                                                                name=project_item['name'],
                                                                                kick_off_date=project_item['kick_off_date'],
                                                                                deliver_date=project_item['deliver_date'],
                                                                                finish_date=project_item['finish_date'],
                                                                                scale=project_item['scale'],
                                                                                contract_price=project_item['contract_price'],
                                                                                tech_incharge_name=project_item['tech_incharge_name'])
                        candidate_incharge_projects.save()

                for project_item in [project_item for project_item in item_detail['candidate_projects'] if
                                      project_item['identity'] == identity_key]:
                    candidate_projects = CandidateProjects(tender_id=list_item['info_id'],
                                                           candidate_id=candidate_id,
                                                           owner=project_item['owner'],
                                                           name=project_item['name'],
                                                           kick_off_date=project_item['kick_off_date'],
                                                           deliver_date=project_item['deliver_date'],
                                                           finish_date=project_item['finish_date'],
                                                           scale=project_item['scale'],
                                                           contract_price=project_item['contract_price'],
                                                           project_incharge_name=project_item['project_incharge_name'])
                    candidate_projects.save()

            candidate_index += 1
        for item in item_detail['other_tenderer_review']:
            other_tenderer_review = OtherTendererReview(tender_id=list_item['info_id'],
                                                        tenderer_name=item['tenderer_name'],
                                                        price_or_vote_down=item['price_or_vote_down'],
                                                        price_review_or_vote_down_reason=item['price_review_or_vote_down_reason'],
                                                        review_score_or_description=item['review_score_or_description'])
            tenderer_id = other_tenderer_review.save()
            item['tenderer_id'] = tenderer_id
        for item in item_detail['review_board_member']:
            review_board_member = ReviewBoardMember(tender_id=list_item['info_id'],
                                                    name=item['member_name'],
                                                    company=item['member_company'])
            review_board_member.save()
