# DPDP Act, 2023 Alignment — Orbit (Module 5)

## Purpose
This document maps Orbit's data-handling design to core principles of India's Digital Personal Data Protection (DPDP) Act, 2023, given that Orbit collects personal and financial data from rural micro-entrepreneurs via a voice interface.

## Data Minimization
Orbit only collects fields directly required to compute the HLDI score and generate a DPR: business type, location, capital, expenses, trade skill, and language preference. No unrelated personal data (e.g. family details, unrelated financial history) is captured.

## Purpose Limitation
Collected data is used strictly for: (1) computing the HLDI score, (2) generating a scheme-matched DPR, and (3) officer review/approval. Data is not repurposed for unrelated analytics without further consent design.

## Consent (Voice Interface)
Since onboarding happens via spoken conversation rather than a written form, consent must be captured verbally at the start of the flow — a short spoken disclosure (in the user's dialect) explaining what data is collected and why, before any data capture begins. This is a requirement for Module 3 (citizen app) to implement, coordinated with Module 5's data classification rules.

## Storage Limitation & Security
Sensitive fields (capital, expenses) are encrypted at rest, both on-device and in the backend database. Data in transit is protected via TLS. Access is restricted through officer role-based access control, with all reads/writes logged.

## Data Principal Rights (Residual Considerations)
This prototype does not yet implement a self-service data deletion/correction flow for entrepreneurs. In a production system, an entrepreneur would need a way to request review, correction, or deletion of their stored profile — noted here as a known gap for future work, not resolved in this hackathon build.