# Church Worship Slides 教會敬拜投影片

A [Manus](https://manus.im) skill that generates 16:9 PPTX worship presentation slides from song lyrics. Create church worship slides from your phone in just a few minutes!
這是一個 [Manus](https://manus.im) 技能，能從詩歌歌詞自動生成 16:9 的 PPTX 敬拜投影片。只需幾分鐘，用手機就能輕鬆製作教會敬拜投影片！

## Motivation & Background 為什麼開發這個技能？

Preparing worship slides every week can be a tedious, repetitive task. It often involves searching for lyrics, finding high-quality background images, manually splitting text across slides, and adjusting fonts to ensure readability.
每個星期的敬拜投影片準備工作往往繁瑣且重複。你需要上網找歌詞、尋找高畫質的背景圖片、手動將歌詞分段，還要調整字體大小以確保會眾能清楚閱讀。

With this skill, you can automate the entire process. Whether you're on the train or grabbing a coffee, simply open Manus on your phone, provide the song names, and let AI handle the heavy lifting. It searches for lyrics, selects beautiful nature backgrounds, formats the text, and compiles a ready-to-use PowerPoint file.
有了這個技能，你可以將整個過程自動化。無論你是在搭車還是喝咖啡，只要在手機上打開 Manus，輸入詩歌名稱，AI 就會為你處理所有繁重的工作。它會自動搜尋歌詞、挑選美麗的自然背景、排版文字，並生成一份立即可用的 PowerPoint 檔案。

## Features 功能特色

- **Proactive Lyrics Search:** Just provide a song name, and it will find the lyrics for you.
  **自動搜尋歌詞：** 只需提供詩歌名稱，系統會自動為你尋找歌詞。
- **Smart Backgrounds:** Automatically searches for high-resolution nature backgrounds.
  **智能背景：** 自動搜尋高畫質的自然風景圖片作為背景。
- **Auto-Formatting:** Splits lyrics (max 3 lines per slide) and auto-scales fonts.
  **自動排版：** 自動分段歌詞（每頁最多三行）並自動調整字體大小。
- **Multi-Song Sets:** Append multiple songs into a single worship PPTX.
  **多首詩歌：** 可將多首詩歌合併到同一個 PPTX 檔案中。
- **Self-Updating:** Automatically detects and applies updates from this repository.
  **自動更新：** 啟動時自動檢測並套用此儲存庫的最新更新。

## Basic Usage 基本用法

We highly recommend using **Manus Lite** for this skill. Generating slides for one standard song usually costs around **50 credits**.
我們強烈建議使用 **Manus Lite** 來執行此技能。為**一首標準詩歌**生成投影片大約只需消耗 **50 個積分**。

See a real example of the workflow in action:
查看實際操作範例：
👉 [Manus Chat Reference 範例對話](https://manus.im/share/IlDyGr9KNgZLSBy0WLKQEz)

### Sample Prompts 範例指令

**1. Create a new slide 製作新投影片**
> "Create church worship slides for 在那裏祢手必引導"

> "幫我製作《在那裏祢手必引導》的敬拜投影片"

---

**2. Adjust lyrics arrangement 調整歌詞鋪排**
> "Can you arrange the lyrics to repeat two and a half times? (verse + chorus ×2, then chorus again)"

> "歌詞可以排成兩次半嗎？（主歌+副歌 ×2，再唱副歌）"

---

**3. Adjust design 調整設計**
> "Can you change the background to a sunset over the ocean?"

> "可以把背景換成海上日落的圖片嗎？"

> "Change the overlay to a white colour."

> "把遮罩顏色改成白色。"

---

**4. Add another song 加入另一首詩歌**
> "Looks great! Now add 《四面環繞的恩惠》 to this worship set."

> "太棒了！現在請將《四面環繞的恩惠》加入這份投影片中。"

---

## Install 安裝方法

1. In Manus, navigate to **'Skills'** > **'Add'** > **'Import from GitHub'**.
   在 Manus 中，前往 **「技能 (Skills)」** > **「新增 (Add)」** > **「從 GitHub 匯入 (Import from GitHub)」**。
2. Paste the GitHub repository URL: `https://github.com/wongsunday/church-worship-slides`.
   貼上此 GitHub 儲存庫網址：`https://github.com/wongsunday/church-worship-slides`。
3. Click **"Add to My Skills"**.
   點擊 **「新增至我的技能 (Add to My Skills)」**。

## Updates 更新

Updates are applied automatically. When a newer version is available, the skill will:
更新會自動套用。當有新版本時，技能會：

1. Self-patch for the current session / 為本次對話自動更新
2. Present a new skill card in the chat / 在對話中顯示新的技能卡片
3. Ask you to click **"Add to My Skills"** to make the update permanent / 提示你點擊 **「新增至我的技能」** 以永久套用更新

For **major version** updates (breaking changes), the skill will stop and ask you to re-install manually from this page.
若遇到**主要版本**更新（重大變更），技能會停止並要求你從此頁面重新手動安裝。

## Sample Output 輸出範例

Here are some examples of the generated slides:
以下是生成的投影片範例：

### Sample Slides
![Sample Slide 1](https://raw.githubusercontent.com/wongsunday/church-worship-slides/master/templates/sample/preview_verse.jpg)

![Sample Slide 2](https://raw.githubusercontent.com/wongsunday/church-worship-slides/master/templates/sample/preview_chorus.jpg)

[Download Sample PPTX 下載範例 PPTX](https://github.com/wongsunday/church-worship-slides/raw/master/templates/sample/%E5%9B%A0%E4%BD%A0%E5%A0%85%E6%8C%81_sample.pptx)

## Release History 更新記錄

See [CHANGELOG.md](CHANGELOG.md).
