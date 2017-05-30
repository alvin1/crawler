CREATE DATABASE crawler DEFAULT CHARACTER SET utf8;

USE crawler;

CREATE TABLE IF NOT EXISTS tender_info (
    tender_id char(36),
    tender_name varchar(1000),
    pubdate datetime,
    owner varchar(1000),
    owner_phone varchar(12),
    tenderee varchar(1000),
    tenderee_phone varchar(12),
    tenderee_proxy varchar(1000),
    tenderee_proxy_phone varchar(12),
    tender_openning_location varchar(1000),
    tender_openning_time datetime,
    tender_ceil_price double,
    publicity_start datetime,
    publicity_end datetime,
    other_description varchar(3000),
    review_department varchar(1000),
    review_department_phone varchar(12),
    administration_department varchar(1000),
    administration_department_phone varchar(12)
) engine=innodb;

CREATE TABLE IF NOT EXISTS candidate (
    tender_id char(36),
    candidate_id char(36),
    ranking varchar(10),
    candidate_name varchar(1000),
    tender_price varchar(50),
    tender_price_review varchar(50),
    review_score double
) engine=innodb;

CREATE TABLE IF NOT EXISTS candidate_incharge (
    tender_id char(36),
    candidate_id char(36),
    incharge_id char(36),
    incharge_type varchar(50),
    incharge_name varchar(50),
    incharge_certificate_name varchar(300),
    incharge_certificate_no varchar(50),
    professional_titles varchar(300),
    professional_grade varchar(50)
) engine=innodb;

CREATE TABLE IF NOT EXISTS candidate_projects (
    tender_id char(36),
    candidate_id char(36),
    owner varchar(1000),
    name varchar(1000),
    kick_off_date datetime,
    deliver_date datetime,
    finish_date datetime,
    scale varchar(300),
    contract_price double,
    project_incharge_name varchar(50)
) engine=innodb;

CREATE TABLE IF NOT EXISTS candidate_incharge_projects (
    tender_id char(36),
    candidate_id char(36),
    incharge_id char(36),
    owner varchar(1000),
    name varchar(1000),
    kick_off_date datetime,
    deliver_date datetime,
    finish_date datetime,
    scale varchar(300),
    contract_price double,
    tech_incharge_name varchar(50)
) engine=innodb;

CREATE TABLE IF NOT EXISTS other_tenderer_review (
    tender_id char(36),
    tenderer_name varchar(1000),
    price_or_vote_down varchar(3000),
    price_review_or_vote_down_reason varchar(3000),
    review_score_or_description varchar(3000)
) engine=innodb;

CREATE TABLE IF NOT EXISTS review_board_member(
    tender_id char(36),
    name varchar(50),
    company varchar(1000)
) engine=innodb;