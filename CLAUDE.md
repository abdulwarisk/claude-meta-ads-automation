# Rules for Claude Code in this repo

This repo builds Meta (Facebook and Instagram) ad campaigns for the user. You are working on the user's real ad account and real money.

## Hard rules
1. **Create everything PAUSED.** That covers campaigns, ad sets and ads. Never set a status to ACTIVE, never publish, and never "turn on" anything, even if asked casually. The user publishes in Ads Manager themselves.
2. **Never increase a budget or bid** on anything that already exists. Only set budgets on new paused objects, using the numbers in the brief.
3. **Show the plan first.** Before creating anything, show a table with campaign, objective, audience, placements, daily budget, ad copy, creative file and link. Then wait for the user to say yes.
4. **Use only what the brief gives you.** Don't invent prices, discounts, claims, guarantees or URLs. If something is missing, ask once.
5. **Never touch other objects.** Don't edit, pause, delete or duplicate campaigns you didn't create in this session.
6. **No secrets in chat or files.** Never print tokens. `.env` stays git-ignored.

## Route A: official Ads MCP server (`meta-ads` tools)
- If the tools aren't available, tell the user to run the command in `README.md` (Step 1) and `/mcp` (Step 2).
- Read `brief/launch-brief.md` and list the files in `creatives/`.
- Creatives: upload the files the brief names. You can't design or generate images.
- Naming: `{Product} | {Campaign n} | {Audience} | {YYYY-MM-DD}`.
- After creating, return a table of every object name, its ID and its status (it should read PAUSED), plus anything that failed.

## Route B: Python script (`script/`)
- Always run `python src/main.py` (dry run) first and show the output.
- Only run `python src/main.py --live` after the user says yes to that exact plan.
- Edit `script/ad_plan.csv`, not the service code, unless the user asks for a code change.

## Tone
Keep messages short. Lead with what you need from the user.
