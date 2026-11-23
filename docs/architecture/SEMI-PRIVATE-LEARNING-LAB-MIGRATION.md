# Semi-private Learning Lab migration — architecture and implementation plan

**Status:** Owner direction recorded; architecture under review; **no production cutover authorized**.  
**Date:** 2026-11-23  
**Scope:** Entire RHHanson-UMD Learning Lab ecosystem, not only ENEE 641.  
**Canonical coordination:** Main/shared-infrastructure repository and chat. Course implementations remain in their own repositories.

## Owner-approved requirements

1. Keep the Learning Lab public and discoverable, including general-purpose mathematics, engineering, programming, resource listings, and original course-independent interactive lessons.
2. Restrict **course-specific** lesson sites, exam preparation, and other course-specific derivatives to individually approved members. Technical access does **not** establish academic redistribution rights.
3. Use **one membership for the entire protected Learning Lab**: membership approved once grants access to ENEE 620, ENEE 630, ENEE 641 and subsequently enrolled protected course sites, until revoked. Authentication sessions can expire without expiring membership.
4. **Zero University of Maryland IT involvement**. No UMD CAS/SAML/OIDC application registration, university administrator consent, directory API, or UMD-managed integration. University email addresses may receive externally generated one-time email codes, without claiming to verify enrollment or affiliation.
5. Owner manually approves/denies access requests and can revoke access. Do not default to allowing every `@umd.edu` or `@terpmail.umd.edu` address.
6. Preserve independently owned course repositories, static HTML/CSS/JS, pure mathematical engines, accessibility, dark default plus persisted light theme, original-content standards, CI and security gates.
7. No production changes, repository visibility flips, deployment/workflow changes, or migrations before a separate explicit approval, with staged tests, rollback and reviewable PRs.

**Not yet owner-decided:** whether non-UMD addresses are eligible by exception; definitive hostname/domain; final form provider; whether the public-safe reusable lesson collection lives in the portal repo or its own public repo; final Cloudflare billing/plan after current pricing and limits are verified.

## Repository-by-repository target classification

| Repository | Target visibility (proposed) | Responsibility | Migration concern |
| --- | --- | --- | --- |
| `RHHanson-UMD.github.io` | Public | Public portal, searchable resources, public general lessons, course descriptions, request/sign-in links | Keep generator `content/courses.json` and `content/resources.json` authoritative; do not edit generated HTML directly |
| `learning-core` | Public for independently authored and rights-cleared general-purpose math | Tested shared pure algorithms; no private course source | Audit copied/vendored content and licensing; pin versions for consumers |
| `course-template` | Public if stripped of private course specifics | Generic accessible static site starter, publication checks and CI | Remove credentials/course sources; future protected-hosting configuration must not publish arbitrary draft content |
| `ENEE-620` | Private **after approved cutover** | Full protected course site | Preserve Gaussian conditioning demo, tests and workflows |
| `ENEE-630` | Private **after approved cutover** | Full protected course site | Preserve periodogram/spectral estimation demo, tests and workflows |
| `ENEE-641` | Private **after approved cutover** | Full protected course site including reviews, interactive labs and numerous mathematical engines/tests | Review all branches, public historical assets, deployment failure, content rights |
| Optional public-general-lessons repo | Proposal only | Standalone original cross-course visualizations | Avoid unnecessary repo duplication; decide after classification |

The portal and public general lessons should load anonymously. Course apps should not embed protected assets into public content. Publicized reusable math engines must contain only independently authorized material; a course-specific source-inspired example does not become public-safe by moving files.

## Proposed hosting and membership topology

- **Public**: existing GitHub Pages root portal, with general-purpose original lessons/Quick Reference and a professional course card linking to each protected app; preserve public search and references.
- **Protected**: independent Cloudflare Pages project per course, each built from its corresponding private GitHub repository (`site/` output, no framework rewrite). Cloudflare Pages + Cloudflare Access is a **candidate** pending account-level availability, current pricing, hostname/preview policy verification, and security acceptance tests.
- **Single membership**: centrally maintained exact-email Cloudflare Access Allow policy/group applied consistently to all protected production applications. One approval grants membership to all protected courses; preview deployments use owner/reviewer-only policy, **not** general membership.
- **Email verification without UMD IT**: Cloudflare One-Time PIN emailed to each allowlisted address. This proves mailbox possession, **not** UMD enrollment. Never configure a blanket UMD email-domain allow rule. Future external identity provider integration requires an explicit new decision; no CAS/SSO needed.
- **Request intake**: public access-request link to a private owner-controlled form (Google Forms is a candidate). Collect minimal identity/contact/reason; no student IDs, grades, uploads, course PDFs or confidential data. Send owner notification; document privacy notice and response retention. Approval means manually adding the verified email to Access policy; denial does not grant access.
- **Membership lifecycle**: requested -> pending -> approved/denied -> active -> revoked. Sessions can expire independently; revocation removes allowlist entry **and** invalidates active sessions/tokens, then tests loss of access.
- **No browser-only security**: protect complete deployed HTML/JS/CSS/JSON and file paths at the edge. A JavaScript sign-in overlay is insufficient.

## Security model and publication safety

**Assets to protect:** private source repos, course-specific site HTML and JavaScript, reviews and tests where they contain protected course-specific information, admin credentials and request records.

**Adversaries/failure modes:** anonymous visitors, unauthorized email addresses, formerly approved identities, leaked Access sessions, public Pages residual content, Cloudflare alternate project/preview/branch/deployment URLs, direct asset fetching, unreviewed CI publication, public Actions artifacts/logs, external source links and public Git-history copies.

Controls / release blockers:

1. Audit all current public branch refs, commit history, forks, releases, PRs, Actions artifacts/logs, Pages outputs, crawler/index links and nondefault branch deployments. Historic public availability cannot be undone by making a repository private; identify remediation needs rather than claiming retroactive secrecy.
2. Existing public URLs `/ENEE-620/`, `/ENEE-630/`, `/ENEE-641/` and old asset/review URLs must no longer serve protected data after cutover. Preserve a public, non-sensitive landing/redirect experience.
3. Enforce Access on production `pages.dev`, all deployment hash URLs, branch preview aliases and any custom domains. Test each separately in anonymous mode; do not assume one policy protects other hostnames. Never allow unauthorized direct retrieval of .js/.css/.html/.json.
4. Require exact-email membership, authentication, MFA on owner/admin account, least-privilege integration permissions, isolated preview policies, and explicit revocation procedure. Review session lifetime (proposed starting point: 24h) and cache policy.
5. Keep pinned GitHub Actions and explicit minimal token permissions; preserve Gitleaks, publication guard, independent math tests, source provenance checks and deployment verification. Branch protection/rulesets and required status checks require account/plan verification; no untrusted PR deployment secrets.
6. Never publish instructor PDFs, copyrighted figures, answer keys, restricted homework/solutions, student data, private Drive/ELMS URLs or credentials, whether in public or protected hosting, absent independently established rights and educational authorization. A released answer is not automatically licensed.
7. Keep backups and restore artifacts private. Do not use anonymous GitHub Pages as emergency fallback for private course content.
8. Inspect content classification by file and dependency; approved public-general material remains accessible even while protected course sites are migrated.

## Current-state evidence (historical audit checkpoint — recheck live before changes)

Read-only GitHub audit conducted 2026-11-20/23 identified **all six repositories public** and using `main`. The root portal contains `scripts/build.py`, `content/courses.json`, `content/resources.json`, `site/quick-reference.html`, source provenance checks, rights policy, publication gate, secret scanning and Pages workflows. ENEE-620 has a Gaussian-conditioning explorer/test; ENEE-630 has a periodogram explorer/test; ENEE-641 contains exam reviews and many mathematical visualizations/test files. `learning-core` has graph/subset-sum tests and versioning notes; `course-template` includes practice starter/tests and an existing Pages deploy workflow.

ENEE-641 latest inspected `main` commit was `5584f2576696a831aab11175ba7f993b88057d2b`. Its 2026-11-19 `main` math tests, secret scanning and publication guard passed, but GitHub Pages deployment run [44608605785](https://github.com/RHHanson-UMD/ENEE-641/actions/runs/44608605785) **failed at the deploy-pages step** after artifact upload; the earlier run [44606781072](https://github.com/RHHanson-UMD/ENEE-641/actions/runs/44606781072) succeeded. Do not conflate green tests with live deployment. At that checkpoint ENEE-641 had 17 branches and no open PRs. Full history scans, live browser inspection, branch protections, Cloudflare account configuration, and current billing/entitlements were **not** verified.

## Phased, reviewable migration

- [ ] **0 — Audit / freeze baseline:** Inventory all six repos, branches, Pages sites, URL paths, build outputs, workflows, permissions, current runs, logs/artifacts, history exposure, licensing and cross-repo links. Resolve ENEE-641 Pages failure's root cause separately; record existing public site hashes, back up privately.
- [ ] **1 — Classification / ADRs:** Tag each path/module as public-general, course-specific protected, excluded/restricted, or unresolved. Create architecture decision records, access/data-retention policy, threat model, deployment matrix, cost plan and acceptance checklist. Obtain architecture approval before infrastructure changes.
- [ ] **2 — ENEE-641 private pilot:** Prepare private repository/visibility transition strategy, protected Pages staging, least-privilege CI and exact-email Access policy without cutting over public site. Preserve all current site functions, tests and theme/keyboard behavior.
- [ ] **3 — Membership pilot:** Configure minimal private form + owner notifications, manual approvals, one-time PIN, persistent membership, no UMD IT, denial and revocation. Test owner-only previews versus member production.
- [ ] **4 — Security acceptance:** Independently test every hostname/asset, anonymous and unauthorized identities, approved users, expired sessions, revoked users, arbitrary deep links, caching, requests to old public paths, and public Actions/artifacts. Record HTTP/browser evidence. Fix before release.
- [ ] **5 — Authorized ENEE-641 cutover:** Only with separate explicit go/no-go approval: publish public landing/redirect, stop old public course-content deployments, change visibility/deployment as authorized, verify real public and protected endpoints, maintain private rollback.
- [ ] **6 — ENEE-620 and ENEE-630 migration:** Separate course-owned PRs and tests; same central member allowlist; independent staging/cutover approvals.
- [ ] **7 — Public/shared alignment:** Keep public portal and general-purpose engines, update approved course links via `content/courses.json` + generator, classify and relocate independent general topics, update `course-template` for safe defaults; coordinate changes in main shared-infrastructure chat.
- [ ] **8 — Operations:** Document onboarding, denial, email change, revocation + session invalidation, tests, backups, cost/build-budget thresholds, incident response, preview hygiene, future-course onboarding and emergency recovery. Check actual live state after each release.

## Release acceptance / fail-closed criteria

- [ ] Public homepage, general Quick Reference/resources/independent lessons remain accessible without login; all general-purpose navigation works.
- [ ] Every protected course production page and *all* static assets require authentication and membership on every hostname.
- [ ] Every preview/deployment/branch alias is denied to non-reviewers, including approved production members unless explicitly authorized for preview.
- [ ] Unapproved address denied; approved address receives email OTP and accesses all protected courses; expired session reauthenticates without membership loss; revoked user cannot continue using a current session.
- [ ] Public GitHub Pages old paths cannot retrieve protected material; paths must be checked by direct unauthenticated HTTP requests, not only UI navigation.
- [ ] Code/content classification, rights review, math tests and existing publication/secret-scanning gates pass.
- [ ] Theme persistence, responsiveness, keyboard focus, deep links, browser ES modules, mathematical interaction/reset and source attribution remain intact.
- [ ] CI cannot publish from untrusted pull requests or feature branches to member production; preview deployments are gated.
- [ ] Recovery release and protected backup tested; cross-course links and sign-in/request workflow verified in a real browser.
- [ ] Owner explicitly authorizes each production cutover after evidence is reviewed.

## Rollback

Before cutover: maintain existing public deployment and revert only staging resources; do not move live links or visibility. At/after cutover: maintain the **public landing** and an authenticated previous-good Cloudflare release / private build artifact. If protected service is unavailable, keep detailed content unavailable rather than restoring it to unrestricted GitHub Pages. Roll back the private release, recheck Access rules on all hostnames, and repeat unauthorized access/revocation tests. Historical public exposure is not reversible; prioritize preventing renewed exposure.

## Costs and administration

Target a free-tier pilot **only if** current Cloudflare Pages, Access, seat, build, preview, domain, and account limitations fit actual usage. Cloudflare pricing/terms, Github private-repo Actions quotas and Google Forms availability must be re-verified before choosing a paid plan or writing billing automation. No purchased domain or backend is required in the initial design, but a domain may improve permanent naming and policy clarity. Monthly usage alerts and source deployments/build counts must be established before ongoing automated course work.

## Decisions that still need explicit owner approval

- Final Cloudflare Pages/Access choice versus alternatives, verified costs and hostnames.
- Existing-course-repo private conversion versus clean-history successor repositories, after assessing historical exposure, GitHub Pages behavior, forks, and workflow constraints.
- Optional external-address exceptions, form retention and owner notifications.
- Public-general lessons destination (portal vs separate public repository), after file-by-file classification.
- Each protected production cutover; no implicit authorization to change repo visibility, production workflows or DNS.

## Coordination and implementation reporting

Main/shared chat owns ecosystem plan, public portal and shared repositories; course chats own protected content and course code changes. Transfer non-sensitive architecture requirements to each course via reviewed issues/PRs once explicitly authorized. Each work session records inspected sources, changed paths, commands/tests actually run, PR/commit, actual Pages/Cloudflare verification, rights/security risks, and next concrete action. **This document is planning only and intentionally makes no configuration or production changes.**
