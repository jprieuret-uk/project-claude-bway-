# Compiles enriched prospect data and drafted messages into a daily email digest.

import argparse
import json
import smtplib
import sys
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


ROOT = Path(__file__).parent.parent


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


def validate_draft(data, slug):
    message = data.get("message", "")
    if "—" in message:
        data["flag_for_review"] = True
        existing = data.get("flag_reason") or ""
        em_dash_note = "Em dash found in message copy. Rewrite before sending."
        data["flag_reason"] = f"{existing} | {em_dash_note}".lstrip(" |") if existing else em_dash_note
        print(f"  [!] Em dash detected in {slug} — auto-flagged.")
    return data


def load_drafts(date_str):
    drafts_dir = ROOT / "data" / "drafts" / date_str
    if not drafts_dir.exists():
        print(f"No drafts directory found for {date_str}.")
        sys.exit(1)
    drafts = []
    for f in sorted(drafts_dir.glob("*.json")):
        data = json.loads(f.read_text())
        data["_slug"] = f.stem
        data = validate_draft(data, f.stem)
        drafts.append(data)
    if not drafts:
        print(f"No drafts found for {date_str}.")
        sys.exit(0)
    return drafts


def load_timing(date_str):
    enriched_dir = ROOT / "data" / "enriched" / date_str
    timing = {}
    for bucket, recommendation in [("contact_now.json", "contact_now"), ("contact_this_week.json", "contact_this_week")]:
        path = enriched_dir / bucket
        if path.exists():
            for entry in json.loads(path.read_text()):
                key = entry.get("company", "").lower()
                timing[key] = {
                    "timing_score": entry.get("timing_score", 0),
                    "recommendation": recommendation,
                }
    return timing


def sort_key(draft, timing):
    company = draft.get("prospect", {}).get("company", "").lower()
    t = timing.get(company, {})
    flagged = draft.get("flag_for_review", False)
    rec = t.get("recommendation", "contact_this_week")
    score = t.get("timing_score", 0)
    rec_order = 0 if flagged else (1 if rec == "contact_now" else 2)
    return (rec_order, -score)


def badge(text, bg, color):
    return (
        f'<span style="background:{bg};color:{color};padding:3px 9px;'
        f'border-radius:4px;font-size:11px;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:0.4px">{text}</span>'
    )


def build_card(draft, timing):
    prospect = draft.get("prospect", {})
    first_name = prospect.get("first_name", "")
    last_name = prospect.get("last_name", "")
    name = f"{first_name} {last_name}".strip() if last_name and last_name.upper() != "OBFUSCATED" else first_name
    title = prospect.get("title", "")
    company = prospect.get("company", "")
    company_key = company.lower()

    t = timing.get(company_key, {})
    rec = t.get("recommendation", "contact_this_week")
    score = t.get("timing_score", "")

    flagged = draft.get("flag_for_review", False)
    flag_reason = draft.get("flag_reason") or ""
    fmt = draft.get("format", "")
    subject = draft.get("subject_line")
    greeting = f"Hi {first_name},<br><br>" if first_name else ""
    message = greeting + draft.get("message", "").replace("\n", "<br>")
    signal = draft.get("signal_referenced", "")
    word_count = draft.get("word_count", "")

    if flagged:
        status = badge("&#9873; Flagged", "#ffebe9", "#cf222e")
    elif rec == "contact_now":
        status = badge("Contact today", "#dafbe1", "#1a7f37")
    else:
        status = badge("This week", "#fff8c5", "#9a6700")

    flag_block = ""
    if flagged and flag_reason:
        flag_block = (
            f'<div style="background:#ffebe9;border-left:3px solid #cf222e;'
            f'padding:8px 12px;margin:10px 0;font-size:13px;color:#cf222e">'
            f'<strong>Flag:</strong> {flag_reason}</div>'
        )

    subject_block = ""
    if fmt == "email" and subject:
        subject_block = (
            f'<div style="font-size:12px;color:#57606a;margin-bottom:6px">'
            f'<strong>Subject:</strong> {subject}</div>'
        )

    format_label = "LinkedIn DM" if fmt == "linkedin_dm" else "Email"

    email = prospect.get("email")
    linkedin_url = prospect.get("linkedin_url")

    if fmt == "linkedin_dm" and linkedin_url:
        send_to_block = (
            f'<div style="font-size:12px;margin-bottom:6px">'
            f'<strong style="color:#57606a">Send to:</strong> '
            f'<a href="{linkedin_url}" style="color:#0969da">{linkedin_url}</a></div>'
        )
    elif fmt == "email" and email:
        send_to_block = (
            f'<div style="font-size:12px;color:#57606a;margin-bottom:6px">'
            f'<strong>Send to:</strong> '
            f'<a href="mailto:{email}" style="color:#0969da">{email}</a></div>'
        )
    else:
        send_to_block = (
            f'<div style="font-size:12px;color:#cf222e;margin-bottom:6px">'
            f'<strong>Send to:</strong> not enriched yet — run apollo_people_match</div>'
        )

    return f"""
<div style="border:1px solid #d0d7de;border-radius:8px;padding:20px;
            margin-bottom:20px;background:#ffffff;font-family:-apple-system,sans-serif">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
    <div>
      <div style="font-size:16px;font-weight:600;color:#1f2328">{name} &mdash; {company}</div>
      <div style="font-size:13px;color:#57606a;margin-top:2px">{title}</div>
    </div>
    <div style="text-align:right;flex-shrink:0;margin-left:16px">
      {status}
      <div style="font-size:11px;color:#888;margin-top:5px">Score: {score}/10</div>
    </div>
  </div>
  {flag_block}
  <div style="font-size:12px;color:#57606a;margin-bottom:8px">
    <strong>Signal:</strong> {signal}
  </div>
  <div style="font-size:12px;color:#57606a;margin-bottom:6px">
    <strong>Format:</strong> {format_label}
  </div>
  {send_to_block}
  {subject_block}
  <div style="background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;
              padding:14px;font-size:14px;line-height:1.65;color:#1f2328;
              white-space:pre-wrap;cursor:text">{message}</div>
  <div style="font-size:11px;color:#888;margin-top:8px;text-align:right">
    {word_count} words
  </div>
</div>"""


def build_html(drafts, timing, date_str):
    n_today = sum(
        1 for d in drafts
        if not d.get("flag_for_review")
        and timing.get(d.get("prospect", {}).get("company", "").lower(), {}).get("recommendation") == "contact_now"
    )
    n_week = sum(
        1 for d in drafts
        if not d.get("flag_for_review")
        and timing.get(d.get("prospect", {}).get("company", "").lower(), {}).get("recommendation") == "contact_this_week"
    )
    n_flagged = sum(1 for d in drafts if d.get("flag_for_review"))
    n_total = len(drafts)

    cards = "\n".join(build_card(d, timing) for d in drafts)

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<title>SDR Digest {date_str}</title>
</head>
<body style="background:#f6f8fa;padding:32px 16px;margin:0;font-family:-apple-system,sans-serif">
  <div style="max-width:660px;margin:0 auto">
    <div style="margin-bottom:28px">
      <h1 style="font-size:22px;font-weight:700;color:#1f2328;margin:0 0 6px">
        SDR Digest &mdash; {date_str}
      </h1>
      <p style="font-size:14px;color:#57606a;margin:0">
        {n_total} draft{"s" if n_total != 1 else ""} ready for review
      </p>
    </div>
    {cards}
    <div style="border-top:1px solid #d0d7de;padding-top:16px;margin-top:4px;
                font-size:13px;color:#57606a;text-align:center;line-height:2">
      {n_today} today &nbsp;|&nbsp; {n_week} this week &nbsp;|&nbsp; {n_flagged} flagged
      <br>
      Nothing has been sent. Review each message and send manually
      from your LinkedIn or email account.
    </div>
  </div>
</body>
</html>"""


def send_email(html, subject, env):
    sender = env["EMAIL_SENDER"]
    password = env["EMAIL_PASSWORD"]
    recipients = [r.strip() for r in env["EMAIL_RECIPIENT"].split(",") if r.strip()]
    smtp_host = env.get("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(env.get("EMAIL_SMTP_PORT", 587))

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())


def main():
    parser = argparse.ArgumentParser(description="Build and send the daily SDR digest.")
    parser.add_argument("--date", default=str(date.today()), help="Date to process (YYYY-MM-DD)")
    args = parser.parse_args()

    date_str = args.date
    env = load_env()

    print(f"Loading drafts for {date_str}...")
    drafts = load_drafts(date_str)
    timing = load_timing(date_str)
    drafts = sorted(drafts, key=lambda d: sort_key(d, timing))

    n = len(drafts)
    n_flagged = sum(1 for d in drafts if d.get("flag_for_review"))
    print(f"Found {n} draft(s), {n_flagged} flagged. Building digest...")

    subject = f"SDR Digest — {date_str} — {n} draft{'s' if n != 1 else ''} ready"
    html = build_html(drafts, timing, date_str)

    sender = env.get("EMAIL_SENDER")
    password = env.get("EMAIL_PASSWORD")
    recipient = env.get("EMAIL_RECIPIENT")

    if sender and password and recipient:
        try:
            send_email(html, subject, env)
            print(f"Sent to {recipient}.")
        except Exception as e:
            print(f"Send failed: {e}")
            print("Saving as HTML instead...")
            out = ROOT / "data" / f"digest_{date_str}.html"
            out.write_text(html)
            print(f"Saved to {out}")
    else:
        out = ROOT / "data" / f"digest_{date_str}.html"
        out.write_text(html)
        print(f"Email not configured. Saved to {out}")


if __name__ == "__main__":
    main()
