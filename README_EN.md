# 🦞 DoctorClaw - Family Health Management
## A Virtual Family Doctor for 120 Million Sandwich Families in China

**Language / 语言:** [English](./README_EN.md) | [中文](./README.md)

---

> *"The best technology is the kind you barely notice, yet it truly makes people feel cared for."*
> *"Truly great AI is not the smartest AI, but the warmest AI."*

---

## Quick Install

Copy the skills in this directory into your OpenClaw skills directory.

```bash
git clone https://github.com/Bonnie970/DoctorClaw.git
cd DoctorClaw
cp -r * ~/.openclaw/skills/.
```

Try uploading a medical record image.

## 📋 Project Basics

| Item | Content |
|------|---------|
| **Project Name** | DoctorClaw — Family Health Management |
| **One-line Intro** | A virtual family doctor on every family phone, helping sandwich families move from hectic health management to calm, organized care |
| **Core Value** | One entrance for whole-family health: medical records, chronic disease metrics, child development, menstrual/fitness tracking, medication safety, nutrition planning, and research tracking—from fragmented records to proactive AI protection |

## 🎯 Project Overview

There is a large but often overlooked group: **sandwich families**.

They care for elderly parents, raise young children, and handle work pressure at the same time. These families carry the health burden of three generations, yet often fall into three major “health black holes”:

| Black Hole | Real Challenge |
|------|----------|
| **Scattered Health Data** | Not only medical records—parents’ blood pressure/glucose logs, children’s vaccine books and growth records, spouse’s menstrual data, your own fitness/body-fat data… family health data is scattered across many apps, paper notes, and WeChat chats, with no complete health profile |
| **No Care Guidance** | Should blood pressure meds be adjusted? Will new and old drugs conflict? Is child development on track? Should menstrual abnormalities trigger a clinic visit? Families lack one “person” who understands the whole family and can guide decisions |
| **Huge Time Loss** | Taking leave for clinic visits, waiting in long lines, forgetting doctor instructions—many of these can be significantly reduced with better preparation and proactive reminders |

**DoctorClaw** is built to solve this exact social pain point. It is not just another health note-taking tool. It gives AI an “autopilot system” for family healthcare—**from passive logging to proactive alerts, from single-person management to whole-family coverage, and from information silos to research linkage**. It becomes every family’s:

- 🏠 **Virtual Family Doctor** — one clear view of everyone’s health status
- 🤝 **AI Medical Visit Assistant** — full support before, during, and after visits
- 🍽️ **Family Nutritionist** — science-based meal planning that balances all family needs
- 🔬 **Medical Intelligence Agent** — latest medical research delivered quickly

---

## 🦞 II. What Can DoctorClaw Do?

### 🔧 Core Capabilities (for the whole family)

| Feature | Description |
|------|------|
| **📸 Photo-based Record Building** | **Problem:** Records are scattered across hospitals/departments and mostly paper-based; history is often incomplete at new hospitals.<br>**How:** Take photos of records/lab sheets/prescriptions. AI performs OCR and structured extraction, then links data to family members via natural language like “This is my mom’s checkup report.” |
| **👨‍👩‍👧‍👦 Family Member Management** | **Problem:** Family health information is scattered and hard to manage together.<br>**How:** Add members via natural language, support three-generation family structures and relationships (e.g., parent-child, spouse). One person can input and benefit the whole family. |
| **🔍 Natural Language Search** | **Problem:** Traditional search needs exact keywords, making health data retrieval difficult.<br>**How:** Ask things like “What medicine did my dad take last year?” or “When did the baby last have a fever?” AI understands intent and returns structured answers. |
| **📋 Visit Summary Generation** | **Problem:** At a new hospital, patients often cannot clearly recall complete history when doctors ask.<br>**How:** One-click history summary by timeline, including key diagnoses/surgeries/medications, ready to print or show to doctors. |
| **🔒 Privacy Protection** | **Promise:** Sensitive medical data is handled only in 1:1 private chat, never leaked in group chat; data is stored locally with physical isolation, fully controlled by users. |

### 👶 Children Module

| Feature | Description |
|------|------|
| **📈 Growth Curves** | **Problem:** Parents often lack intuitive reference for whether growth and development are normal.<br>**How:** Record height/weight/head circumference, compare against WHO growth percentiles, generate growth curves, and flag outliers (<P3 or >P97). |
| **💉 Vaccine Assistant** | **Problem:** New parents are often unsure what vaccine is due now.<br>**How:** Built-in China 0–6 years vaccine schedule (Category I + II), auto-calculate due vaccines by birth date, track dose/batch/institution, and remind ahead of time. |
| **🤒 Illness Log** | **Problem:** Frequent childhood illness makes medication history hard to remember, increasing repeated prescriptions.<br>**How:** Track each illness event (time/symptoms/diagnosis), medication history and outcomes, and frequency patterns. |

### 👩 Women/Adults Module

| Feature | Description |
|------|------|
| **🩸 Menstrual Tracking** | **Problem:** Women need cycle/symptom tracking, next-period prediction, and pregnancy planning support.<br>**How:** Record cycle/symptoms/flow, predict next period and ovulation, provide fertility reminders, and detect abnormal patterns. |
| **💪 Body Fat / Fitness Tracking** | **Problem:** Weight loss and fitness need scientific tracking rather than feelings.<br>**How:** Track weight/body fat/BMI, generate trend charts, and track progress against goals. |
| **💊 Drug Interaction Detection** | **Problem:** Multi-drug use in chronic disease carries high interaction risk (e.g., warfarin + NSAIDs severe bleeding risk).<br>**How:** Built-in 2000+ common interaction rules. New prescriptions are automatically checked against current medications and chronic contraindications, with immediate red warnings and doctor-consult suggestions. |

### 👴 Elderly Module

| Feature | Description |
|------|------|
| **📊 Chronic Metric Tracking** | **Problem:** Shift from “treat after getting sick” to long-term health management.<br>**How:** Record blood pressure/glucose/uric acid, auto-generate trend charts, flag abnormal values with ranges, and support time/member comparison queries. |
| **⏰ Follow-up / Medication Reminders** | **Problem:** Doctors often say “review in 3 months,” but busy schedules make it easy to forget.<br>**How:** OCR automatically extracts “review after X months” instructions, calculates due date, creates reminders, and tracks status (pending/completed/overdue). |
| **📝 Medication List** | **Problem:** Elderly patients often take many drugs and can get confused; family members may not know full medication details.<br>**How:** Build a complete active-medication list with dosage/usage/contraindications; export with one click for clinic visits. |

### 🍽️ Whole-family Features

| Feature | Description |
|------|------|
| **🍽️ Family Diet Planning** | **Problem:** One family may include a hypertensive elder (low sodium), a gout patient (low purine), and growing children (high calcium)—needs conflict with each other.<br>**How:** Combine all members’ chronic conditions and diagnoses, intersect disease diet rules, prioritize child nutrition, and generate daily/weekly menu suggestions. |
| **💰 Medical Expense Ledger** | **Problem:** Most families have no clear view of annual medical spending or where it goes.<br>**How:** Automatically aggregate medical costs, analyze by member/department/time period, generate spending charts, and support natural language queries. |
| **🚨 Emergency Card** | **Problem:** In emergencies, caregivers need key medical info immediately.<br>**How:** One-click emergency card (allergies/blood type/chronic diseases/emergency contacts), ready for lock screen storage. |
| **🌡️ Seasonal Alerts** | **Problem:** Different seasons carry different health risks and require prevention in advance.<br>**How:** Issue region + season risk alerts (e.g., spring allergy reminders and medication prep suggestions). |

### 🔬 Advanced Feature: Medical Radar

| Feature | Description |
|------|------|
| **🔍 Paper Search** | **Problem:** Families cannot easily access the latest research on new drugs or therapies.<br>**How:** Subscribe to disease keywords, track latest PubMed/medRxiv papers, and use LLM to generate Chinese summaries so non-experts can benefit. |
| **📡 Subscription Push** | **Problem:** Hard to continuously follow updates on a specific disease/drug.<br>**How:** Follow topics and receive weekly updates linked to family conditions. |
| **🔗 Condition Linkage** | **Problem:** Users often don’t know which research directions to follow.<br>**How:** Recommend research directions based on family medical history, with special flags for highly relevant studies. |

---

## ⚙️ Technical Implementation

### System Architecture

```text
family-doctor/
├─ SKILL.md                  # ~130 lines, compact skill description
├─ scripts/
│  ├─ init_db.py             # Initialize family private database
│  ├─ query_db.py            # 15+ query functions for complex health queries
│  └─ charts.py              # Data visualization (growth curves, metric trends, etc.)
└─ references/
   ├─ schema.md              # Complete field documentation for data consistency
   ├─ drug-interactions.md   # Drug interaction rule set based on authoritative medical guidance
   ├─ vaccine-schedule.md    # China vaccine schedule, official sources
   ├─ growth-standards.md    # WHO growth standards
   └─ dietary-guidelines.md  # Dietary guidelines integrating nutrition principles

med-radar/
├─ SKILL.md                  # Medical research radar skill
├─ scripts/
│  ├─ init_db.py             # Initialize subscription database
│  ├─ query_db.py            # Subscription management and summary queries
│  └─ search_pubmed.py       # PubMed/medRxiv paper search
└─ references/
   ├─ sources.md             # Data source details
   └─ prompt-templates.md    # Summary templates (weekly digest/single-paper brief)
```

### Technical Highlights

| Highlight | Description |
|------|------|
| **Local-first** | Core health data is stored locally in the family environment for better privacy |
| **Modular Design** | Eight major capabilities are independent yet integrated for fast iteration |
| **AI Capability** | Uses Claude OCR, understanding, and reasoning for medical text processing |
| **Open Interfaces** | Supports integration with mainstream health devices and hospital systems |
| **Skill Linkage** | `family-doctor` and `med-radar` coordinate automatically, recommending research subscriptions based on diagnoses |

### Database Design

Uses SQLite3 (with FTS5 full-text search):

- `family_members` - Basic family member info
- `medical_records` - Medical records (with FTS search)
- `medications` - Medication records
- `followups` - Follow-up reminders
- `health_metrics` - Health metrics
- `vaccinations` - Vaccination records
- `growth_records` - Child growth records
- `expenses` - Medical expenses
- `health_notes` - Health notes

---

## 📖 Real Usage Scenarios: A Family Story

### Scenario 1: Taking Dad for Follow-up — Less stress, no missed instructions

> “Next week I’m taking my dad for an atrial fibrillation follow-up.”
>
> → DoctorClaw automatically generates:
>
> - ❓ **Questions for the doctor** (smart suggestions based on condition)
> - 📋 **Visit prep checklist** (documents and precautions)
> - 🏥 **Visit summary** (one-click history summary for new doctors)
> - ⏰ **Follow-up and medication reminders** (automatically set)

> @Filial daughter Ms. Wang: “During the National Day visit, I answered all history questions clearly. The doctor even praised how well prepared we were.”

**Why it’s stronger than others:** Not a simple notes app; it recommends questions by diagnosis, extracts doctor instructions, and sets reminders automatically.

---

### Scenario 2: Dinner for a Family of Five — One table, everyone covered

> “Family of five: grandma has gout, dad has hypertension, mom is losing weight, two kids are growing.”
>
> → DoctorClaw generates a weekly meal plan:
>
> - 🍽️ **Plan A for grandma** (low purine: avoid seafood, organ meat, rich broth)
> - 🍽️ **Plan B for dad** (low-sodium DASH diet)
> - 🍽️ **Plan C for kids** (calcium + quality protein)
> - 💡 **Shared core dishes** with differentiated side options

> @Sandwich dad Mr. Chen: “We used to struggle every day with what to cook. Now one table can take care of everyone.”

**Why it’s stronger than others:** Not just recipe suggestions; it balances all family needs and prioritizes child nutrition.

---

### Scenario 3: Remote Care for Parents — Distance is no longer a barrier

> “I created health profiles for both parents. They live in hometown, I live in Beijing, and I can still check anytime.”
>
> → DoctorClaw provides:
>
> - 👀 **Remote view** of parent records
> - 💊 **Medication reminders** pushed to parents
> - 📈 **Abnormal metric alerts**
> - 🏥 **Automatic follow-up reminders**

**Why it’s stronger than others:** Not simple syncing, but proactive alerting so children living far away can still track parents’ health.

---

### Scenario 4: Photo-based Record Entry — Snap once, structured instantly

> Take a photo of a medical report → AI instant OCR → structured storage
>
> → “This is your checkup report from PUMCH. Thyroid nodule TI-RADS 2, follow-up in 6 months.”

**Why it’s stronger than others:** Not image storage, but OCR + structured extraction + natural-language family linking (e.g., “This is my mom’s report”).

---

### Scenario 5: Baby Growth Tracking — Development at a glance

> “How is Xiyuan’s development?” → Automatically generate WHO growth curves
>
> “Which vaccine is due now?” → List due vaccines by age in months

> @New dad Mr. Li: “My son reached 2 months and I had no idea what to do. DoctorClaw told me exactly which vaccines were due. I booked immediately.”

**Why it’s stronger than others:** Not simple logging; it evaluates growth against WHO standards and auto-calculates vaccines from national guidelines.

---

### Scenario 6: Elderly Chronic Care — Long-term trends and anomaly alerts

> Enter blood pressure data → trend chart + anomaly highlighting
>
> “How has dad’s blood pressure been lately?” → “Weekly average 145/92, higher than last month, consider clinical adjustment.”

**Why it’s stronger than others:** Upgrades from “recording numbers” to “health management” via trend analysis and actionable prompts.

---

### Scenario 7: Drug Conflict Detection — First safety guardrail for medication

> @Working mom Ms. Zhang: “My husband has gout + hypertension. I entered a new drug ‘ibuprofen,’ and DoctorClaw immediately warned: ❌ Warfarin + NSAIDs increases bleeding risk!”

**Why it’s stronger than others:** Built-in 2000+ interaction rules; checks active meds + chronic contraindications with immediate red alerts.

---

### Scenario 8: Medical Radar — Stay synchronized with medical progress

> “Search recent papers on cervical spondylosis.”
>
> → Returns 4 related paper summaries in Chinese, with relevance to family condition
>
> “What makes this better than normal search?” → Automatic condition linkage and precise recommendation

**Why it’s stronger than others:** Not simple paper search; it links to family conditions, proactively recommends relevant research, and translates progress into user-friendly summaries.
