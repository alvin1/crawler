from datetime import datetime

from .settings import Settings
from .file_helper import FileHelper

class Extracter(object):
    def __init__(self):
        self.extracter_status_file = 'var/status/last_extract.json'
        self.file_helper = FileHelper()
        self.file_helper.poke_dir(self.file_helper.get_dir_from_path(self.extracter_status_file))

    def clean_content(self, content):
        return content.replace('\r\n', '').replace('\t', '')

    def extract_list(self, soup, page):
        list = []
        for item in soup.select('#MoreInfoList1_tdcontent tr'):
            a = item.select('a')[0]
            date = self.clean_content(item.select('td[width=80]')[0].string)

            list.append({
                'title': a['title'].encode("utf8"),
                'publish_date': date,
                'page_url': "%s%s" % (Settings.DOMAIN, a['href']),
                'page_index': page
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
                if item and key in item:
                    return start_line
            start_line += 1
        return None
    
    def extract_detail(self, soup):
        detail = {}
        rows = soup.select('#_Sheet1 tr')

        for item in Settings.DETAIL_COORDINATE:
            target_table = item['target_table']
            multiple_lines = item['multiple_lines']

            if target_table not in detail:
                detail[target_table] = []
            if not multiple_lines:
                data = {}
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
                    if len(row_data.items()) > 0:
                        detail[target_table].append(row_data)

        return detail
