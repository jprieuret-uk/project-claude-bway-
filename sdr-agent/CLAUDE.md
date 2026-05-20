# SDR Agent — Master Context File

## What We Sell

Brighterway is an AI-powered medical record review platform built for the workers' compensation space. It ingests disorganized medical records, deduplicates them, and surfaces only the 10–15% of pages relevant to a physician's specialty — cutting hours of manual review to minutes.

Physicians access an online portal with AI-generated summaries alongside original documents. They can filter, search, and edit by category (e.g. "Clinical Notes", "Ankle") in seconds. The platform also automates manual tasks and delivers analytics across the full record pipeline.

**Core value props (in order of priority):**
1. Cheaper than competitors for QME work
2. Better AI output quality than other AI startups in this space
3. Replaces or reduces reliance on offshore review staff

---

## Ideal Customer Profile (ICP)

**Primary target:** QME/IME management companies that coordinate work for 10 or more physicians. The key is not how many doctors they employ — it's how many physician relationships they manage and route cases through.

**Secondary target:** Third-Party Administrators (TPAs) handling workers' comp claims at scale.

**Firmographic filters:**
- Operates in the workers' compensation space (QME, IME, med-legal)
- Manages or coordinates records for 10+ physicians
- Based in the US (California is the core market — QME is CA-specific)
- Company types: IME management companies, QME panels, med-legal evaluation firms, TPA vendors

**Exclude:**
- Solo physicians with no management layer
- General hospitals or health systems (not the target vertical)
- Law firms (buyers of reports, not record review platforms)

---

## Buyer Personas

| Segment | Title | Notes |
|---|---|---|
| QME / IME company | Owner, Head of Operations, Workers' Comp Manager | Often the same person in smaller firms |
| TPA | Claims Manager, Head of Vendor Services, Vendor Relations Manager | Cares about turnaround time and cost per claim |

Outreach should be addressed to the operations decision-maker, not the physician unless they are the owner.

---

## Buying Signals (prospect is likely ready now)

These indicate the pain is proven and budget likely exists:

1. **Already using an AI platform** — they've validated the category, may be dissatisfied with output quality or cost
2. **Using offshore staff for record review** — active spend on a problem we solve; cost and quality argument lands immediately
3. **Hiring for medical records or operations roles** — signals volume growth and process pain
4. **Expanding physician network or opening new locations** — case volume is increasing
5. **Job postings for IME coordinators, medical record reviewers, or QME schedulers** — operational strain is visible

---

## Messaging Guidelines

**Lead with cost and quality — in that order.**

- Cheaper than competitors for QME work (lead with this for price-sensitive ops buyers)
- AI output quality is meaningfully better than other platforms (use this to differentiate from AI-first competitors)
- If they use offshore: frame Brighterway as a direct replacement that costs less and makes fewer errors

**Tone:** Direct, short, ops-minded. These are busy people managing high case volume. No fluff.

**What to reference in outreach:**
- Their physician network size or specialty if known
- If they're an IME company vs. QME panel vs. TPA (shows you know the space)
- Workers' comp specific language: QME, IME, AME, case volume, turnaround time, specialty filtering

**What to avoid:**
- Generic "AI-powered" language without specifics
- Clinical language (we're not selling to physicians, we're selling to ops)
- Long emails

---

## Prospecting Tools

To be configured. Likely sources:
- Apollo.io (primary — contact and company search)
- LinkedIn / Sales Navigator (signal detection, job postings)
- Manual research on state QME panel directories (California DIR)

---

## Data Flow

```
data/prospects/   ← raw lists from Apollo or manual sourcing
data/enriched/    ← prospects with signals, ICP score, and context added
data/drafts/      ← personalised outreach messages ready for review
```

---

## Agent Workflow

1. **prospect_finder** — searches for QME/IME management companies matching ICP, outputs to `data/prospects/`
2. **signal_detector** — scans each prospect for buying signals (AI tool use, offshore staff, hiring), outputs to `data/enriched/`
3. **message_writer** — drafts personalised outreach per prospect based on signals found, outputs to `data/drafts/`
4. **email_digest** — compiles enriched prospects and drafted messages into a daily summary email for human review before sending
