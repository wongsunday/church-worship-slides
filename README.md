# Church Worship Slides

A [Manus](https://manus.im) skill that generates 16:9 PPTX worship presentation slides from song lyrics. Each slide displays up to 3 lyric lines over a nature photo background with a semi-transparent overlay box, rendered at Full HD (1920×1080).

## Features

- Automatic lyric search and confirmation when only a song name is provided
- Background image search with resolution validation
- Configurable overlay colour and opacity
- Multi-song worship set support (append songs into one PPTX)
- Delivery modes: screen, standard, print
- **Self-updating:** automatically detects and applies updates from this repo at session start

## Install

1. In Manus, navigate to 'Skills' > 'Add' > 'Import from GitHub'.
2. Paste the GitHub repository URL: `https://github.com/wongsunday/church-worship-slides`.
3. Click **"Add to My Skills"**.

## Updates

Updates are applied automatically. When a newer version is available, the skill will:
1. Self-patch for the current session
2. Present a new skill card in the chat
3. Ask you to click **"Add to My Skills"** to make the update permanent

For **major version** updates (breaking changes), the skill will stop and ask you to re-install manually from this page.

## Release History

See [CHANGELOG.md](CHANGELOG.md).
