# Learning Lab shared-infrastructure launch status

## 2026-11-18 shared launch cycle

- Reviewed current open shared issues and PRs in the portal, `learning-core`, and `course-template`. Course repos remain separately owned and were not edited.
- [learning-core PR #2](https://github.com/RHHanson-UMD/learning-core/pull/2) was squash-merged as `def3367502914655f01edd953495f3bf7b8b5790`. It adds independent truth-table/clique regression tests, `AGENTS.md), and pinned vendoring policy `docs/VERSIONING.md`. GitHub Actions **Tests** PR run `44263398455` completed successfully. No shared release tag or consuming-course migration yet.
- [portal PR #11](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/pull/11) was squash-merged as `1e272df56553a837009fee89c57c2f232b0ea711`. It adds `scripts/verify_site.py` and an independent static Pages verification workflow. GitHub Actions PR run `44263820317` passed all build, local-link, dark-default, metadata and generated-diff checks.
- [portal PR #12](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/pull/12) adds public-safe issue forms for bugs, shared components and educational resources, without changing course repositories.
- **Not verified**: live Pages page and Quick Reference, Pages Settings source, latest push-triggered deploy run, browser/mobile/keyboard behavior, or template-repository Settings. The available public-web reads could not retrieve the site or deployment. A passing static CI workflow is not deployment proof.
- **Cover art** for ENEE-620/630/641 remains proposed under [portal issue #9](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/issues/9); no image binaries were committed pending publication rights and correctness review.
- Next: verify public Pages/Actions, confirm template Settings, then review the still-open release tag and ENEE-641 compatibility tasks in [learning-core issue #1](https://github.com/RHHanson-UMD/learning-core/issues/1). Keep the high-frequency launch automation enabled until real deployment and launch acceptance are confirmed.

Last edited: **2026-11-17**. This is a dated coordination snapshot, **not** a live health dashboard. Read GitHub repositories, issues, PRs, Actions and Pages again before acting.

## Ownership

Main/shared chat owns `RHHanson-UMD.github.io`, `learning-core`, and `course-template`. Course-specific code and source verification stay in `ENEE-620`, `ENEE-630` and `ENEE-641` maintenance chats. Cross-repo requirements should be transferred with issue links.

## Verified in the 2026-11-17 launch cycle

- Root `site/index.html` includes `data-theme="dark"` by default, `site/assets/app.js` remembers explicit light mode, and `site/assets/styles.css` defines light/dark palette values.
- The homepage generator reads `content/courses.json` and `content/resources.json`, then updates the marked blocks in `site/index.html`.
- [PR #1](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/pull/1) (Quick Reference companion page) is merged.
- [PR #8](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/pull/8) added visible attribution/rights notices and `docs/RIGHTS.md`; squash-merged as commit `3e76fa77b03112c50f61a3f3ed16f8d59da2974e`.
- Static assertions checked unchanged dark defaults, generated block markers, one rights notice per page, report links and link color contrast; contrast values were at least 6.55:1 for sampled muted/accent-on-background pairs.
- The root `.github/workflows/deploy.yml` runs the Python generator and uploads `./site` to GitHub Pages.
- `learning-core/package.json` remains `"private": true` with Node test script; reusable versioning still needs a decision. `course-template` still contains a Pages deployment workflow; whether it is marked as a GitHub template is unverified.

## Checks still requiring confirmation

- **Live Pages:** the automation's web access did not retrieve the homepage or workflow-run status. Do not claim a successful deployment without observing the GitHub Pages run and public `https://rhhanson-umd.github.io/` and `/quick-reference.html`.
- **Browser QA:** `python scripts/build.py`, an HTTP-based local browser preview, mobile behavior, and keyboard interaction have not been executed in this session; source assertions alone are not sufficient.
- **Rights notice issue:** [#6](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/issues/6) remains open pending browser and published-site verification.
- **Course covers:** [#9](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/issues/9) tracks three proposed uploaded covers, including publication rights, math/art verification and optimized portal asset integration. The binaries are not yet committed.
- **Future backlog:** [#2](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/issues/2) scope, [#3](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/issues/3) issue workflow, [#4](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/issues/4) knowledge map, [#5](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/issues/5) exam/review standards, [#7](https://github.com/RHHanson-UMD/RHHanson-UMD.github.io/issues/7) resource catalog.

## Concrete next shared tasks

1. Verify Pages source/settings, newest deployment run, homepage URL and Quick Reference in a real browser. Close issue #6 only after evidence.
2. Confirm `course-template` template setting and resolve the template-only failed Pages workflow; document a straightforward new-course checklist.
3. Define a pinned vendoring/version-tag release policy in `learning-core` issue #1 with compatibility tests before moving code between repositories.
4. Add root `AGENTS.md` equivalents to `learning-core` and `course-template` if still absent; maintain clear per-repo ownership.
5. Continue shared content with small separately reviewed changes; use actual sources and keep course-specific work with its owner.

**Publication boundary:** Do not put private source documents, instructor solutions, non-redistributable figures or credentials in public Git history, issues, PRs or Actions artifacts.
