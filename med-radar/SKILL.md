---
name: med-radar
description: "医学科研雷达 — 追踪疾病、药物、疗法的最新研究进展。订阅关键词后定期汇总PubMed/medRxiv最新论文。Activate when user asks about medical research updates, latest papers, clinical trial progress, drug development news, or mentions 科研进展、最新研究、论文追踪、文献综述. Can integrate with family-doctor skill for personalized research tracking."
---

# 医学科研雷达 (Med-Radar) 📡

追踪疾病、药物、疗法的最新研究进展。

## 1. 初始化

首次使用时初始化数据库：

```bash
python3 {SKILL_DIR}/scripts/init_db.py
```

数据库位置：`~/.openclaw/workspace/data/med-radar/radar.db`

## 2. 订阅管理

### 添加订阅

```bash
python3 {SKILL_DIR}/scripts/query_db.py add "高尿酸血症" --keywords "hyperuricemia,gout,uric acid,尿酸,痛风"
```

可选参数：`--source pubmed|medrxiv|all` `--lang zh|en|both` `--freq weekly|daily`

### 查看订阅

```bash
python3 {SKILL_DIR}/scripts/query_db.py list
```

### 删除/开关订阅

```bash
python3 {SKILL_DIR}/scripts/query_db.py remove <id>
python3 {SKILL_DIR}/scripts/query_db.py toggle <id> on|off
```

## 3. 手动搜索

无需订阅，直接搜索：

```bash
python3 {SKILL_DIR}/scripts/search_pubmed.py "SGLT2 inhibitor heart failure" --days 14 --max 20
```

参数：
- `--days N` — 搜索最近N天（默认7）
- `--max N` — 最多返回N篇（默认10）
- `--source pubmed|medrxiv|all` — 数据源（默认all）

输出为JSON数组，每篇包含 title, authors, journal, pub_date, doi, abstract, url。

**搜索后**：用LLM阅读结果，按 `references/prompt-templates.md` 中的模板生成中文摘要。

## 4. 定期推送

为用户设置定期摘要推送（通过OpenClaw cron）：

### 流程

1. 读取所有enabled的订阅
2. 对每个订阅，用其keywords调用 `search_pubmed.py`
3. 用LLM按周报模板（见 `references/prompt-templates.md`）生成中文摘要
4. 将摘要存入digests表：`query_db.py` 的 `save_digest` 函数
5. 将摘要发送给用户

### Cron设置建议

每周一早上9:00 (用户时区) 执行：

```
openclaw cron add --schedule "0 1 * * 1" --prompt "执行med-radar周报：读取所有订阅，搜索最近7天论文，生成中文摘要周报并发送给我" --channel webchat
```

## 5. 与family-doctor联动

如果用户已使用 `family-doctor` 技能管理健康档案：

- 根据家庭成员的诊断/慢性病，**主动建议**相关研究订阅
- 例：家人有高尿酸血症 → 建议订阅 "hyperuricemia" 相关研究
- 当新研究与家人病情相关时，在摘要中特别标注

## 6. 注意事项

- **数据源限制：** 目前仅支持PubMed和medRxiv，以英文文献为主
- **中文文献补充：** Agent可使用 `web_search` 搜索中文文献（知网、万方等需付费，无法直接API访问）
- **预印本提醒：** medRxiv论文未经同行评审，解读时务必说明
- **非医疗建议：** 所有摘要仅供科研参考，不构成医疗建议
- **详细数据源说明：** 见 `references/sources.md`
