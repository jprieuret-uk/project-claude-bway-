You are the discovery engine for an SDR agent.

Read CLAUDE.md. Use the "Prospect Query" section to run discovery
with whichever tool is connected.

Steps:
1. Read the Prospect Query from CLAUDE.md — it contains the exact
   parameters to use with the connected tool
2. If Apollo is connected: call Apollo MCP with those parameters
3. If Clay is connected: call Clay MCP with those parameters
4. If neither is connected: check data/prospects/ for a CSV file
   loaded manually, parse it, and proceed from there
5. Print which source was used before continuing
6. Request 30-50 prospects per run
7. For each prospect returned, extract:
   first_name, last_name, title, company, employee_count,
   linkedin_url, email, source_id
8. Filter out any prospect matching the "Who to skip" criteria
   in CLAUDE.md
9. If Clay is connected and wasn't used for discovery, call it now
   to enrich each prospect with: funding history, recent headcount
   changes, tech stack, key leadership hires in the last 90 days
10. If HubSpot or Salesforce is connected, check whether each prospect
    already exists in the CRM — skip anyone already in active sequences
11. Save the final list to data/prospects/[date].json
12. Return a summary: source used, prospects found, filtered out,
    enriched (if applicable), skipped as existing CRM contacts
