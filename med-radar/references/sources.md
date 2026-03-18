# 数据源说明

## PubMed (主要来源)
- **API:** NCBI E-utilities (免费，无需API key)
- **地址:** https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
- **覆盖:** 全球主要生物医学期刊，以英文为主
- **频率限制:** 无API key时每秒3次请求
- **优势:** 权威、全面、结构化摘要

## medRxiv (预印本)
- **API:** https://api.medrxiv.org/
- **覆盖:** 医学预印本，未经同行评审
- **优势:** 最新研究，比正式发表早数月
- **注意:** 预印本未经同行评审，结论需谨慎对待

## 暂不支持的来源
- **知网 (CNKI):** 需付费账号，无公开API
- **万方:** 需付费账号
- **变通方案:** Agent可通过 `web_search` 搜索中文文献作为补充

## 搜索策略建议
1. 英文关键词搜PubMed/medRxiv（主力）
2. 中文关键词通过web_search补充知网/万方结果
3. 对重要主题同时使用疾病名+药物名+机制关键词
