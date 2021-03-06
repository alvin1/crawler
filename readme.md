### 安装向导
#### 运行环境要求
- python: 2.7.10
- MySQL
- Microsoft Visual C++ Compiler for Python 2.7
- MySQL connector header files
- pip
- bs4
- threadpool
- MySQL-python
- sudo pip install html5lib --upgrade --ignore-installed six

#### 运行环境配置
- 安装MySQL
- 安装MySQL Connector C library
    - mysql-connector-c-6.0.2-winx64.msi
- 安装python
    - python-2.7.13.amd64.msi
- 安装pip

    ``python get-pip.py``
- 安装MySQL-python
    - 解压MySQL-pyhon-1.2.5.zip
    - 进入MySQL-python-1.2.5文件夹
    - 编辑site.cfg，修改connector的路径到实际安装路径
    - python setup,py install
- 安装其他依赖包

    ``pip install -r requirements.txt``

### 数据库结构说明
- tender_info：标的基本信息
    - tender_id: 投标ID
	- tender_name: 项目及标段名称
	- pubdate: 发布时间
	- page_url: 内容网址
    - owner: 项目业主
    - owner_phone: 项目业主联系电话
    - tenderee: 招标人
    - tenderee_phone: 招标人联系电话
    - tenderee_proxy: 招标代理机构
    - tenderee_proxy_phone: 招标代理机构联系电话
    - tender_openning_location: 开标地点
    - tender_openning_time: 开标时间
    - tender_ceil_price: 投标最高限价
    - publicity_start: 公示期开始日期
    - publicity_end: 公示期结束日期
    - other_description: 其他需说明事项
    - review_department: 项目审批部门
    - review_department_phone: 项目审批部门联系电话
    - administration_department: 行业主管部门
    - administration_department_phone: 行业主管部门联系电话
- candidate: 候选人表
    - tender_id: 投标ID
    - candidate_id: 候选人ID
    - ranking: 排名
    - candidate_name: 中标候选人名称
    - tender_price: 投标报价
    - tender_price_review: 经评审的投标价
    - review_score: 综合评标得分
- candidate_incharge：候选人负责人
    - tender_id: 投标ID
    - candidate_id： 候选人ID
    - incharge_id: 负责人ID
    - incharge_type: 负责人类型（项目，技术）
    - incharge_name: 姓名
    - incharge_certificate_name: 证书名称
    - incharge_certificate_no: 证书编号
    - professional_titles: 职称专业
    - professional_grade: 级别
- candidate_projects: 候选人类似项目
    - tender_id: 投标ID
    - candidate_id： 候选人ID
    - owner: 项目业主
    - name: 项目名称
    - kick_off_date: 开工日期
    - deliver_date: 交工日期
    - finish_date: 竣工日期
    - scale: 建设规模
    - contract_price: 合同价格
    - project_incharge_name: 项目负责人
- candidate_incharge_projects：候选人项目负责人类似项目
    - tender_id: 投标ID
    - candidate_id： 候选人ID
    - incharge_id: 负责人ID
    - owner: 项目业主
    - name: 项目名称
    - kick_off_date: 开工日期
    - deliver_date: 交工日期
    - finish_date: 竣工日期
    - scale: 建设规模
    - contract_price: 合同价格
    - tech_incharge_name: 项目负责人
- other_tenderer_review:
    - tender_id: 投标ID
    - tenderer_name: 投标人名称
    - price_or_vote_down: 投标报价或否决投标依据条款 
    - price_review_or_vote_down_reason: 经评审的投标价或否决投标理由
    - review_score_or_description: 综合评标得分或备注
- review_board_member: 评标委员会成员名单
    - tender_id: 投标ID
    - name: 姓名
    - company: 单位
    
### TODO:
- 判断页面类型
    - 部分字段不存在
    - 项目负责人和候选人在同一行
    - 只有项目审核部门，没有行政管理部门
    - 有无变更原因
    - 是否为取消投标
    - 适用的提取方式（html里面的ID，元素等）