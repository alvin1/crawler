import logging
import re

class Settings(object):
    # Extract settings
    RETRY_TIMES = 3
    MAX_EXTRACTS_EVERY_TIME = 100
    PAGE_SIZE = 20
    DOMAIN = 'http://www.spprec.com'
    URL = DOMAIN + '/sczw/jyfwpt/005001/005001003/MoreInfo.aspx?CategoryNum=005001003'
    PAGE_WAIT_TIMEOUT = 6000
    MAX_CLIENTS = 5
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'root'
    DB_PASSWD = 'abcd1234'
    DB_NAME = 'crawler'

    DETAIL_COORDINATE = {
        'tender_name': {
            'title_row_key': [u'\u9879\u76ee\u53ca\u6807\u6bb5\u540d\u79f0'],
            'fields': [
                {
                    'field_name': 'tender_name',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                }
            ]
        },
        'owner': {
            'title_row_key': [u'\u9879\u76ee\u4e1a\u4e3b\uff08\u62db\u6807\u4eba\uff09',
                              u'\u9879\u76ee\u4e1a\u4e3b'],
            'fields': [
                {
                    'field_name': 'owner',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                }
            ]
        },
        'owner_phone': {
            'title_row_key': [u'\u9879\u76ee\u4e1a\u4e3b\uff08\u62db\u6807\u4eba\uff09\u8054\u7cfb\u7535\u8bdd',
                              u'\u9879\u76ee\u4e1a\u4e3b\u8054\u7cfb\u7535\u8bdd'],
            'fields': [
                {
                    'field_name': 'owner_phone',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                }
            ]
        },
        'tenderee': {
            'title_row_key': [u'\u62db\u6807\u4eba',
                              u'\u9879\u76ee\u4e1a\u4e3b\uff08\u62db\u6807\u4eba\uff09'],
            'fields': [
                {
                    'field_name': 'tenderee',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                }
            ]
        },
        'tenderee_phone': {
            'title_row_key': [u'\u9879\u76ee\u4e1a\u4e3b\uff08\u62db\u6807\u4eba\uff09\u8054\u7cfb\u7535\u8bdd',
                              u'\u62db\u6807\u4eba\u8054\u7cfb\u7535\u8bdd'],
            'fields': [
                {
                    'field_name': 'tenderee_phone',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                }
            ]
        },
        'tenderee_proxy': {
            'title_row_key': [u'\u62db\u6807\u4ee3\u7406\u673a\u6784'],
            'fields': [
                {
                    'field_name': 'tenderee_proxy',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                }
            ]
        },
        'tenderee_proxy_phone': {
            'title_row_key': [u'\u62db\u6807\u4ee3\u7406\u673a\u6784\u8054\u7cfb\u7535\u8bdd'],
            'fields': [
                {
                    'field_name': 'tenderee_proxy_phone',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                }
            ]
        },
        'tender_openning_location': {
            'title_row_key': [u'\u5f00\u6807\u5730\u70b9'],
            'fields': [
                {
                    'field_name': 'tender_openning_location',
                    'data_type': 'string',
                    'extract': {
                        'column': 1
                    }
                }
            ]
        },
        'tender_openning_time': {
            'title_row_key': [u'\u5f00\u6807\u65f6\u95f4'],
            'fields': [
                {
                    'field_name': 'tender_openning_time',
                    'data_type': 'string',
                    'extract': {
                        'column': 3
                    }
                }
            ]
        },
        'publicity': {
            'title_row_key': [u'\u516c\u793a\u671f'],
            'fields': [
                {
                    'field_name': 'publicity',
                    'data_type': 'string',
                    'extract': {
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
                }
            ]
        },
        'tender_ceil_price': {
            'title_row_key': [u'\u6295\u6807\u6700\u9ad8\u9650\u4ef7(\u5143)'],
            'fields': [
                {
                    'field_name': 'tender_ceil_price',
                    'data_type': 'string',
                    'extract': {
                        'column': 3,
                        'remove': [u'\u5143']
                    }
                }
            ]
        },
        'tender_info': {
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
                        'column': 1
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
                        'column': 3,
                        'remove': [u'\u5143']
                    }
                }
            ]
        },
        'candidate': {
            'title_row_key': [u'\u4e2d\u6807\u5019\u9009\u4eba\u53ca\u6392\u5e8f'],
            'next_title_row_key': [u'\u5176\u4ed6\u6295\u6807\u4eba\uff08\u9664\u4e2d\u6807\u5019\u9009\u4eba\u4e4b\u5916\u7684\uff09\u8bc4\u5ba1\u60c5\u51b5'],
            'has_title': True,
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
                        'column': 2,
                        'remove': [u'\u5143']
                    }
                },
                {
                    'field_name': 'tender_price_review',
                    'field_title': u'\u7ecf\u8bc4\u5ba1\u7684\u6295\u6807\u4ef7\uff08\u5143\uff09',
                    'data_type': 'string',
                    'extract': {
                        'column': 3,
                        'remove': [u'\u5143']
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
            ],
            'inchage_fields': [
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
            ],
            'project_fields': [
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
            ],
            'inchage_project_fields': [
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
        'other_tenderer_review': {
            'title_row_key': [u'\u5176\u4ed6\u6295\u6807\u4eba\uff08\u9664\u4e2d\u6807\u5019\u9009\u4eba\u4e4b\u5916\u7684\uff09\u8bc4\u5ba1\u60c5\u51b5',
                              u'\u5e9f\u6807\u5355\u4f4d\u53ca\u7406\u7531'],
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
        'other_description': {
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
        'review_board_member': {
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
        'review_department': {
            'title_row_key': [u'\u9879\u76ee\u5ba1\u6279\u90e8\u95e8'],
            'next_title_row_key': [u'\u884c\u4e1a\u4e3b\u7ba1\u90e8\u95e8'],
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
        'administration_department': {
            'title_row_key': [u'\u884c\u4e1a\u4e3b\u7ba1\u90e8\u95e8'],
            'next_title_row_key': [u'\u5f02\u8bae\u6295\u8bc9\u6ce8\u610f\u4e8b\u9879',
                                   u'\u62db\u6807\u4eba\u4e3b\u8981\u8d1f\u8d23\u4eba\u7b7e\u5b57\u3001\u76d6\u7ae0'],
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
    }

    # Logging settings
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_MSG_FORMAT = '%(asctime)s - [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s'
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    # Paging settings
    VIEWSTATEGENERATOR = '0373971A'
    EVENTTARGET = 'MoreInfoList1$Pager'
    VIEWSTATE='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'
