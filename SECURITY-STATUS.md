# SECURITY STATUS: INACTIVE (classified 2026-11-09)

On 2026-11-09, Shannon Gray classified this repository as **inactive** for his own work. This is Shannon Gray's classification of his own use of the project. It is not an independent assessment of whether the code is maintained.

It **has known, unfixed security vulnerabilities** in its dependencies. Sentry's scan of 2026-11-09 (OSV, GitHub Advisory Database via OSV, CISA KEV) recorded 443 open advisories against this repository's default branch: 20 critical, 146 high, 181 medium, 41 low, 53 unknown, 2 none; 2 are on the CISA Known Exploited Vulnerabilities list.

Most serious (up to 5):

- starlette 0.38.5 (PyPI): GHSA-86qp-5c8j-p5mr / CVE-2026-48710, severity medium, CISA KEV (actively exploited); fixed in 1.0.1
- starlette 0.38.5 (PyPI): PYSEC-2026-161 / CVE-2026-48710, severity unknown, CISA KEV (actively exploited); fixed in 1.0.1
- langchain-experimental 0.3.0 (PyPI): GHSA-p2qj-r53j-h3xj / CVE-2024-46946, severity critical; fixed in no fix listed
- langchain-experimental 0.3.0 (PyPI): PYSEC-2026-374 / CVE-2024-46946, severity critical; fixed in no fix listed
- langchain-core 0.2.3 (PyPI): GHSA-c67j-w6g6-q2cm / CVE-2025-68664, severity critical; fixed in 1.2.5, 0.3.81

## Retained findings

Known findings for this repository are kept on record (Sentry's parked-findings list) and are not deleted while it is inactive.

## Before work resumes

1. Review the recorded findings and re-scan for newer advisories.
2. Remediate: update affected dependencies to fixed versions.
3. Test the project after the updates.
4. Then update or remove this file.

## Alerts while inactive

While this repository is inactive, Shannon gets a security alert only for **confirmed active exploitation**: a listing in the CISA Known Exploited Vulnerabilities catalog, OR reliable evidence of in-the-wild exploitation from another source (with source, URL and date). A public proof-of-concept or exploit code alone is not enough. Other advisories are kept on record without an alert.

## About this file

This file is a notice only. Placing it here does not guarantee that every person or tool reading the repository will see it. It does not replace or change any existing security policy. This repository does not include a SECURITY.md or another security-policy file, so this notice does not link to one.
