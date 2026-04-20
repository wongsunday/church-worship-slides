# Changelog

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

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
