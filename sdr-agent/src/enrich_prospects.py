# Calls Apollo people/match for every prospect in contact_now and contact_this_week.
# Writes first_name, last_name, email, and linkedin_url back into each draft file.
# Safe to re-run — skips any prospect already enriched.

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests is not installed. Run: pip install requests")
    sys.exit(1)


ROOT = Path(__file__).parent.parent
APOLLO_MATCH_URL = "https://api.apollo.io/v1/people/match"


def load_env():
    env = {}
    env_path = ROOT / ".env"
    if not env_path.exists():
        return env
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip()
    return env


def already_enriched(prospect):
    return bool(prospect.get("email") or prospect.get("linkedin_url"))


def apollo_match(first_name, company, title, api_key):
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "first_name": first_name,
        "organization_name": company,
        "title": title,
        "reveal_personal_emails": False,
        "reveal_phone_number": False,
    }
    resp = requests.post(APOLLO_MATCH_URL, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    person = data.get("person") or {}
    return {
        "first_name": person.get("first_name", first_name),
        "last_name": person.get("last_name"),
        "email": person.get("email"),
        "linkedin_url": person.get("linkedin_url"),
    }


def load_bucket(enriched_dir, filename):
    path = enriched_dir / filename
    if not path.exists():
        return []
    return json.loads(path.read_text())


def find_draft(drafts_dir, company):
    company_slug = company.lower().replace(" ", "_").replace("-", "_")
    for f in drafts_dir.glob("*.json"):
        if company_slug in f.stem or f.stem in company_slug:
            return f
    # fallback: match by company field inside the file
    for f in drafts_dir.glob("*.json"):
        data = json.loads(f.read_text())
        if data.get("prospect", {}).get("company", "").lower() == company.lower():
            return f
    return None


def main():
    parser = argparse.ArgumentParser(description="Enrich prospects via Apollo people/match.")
    parser.add_argument("--date", default=str(date.today()), help="Date to process (YYYY-MM-DD)")
    args = parser.parse_args()

    date_str = args.date
    env = load_env()
    api_key = env.get("APOLLO_API_KEY")

    if not api_key:
        print("APOLLO_API_KEY not set in .env — cannot run enrichment.")
        sys.exit(1)

    enriched_dir = ROOT / "data" / "enriched" / date_str
    drafts_dir = ROOT / "data" / "drafts" / date_str

    if not drafts_dir.exists():
        print(f"No drafts directory for {date_str}. Run message_writer first.")
        sys.exit(1)

    prospects = (
        load_bucket(enriched_dir, "contact_now.json")
        + load_bucket(enriched_dir, "contact_this_week.json")
    )

    if not prospects:
        print(f"No prospects to enrich for {date_str}.")
        sys.exit(0)

    print(f"Enriching {len(prospects)} prospect(s) for {date_str}...")

    enriched_count = 0
    skipped_count = 0

    for entry in prospects:
        company = entry.get("company", "")
        draft_file = find_draft(drafts_dir, company)

        if not draft_file:
            print(f"  [!] No draft found for {company} — skipping.")
            continue

        draft = json.loads(draft_file.read_text())
        prospect = draft.get("prospect", {})

        if already_enriched(prospect):
            print(f"  [skip] {company} already enriched.")
            skipped_count += 1
            continue

        first_name = prospect.get("first_name", "")
        title = prospect.get("title", "")

        print(f"  Matching {first_name} at {company}...")
        try:
            result = apollo_match(first_name, company, title, api_key)
        except Exception as e:
            print(f"  [error] Apollo match failed for {company}: {e}")
            continue

        prospect.update({k: v for k, v in result.items() if v})
        draft["prospect"] = prospect
        draft_file.write_text(json.dumps(draft, indent=2))

        email_display = result.get("email") or "no email returned"
        last_name = result.get("last_name") or ""
        print(f"  {first_name} {last_name} — {email_display}")
        enriched_count += 1

        time.sleep(0.5)

    print(f"\nDone. {enriched_count} enriched, {skipped_count} skipped.")


if __name__ == "__main__":
    main()
