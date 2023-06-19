# Dev Notes
## Tech stack setup goal before camp
The setup goal is accomplished, when we have the following:
- An IntelliJ run config, which
- opens a Tauri-based GUI window, which
- shows a Solid.js-generated and Tailwind-styled button, which
- fetches a list of pending download links via Python backend and
- displays them in the UI, and
- we can change the font of that list in code and see the effects without page reload.

## Main areas of work
- Basic functionality in UI
  - add new links
  - download pending videos
  - view data as table
- Nice data presentation, including videos
- Crawler
  - Identify relevant hashtags / challenges / authors / keywords from transcript, description, etc.
  - Introduce a manual usefulness rating / categorization system
  - Learn category
- Data condensation
  - 1-sentence abstract
  - extract names of websites, resources, etc.
- GitHub Actions

# Other useful ideas
- introduce a mock TikTok API and some unit / DB / e2e tests, including a test DB, etc.
- clean up naming clutter (save / insert) in transactions
- "drop zone" for dropping tiktok links from smartphone (cloud-based)

## Possible dirty DB states
- orphan authors (all their videos deleted)
- video with no author (don't want to delete their videos if we delete an author)
- orphan hashtags / challenges (still in DB, but no longer associated with any video id)
