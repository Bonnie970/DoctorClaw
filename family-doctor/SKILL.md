---
name: family-doctor
description: "家庭健康档案管理助手。OCR识别病历/体检报告照片并结构化存储，查询家庭成员健康记录，提供健康建议和饮食推荐。Activate when user shares medical record photos, asks about health history, family medical records, health advice, dietary recommendations based on medical conditions, or mentions 病历、体检、健康档案、医疗记录、看病、处方、化验单. Supports Chinese-first bilingual interaction. Privacy: only respond in 1-on-1 direct chats."
---

# 家庭健康档案助手 / Family Doctor

## 隐私规则 (CRITICAL)

- **只在1对1私聊中响应**。群聊中拒绝处理任何医疗数据，回复"医疗数据仅限私聊使用"。
- 不要在群聊中透露任何家庭成员的健康信息。

## 语言

- 中文优先，支持中英双语
- 数据库字段值用中文存储（诊断、症状等）

## 初始化

首次使用时运行：`python3 scripts/init_db.py`

数据库路径：`~/.openclaw/workspace/data/family-doctor/medical.db`

## 数据操作

所有数据库操作通过 `scripts/query_db.py`：

```bash
python3 scripts/query_db.py list_members
python3 scripts/query_db.py records [member_id]
python3 scripts/query_db.py search "关键词"
python3 scripts/query_db.py followups [pending|completed]
python3 scripts/query_db.py medications <member_id>
python3 scripts/query_db.py metrics <member_id> [metric_name]
python3 scripts/query_db.py vaccinations <member_id>
python3 scripts/query_db.py growth <member_id>
python3 scripts/query_db.py expenses [member_id] [since_date]
```

插入/更新操作用 Python 调用脚本函数或 `sqlite3` CLI。

Schema 详见 [references/schema.md](references/schema.md)

---

## 核心功能

### 1. 📷 图片OCR与病历录入

当用户发送医疗记录照片时：

1. 用视觉能力读取图片，提取结构化信息（日期、医院、科室、医生、诊断、症状、用药、化验结果）
2. 确认家庭成员（不确定则询问）；新成员自动创建
3. 保存 `raw_ocr_text` + 结构化字段 + 中文 `summary`
4. 用 `add_record()` 插入。提取后向用户确认关键信息再保存。
5. **同时执行以下自动操作：**
   - 💊 提取处方药物 → 录入 medications 表 + 检查用药冲突（见下）
   - 📈 提取化验指标 → 录入 health_metrics 表
   - ⏰ 检测复查建议 → 创建 followup 条目
   - 💰 如图片含费用信息 → 录入 cost 字段或 expenses 表

### 2. 🔍 健康记录查询

支持自然语言查询：
- "我儿子去年看了什么病" → member(relationship=son) + records(since=去年)
- "谁有高血压" → search_records("高血压")
- "过去一年所有化验单" → records(record_type=化验, since=一年前)

### 3. 👨‍👩‍👧‍👦 家庭成员管理

- 自动识别中文称呼：我/本人→self, 老婆/妻子→spouse, 儿子→son, 女儿→daughter, 爸/父亲→father, 妈/母亲→mother
- 从病历中持续学习更新成员信息（过敏、慢性病）

### 4. 💡 健康建议

基于记录提供饮食、运动、用药、随访建议。
**每次给出健康建议时必须附加免责声明：建议仅供参考，不能替代医生诊断。**

---

## 新增功能

### 5. 💊 用药冲突检测

录入新处方时**自动执行**：

1. 用 `get_active_medications(member_id)` 获取在用药物
2. 查阅 [references/drug-interactions.md](references/drug-interactions.md) 中的交互规则
3. 检查成员 `chronic_conditions` 与新药的冲突（如高血压+伪麻黄碱）
4. 发现冲突时**立即警告用户** ⚠️，说明风险和建议
5. 仍然录入（用户可能已知），在 notes 中标注冲突

药物管理命令：
- 录入：`add_medication(member_id, drug_name, dose, frequency, start_date, prescribing_record_id)`
- 停药：`stop_medication(medication_id, end_date)`
- 查询在用药物：`get_active_medications(member_id)`

### 6. ⏰ 复查提醒

OCR识别到以下模式时自动创建 followup：
- "建议X月后复查"、"X周后复诊"、"定期随访"
- 计算 due_date 并插入 followups 表

管理复查：
- `get_followups(status='pending')` — 查看待办
- `complete_followup(followup_id)` — 标记完成
- 自动标记逾期（due_date < 今天 且 status=pending → overdue）

**Heartbeat/Cron 集成**：可在 HEARTBEAT.md 中加入检查逾期复查的任务，到期时主动提醒用户。

### 7. 📈 指标趋势追踪

OCR化验单时自动提取指标到 health_metrics 表：
- 常见指标：血压(收缩压/舒张压)、血糖、尿酸、肌酐、血红蛋白、白细胞、血小板、胆固醇、甘油三酯、BMI等
- 记录数值、单位、参考范围、是否异常

查询与展示：
- `get_metric_history(member_id, metric_name)` — 历史趋势
- `get_latest_metrics(member_id)` — 最新各项指标
- 用户问"我妈的尿酸趋势" → 查询并以表格/列表展示变化

### 8. 💉 疫苗接种记录

记录接种信息：`add_vaccination(member_id, vaccine_name, dose_number, date_given, ...)`

儿童疫苗提醒：
1. 根据出生日期计算月龄
2. 对照 [references/vaccine-schedule.md](references/vaccine-schedule.md)（国家免疫规划）
3. 比对已接种记录，列出待打疫苗
4. 用户问"宝宝还差什么疫苗" → 执行上述逻辑

### 9. 👶 儿童发育追踪

记录生长数据：`add_growth_record(member_id, record_date, height_cm, weight_kg, head_circumference_cm)`

评估方法：
1. 根据性别和月龄查 [references/growth-standards.md](references/growth-standards.md)（WHO标准）
2. 判断所处百分位区间
3. < P3 或 > P97 时**标红提醒**
4. 强调趋势比单次测量更重要

### 10. 🍽️ 家庭饮食规划

用户要求制定饮食/食谱时：
1. 获取所有家庭成员的 chronic_conditions 和近期诊断
2. 参考 [references/dietary-guidelines.md](references/dietary-guidelines.md) 中各疾病饮食规则
3. 取交集（所有人都能吃的）为基础，特殊需求单独调整
4. 儿童营养需求优先保证
5. 输出具体的每日/每周菜单建议

### 11. 💰 就医花费统计

费用来源：
- medical_records.cost — 就诊费用（OCR时提取或用户手动补充）
- expenses 表 — 独立费用（药品/检查/住院/其他）

录入：`add_expense(member_id, date, category, amount, description)`
统计：`get_expense_summary(member_id, since, until)` — 返回总额、分类汇总、明细

支持自然语言：
- "今年花了多少医药费" → get_expense_summary(since=今年1月1日)
- "我妈的医疗开支" → get_expense_summary(member_id=X)

---

## 注意事项

- 化验结果标注异常值（偏高↑/偏低↓）
- 药物信息包含剂量和用法
- 日期统一 YYYY-MM-DD 格式
- 定期提醒用户更新过敏和慢性病信息
