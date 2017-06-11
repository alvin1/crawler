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
            date = self.clean_content(item.select('td')[2].string)

            list.append({
                'title': a['title'].encode("gbk"),
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
            return value.replace(u'\xa0', u' ').encode('gbk')
        elif data_type == 'int':
            return int(value)
        elif data_type == 'datetime':
            if len(value) > 10:
                return datetime.strptime(value.replace("/", "-"), '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
            else:
                return datetime.strptime(value.replace("/", "-"), '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S")
            # return value
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

    def extract_detail_old(self, soup):
        detail = {}
        rows = soup.select('#_Sheet1 tr')

        for item in Settings.DETAIL_COORDINATE:
            target_table = item['target_table']
            is_dynamic = item['dynamic']

            if target_table not in detail:
                detail[target_table] = []
            if not is_dynamic:
                data = {}
                if 'identity' in item:
                    data['identity'] = item['identity']
                for field in item['fields']:
                    field_name = field['field_name']
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

                data_of_range = rows[start_line + title_row_offset + 1 : next_start_line]
                for data in data_of_range:
                    cells = data.select('td')
                    if len(cells) == 0:
                        continue
                    row_data = {}
                    if 'identity' in item:
                        row_data['identity'] = item['identity']
                    for field in item['fields']:
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

    def extract_detail(self, soup):
        details = {}

        rows = soup.select('#_Sheet1 tr')
        # 1. extract tender info
        tender_config = Settings.DETAIL_COORDINATE['tender_info']
        details['tender_info'] = []
        tender_info = {}
        for field in tender_config['fields']:
            value_of_key = rows[field['extract']['row'] + 1].select('td')[field['extract']['column']].string
            if 'remove' in field['extract']:
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
        for row_data in rows_of_range:
            tmp_row_index += 1
            columns = row_data.select('td')
            if len(columns) != len(candidate_config['fields']):
                break

            candidate = {}
            for field in candidate_config['fields']:
                value_of_key = columns[field['extract']['column']].string
                if 'remove' in field['extract']:
                    for remove_key in field['extract']['remove']:
                        value_of_key = value_of_key.replace(remove_key, u'')
                if 'split_pattern' in field['extract']:
                    match = field['extract']['split_pattern'].match(value_of_key)
                    if match:
                        for split_field in field['extract']['split_result']:
                            split_data = match.group(split_field['key'])
                            candidate[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                else:
                    candidate[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
            details['candidate'].append(candidate)
        # 2.1 extract candidate_incharge list
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
                columns = incharge_row.select('td')
                incharge = {}
                for field in candidate_config['inchage_fields']:
                    value_of_key = columns[field['extract']['column']].string
                    if 'remove' in field['extract']:
                        for remove_key in field['extract']['remove']:
                            value_of_key = value_of_key.replace(remove_key, u'')
                    if 'split_pattern' in field['extract']:
                        match = field['extract']['split_pattern'].match(value_of_key)
                        if match:
                            for split_field in field['extract']['split_result']:
                                split_data = match.group(split_field['key'])
                                incharge[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                    else:
                        incharge[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
                candidate['incharge'].append(incharge)
        # 2.2 extract the candidate projects and candidate incharge projects
        break_time = 0
        for candidate in details['candidate']:
            candidate['project_start'] = tmp_row_index + 1
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
        details['candidate'][-1]['incharge_project_end'] = tmp_row_index

        for candidate in details['candidate']:
            candidate['projects'] = []
            for project_row in rows_of_range[candidate['project_start']:candidate['project_end']]:
                project = {}
                columns = project_row.select('td')
                for field in candidate_config['project_fields']:
                    value_of_key = columns[field['extract']['column']].string
                    if 'remove' in field['extract']:
                        for remove_key in field['extract']['remove']:
                            value_of_key = value_of_key.replace(remove_key, u'')
                    if 'split_pattern' in field['extract']:
                        match = field['extract']['split_pattern'].match(value_of_key)
                        if match:
                            for split_field in field['extract']['split_result']:
                                split_data = match.group(split_field['key'])
                                project[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                    else:
                        project[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
                candidate['projects'].append(project)
            candidate['incharge_projects'] = []
            for project_row in rows_of_range[candidate['incharge_project_start']:candidate['incharge_project_end']]:
                project = {}
                columns = project_row.select('td')
                for field in candidate_config['inchage_project_fields']:
                    value_of_key = columns[field['extract']['column']].string
                    if 'remove' in field['extract']:
                        for remove_key in field['extract']['remove']:
                            value_of_key = value_of_key.replace(remove_key, u'')
                    if 'split_pattern' in field['extract']:
                        match = field['extract']['split_pattern'].match(value_of_key)
                        if match:
                            for split_field in field['extract']['split_result']:
                                split_data = match.group(split_field['key'])
                                project[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                    else:
                        project[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
                candidate['incharge_projects'].append(project)

        # 3 extract other tenders list
        other_tenders_config = Settings.DETAIL_COORDINATE['other_tenderer_review']
        start_row = self.find_row_number_by_key(other_tenders_config['title_row_key'], rows)
        next_start_row = self.find_row_number_by_key(other_tenders_config['next_title_row_key'], rows)
        rows_of_range = rows[start_row + 2:next_start_row]
        details['other_tenderer_review'] = []
        for row in rows_of_range:
            other_tender = {}
            for field in other_tenders_config['fields']:
                value_of_key = row.select('td')[field['extract']['column']].string
                if 'remove' in field['extract']:
                    for remove_key in field['extract']['remove']:
                        value_of_key = value_of_key.replace(remove_key, u'')
                if 'split_pattern' in field['extract']:
                    match = field['extract']['split_pattern'].match(value_of_key)
                    if match:
                        for split_field in field['extract']['split_result']:
                            split_data = match.group(split_field['key'])
                            other_tender[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                else:
                    other_tender[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
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
                value_of_key = row.select('td')[field['extract']['column']].string
                if 'remove' in field['extract']:
                    for remove_key in field['extract']['remove']:
                        value_of_key = value_of_key.replace(remove_key, u'')
                if 'split_pattern' in field['extract']:
                    match = field['extract']['split_pattern'].match(value_of_key)
                    if match:
                        for split_field in field['extract']['split_result']:
                            split_data = match.group(split_field['key'])
                            other_desc[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                else:
                    other_desc[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
            details['other_description'].append(other_desc)

        # 5 extract review_board_member
        review_member_config = Settings.DETAIL_COORDINATE['review_board_member']
        start_row = self.find_row_number_by_key(review_member_config['title_row_key'], rows)
        next_start_row = self.find_row_number_by_key(review_member_config['next_title_row_key'], rows)
        rows_of_range = rows[start_row + 2:next_start_row]
        details['review_board_member'] = []
        for row in rows_of_range:
            review_member = {}
            for field in review_member_config['fields']:
                value_of_key = row.select('td')[field['extract']['column']].string
                if 'remove' in field['extract']:
                    for remove_key in field['extract']['remove']:
                        value_of_key = value_of_key.replace(remove_key, u'')
                if 'split_pattern' in field['extract']:
                    match = field['extract']['split_pattern'].match(value_of_key)
                    if match:
                        for split_field in field['extract']['split_result']:
                            split_data = match.group(split_field['key'])
                            review_member[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                else:
                    review_member[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
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
                value_of_key = row.select('td')[field['extract']['column']].string
                if 'remove' in field['extract']:
                    for remove_key in field['extract']['remove']:
                        value_of_key = value_of_key.replace(remove_key, u'')
                if 'split_pattern' in field['extract']:
                    match = field['extract']['split_pattern'].match(value_of_key)
                    if match:
                        for split_field in field['extract']['split_result']:
                            split_data = match.group(split_field['key'])
                            review_depart[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                else:
                    review_depart[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
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
                value_of_key = row.select('td')[field['extract']['column']].string
                if 'remove' in field['extract']:
                    for remove_key in field['extract']['remove']:
                        value_of_key = value_of_key.replace(remove_key, u'')
                if 'split_pattern' in field['extract']:
                    match = field['extract']['split_pattern'].match(value_of_key)
                    if match:
                        for split_field in field['extract']['split_result']:
                            split_data = match.group(split_field['key'])
                            admin_depart[split_field['name']] = self.convert_type(split_field['data_type'], split_data)
                else:
                    admin_depart[field['field_name']] = self.convert_type(field['data_type'], value_of_key)
            details['administration_department'].append(admin_depart)

        return details

    def save_extracted_data(self, list_item, item_detail):
        tender_info = TrenderInfo(tender_id=list_item['info_id'],
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
                                   other_description=item_detail['other_description'][0]['other_description'] if len(item_detail['other_description']) == 1 else '',
                                   review_department=item_detail['review_department'][0]['review_department'],
                                   review_department_phone=item_detail['review_department'][0]['review_department_phone'],
                                   administration_department=item_detail['administration_department'][0]['administration_department'],
                                   administration_department_phone=item_detail['administration_department'][0]['administration_department_phone']
                                   )
        tender_info.save()

        # candidate_index = 1
        for item in item_detail['candidate']:
            candidate = Candidate(tender_id=list_item['info_id'],
                                  ranking=item['ranking'],
                                  candidate_name=item['candidate_name'],
                                  tender_price=item['tender_price'],
                                  tender_price_review=item['tender_price_review'],
                                  review_score=item['review_score'])
            candidate_id = candidate.save()
            item['candidate_id'] = candidate_id
            # identity_key = "candidate_%s" % candidate_index
            for incharge_item in item['incharge']:
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
            for project_item in item['projects']:
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
            for project_item in item['incharge_projects']:
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
                                                                        tech_incharge_name=project_item[
                                                                            'tech_incharge_name'])
                candidate_incharge_projects.save()

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
