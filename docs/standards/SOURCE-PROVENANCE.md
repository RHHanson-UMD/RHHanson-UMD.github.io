# Learning Lab source provenance and unlabeled intake (v1)

This is a **course-relative evidence taxonomy**, not the conventional scholarly primary/secondary/tertiary taxonomy. It does not rank truth, correctness, licensing, or teaching importance.

## Source tiers
- **primary**: instructor-provided or instructor-authored course materials (syllabus, slides, official assignments, released official solutions, instructor notes, announcements) and an authentic lecture recording. Verify authorship; a file name alone is not proof.
- **secondary**: student notes/work, AI-generated summaries, and derivative representations of instruction. An automatically generated lecture transcript is **secondary**, subtype `lecture_transcript`, with `derived_from` pointing to the lecture/recording if known. A transcript checked against the recording remains a transcript; record the check separately.
- **tertiary**: independently produced external material, such as textbooks, outside tutorials, papers, public references. An assigned external textbook remains tertiary with `course_role: assigned_reference`.
- **unknown**: insufficient evidence; never force a guess.

## Intake behavior (unlabeled by default)
1. Treat all incoming files as unlabeled and **private by default**. Never assume that a Drive file, attachment, filename, or generated text is authorized for public redistribution.
2. Inspect accessible file content and trustworthy metadata (creator, provenance, context, format, source links). Record evidence and uncertainty without copying restricted content into a public issue or repo.
3. Assign a tier automatically only if origin is supported by clear evidence. Classification `status` is `provisional` until corroborated or confirmed. No arbitrary numerical confidence scores.
4. **If the origin, author, transcription method, instructor assignment, or release status affects classification and is unclear, prompt the owner with one targeted question and options including `I don't know`.** Do not silently choose. Keep the record `unknown` / `needs_clarification` when unresolved. Avoid repeat prompts for previously answered identical evidence; preserve an audit trail.
5. For transcripts, distinguish the original lecture/recording (primary) from the transcript (secondary). Flag mathematical notation, negation, units, equations, and speaker attribution for verification against audio or another authoritative source. Transcripts can be useful evidence without being assumed accurate.
6. Track verification independently: `unverified`, `cross_checked`, `verified`, `disputed`, `corrected`. Record method and source IDs, not an unsupported blanket accuracy claim.
7. Track **access** and **redistribution** independently. `verified` and `primary` never imply permission to publish. Release of official homework solutions does not grant republication rights.
8. Never commit private lecture PDFs, recordings, transcripts, homework, instructor keys, student information, secrets, private URLs, or sensitive extracted excerpts to public GitHub history, issues, PRs or Pages. Public metadata must be separately reviewed and approved.

## Implementation contract
- Schema: `schemas/source-record.schema.json`; example: `examples/source-record.example.json`.
- Optional private intake tools may emit records matching this schema, but this repository does **not** ingest private course files, connect to Drive, classify with an AI service, or automatically prompt through GitHub Actions.
- Classification is evidence-based, not a deterministic filename heuristic. The validator checks record shape and safety fields; it **does not** infer provenance or certify publication rights.
- Course-specific inventories belong to each course's own controlled workflow. Coordinate adoption through course-owned issues/PRs. Keep `learning-core` focused on pure mathematical algorithms.
- Public pages may display an approved citation and source tier only after metadata publication review. Keep private locator values out of public JSON and HTML.

## Suggested clarification
> This looks like lecture notes, but I cannot determine who created them. Were they (1) provided/authored by the instructor, (2) produced by a student or transcription tool, (3) obtained from an independent external source, or (4) unknown?

A response updates the classification evidence and review trail; it does not change publication authorization.
