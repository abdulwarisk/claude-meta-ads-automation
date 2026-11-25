---
name: meta-ads-launch
description: Create 4 paused Meta campaigns from brief/launch-brief.md and the images in creatives/ using Meta's official Ads MCP server (meta-ads tools). Shows the plan and waits for a yes first.
---

1. Read `CLAUDE.md` and follow its hard rules.
2. Read `brief/launch-brief.md` and list `creatives/`. If the link, country, budget or a creative is missing, ask once.
3. Show a plan table for the 4 campaigns: name, objective, audience, placements, daily budget, copy, creative, link. Wait for the user's yes.
4. Using the meta-ads tools, create each campaign, ad set and ad with status **PAUSED**. Upload the named creatives.
5. Return a table of every object with its ID and status, and list anything that failed and why.
6. Remind the user to review in Ads Manager and publish themselves (prompts/02-review-before-publish.md).
