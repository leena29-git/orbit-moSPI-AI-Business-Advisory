# Lightweight Threat Model — Orbit (Module 5)

## Purpose
This document outlines Orbit's key offline-first risk profile and the mitigations built into the current prototype.

## Threat 1: Device Loss or Theft
**Risk:** A lost/stolen device could expose an entrepreneur's full financial profile stored locally.
**Mitigation:** Sensitive fields (capital_available, expenses) are encrypted before storage using Fernet symmetric encryption. In a production build, the encryption key itself would be stored in the device's secure hardware keystore (Android Keystore / iOS Secure Enclave) rather than in a plaintext .env file, as used in this prototype.

## Threat 2: Insecure Network at Sync Time
**Risk:** Rural connectivity often means unsecured public/shared networks, exposing data in transit during sync.
**Mitigation:** All API/sync traffic is served over TLS (HTTPS), verified in this prototype via a self-signed certificate on port 8443.

## Threat 3: Officer Over-Access
**Risk:** An officer could view or modify data beyond their assigned responsibility (e.g. a viewer approving DPRs, or an unauthorized party accessing sensitive fields).
**Mitigation:** Role-based access control (viewer / approver / admin) is enforced at the API layer via `require_role()`. Verified in testing: a `viewer`-role officer received a 403 Forbidden when attempting to create a profile, while retaining read access.

## Threat 4: Interrupted or Partial Sync
**Risk:** A sync interrupted mid-transfer (common in low-connectivity rural areas) could leave partial or corrupted records.
**Mitigation:** Records use a stable `profile_id` as primary key, allowing safe upsert-based retry logic rather than duplicate/corrupted inserts. Full conflict-resolution protocol design is a coordination point with Module 1 (backend/sync owner) — not fully implemented in this prototype.

## Residual Risks (Not Yet Mitigated)
- Encryption key currently lives in a local `.env` file rather than a hardware-backed keystore — acceptable for hackathon demo, not production-ready.
- No automated key-rotation policy.
- No rate-limiting on login attempts (brute-force risk on officer accounts).