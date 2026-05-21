Open the sdr-agent project folder and read CLAUDE.md.
Run the full SDR pipeline:

STEP 1 — DISCOVERY
Read prompts/prospect_finder.md.
Find today's prospects via the connected MCP tool.
Do NOT enrich contacts at this stage.
Save raw list to data/prospects/[today's date].json.
Print: source used, found, filtered.

STEP 2 — SIGNAL DETECTION
Read prompts/signal_detector.md.
For each prospect, search the web for buying signals.
Score against the Intent Signals defined in CLAUDE.md.
Save enriched data to data/enriched/[date]/.
Produce contact_now.json, contact_this_week.json, monitor.json.
Print: N now / N this week / N monitor.

STEP 3 — APOLLO ENRICHMENT
For each prospect in contact_now.json and contact_this_week.json only:
Run apollo_people_match to reveal full name and email.
Update their record with: last_name, email, linkedin_url.
Do not enrich anyone in monitor.json — skip them entirely.
Print: N enriched, N skipped (monitor).

STEP 4 — DRAFT GENERATION
Read prompts/message_writer.md.
For each enriched prospect from Step 3, write a personalised message
using their signal data.
Save drafts to data/drafts/[date]/.
Print: N drafts, N flagged.

STEP 5 — DELIVER DIGEST
Run: python3 src/email_digest.py --date [today]
Confirm digest delivered to EMAIL_RECIPIENT in .env.

STEP 6 — LOG TO CRM (skip if no CRM connected)
For each prospect that received a draft today, create or update a
contact record in HubSpot or Salesforce via MCP:
- Set status: "Outreach Pending"
- Add note: signal detected, message format (LinkedIn DM or email),
  draft date
- Do not create duplicate records — update if contact already exists

If any step fails, fix it once and retry.
Print a final summary when done:

  Source: [connector used]
  Prospects: [N found] → [N after filter]
  Signals: [N now] / [N this week] / [N monitor]
  Enriched: [N enriched] / [N skipped]
  Drafts: [N total] ([N flagged])
  CRM: [N contacts logged] (or "skipped — no CRM connected")
  Digest: sent to [email] at [time]
