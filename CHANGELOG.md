# Changelog

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.2.1] - 2026-04-21

### Fixed
- **Installation Instructions:** Corrected the README to reflect the actual GitHub import method in Manus ('Skills' > 'Add' > 'Import from GitHub').

## [1.2.0] - 2026-04-21

### Added
- **Step 3 – Inline image list-view:** Background options are now presented as a numbered list with inline image previews (uploaded to CDN URLs via `manus-upload-file`) so users can see each option directly in the chat without clicking external links.

### Changed
- **Step 3 – Pre-filter before user selection:** Resolution (< 1280×720) and watermark checks (Shutterstock, Getty, iStock, Dreamstime) are now applied silently *before* presenting options to the user. Low-res or watermarked images are discarded automatically; if fewer than 3 valid images remain, a refined search is triggered.
- **Step 4 – Resolution validation moved upstream:** Step 4 now only confirms the resolution tier of the already-validated image; the disruptive "pick again" loop after user selection has been eliminated.

---

## [1.1.3] - 2026-04-20

### Changed
- `version` field reverted to `metadata.version` (Manus convention) for validator compatibility.

---

## [1.1.2] - 2026-04-20

### Changed
- `version` field moved to top-level frontmatter (gstack convention), removing `metadata` nesting.

---

## [1.1.1] - 2026-04-20

### Changed
- **Step 0 simplified:** Removed major/minor version branching. All updates (patch, minor, major) now follow the same single path — self-patch, show changelog, present `.skill` card, proceed. Major version bumps are flagged with a prominent notice in the update message rather than a hard stop.

---

## [1.1.0] - 2026-04-20

### Added
- **Step 0 – Self-update check:** Skill now automatically compares its local version against the GitHub source at the start of every session. If a minor/patch update is available, it self-patches and presents a `.skill` card for the user to make the update permanent. Major version bumps require manual re-install.
- `VERSION` file as canonical version source.
- `CHANGELOG.md` (this file).
- `metadata.version` field in `SKILL.md` frontmatter mirroring `VERSION`.

---

## [1.0.0] - 2026-04-16

### Added
- Initial release.
- Full 7-step workflow: lyrics acquisition, lyric splitting, background search, resolution validation, overlay colour selection, PPTX rendering, and post-build review loop.
- Multi-song append support via `append_slides.py`.
- Full HD (1920×1080) rendering with configurable delivery modes (screen / standard / print).
- Chinese/English bilingual lyric support with auto font-size scaling.
- Sample output bundled in `templates/sample/`.
