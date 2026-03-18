# 数据库字段参考 / Database Schema Reference

## family_members 家庭成员表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| name | TEXT | 姓名 |
| relationship | TEXT | 与用户关系（self/spouse/son/daughter/father/mother 等） |
| birthday | TEXT | 生日 YYYY-MM-DD |
| gender | TEXT | 性别 male/female |
| blood_type | TEXT | 血型 |
| allergies | TEXT | 过敏信息，逗号分隔 |
| chronic_conditions | TEXT | 慢性病，逗号分隔 |
| notes | TEXT | 备注 |

## medical_records 病历记录表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| member_id | INTEGER FK | 关联家庭成员 |
| record_date | TEXT | 就诊/报告日期 YYYY-MM-DD |
| record_type | TEXT | 类型：门诊/住院/体检/化验/处方/影像/疫苗/其他 |
| hospital | TEXT | 医院名称 |
| department | TEXT | 科室 |
| doctor | TEXT | 医生 |
| diagnosis | TEXT | 诊断 |
| symptoms | TEXT | 症状 |
| medications | TEXT | 用药，JSON array |
| lab_results | TEXT | 检验结果，JSON |
| raw_ocr_text | TEXT | OCR原文 |
| summary | TEXT | AI生成摘要 |
| source_file | TEXT | 原始图片路径 |
| tags | TEXT | 标签，逗号分隔 |
| cost | REAL | 本次就诊费用（可选） |

## medications 用药记录表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| member_id | INTEGER FK | 关联家庭成员 |
| drug_name | TEXT | 药品名称 |
| dose | TEXT | 剂量（如 "10mg"） |
| frequency | TEXT | 用法（如 "每日两次"） |
| start_date | TEXT | 开始日期 |
| end_date | TEXT | 结束日期（NULL=持续服用） |
| prescribing_record_id | INTEGER FK | 关联处方记录 |
| is_active | INTEGER | 1=在用, 0=已停 |
| notes | TEXT | 备注 |

## followups 复查提醒表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| member_id | INTEGER FK | 关联家庭成员 |
| description | TEXT | 复查内容描述 |
| due_date | TEXT | 复查到期日 YYYY-MM-DD |
| source_record_id | INTEGER FK | 来源病历 |
| status | TEXT | pending/completed/overdue |
| completed_date | TEXT | 完成日期 |

## health_metrics 健康指标表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| member_id | INTEGER FK | 关联家庭成员 |
| metric_date | TEXT | 检测日期 |
| metric_name | TEXT | 指标名称（如 血压收缩压、尿酸、BMI） |
| value | REAL | 数值 |
| unit | TEXT | 单位 |
| reference_range | TEXT | 参考范围 |
| is_abnormal | INTEGER | 0=正常, 1=异常 |
| source_record_id | INTEGER FK | 来源记录 |

## vaccinations 疫苗接种表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| member_id | INTEGER FK | 关联家庭成员 |
| vaccine_name | TEXT | 疫苗名称 |
| dose_number | INTEGER | 第几剂 |
| date_given | TEXT | 接种日期 |
| next_due_date | TEXT | 下次接种日期 |
| batch_number | TEXT | 批号 |
| hospital | TEXT | 接种单位 |
| notes | TEXT | 备注 |

## growth_records 生长发育记录表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| member_id | INTEGER FK | 关联家庭成员 |
| record_date | TEXT | 测量日期 |
| height_cm | REAL | 身高(cm) |
| weight_kg | REAL | 体重(kg) |
| head_circumference_cm | REAL | 头围(cm) |
| notes | TEXT | 备注 |

## expenses 医疗支出表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| member_id | INTEGER FK | 关联家庭成员 |
| date | TEXT | 日期 |
| category | TEXT | 分类：药品/检查/住院/其他 |
| amount | REAL | 金额(元) |
| description | TEXT | 说明 |
| source_record_id | INTEGER FK | 关联就诊记录 |

## health_notes 健康笔记表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增ID |
| member_id | INTEGER FK | 关联家庭成员（可选） |
| note_date | TEXT | 日期 |
| category | TEXT | 分类 |
| content | TEXT | 内容 |
