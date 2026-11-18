# AGENTS.md — Learning Lab main portal

## Project ownership and boundaries

This repository owns the independent public portal at https://rhhanson-umd.github.io/ for the RHHanson-UMD Learning Lab. It is **not** an official University of Maryland site.

The main/shared infrastructure chat may directly maintain this repo, `RHHanson-UMD/learning-core`, and `RHHanson-UMD/course-template`. ENEE 620, ENEE 630 and ENEE 641 each have their own repository, Pages subsite, source materials and maintenance chat. Do not silently edit or deploy a course repo from this scope. Use a GitHub issue/PR or explicit transfer note for course dependencies.

## Canonical source and architecture

- Edit `content/courses.json` for course cards and `content/resources.json` for curated references.
- Run `python scripts/build.py` to regenerate `site/index.html`. Sections between `<!-- COURSES_BEGIN/END -->`, `<!-- FILTERS_BEGIN/END -->` and `<!-- RESOURCES_BEGIN/END -->` are generated and must not be hand-edited.
- `site/assets/app.js` handles theme, resource search/filter and counts; `site/assets/styles.css` holds theme variables and responsive CSS.
- `site/quick-reference.html` contains the companion set of original refresher examples. Keep its links, search, keyboard access and theme compatible with the homepage.
- `docs/RIGHTS.md` describes the public attribution/rights review process. Keep its policy and visible footer notices consistent.
- This is a static HTML/CSS/vanilla-JavaScript project, not React/Vite; new frameworks or backend services require a clear need.

Current GitHub files, issues, open PRs and Pages workflow runs are the **source of truth** for implementation. Project handoff notes and `docs/maintenance/STATUS.md` are dated context, not live deployment proof.

## Teaching, attribution and privacy

Develop original, testable explanations with interactive states, clear assumptions, units/conventions and counterexamples. Separate reusable pure math from page controllers and test against independent expected results. For instructor-specific statements, open the *exact* authorized source material first; preserve course notation and distinguish evidence from interpretation.

Never commit private Google Drive lecture PDFs, unreleased homework/solutions, copyrighted figures without permission, student data, credential files, tokens, or unapproved publication assets. Official solution release does not itself grant permission to redistribute. Keep issue and PR descriptions free of restricted source material. Cover art may only be added when its provenance, publication rights and displayed mathematical accuracy have been reviewed.

## Design and verification

- Dark theme by default for new visitors, explicit remembered light selection.
- Responsive layout, meaningful labels, visible focus indicators, accessible contrast, keyboard operation and reduced-motion support.
- Course links must use correct GitHub Pages paths; verify that the site loads from a project subpath when relevant.
- Preserve existing resources and generated content; avoid replacing data with a static duplicate.
- No analytics, accounts or unnecessary external runtime dependencies without explicit approval.

For portal changes:

```sh
python scripts/build.py
python -m http.server 8000 -d site
```

Check the generated diff, homepage course links, resource search/category filtering, Quick Reference, both themes and mobile/keyboard layout. A passing source-level check is **not** a browser test. For `learning-core`, run `npm test` with Node 20+.

The portal deploys from `site/` using `.github/workflows/deploy.yml` and GitHub Actions Pages. Inspect the Pages workflow and then the *public* URL; do not equate a green test or merged PR with a live deployment. If Pages serves a README or a wrong location, check Settings > Pages > Source: GitHub Actions and the uploaded artifact path.

## Changes, coordination and reporting

Prefer small feature branches and reviewable PRs with linked issues. Check existing issues/PRs before starting to avoid duplicate work. Report sources actually opened, exact paths changed, tests *actually* executed, PR/commit, Pages status/live URL, restrictions/risks and a concrete next step. Keep a non-sensitive update in a relevant issue or `docs/maintenance/STATUS.md` for continuity between automation runs and course chats. Do not report unperformed tests or deployments as successful.

## Repository-specific acceptance checks (tracked in #14)

1. For every change to generated home content, edit the appropriate JSON input, run `python3 scripts/build.py`, then `python3 scripts/verify_site.py`, and verify `git diff --exit-code -- site/index.html` succeeds after the generated page is committed. Do not hand-edit generated course/resource blocks.
2. Run the Python live-Pages tests separately when the verifier or deployment workflow changes; verify the public root page and `/quick-reference.html` after a deployment. Network access or green CI must not be mistaken for actual browser verification.
3. Keep course-specific coverage, syllabus interpretation, figures and homework out of this portal's general knowledge map unless independently vetted as general education; file course-specific follow-ups in the course-owned repository.
4. Treat cover artwork and other third-party imagery as publication-gated: confirm creation/redistribution rights and inspect visible mathematics before committing binaries. Do not embed private source URLs in issue bodies.
5. For cross-repository maintenance, record explicit issue/PR handoffs and respect each course repo's own AGENTS.md. The main portal is the coordination point, not a mandate to edit every course simultaneously.
