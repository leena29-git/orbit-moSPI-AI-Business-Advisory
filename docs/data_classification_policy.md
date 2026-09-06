# Data Classification Policy — Orbit (Module 5)

## Purpose
This document defines which data fields handled by Orbit are sensitive and require encryption or restricted access, versus fields that are safe to store or display in plaintext.

## Classification Levels

| Level | Definition | Handling Rule |
|---|---|---|
| **Sensitive** | Financial figures, identity-linked details, or data that could harm an entrepreneur if leaked | Must be encrypted at rest, access-logged, and restricted by role |
| **Non-sensitive** | Aggregated statistics, scores, or location codes with no individual identity link | Can be stored/displayed in plaintext |

## Field-Level Classification

| Field | Table | Classification | Handling |
|---|---|---|---|
| capital_available | profiles | Sensitive | Encrypted (Fernet) before storage |
| expenses | profiles | Sensitive | Encrypted (Fernet) before storage |
| trade_skill | profiles | Sensitive (identity-adjacent) | Currently plaintext — candidate for encryption in future iteration |
| language_dialect | profiles | Non-sensitive | Plaintext (no individual harm if exposed) |
| district_id / block_id | profiles | Non-sensitive | Plaintext (used for aggregation, not identity) |
| business_type | profiles | Non-sensitive | Plaintext |
| hldi_score | HLDI output | Non-sensitive | Plaintext, used in officer dashboard |
| matched_scheme | dpr_records | Non-sensitive | Plaintext |
| dpr status / reviewer | dpr_records | Sensitive (audit-relevant) | Access-logged via audit_logs |
| officer credentials | officers | Sensitive | Password hashed (bcrypt), never stored or transmitted in plaintext |

## Access Rule Summary
- Sensitive fields are only ever decrypted server-side, on request, by an authenticated officer.
- Every read or write to a profile or DPR record is recorded in the audit log with actor identity and role.
- Officer roles (`viewer`, `approver`, `admin`) determine which actions are permitted, per the RBAC implementation in `app/security/auth.py`.