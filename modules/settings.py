import logging
import re

class Settings(object):
    # Extract settings
    RETRY_TIMES = 3
    MAX_EXTRACTS_EVERY_TIME = 100
    PAGE_SIZE = 20
    DOMAIN = 'http://www.spprec.com'
    URL = DOMAIN + '/sczw/jyfwpt/005001/005001003/MoreInfo.aspx?CategoryNum=005001003'
    PAGE_WAIT_TIMEOUT = 60
    MAX_CLIENTS = 5
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'root'
    DB_PASSWD = 'abcd1234'
    DB_NAME = 'crawler'

    DETAIL_COORDINATE = [
        {
            'target_table': 'tender_info',
            'multiple_lines': False,
            'fields': [
                {
                    'field_name': 'tender_name',
                    'data_type': 'string',
                    'extract': {
                        'row': 1,
                        'column': 1
                    }
                },
                {
                    'field_name': 'owner',
                    'data_type': 'string',
                    'extract': {
                        'row': 2,
                        'column': 1
                    }
                },
                {
                    'field_name': 'owner_phone',
                    'data_type': 'string',
                    'extract': {
                        'row': 2,
                        'column': 3
                    }
                },
                {
                    'field_name': 'tenderee',
                    'data_type': 'string',
                    'extract': {
                        'row': 3,
                        'column': 3
                    }
                },
                {
                    'field_name': 'tenderee_phone',
                    'data_type': 'string',
                    'extract': {
                        'row': 3,
                        'column': 3
                    }
                },
                {
                    'field_name': 'tenderee_proxy',
                    'data_type': 'string',
                    'extract': {
                        'row': 4,
                        'column': 1
                    }
                },
                {
                    'field_name': 'tenderee_proxy_phone',
                    'data_type': 'string',
                    'extract': {
                        'row': 4,
                        'column': 3
                    }
                },
                {
                    'field_name': 'tender_openning_location',
                    'data_type': 'string',
                    'extract': {
                        'row': 5,
                        'column': 1
                    }
                },
                {
                    'field_name': 'tender_openning_time',
                    'data_type': 'datetime',
                    'extract': {
                        'row': 5,
                        'column': 3
                    }
                },
                {
                    'field_name': 'publicity',
                    'data_type': 'string',
                    'extract': {
                        'row': 6,
                        'column': 1,
                        'split_pattern': re.compile(u'(?P<START>.+)\xa0\u81f3\xa0(?P<END>.+)'),
                        'split_result': [
                            {
                                'name': 'publicity_start',
                                'key': 'START',
                                'data_type': 'datetime'
                            },
                            {
                                'name': 'publicity_end',
                                'key': 'END',
                                'data_type': 'datetime'
                            }
                        ]
                    }
                },
                {
                    'field_name': 'tender_ceil_price',
                    'data_type': 'string',
                    'extract': {
                        'row': 6,
                        'column': 3
                    }
                }
            ]
        },
        {
            'target_table': 'candidate',
            'multiple_lines': True,
            'title_row_key': [u'\u4e2d\u6807\u5019\u9009\u4eba\u53ca\u6392\u5e8f'],
            'next_title_row_key': [
                u'\u7b2c1\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458',
                u'\u7b2c\u4e00\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458'
            ],
            'title_row_offset': 2,
            'fields': [
                {
                    'field_name': 'ranking',
                    'field_title': u'\u4e2d\u6807\u5019\u9009\u4eba\u53ca\u6392\u5e8f',
                    'data_type': 'string',
                    'extract': {
                        'column': 0
                    }
                },
                {
                    'field_name': 'candidate_name',
                    'field_title': u'\u4e2d\u6807\u5019\u9009\u4eba\u540d\u79f0',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                },
                {
                    'field_name': 'tender_price',
                    'field_title': u'\u6295\u6807\u62a5\u4ef7\uff08\u5143\uff09',
                    'data_type': 'string',
                    'extract': {
                        'column': 2
                    }
                },
                {
                    'field_name': 'tender_price_review',
                    'field_title': u'\u7ecf\u8bc4\u5ba1\u7684\u6295\u6807\u4ef7\uff08\u5143\uff09',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'review_score',
                    'field_title': u'\u7efc\u5408\u8bc4\u6807\u5f97\u5206',
                    'data_type': 'decimal',
                    'extract': {
                        'column': 4
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_incharge',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c1\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458',
                u'\u7b2c\u4e00\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458'
            ],
            'next_title_row_key': [
                u'\u7b2c2\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458',
                u'\u7b2c\u4e8c\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458'
            ],
            'title_row_offset': 2,
            'identity': 'candidate_1',
            'fields': [
                {
                    'field_name': 'incharge_type',
                    'data_type': 'string',
                    'extract': {
                        'column': 0
                    }
                },
                {
                    'field_name': 'incharge_name',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                },
                {
                    'field_name': 'incharge_certificate_name',
                    'data_type': 'string',
                    'extract': {
                        'column': 2
                    }
                },
                {
                    'field_name': 'incharge_certificate_no',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'professional_titles',
                    'data_type': 'string',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'professional_grade',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_incharge',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c2\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458',
                u'\u7b2c\u4e8c\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458'
            ],
            'next_title_row_key': [
                u'\u7b2c3\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458',
                u'\u7b2c\u4e09\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458'
            ],
            'identity': 'candidate_2',
            'title_row_offset': 2,
            'fields': [
                {
                    'field_name': 'incharge_type',
                    'data_type': 'string',
                    'extract': {
                        'column': 0
                    }
                },
                {
                    'field_name': 'incharge_name',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                },
                {
                    'field_name': 'incharge_certificate_name',
                    'data_type': 'string',
                    'extract': {
                        'column': 2
                    }
                },
                {
                    'field_name': 'incharge_certificate_no',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'professional_titles',
                    'data_type': 'string',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'professional_grade',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_incharge',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c3\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458',
                u'\u7b2c\u4e09\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u7ba1\u7406\u673a\u6784\u4e3b\u8981\u4eba\u5458'
            ],
            'next_title_row_key': [
                u'\u7b2c1\u540d\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e00\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'title_row_offset': 2,
            'identity': 'candidate_3',
            'fields': [
                {
                    'field_name': 'incharge_type',
                    'data_type': 'string',
                    'extract': {
                        'column': 0
                    }
                },
                {
                    'field_name': 'incharge_name',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                },
                {
                    'field_name': 'incharge_certificate_name',
                    'data_type': 'string',
                    'extract': {
                        'column': 2
                    }
                },
                {
                    'field_name': 'incharge_certificate_no',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'professional_titles',
                    'data_type': 'string',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'professional_grade',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_projects',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c1\u540d\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e00\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'next_title_row_key': [
                u'\u7b2c1\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e00\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'identity': 'candidate_1',
            'fields': [
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
                    'field_name': 'deliver_date',
                    'field_title': u'\u4ea4\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'finish_date',
                    'field_title': u'\u7ae3\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'scale',
                    'field_title': u'\u5efa\u8bbe\u89c4\u6a21',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                },
                {
                    'field_name': 'contract_price',
                    'field_title': u'\u5408\u540c\u4ef7\u683c\uff08\u5143\uff09',
                    'data_type': 'decimal',
                    'extract': {
                        'column': 6
                    }
                },
                {
                    'field_name': 'project_incharge_name',
                    'field_title': u'\u9879\u76ee\u8d1f\u8d23\u4eba',
                    'data_type': 'string',
                    'extract': {
                        'column': 7
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_incharge_projects',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c1\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e00\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'next_title_row_key': [
                u'\u7b2c2\u540d\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e8c\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'identity': 'candidate_1',
            'fields': [
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
                    'field_name': 'deliver_date',
                    'field_title': u'\u4ea4\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'finish_date',
                    'field_title': u'\u7ae3\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'scale',
                    'field_title': u'\u5efa\u8bbe\u89c4\u6a21',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                },
                {
                    'field_name': 'contract_price',
                    'field_title': u'\u5408\u540c\u4ef7\u683c\uff08\u5143\uff09',
                    'data_type': 'decimal',
                    'extract': {
                        'column': 6
                    }
                },
                {
                    'field_name': 'tech_incharge_name',
                    'field_title': u'\u6280\u672f\u8d1f\u8d23\u4eba',
                    'data_type': 'string',
                    'extract': {
                        'column': 7
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_projects',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c2\u540d\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e8c\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'next_title_row_key': [
                u'\u7b2c2\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e8c\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'identity': 'candidate_2',
            'fields': [
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
                    'field_name': 'deliver_date',
                    'field_title': u'\u4ea4\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'finish_date',
                    'field_title': u'\u7ae3\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'scale',
                    'field_title': u'\u5efa\u8bbe\u89c4\u6a21',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                },
                {
                    'field_name': 'contract_price',
                    'field_title': u'\u5408\u540c\u4ef7\u683c\uff08\u5143\uff09',
                    'data_type': 'decimal',
                    'extract': {
                        'column': 6
                    }
                },
                {
                    'field_name': 'project_incharge_name',
                    'field_title': u'\u9879\u76ee\u8d1f\u8d23\u4eba',
                    'data_type': 'string',
                    'extract': {
                        'column': 7
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_incharge_projects',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c2\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e8c\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'next_title_row_key': [
                u'\u7b2c3\u540d\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e09\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'identity': 'candidate_2',
            'fields': [
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
                    'field_name': 'deliver_date',
                    'field_title': u'\u4ea4\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'finish_date',
                    'field_title': u'\u7ae3\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'scale',
                    'field_title': u'\u5efa\u8bbe\u89c4\u6a21',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                },
                {
                    'field_name': 'contract_price',
                    'field_title': u'\u5408\u540c\u4ef7\u683c\uff08\u5143\uff09',
                    'data_type': 'decimal',
                    'extract': {
                        'column': 6
                    }
                },
                {
                    'field_name': 'tech_incharge_name',
                    'field_title': u'\u6280\u672f\u8d1f\u8d23\u4eba',
                    'data_type': 'string',
                    'extract': {
                        'column': 7
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_projects',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c3\u540d\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e09\u4e2d\u6807\u5019\u9009\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'next_title_row_key': [
                u'\u7b2c3\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e09\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'identity': 'candidate_3',
            'fields': [
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
                    'field_name': 'deliver_date',
                    'field_title': u'\u4ea4\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'finish_date',
                    'field_title': u'\u7ae3\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'scale',
                    'field_title': u'\u5efa\u8bbe\u89c4\u6a21',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                },
                {
                    'field_name': 'contract_price',
                    'field_title': u'\u5408\u540c\u4ef7\u683c\uff08\u5143\uff09',
                    'data_type': 'decimal',
                    'extract': {
                        'column': 6
                    }
                },
                {
                    'field_name': 'project_incharge_name',
                    'field_title': u'\u9879\u76ee\u8d1f\u8d23\u4eba',
                    'data_type': 'string',
                    'extract': {
                        'column': 7
                    }
                }
            ]
        },
        {
            'target_table': 'candidate_incharge_projects',
            'multiple_lines': True,
            'title_row_key': [
                u'\u7b2c3\u540d\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9',
                u'\u7b2c\u4e09\u4e2d\u6807\u5019\u9009\u4eba\u9879\u76ee\u8d1f\u8d23\u4eba\u7c7b\u4f3c\u4e1a\u7ee9'
            ],
            'next_title_row_key': [u'\u5176\u4ed6\u6295\u6807\u4eba\uff08\u9664\u4e2d\u6807\u5019\u9009\u4eba\u4e4b\u5916\u7684\uff09\u8bc4\u5ba1\u60c5\u51b5'],
            'identity': 'candidate_3',
            'fields': [
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
                    'field_name': 'deliver_date',
                    'field_title': u'\u4ea4\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 3
                    }
                },
                {
                    'field_name': 'finish_date',
                    'field_title': u'\u7ae3\u5de5\u65e5\u671f',
                    'data_type': 'datetime',
                    'extract': {
                        'column': 4
                    }
                },
                {
                    'field_name': 'scale',
                    'field_title': u'\u5efa\u8bbe\u89c4\u6a21',
                    'data_type': 'string',
                    'extract': {
                        'column': 5
                    }
                },
                {
                    'field_name': 'contract_price',
                    'field_title': u'\u5408\u540c\u4ef7\u683c\uff08\u5143\uff09',
                    'data_type': 'decimal',
                    'extract': {
                        'column': 6
                    }
                },
                {
                    'field_name': 'tech_incharge_name',
                    'field_title': u'\u6280\u672f\u8d1f\u8d23\u4eba',
                    'data_type': 'string',
                    'extract': {
                        'column': 7
                    }
                }
            ]
        },
        {
            'target_table': 'other_tenderer_review',
            'multiple_lines': True,
            'title_row_key': [u'\u5176\u4ed6\u6295\u6807\u4eba\uff08\u9664\u4e2d\u6807\u5019\u9009\u4eba\u4e4b\u5916\u7684\uff09\u8bc4\u5ba1\u60c5\u51b5'],
            'next_title_row_key': [u'\u5176\u4ed6\u9700\u8bf4\u660e\u4e8b\u9879'],
            'fields': [
                {
                    'field_name': 'tenderer_name',
                    'field_title': u'\u6295\u6807\u4eba\u540d\u79f0 ',
                    'data_type': 'string',
                    'extract': {
                        'column': 0
                    }
                },
                {
                    'field_name': 'price_or_vote_down',
                    'field_title': u'\u6295\u6807\u62a5\u4ef7\uff08\u5143\uff09',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }},
                {
                    'field_name': 'price_review_or_vote_down_reason',
                    'field_title': u'\u7ecf\u8bc4\u5ba1\u7684\u6295\u6807\u4ef7\uff08\u5143\uff09',
                    'data_type': 'string',
                    'extract': {
                        'column': 2
                    }
                },
                {
                    'field_name': 'review_score_or_description',
                    'field_title': u'\u7efc\u5408\u8bc4\u6807\u5f97\u5206',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                }
            ]
        },
        {
            'target_table': 'other_description',
            'multiple_lines': False,
            'title_row_key': u'\u5176\u4ed6\u9700\u8bf4\u660e\u4e8b\u9879',
            'next_title_row_key': u'\u8bc4\u6807\u59d4\u5458\u4f1a\u6210\u5458\u540d\u5355',
            'fields': [
                {
                    'field_name': 'other_description',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                }
            ]
        },
        {
            'target_table': 'review_board_member',
            'multiple_lines': True,
            'title_row_key': [u'\u8bc4\u6807\u59d4\u5458\u4f1a\u6210\u5458\u540d\u5355'],
            'next_title_row_key': [u'\u76d1\u7763\u90e8\u95e8\u540d\u79f0\u53ca\u76d1\u7763\u7535\u8bdd'],
            'fields': [
                {
                    'field_name': 'member_name',
                    'data_type': 'string',
                    'extract': {
                        'column': 0,
                        'split_pattern': re.compile(u'\u59d3\u540d\uff1a(?P<NAME>.+)'),
                        'split_result': [
                            {
                                'name': 'member_name',
                                'key': 'NAME',
                                'data_type': 'string'
                            }
                        ]
                    }
                },
                {
                    'field_name': 'member_company',
                    'data_type': 'string',
                    'extract': {
                        'column': 1,
                        'split_pattern': re.compile(u'\u5355\u4f4d\uff1a(?P<COMPANY>.+)'),
                        'split_result': [
                            {
                                'name': 'member_company',
                                'key': 'COMPANY',
                                'data_type': 'string'
                            }
                        ]
                    }
                }
            ]
        },
        {
            'target_table': 'review_department',
            'multiple_lines': True,
            'title_row_key': [u'\u9879\u76ee\u5ba1\u6279\u90e8\u95e8'],
            'next_title_row_key': [u'\u884c\u4e1a\u4e3b\u7ba1\u90e8\u95e8'],
            'data_element': 'td',
            'title_row_offset': -1,
            'fields': [
                {
                    'field_name': 'review_department',
                    'data_type': 'string',
                    'extract': {
                        'column': 2
                    }
                },
                {
                    'field_name': 'review_department_phone',
                    'data_type': 'string',
                    'extract': {
                        'column': 4
                    }
                }
            ]
        },
        {
            'target_table': 'administration_department',
            'multiple_lines': True,
            'title_row_key': [u'\u884c\u4e1a\u4e3b\u7ba1\u90e8\u95e8'],
            'next_title_row_key': [u'\u5f02\u8bae\u6295\u8bc9\u6ce8\u610f\u4e8b\u9879'],
            'data_element': 'td',
            'title_row_offset': -1,
            'fields': [
                {
                    'field_name': 'administration_department',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                },
                {
                    'field_name': 'administration_department_phone',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                }
            ]
        }
    ]

    # Logging settings
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_MSG_FORMAT = '%(asctime)s - [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s'
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    # Paging settings
    VIEWSTATEGENERATOR = '0373971A'
    EVENTTARGET = 'MoreInfoList1$Pager'
    VIEWSTATE = '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'
