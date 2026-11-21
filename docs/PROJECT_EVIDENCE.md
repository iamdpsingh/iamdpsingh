# Project evidence and scope

These are the owner-supplied, dated project records. OBSERVED, IMPLEMENTED, and REPORTED
retain the meanings and limitations supplied by the owner. This profile update does not
rerun the historical test suites, restore drills, production workloads, or provider gates.

The Rolewisp website could not be read by the web verification tool during this update;
its URL is retained as supplied, without asserting present availability. The supplied
Immune System source files were inspected: the diagnosis client is heuristic, the risk
agent has explicit safety boundaries, and all five domain job families are present.

## Rolewisp

**V-INDEX / Rolewisp — Source-Backed Job Data Platform**

Activity observed: 5–21 November 2026.

Stack: Python, FastAPI, PostgreSQL, SQLAlchemy, Redis, Next.js, GitHub Actions.

### V1 — OBSERVED / IMPLEMENTED

Delivered native job-source coverage across 71 of 78 target platforms (91.0%), by implementing platform-specific collectors, shared normalization, provenance tracking, and independently live-verified examples.

**Scope and limits:** Seven platform requirements remained unmet; 91.0% is platform coverage, not project completion or reliability.

### V2 — OBSERVED

Built a searchable hosted index containing 9,187 jobs at the 21 November review, by running a persistent indexing worker across 142 registered sources, 130 of which had completed an initial successful collection.

**Scope and limits:** Dated snapshot, not a current live count or a sustained-throughput result; 12 sources still lacked initial success.

### V3 — IMPLEMENTED

Implemented conservative job-closure handling requiring two complete-enumeration misses at least 24 hours apart, by retaining source observations and rejecting incomplete batches before index mutation.

**Scope and limits:** Closure-policy scope; no measured false-closure reduction is claimed.

### V4 — OBSERVED

Verified recoverability of all 16 database tables with matching row counts in a recorded restore drill, by restoring a 42,387,200-byte encrypted production snapshot into an isolated PostgreSQL instance.

**Scope and limits:** The drill did not mutate production; independent recovery-key custody and deletion reconciliation were still open.

### V5 — IMPLEMENTED / OBSERVED

Delivered private workspaces for two account roles, Candidate and Employer, by implementing ownership checks, protected profile/resume operations, hashed session tokens, and Redis-backed credential rate limits.

**Scope and limits:** Hosted ownership checks are documented; live email/OAuth provider activation remained a separate gate.

### V6 — REPORTED

Established regression coverage with 1,269 passing backend tests and one skip in the final recorded cleanup run, by testing source collectors, lifecycle rules, account isolation, and PostgreSQL/Redis integrations.

**Scope and limits:** Final cleanup revision; earlier totals of 1,244, 1,249, and 1,272 refer to different revisions and must not be added together.

### Sources

- [Application (1)](https://rolewisp.vercel.app/)

## Data Pipeline Immune System

**Data Pipeline Immune System — Multi-Agent Data Reliability**

Activity observed: 23–28 October 2026 (authored default-branch activity).

Stack: Python, PySpark, BigQuery, Cloud Storage, Airflow, Cloud Run, Terraform.

### D1 — IMPLEMENTED

Delivered a six-agent pipeline-recovery workflow, by separating detection, diagnosis, risk assessment, remediation, verification, and learning behind explicit action policies and human-escalation gates.

**Scope and limits:** Agent count measures implemented responsibilities; the current diagnosis client is heuristic, not a verified live LLM integration.

### D2 — IMPLEMENTED

Added recovery-scenario coverage for four failure types, by injecting timeouts, corrupted records, volume drops, and additive schema drift into a controlled simulation harness with quarantine and verification paths.

**Scope and limits:** Scenario coverage, not proof of four production incidents resolved or a universal recovery-success rate.

### D3 — IMPLEMENTED

Added Bronze/Silver processing jobs for five business domains, by implementing PySpark ingestion and transformation modules for orders, customers, payments, inventory, and shipments.

**Scope and limits:** Five domain families are present in the codebase; this is not a measured processed-row count.

### D4 — IMPLEMENTED

Implemented a five-factor pipeline-health score, by combining reliability, freshness, data quality, schema stability, and SLA compliance into a weighted operational indicator.

**Scope and limits:** The factors are weighted 30%, 20%, 20%, 15%, and 15%; the formula does not establish achieved SLA compliance.

### D5 — IMPLEMENTED

Added two operational notification cadences, hourly Telegram summaries and six-hour email briefings, by implementing a reporting daemon and timeout/retry handling for external notification and BigQuery calls.

**Scope and limits:** Configured schedules and error-handling work; no measured alert-delivery or downtime improvement is claimed.

### Sources

- [Data-Pipeline-Immune-System (1)](https://github.com/iamdpsingh/Data-Pipeline-Immune-System)
- [diagnosis_agent.py (2)](https://github.com/iamdpsingh/Data-Pipeline-Immune-System/blob/main/agents/diagnosis_agent.py)
- [risk_agent.py (3)](https://github.com/iamdpsingh/Data-Pipeline-Immune-System/blob/main/agents/risk_agent.py)
- [llm_client.py (4)](https://github.com/iamdpsingh/Data-Pipeline-Immune-System/blob/main/src/diagnosis/llm_client.py)
- [run_5_day_simulation.py (5)](https://github.com/iamdpsingh/Data-Pipeline-Immune-System/blob/main/scripts/run_5_day_simulation.py)
- [jobs (6)](https://github.com/iamdpsingh/Data-Pipeline-Immune-System/tree/main/spark/jobs)
