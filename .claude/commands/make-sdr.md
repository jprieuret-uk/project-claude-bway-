You are helping the user build a complete AI SDR agent from scratch. Work through the following steps in order, asking for input at each stage before building anything.

---

## STEP 1 — COMPANY CONTEXT

Ask the user for:
- What does the company sell? (product description, 2-3 sentences)
- Who buys it? (job titles, company types, company size)
- What pain does it solve, and what does the buyer already spend money on today to solve it?
- What is the pricing angle vs competitors?
- What geographies to target first?

Save everything they tell you. You will use it to build CLAUDE.md.

---

## STEP 2 — IDEAL CUSTOMER PROFILE

Ask the user:
- Who is the primary ICP? (company type + decision maker title)
- Who is the secondary ICP if any?
- What is the minimum bar to qualify? (headcount, revenue, volume threshold)
- Who should be excluded entirely?

---

## STEP 3 — INTENT SIGNALS

Ask the user what buying signals matter for their product. Guide them with examples:
- Hiring for a role that suggests the problem is growing
- Using a competitor or legacy solution
- Recent funding or headcount growth
- Leadership change (new ops hire, new VP)
- Company expanding into new markets or geographies

For each signal they name, agree on:
- Tier: High / Medium
- Why it matters in the context of their product

---

## STEP 4 — MESSAGE RULES

Ask the user:
- What tone? (direct / consultative / challenger)
- Word count target?
- What words or phrases are banned?
- What is the one CTA? (call, demo, reply)
- What should every message reference? (a specific signal, a company detail, a geography)

---

## STEP 5 — BUILD THE FILE STRUCTURE

Once you have all the above, create the following:

```
sdr-agent/
  CLAUDE.md                  ← master context: company, ICP, signals, message rules, prospect query, agent workflow
  .env                       ← API keys and email config (never commit real values)
  .gitignore                 ← ignore .env, __pycache__, data/digest*.html
  TODO.md                    ← track what still needs doing
  prompts/
    prospect_finder.md       ← Apollo search instructions: titles, company keywords, filters, exclusions, output format
    signal_detector.md       ← signal search + scoring logic with recency caps
    message_writer.md        ← message tone, rules, format (email vs LinkedIn DM), output schema
    run_pipeline.md          ← end-to-end pipeline instructions Claude follows step by step
  src/
    email_digest.py          ← compiles drafts into HTML digest, sends via SMTP
    enrich_prospects.py      ← runs apollo_people_match for contact_now and contact_this_week only
  data/
    prospects/.gitkeep
    enriched/.gitkeep
    drafts/.gitkeep
```

---

## STEP 6 — CLAUDE.md

Write CLAUDE.md using everything gathered in Steps 1-4. It must include:

- **Company** — what it sells, product A and B if applicable
- **Ideal Customer Profile** — who to target, who to skip, minimum bar, decision makers
- **Intent Signals** — table with signal name, tier, why it matters
- **Message Rules** — numbered list, all constraints and tone guidance
- **Prospect Query** — Apollo filters: titles, company keywords, industries, headcount, geography, exclusions, search sequence
- **Agent Workflow** — the 5-step pipeline with the hard rule: Apollo credits only after timing score of 5+

---

## STEP 7 — PROMPTS

Write each prompt file using the context from CLAUDE.md:

**prospect_finder.md** — instructs Claude to search Apollo with the exact filters from CLAUDE.md, skip existing clients, save output to data/prospects/[date].json with fields: name, title, company, email, linkedin_url, employee_count, state, segment.

**signal_detector.md** — instructs Claude to:
- Run web searches per prospect (funding, hiring, LinkedIn posts, pain-area keywords)
- Score against the Intent Signals in CLAUDE.md
- Apply recency caps: within 30 days → score 8-10 (contact_now), 31-90 days → score 5-7 (contact_this_week), older than 90 days → score capped at 4 (monitor)
- Require ISO dates (YYYY-MM-DD) — never accept vague ranges
- Include signal_age_days in output
- Save to data/enriched/[date]/ as contact_now.json, contact_this_week.json, monitor.json
- Re-score monitor prospects only if last_checked > 14 days ago

**message_writer.md** — instructs Claude to:
- Write one message per enriched prospect in contact_now and contact_this_week
- Apply all message rules from CLAUDE.md
- Choose format: email (with subject line) or LinkedIn DM based on what contact info is available
- Output JSON per prospect: prospect, format, subject_line, message, signal_referenced, word_count
- Save to data/drafts/[date]/[company_slug]_[firstname].json

**run_pipeline.md** — step-by-step pipeline Claude executes:
1. Run prospect_finder
2. Run signal_detector
3. Run apollo_people_match on contact_now and contact_this_week only — never on monitor
4. Run message_writer
5. Run: python3 src/email_digest.py --date [today]
6. Log to CRM if connected (status: Outreach Pending, note: signal + format + date)
- Print a final summary after each step and at the end

---

## STEP 8 — email_digest.py

Write src/email_digest.py with:
- Loads drafts from data/drafts/[date]/
- Validates each draft for banned phrases (em dash, forbidden words from message rules)
- Loads timing scores from data/enriched/[date]/contact_now.json and contact_this_week.json
- Sorts cards: flagged first, then contact_now by score desc, then contact_this_week by score desc
- Builds HTML email with one card per prospect showing: full name, title, company, timing badge, score, signal, format, send-to (email or LinkedIn URL), subject line if email, message body with "Hi [first_name]," prepended
- Supports multiple recipients via comma-separated EMAIL_RECIPIENT in .env
- Falls back to saving HTML file if .env not configured
- Sends via Gmail SMTP by default (smtp.gmail.com:587), Outlook if EMAIL_SMTP_HOST overridden

---

## STEP 9 — .env and .gitignore

Write .env with blank placeholders:
```
APOLLO_API_KEY=
EMAIL_SENDER=
EMAIL_PASSWORD=
EMAIL_RECIPIENT=
# EMAIL_SMTP_HOST=smtp.office365.com
# EMAIL_SMTP_PORT=587
```

Write .gitignore to exclude:
```
.env
__pycache__/
*.pyc
data/digest*.html
```

---

## STEP 10 — SLASH COMMAND

Create .claude/commands/run-sdr.md containing:
```
Read sdr-agent/prompts/run_pipeline.md and execute it.
```

This lets the user trigger the full pipeline with /run-sdr in Claude Code.

---

## STEP 11 — COMMIT

Stage and commit everything to the working branch with a clear message. Push to remote. Print a summary of what was built.
