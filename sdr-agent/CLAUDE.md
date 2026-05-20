# SDR Agent — Master Context

## Company

Brighterway is an AI platform that handles the full medical record review pipeline for workers' comp and med-legal work. It is not just a filter. Here is what it actually does:

1. **Organizes and deduplicates** disorganized medical records (usually large PDF batches)
2. **Filters out 80% of irrelevant records**, surfacing only what is relevant to the physician's specialty
3. **Generates AI summaries** of the relevant records, reviewed by human medical experts for accuracy
4. **Lets physicians write reports directly in the platform** — summaries sit side-by-side with original documents in an editable view (like Google Docs), so physicians never leave the page to draft their report
5. **Analytics** across the full record pipeline
6. **Searchable by body part, document type, or keyword** (e.g. "Ankle," "Clinical Notes") in seconds

It is cheaper than other AI tools doing this. The output quality is better than other AI startups in this space. It replaces or reduces the need for offshore medical record reviewers.

The people buying it are not physicians. They are the operations people who manage the flow of cases to physicians.

---

## Ideal Customer Profile

### Who to target

**Primary:** QME and IME management companies that coordinate records across 10 or more physicians. These companies sit between the insurance carriers or attorneys and the doctors. They handle scheduling, record retrieval, and the full evaluation pipeline. Volume comes from the network they manage, not how many people they employ.

**Secondary:** Third-Party Administrators (TPAs) focused primarily on workers' comp, with annual revenue between $1M and $50M. These are mid-size TPAs large enough to have dedicated vendor management but small enough that they're still making cost-driven decisions. They buy medical evaluation services from vendors and care deeply about turnaround time, report quality, and cost per claim.

**Also works:** These verticals are proven by existing clients:
- Med-legal and forensic evaluation companies (e.g. forensic IMEs, expert witness review firms)
- Specialty med-legal practices doing evaluation work — orthopedics, pain management, rehabilitation, dental QMEs

**Geography:** California first — QME is a California-specific regulatory designation. Secondary: New York, Texas, Florida (high workers' comp volume states).

**Decision makers:**
- IME/QME companies → Owner, Head of Operations, Workers' Comp Manager
- TPAs → Claims Manager, Head of Vendor Services, Vendor Relations Director

**Minimum bar:** Managing QME/IME work for 10+ physicians. Below that, the economics don't work for us or them.

### Who to skip

- Solo physicians with no management layer
- General hospitals, health systems, urgent care clinics
- Law firms (they receive reports; they don't review records)
- Companies where the only decision maker is a physician with no ops staff

---

## Intent Signals

| Signal | Tier | Why it matters for us |
|---|---|---|
| Currently using an AI medical record platform | High | Budget is proven and they already believe in the category — sell on better output and lower price |
| Using offshore staff for record review | High | They have a recurring cost we can undercut today; no education needed on why the problem is real |
| Hiring for medical record reviewer or IME coordinator roles | High | Case volume is growing faster than their current process handles — they're feeling it right now |
| Recently added new physicians or specialties to their panel | Medium | More physicians means more record volume means the pain gets worse from here |
| Hiring for operations or admin roles in a QME/IME context | Medium | Process strain is showing up in headcount even when it's not record-specific |

---

## Message Rules

1. Lead with price. "Cheaper for QME work" is the fastest door-opener with ops buyers who are already spending money on this problem.
2. If they use offshore staff, make the comparison explicit. They know exactly what it costs them per case. We don't need to explain the problem — just say we're cheaper and the quality doesn't slip.
3. If they already use an AI platform, don't name it. Say our output is better and offer to show them a side-by-side.
4. Write under 75 words. These people manage high case volume all day. They delete long emails.
5. Reference something specific — their company name in context, the state they operate in, or their specialty mix if known.
6. Never use: "AI-powered," "streamline," "revolutionize," "cutting-edge," "solution," "leverage," or "excited to connect."
7. One CTA only — a 15-minute call or a demo. Not both. Not "let me know if you have questions."
8. Write like a person who knows the workers' comp space, not a vendor who just learned what a QME is.

---

## Prospect Query

**Tool: Apollo.io**

### People filters

**Job titles — include any of:**
- Owner
- Head of Operations
- Director of Operations
- Workers Compensation Manager
- QME Manager
- IME Manager
- IME Coordinator (only where company size suggests a management role)
- Claims Manager
- Vendor Services Manager
- Vendor Relations Manager
- Director of Vendor Services

**Exclude titles containing:**
- Physician, Doctor, MD, DO (unless combined with Owner or Director)
- Nurse, Therapist, Technician
- Attorney, Paralegal, Legal

---

### Company filters

**Keywords — company name or description must match at least one:**
- "independent medical evaluation"
- "IME"
- "QME"
- "qualified medical evaluator"
- "medical legal"
- "workers compensation evaluation"
- "workers comp evaluation"
- "medical evaluation"

**Industries:**
- Medical Practice
- Hospital & Health Care *(use only with keyword filter above to avoid hospitals)*
- Insurance *(TPA angle — pair with workers' comp keyword)*

**Headcount:** 10–500 employees
*(Exclude solos. Large networks like ExamWorks and Leidos QTC are already known accounts.)*

**Geography:** United States — filter California first, then NY, TX, FL

---

### Exclusion filters

- Company name contains: "hospital," "urgent care," "emergency," "hospice," "pharmacy"
- Industry is: Pharmaceuticals, Biotechnology, Medical Device (not the right vertical)

---

### Apollo search sequence

**Run 1 — QME/IME companies (primary ICP):**
1. Title search against QME/IME keyword companies in California, headcount 10–200
2. Export to `data/prospects/` as CSV with: name, title, company, email, LinkedIn URL, employee count, state
3. Flag any company already in current client list as duplicate and skip

**Run 2 — TPA companies (secondary ICP):**
1. Use these additional filters on top of the base people filters:
   - Company keywords: "third party administrator," "TPA," "workers compensation claims," "claims administration," "workers comp TPA"
   - Industry: Insurance
   - Estimated revenue: $1M–$50M
   - Headcount: 10–250 employees
   - Geography: United States (workers' comp is regulated by state — prioritize CA, TX, NY, FL)
2. Target titles: Claims Manager, Director of Claims, Head of Vendor Services, Vendor Relations Manager, Owner
3. Export to same `data/prospects/` CSV with a `segment` column set to `TPA`
