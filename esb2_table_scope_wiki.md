# 第一部分：数据库表级说明与逻辑外键导航（用于查表范围定位）

## 1. 使用原则

本文件只用于“需求理解 → 锁定查表范围 → 判断表之间如何关联”。因此只保留表名、表级功能说明、主键概览和逻辑外键关系，不展开字段类型、可空、默认值等完整字段 Schema。

- 先根据业务问题在本文件中定位可能相关的表。
- 再根据“逻辑外键关系”判断这些表如何连接。
- 确认候选表后，再动态加载第二部分中对应表的独立 JSON Schema，读取该表完整字段定义。
- 第二部分每张表是独立文件，只描述本表自身字段，不嵌入其他表 Schema。

## 2. 简单数据库结构介绍

从业务范围看，数据库主要围绕以下对象展开：客户/供应商主数据、客户联系人、销售机会、售前行动、合同审批、合同台账、费用报销、成本空间、物料产品、项目售后、系统用户权限、新闻通知与操作日志。

这里的“逻辑外键”不是要求数据库一定建有物理 FOREIGN KEY 约束，而是说明：某张表中的某个字段，在业务上指向另一张表的主键或识别字段。它的作用是帮助系统判断：要查哪些表、这些表之间用什么字段连接、避免 SQL 生成时乱连表。

## 3. 逻辑外键使用示例

- `zzvc_bad_bill.user_id` → `zzvc_user.id`：表示 `zzvc_bad_bill` 里的 `user_id` 不是孤立值，而是用来找到 `zzvc_user` 中对应记录的连接线索。
- `zzvc_bad_bill_upload_file.bad_bill_id` → `zzvc_bad_bill.id`：表示 `zzvc_bad_bill_upload_file` 里的 `bad_bill_id` 不是孤立值，而是用来找到 `zzvc_bad_bill` 中对应记录的连接线索。
- `zzvc_business_before_sale.chance_Id` → `zzvc_business_chance.id`：表示 `zzvc_business_before_sale` 里的 `chance_Id` 不是孤立值，而是用来找到 `zzvc_business_chance` 中对应记录的连接线索。
- `zzvc_business_before_sale.uId` → `zzvc_user.id`：表示 `zzvc_business_before_sale` 里的 `uId` 不是孤立值，而是用来找到 `zzvc_user` 中对应记录的连接线索。

## 4. 表级功能目录与逻辑外键导航

说明：
- “本表逻辑外键”表示本表通过哪些字段指向其他表。
- “被哪些表引用”表示其他表通过哪些字段指向本表。
- 本节只列连接线索，不展开字段类型、字段含义等完整字段 Schema。

### 系统用户、权限、配置与基础字典

#### 1. `zzvc_admin_user`

- 表级总体说明：后台管理员用户表,管理老后台登录账号与管理端权限基础用户。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 2. `zzvc_app_active`

- 表级总体说明：移动端激活记录表,记录 App 版本、设备标识和激活时间。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 3. `zzvc_area`

- 表级总体说明：区域树表,包含了地区/区域层级数据,用于客户地区、组织区域等树形选择。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_area.companyId` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 4. `zzvc_category`

- 表级总体说明：菜单与权限分类表,定义系统菜单、路由、权限节点和角色授权树。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 5. `zzvc_company_authorization`

- 表级总体说明：公司授权表,定义公司授权邮箱、机器码、截止日期和提醒状态。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 6. `zzvc_config`

- 表级总体说明：系统配置表,定义键值型系统配置,例如阈值、提醒和搜索条件配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 7. `zzvc_customer_area_config`

- 表级总体说明：客户区域配置表,定义客户公海/区域分组授权配置,用于保存用户和角色范围。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 8. `zzvc_customer_area_role`

- 表级总体说明：客户区域角色表,定义客户区域或公海组角色权限配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 9. `zzvc_dictionary`

- 表级总体说明：字典表,定义部门、角色选项、业务选项等通用字典数据。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 10. `zzvc_role`

- 表级总体说明：角色表,定义系统角色、菜单权限序列化数据和授权用户。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_role.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 11. `zzvc_sale_task_user`

- 表级总体说明：个人销售指标表,定义用户年度销售指标金额配置。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_sale_task_user.userId` → `zzvc_user.id`
- 被哪些表引用：无

#### 12. `zzvc_total_summary_role`

- 表级总体说明：合同汇总角色表,定义合同汇总/统计页面的角色权限配置。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_total_summary_role.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 13. `zzvc_user`

- 表级总体说明：用户表,定义系统用户、销售人员、部门、平台角色、指标和登录信息。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：
  - `zzvc_bad_bill.user_id` → `zzvc_user.id`
  - `zzvc_bank_account.uid` → `zzvc_user.id`
  - `zzvc_business_before_sale.uId` → `zzvc_user.id`
  - `zzvc_business_chance.cId` → `zzvc_user.id`
  - `zzvc_business_chance.shared_userId` → `zzvc_user.id`
  - `zzvc_business_chance.uId` → `zzvc_user.id`
  - `zzvc_c135.uid` → `zzvc_user.id`
  - `zzvc_chance_order_edit.user_id` → `zzvc_user.id`
  - `zzvc_comment.user_id` → `zzvc_user.id`
  - `zzvc_company_customer_add_temp_contract.create_person_id` → `zzvc_user.id`
  - `zzvc_company_customer_contract.create_person_id` → `zzvc_user.id`
  - `zzvc_contract_list.user_id` → `zzvc_user.id`
  - `zzvc_contract_list_openbill_comment.user_id` → `zzvc_user.id`
  - `zzvc_contract_review.saler_id` → `zzvc_user.id`
  - `zzvc_cost_detail_log.uid` → `zzvc_user.id`
  - `zzvc_cost_detail_log_esb2.uid` → `zzvc_user.id`
  - `zzvc_crm_log_esb2.uid` → `zzvc_user.id`
  - `zzvc_customer_competitor.create_person_id` → `zzvc_user.id`
  - `zzvc_customer_contract_relationships.uid` → `zzvc_user.id`
  - `zzvc_dd_open_bill.cId` → `zzvc_user.id`
  - `zzvc_dd_open_bill.uId` → `zzvc_user.id`
  - `zzvc_dd_open_bill2.cId` → `zzvc_user.id`
  - `zzvc_dd_open_bill2.uId` → `zzvc_user.id`
  - `zzvc_demand_template.uId` → `zzvc_user.id`
  - `zzvc_device_basic_bom.cId` → `zzvc_user.id`
  - `zzvc_expenses.create_person_id` → `zzvc_user.id`
  - `zzvc_expenses_delzxh.create_person_id` → `zzvc_user.id`
  - `zzvc_expenses_sketch.uid` → `zzvc_user.id`
  - `zzvc_gift_apply.user_id` → `zzvc_user.id`
  - `zzvc_materiel.create_person_id` → `zzvc_user.id`
  - `zzvc_my_log.uid` → `zzvc_user.id`
  - `zzvc_my_log_esb2.uid` → `zzvc_user.id`
  - `zzvc_order.create_person_id` → `zzvc_user.id`
  - `zzvc_role.uid` → `zzvc_user.id`
  - `zzvc_sale_task_user.userId` → `zzvc_user.id`
  - `zzvc_sales_contract_search_condition.uid` → `zzvc_user.id`
  - `zzvc_schdule_search_condition.uid` → `zzvc_user.id`
  - `zzvc_total_summary_role.uid` → `zzvc_user.id`
  - `zzvc_user_news.user_id` → `zzvc_user.id`

#### 14. `zzvc_user_news`

- 表级总体说明：用户新闻阅读表,定义用户与新闻的阅读/关联记录。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_user_news.news_id` → `zzvc_news.id`
  - `zzvc_user_news.user_id` → `zzvc_user.id`
- 被哪些表引用：无

#### 15. `zzvc_version`

- 表级总体说明：版本管理表,定义App 版本、升级地址、强制升级和状态配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

### 客户、供应商主数据与联系人关系

#### 1. `zzvc_bank_account`

- 表级总体说明：银行账户信息表,包含收款账户、开户银行和账号信息。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_bank_account.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 2. `zzvc_company_customer`

- 表级总体说明：客户信息表,是客户主档,用于保存客户编码、名称、工商、开票、归属和授权信息。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：
  - `zzvc_area.companyId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_add_temp_contract.companyId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_add_temp_contract.customerId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_contract.companyId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_contract.customerId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_contract_gys.companyId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_stakeholder.companyId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_stakeholder_gys.companyId` → `zzvc_company_customer.id`
  - `zzvc_contract_list.companyId` → `zzvc_company_customer.id`
  - `zzvc_contract_review.customer_id` → `zzvc_company_customer.id`
  - `zzvc_customer_competitor.customer_id` → `zzvc_company_customer.id`
  - `zzvc_customer_contract_job_record.customerId` → `zzvc_company_customer.id`
  - `zzvc_customer_contract_stem.customer_id` → `zzvc_company_customer.id`
  - `zzvc_dd_open_bill2.companyId` → `zzvc_company_customer.id`
  - `zzvc_device_basic_norm.companyId` → `zzvc_company_customer.id`
  - `zzvc_expenses.customer_id` → `zzvc_company_customer.id`
  - `zzvc_expenses_delzxh.customer_id` → `zzvc_company_customer.id`
  - `zzvc_meeting_room.companyId` → `zzvc_company_customer.id`
  - `zzvc_order.customer_id` → `zzvc_company_customer.id`
  - `zzvc_tax.companyId` → `zzvc_company_customer.id`
  - `zzvc_tax_gys.companyId` → `zzvc_company_customer.id`
  - `zzvc_ticket_num.customer_id` → `zzvc_company_customer.id`

#### 3. `zzvc_company_customer_add_temp_contract`

- 表级总体说明：临时联系人表,定义客户联系人新增/导入过程中的临时联系人数据。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_company_customer_add_temp_contract.companyId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_add_temp_contract.create_person_id` → `zzvc_user.id`
  - `zzvc_company_customer_add_temp_contract.customerId` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 4. `zzvc_company_customer_contract`

- 表级总体说明：客户联系人表,是客户联系人主数据,包含姓名、职位、电话、邮箱、部门和主联系人标记。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_company_customer_contract.companyId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_contract.create_person_id` → `zzvc_user.id`
  - `zzvc_company_customer_contract.customerId` → `zzvc_company_customer.id`
- 被哪些表引用：
  - `zzvc_expenses.contacts_id` → `zzvc_company_customer_contract.id`
  - `zzvc_expenses_delzxh.contacts_id` → `zzvc_company_customer_contract.id`
  - `zzvc_order.contacts_id` → `zzvc_company_customer_contract.id`

#### 5. `zzvc_company_customer_contract_gys`

- 表级总体说明：供应商联系人镜像表,包含供应商侧联系人历史/镜像数据。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_company_customer_contract_gys.companyId` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 6. `zzvc_company_customer_gys`

- 表级总体说明：供应商客户镜像表,定义供应商侧客户/公司资料镜像,用于保留客户主档类似字段。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 7. `zzvc_company_customer_interlocutor`

- 表级总体说明：商机沟通人关系表,定义销售机会与客户联系人/沟通人的关联关系。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_company_customer_interlocutor.business_chance_id` → `zzvc_business_chance.id`
- 被哪些表引用：无

#### 8. `zzvc_company_customer_stakeholder`

- 表级总体说明：客户干系人表,定义客户项目干系人资料,包含角色、合同编号、联系方式和客户关系。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_company_customer_stakeholder.companyId` → `zzvc_company_customer.id`
  - `zzvc_company_customer_stakeholder.contractId` → `zzvc_contract.id`
- 被哪些表引用：无

#### 9. `zzvc_company_customer_stakeholder_gys`

- 表级总体说明：供应商干系人镜像表,定义供应商侧干系人历史/镜像数据。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_company_customer_stakeholder_gys.companyId` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 10. `zzvc_company_supplier`

- 表级总体说明：供应商信息表,是供应商主档,用于保存供应商名称、工商、开票、联系人和归属信息。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 11. `zzvc_company_supplier_gys`

- 表级总体说明：供应商扩展镜像表,定义供应商完整公司资料镜像,字段结构接近客户/供应商主档。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 12. `zzvc_contact_chance`

- 表级总体说明：联系人商机关联表,定义联系人与销售机会之间的关联关系。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 13. `zzvc_customer_competitor`

- 表级总体说明：客户竞争对手表,定义客户与竞争对手客户之间的关系。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_customer_competitor.create_person_id` → `zzvc_user.id`
  - `zzvc_customer_competitor.customer_id` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 14. `zzvc_customer_contract_job_record`

- 表级总体说明：联系人职位记录表,定义客户联系人职位/任职历史记录。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_customer_contract_job_record.customerId` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 15. `zzvc_customer_contract_relationships`

- 表级总体说明：联系人关系表,定义客户联系人之间或联系人与对象之间的关系。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_customer_contract_relationships.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 16. `zzvc_customer_contract_stem`

- 表级总体说明：客户合同访问令牌表,定义 客户合同/联系人访问 token 或临时关系记录。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_customer_contract_stem.contract_id` → `zzvc_contract.id`
  - `zzvc_customer_contract_stem.customer_id` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 17. `zzvc_high_sea_group`

- 表级总体说明：客户公海组表,定义客户公海/高海分组及授权配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 18. `zzvc_tax`

- 表级总体说明：客户开票税务信息表,定义客户税务、开户行、税号、许可证和开票文件信息。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_tax.companyId` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 19. `zzvc_tax_gys`

- 表级总体说明：供应商开票税务信息表,定义供应商税务、开户行、税号、许可证和开票文件信息。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_tax_gys.companyId` → `zzvc_company_customer.id`
- 被哪些表引用：无

### 商机、售前、销售日志与销售指标

#### 1. `zzvc_business_before_sale`

- 表级总体说明：售前行动记录表,包含商机相关售前行动、完成期限、行为结果和后续计划。
- 主键概览：`id`, `type`
- 本表逻辑外键：
  - `zzvc_business_before_sale.chance_Id` → `zzvc_business_chance.id`
  - `zzvc_business_before_sale.uId` → `zzvc_user.id`
- 被哪些表引用：无

#### 2. `zzvc_business_chance`

- 表级总体说明：销售机会表,是销售商机主表,用于保存客户、主题、阶段、金额、负责人和审批状态。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_business_chance.cId` → `zzvc_user.id`
  - `zzvc_business_chance.shared_userId` → `zzvc_user.id`
  - `zzvc_business_chance.uId` → `zzvc_user.id`
- 被哪些表引用：
  - `zzvc_business_before_sale.chance_Id` → `zzvc_business_chance.id`
  - `zzvc_business_chance_follow.f_chanceId` → `zzvc_business_chance.id`
  - `zzvc_c135.chance_id` → `zzvc_business_chance.id`
  - `zzvc_company_customer_interlocutor.business_chance_id` → `zzvc_business_chance.id`
  - `zzvc_contract_list.chanceId` → `zzvc_business_chance.id`
  - `zzvc_contract_review.chance_id` → `zzvc_business_chance.id`
  - `zzvc_expenses.chance_id` → `zzvc_business_chance.id`
  - `zzvc_expenses_delzxh.chance_id` → `zzvc_business_chance.id`
  - `zzvc_order.chance_id` → `zzvc_business_chance.id`

#### 3. `zzvc_business_chance_follow`

- 表级总体说明：销售日志表,包含销售机会跟进日志/行动记录,关联客户、商机和销售人员。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_business_chance_follow.f_chanceId` → `zzvc_business_chance.id`
- 被哪些表引用：无

#### 4. `zzvc_c135`

- 表级总体说明：C135 评分表,定义商机 C135 评估问卷/评分明细,用于机会评估和提醒。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_c135.chance_id` → `zzvc_business_chance.id`
  - `zzvc_c135.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 5. `zzvc_chance_order_edit`

- 表级总体说明：商机订单编辑阈值表,按年月记录商机订单修改阈值或限制配置。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_chance_order_edit.user_id` → `zzvc_user.id`
- 被哪些表引用：无

#### 6. `zzvc_depart_task`

- 表级总体说明：部门销售任务表,定义部门维度年度指标任务配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 7. `zzvc_sales_contract_search_condition`

- 表级总体说明：销售合同搜索条件表,定义用户保存的销售合同高级搜索条件。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_sales_contract_search_condition.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 8. `zzvc_sale_task_department`

- 表级总体说明：部门销售指标表,定义部门年度销售指标金额配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 9. `zzvc_sale_task_total`

- 表级总体说明：销售总指标表,定义公司或整体年度销售指标金额配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 10. `zzvc_schdule_search_condition`

- 表级总体说明：日程搜索条件表,定义用户保存的销售日程/漏填日志搜索条件。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_schdule_search_condition.uid` → `zzvc_user.id`
- 被哪些表引用：无

### 合同、审批、开票、回款、坏账与赠品

#### 1. `zzvc_bad_bill`

- 表级总体说明：坏账审批表,是销售合同坏账审批主表,用于保存合同、客户、坏账金额、审批状态和钉钉实例信息。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_bad_bill.user_id` → `zzvc_user.id`
- 被哪些表引用：
  - `zzvc_bad_bill_upload_file.bad_bill_id` → `zzvc_bad_bill.id`

#### 2. `zzvc_bad_bill_upload_file`

- 表级总体说明：坏账审批附件表,包含坏账审批关联的钉钉/本地上传附件元数据。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_bad_bill_upload_file.bad_bill_id` → `zzvc_bad_bill.id`
- 被哪些表引用：无

#### 3. `zzvc_basic_products`

- 表级总体说明：商品信息表,是发票/采购相关商品基础资料表单,包含商品名称、税率、税收编码和对应名称。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 4. `zzvc_contract`

- 表级总体说明：老合同主表,定义旧版合同录入/销售管理合同信息。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：
  - `zzvc_company_customer_stakeholder.contractId` → `zzvc_contract.id`
  - `zzvc_contract_po.contract_id` → `zzvc_contract.id`
  - `zzvc_customer_contract_stem.contract_id` → `zzvc_contract.id`
  - `zzvc_expenses.contracts_id` → `zzvc_contract.id`
  - `zzvc_expenses_delzxh.contracts_id` → `zzvc_contract.id`
  - `zzvc_order.contracts_id` → `zzvc_contract.id`
  - `zzvc_ticket_num.contract_id` → `zzvc_contract.id`

#### 5. `zzvc_contract_business_code`

- 表级总体说明：合同业务编码规则表,包含合同编码规则中的业务类型名称、编码和适用部门。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 6. `zzvc_contract_change`

- 表级总体说明：合同变更记录表,定义合同变更/改签/人员变更相关记录。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 7. `zzvc_contract_cost_detail`

- 表级总体说明：合同成本明细表,定义合同商品/成本明细,包含货号、数量、单价和成本会议室分配标记。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 8. `zzvc_contract_department_code`

- 表级总体说明：销售部门编码规则表,定义合同编码规则中的部门编码和公司主体配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：
  - `zzvc_contract_list.department_id` → `zzvc_contract_department_code.id`
  - `zzvc_contract_review.department_id` → `zzvc_contract_department_code.id`
  - `zzvc_gift_apply.department_id` → `zzvc_contract_department_code.id`

#### 9. `zzvc_contract_engineering_construction_cost`

- 表级总体说明：工程施工成本方向表,定义合同审批工程施工成本科目或方向配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 10. `zzvc_contract_hardware_cost`

- 表级总体说明：硬件成本方向表,定义合同审批硬件成本科目或方向配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 11. `zzvc_contract_labor_cost`

- 表级总体说明：劳务成本方向表,定义合同审批外部劳务成本科目或方向配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 12. `zzvc_contract_list`

- 表级总体说明：合同明细主表,定义新版合同台账/合同明细主表,用于保存合同金额、回款、开票、阶段、销售和项目状态。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_contract_list.chanceId` → `zzvc_business_chance.id`
  - `zzvc_contract_list.companyId` → `zzvc_company_customer.id`
  - `zzvc_contract_list.department_id` → `zzvc_contract_department_code.id`
  - `zzvc_contract_list.user_id` → `zzvc_user.id`
- 被哪些表引用：无

#### 13. `zzvc_contract_list_openbill_comment`

- 表级总体说明：合同开票回款评论表,定义合同开票/回款阶段备注、撤销和评论记录。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_contract_list_openbill_comment.user_id` → `zzvc_user.id`
- 被哪些表引用：无

#### 14. `zzvc_contract_main_business_income`

- 表级总体说明：主营业务收入方向表,定义合同审批主营业务收入科目或方向配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 15. `zzvc_contract_po`

- 表级总体说明：合同 PO 表,定义合同关联 PO 编号、金额和日期。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_contract_po.contract_id` → `zzvc_contract.id`
- 被哪些表引用：无

#### 16. `zzvc_contract_rate`

- 表级总体说明：合同审批税率表,定义合同审批使用的税率基础配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 17. `zzvc_contract_review`

- 表级总体说明：销售合同审批表,是销售合同审批主表,用于保存合同审批、成本、毛利、附件和钉钉审批状态。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_contract_review.chance_id` → `zzvc_business_chance.id`
  - `zzvc_contract_review.customer_id` → `zzvc_company_customer.id`
  - `zzvc_contract_review.department_id` → `zzvc_contract_department_code.id`
  - `zzvc_contract_review.saler_id` → `zzvc_user.id`
- 被哪些表引用：
  - `zzvc_contract_review_upload_file.review_id` → `zzvc_contract_review.id`

#### 18. `zzvc_contract_review_upload_file`

- 表级总体说明：销售合同审批附件表,定义销售合同审批关联文件元数据。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_contract_review_upload_file.review_id` → `zzvc_contract_review.id`
- 被哪些表引用：无

#### 19. `zzvc_contract_sheet`

- 表级总体说明：合同回款/收款计划表,定义合同阶段性收款、验收或回款计划明细。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 20. `zzvc_contract_ticket_opening_detailed`

- 表级总体说明：合同开票明细表,定义合同开票日期、回票日期、提醒和开票类型明细。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 21. `zzvc_dd_open_bill`

- 表级总体说明：钉钉开票申请表,定义钉钉开票申请单及附件基础信息。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_dd_open_bill.cId` → `zzvc_user.id`
  - `zzvc_dd_open_bill.uId` → `zzvc_user.id`
- 被哪些表引用：无

#### 22. `zzvc_dd_open_bill2`

- 表级总体说明：钉钉开票申请明细表,定义新版钉钉开票申请、产品文件、公司主体、同步和完成状态。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_dd_open_bill2.cId` → `zzvc_user.id`
  - `zzvc_dd_open_bill2.companyId` → `zzvc_company_customer.id`
  - `zzvc_dd_open_bill2.uId` → `zzvc_user.id`
- 被哪些表引用：无

#### 23. `zzvc_gift_apply`

- 表级总体说明：赠品审批表,是赠品审批主表,用于保存合同、客户、金额、附件和钉钉审批信息。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_gift_apply.department_id` → `zzvc_contract_department_code.id`
  - `zzvc_gift_apply.user_id` → `zzvc_user.id`
- 被哪些表引用：
  - `zzvc_gift_apply_upload_file.gift_apply_id` → `zzvc_gift_apply.id`

#### 24. `zzvc_gift_apply_upload_file`

- 表级总体说明：赠品审批附件表,定义赠品审批关联文件元数据。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_gift_apply_upload_file.gift_apply_id` → `zzvc_gift_apply.id`
- 被哪些表引用：无

#### 25. `zzvc_sale_open_approved`

- 表级总体说明：销售开票审批汇总表,定义销售开票审批相关联系人或统计信息。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 26. `zzvc_sync_bill_record`

- 表级总体说明：开票同步记录表,定义开票/回票同步记录和提醒状态。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 27. `zzvc_ticket_num`

- 表级总体说明：客户合同票号表,定义供应商税务、开户行、税号、许可证和开票文件信息。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_ticket_num.contract_id` → `zzvc_contract.id`
  - `zzvc_ticket_num.customer_id` → `zzvc_company_customer.id`
- 被哪些表引用：无

### 费用、成本、报销与成本空间

#### 1. `zzvc_bind_cost_meeting_room`

- 表级总体说明：费用明细会议室绑定表,定义费用明细与会议室/成本空间的绑定关系。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_bind_cost_meeting_room.meetingRoomId` → `zzvc_meeting_room.id`
- 被哪些表引用：无

#### 2. `zzvc_cost_company`

- 表级总体说明：成本公司表,定义成本归属公司/主体基础资料。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 3. `zzvc_cost_detail_log`

- 表级总体说明：成本明细操作日志表,定义成本明细变更/操作日志。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_cost_detail_log.meetingRoomId` → `zzvc_meeting_room.id`
  - `zzvc_cost_detail_log.uid` → `zzvc_user.id`
- 被哪些表引用：
  - `zzvc_expenses.cost_id` → `zzvc_cost_detail_log.id`
  - `zzvc_expenses_delzxh.cost_id` → `zzvc_cost_detail_log.id`
  - `zzvc_order.cost_id` → `zzvc_cost_detail_log.id`

#### 4. `zzvc_cost_detail_log_esb2`

- 表级总体说明：ESB2 成本明细操作日志表,定义ESB2 版本成本明细变更/操作日志。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_cost_detail_log_esb2.meetingRoomId` → `zzvc_meeting_room.id`
  - `zzvc_cost_detail_log_esb2.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 5. `zzvc_cost_maintain`

- 表级总体说明：成本维护明细表,定义成本维护批次、序列号、数量和单位。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_cost_maintain.meetingRoomId` → `zzvc_meeting_room.id`
- 被哪些表引用：无

#### 6. `zzvc_expenses`

- 表级总体说明：费用报销表,是销售费用/差旅/报销记录,用于保存费用、客户、合同、审批和报销状态。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_expenses.chance_id` → `zzvc_business_chance.id`
  - `zzvc_expenses.contacts_id` → `zzvc_company_customer_contract.id`
  - `zzvc_expenses.contracts_id` → `zzvc_contract.id`
  - `zzvc_expenses.cost_id` → `zzvc_cost_detail_log.id`
  - `zzvc_expenses.create_person_id` → `zzvc_user.id`
  - `zzvc_expenses.customer_id` → `zzvc_company_customer.id`
- 被哪些表引用：
  - `zzvc_expenses_delzxh.expenses_id` → `zzvc_expenses.id`
  - `zzvc_expenses_revoke.expenses_id` → `zzvc_expenses.id`
  - `zzvc_expenses_trip.expenses_id` → `zzvc_expenses.id`

#### 7. `zzvc_expenses_delzxh`

- 表级总体说明：费用报销历史备份表,是费用报销旧版本/历史备份表,字段接近 zzvc_expenses。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_expenses_delzxh.chance_id` → `zzvc_business_chance.id`
  - `zzvc_expenses_delzxh.contacts_id` → `zzvc_company_customer_contract.id`
  - `zzvc_expenses_delzxh.contracts_id` → `zzvc_contract.id`
  - `zzvc_expenses_delzxh.cost_id` → `zzvc_cost_detail_log.id`
  - `zzvc_expenses_delzxh.create_person_id` → `zzvc_user.id`
  - `zzvc_expenses_delzxh.customer_id` → `zzvc_company_customer.id`
  - `zzvc_expenses_delzxh.expenses_id` → `zzvc_expenses.id`
- 被哪些表引用：无

#### 8. `zzvc_expenses_revoke`

- 表级总体说明：费用报销撤销表,定义费用报销撤销原因、时间和操作人。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_expenses_revoke.expenses_id` → `zzvc_expenses.id`
- 被哪些表引用：无

#### 9. `zzvc_expenses_sketch`

- 表级总体说明：费用报销草稿表,是费用报销草稿/汇总单,用于保存销售费用集合和附件。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_expenses_sketch.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 10. `zzvc_expenses_trip`

- 表级总体说明：差旅行程表,定义费用报销关联的差旅行程起止时间和天数类型。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_expenses_trip.expenses_id` → `zzvc_expenses.id`
- 被哪些表引用：无

#### 11. `zzvc_meeting_room`

- 表级总体说明：会议室/成本空间表,定义会议室或成本空间基础资料及成本项关联。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_meeting_room.companyId` → `zzvc_company_customer.id`
- 被哪些表引用：
  - `zzvc_bind_cost_meeting_room.meetingRoomId` → `zzvc_meeting_room.id`
  - `zzvc_cost_detail_log.meetingRoomId` → `zzvc_meeting_room.id`
  - `zzvc_cost_detail_log_esb2.meetingRoomId` → `zzvc_meeting_room.id`
  - `zzvc_cost_maintain.meetingRoomId` → `zzvc_meeting_room.id`

#### 12. `zzvc_order`

- 表级总体说明：销售费用表,定义销售费用申请/订单协作费用记录，包含客户、合同、费用类型和审批状态。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_order.chance_id` → `zzvc_business_chance.id`
  - `zzvc_order.contacts_id` → `zzvc_company_customer_contract.id`
  - `zzvc_order.contracts_id` → `zzvc_contract.id`
  - `zzvc_order.cost_id` → `zzvc_cost_detail_log.id`
  - `zzvc_order.create_person_id` → `zzvc_user.id`
  - `zzvc_order.customer_id` → `zzvc_company_customer.id`
- 被哪些表引用：
  - `zzvc_order_revoke.order_id` → `zzvc_order.id`

#### 13. `zzvc_order_revoke`

- 表级总体说明：销售费用撤销表,定义销售费用撤销原因、时间和操作人。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_order_revoke.order_id` → `zzvc_order.id`
- 被哪些表引用：无

#### 14. `zzvc_sale_cost_type`

- 表级总体说明：销售费用类型表,定义销售费用/报销费用类型配置。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

### 产品、物料、设备选型与 BOM

#### 1. `zzvc_cjmd`

- 表级总体说明：厂家名单表,定义厂家/厂商名单基础数据。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 2. `zzvc_device_basic_bom`

- 表级总体说明：产品选型 BOM 表,定义产品选型设备的 BOM/配件明细。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_device_basic_bom.cId` → `zzvc_user.id`
- 被哪些表引用：无

#### 3. `zzvc_device_basic_norm`

- 表级总体说明：产品选型基础参数表,定义产品选型设备的键值参数。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_device_basic_norm.companyId` → `zzvc_company_customer.id`
- 被哪些表引用：无

#### 4. `zzvc_device_metrics`

- 表级总体说明：产品选型设备表,是产品选型主表,用于保存产品名称、型号、图片、规格和 PO 包装参数。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 5. `zzvc_materiel`

- 表级总体说明：物料表,是物料主数据表单,用于保存编码、型号、品牌、采购、供应商和审批状态。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_materiel.create_person_id` → `zzvc_user.id`
- 被哪些表引用：
  - `zzvc_materiel_edit_column.materiel_id` → `zzvc_materiel.id`
  - `zzvc_materiel_notice.materiel_id` → `zzvc_materiel.id`
  - `zzvc_materiel_notice_assistant.materiel_id` → `zzvc_materiel.id`

#### 6. `zzvc_materiel_edit_column`

- 表级总体说明：物料编辑字段记录表,定义物料被编辑字段的记录。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_materiel_edit_column.materiel_id` → `zzvc_materiel.id`
- 被哪些表引用：无

#### 7. `zzvc_materiel_notice`

- 表级总体说明：物料通知表,定义物料审核/通知接收状态。
- 主键概览：未声明
- 本表逻辑外键：
  - `zzvc_materiel_notice.materiel_id` → `zzvc_materiel.id`
- 被哪些表引用：无

#### 8. `zzvc_materiel_notice_assistant`

- 表级总体说明：物料协助通知表,定义物料协助人通知和查看状态。
- 主键概览：未声明
- 本表逻辑外键：
  - `zzvc_materiel_notice_assistant.materiel_id` → `zzvc_materiel.id`
- 被哪些表引用：无

#### 9. `zzvc_software`

- 表级总体说明：软件产品表,定义软件/服务器产品选型资料，包含硬件、内存、硬盘、显卡、接口等。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

### 项目、售后、工程日报与需求模板

#### 1. `zzvc_after_sale`

- 表级总体说明：售后项目表,包含售后合同/项目执行信息,用于售后项目列表、未完成项目和售后执行跟踪。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 2. `zzvc_demand_template`

- 表级总体说明：项目需求模板表,定义项目需求/会议室/服务器/部署等需求模板信息。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_demand_template.uId` → `zzvc_user.id`
- 被哪些表引用：无

#### 3. `zzvc_integration_projects`

- 表级总体说明：集成项目表,定义集成项目编号、名称、起止时间和客户联系人。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 4. `zzvc_khda_test_shan`

- 表级总体说明：客户档案测试表,定义客户档案测试/临时表。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 5. `zzvc_project_daily`

- 表级总体说明：工程日报表,是工程日报主表，用于保存日报编号、创建人、部门、图片、工时和计划。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

### 新闻通知、评论、日志与同步记录

#### 1. `zzvc_comment`

- 表级总体说明：评论表,定义新闻或通知评论及回复关系。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_comment.news_id` → `zzvc_news.id`
  - `zzvc_comment.user_id` → `zzvc_user.id`
- 被哪些表引用：无

#### 2. `zzvc_crm_log_esb2`

- 表级总体说明：ESB2 CRM 操作日志表,是ESB2 模块操作审计日志,用于记录模块、SQL、用户和属性 ID。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_crm_log_esb2.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 3. `zzvc_loop_record`

- 表级总体说明：轮询记录表,定义外部单据或钉钉同步轮询记录。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无

#### 4. `zzvc_my_log`

- 表级总体说明：个人日志表,定义老系统个人/登录/操作日志。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_my_log.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 5. `zzvc_my_log_esb2`

- 表级总体说明：ESB2 个人日志表,定义 ESB2 版本个人/登录/操作日志。
- 主键概览：`id`
- 本表逻辑外键：
  - `zzvc_my_log_esb2.uid` → `zzvc_user.id`
- 被哪些表引用：无

#### 6. `zzvc_news`

- 表级总体说明：新闻表,定义新闻内容、分类、图片、阅读和评论统计。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：
  - `zzvc_comment.news_id` → `zzvc_news.id`
  - `zzvc_user_news.news_id` → `zzvc_news.id`

#### 7. `zzvc_notice`

- 表级总体说明：通知公告表,定义系统通知公告、接收人、阅读人和置顶状态。
- 主键概览：`id`
- 本表逻辑外键：无
- 被哪些表引用：无
