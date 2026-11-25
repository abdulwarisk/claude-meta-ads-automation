# Claude Code × Meta Ads: 4 campaigns from one message

Build Meta (Facebook + Instagram) campaigns by describing them in plain English to **Claude Code**. Every campaign is created **PAUSED**, so nothing spends until you've reviewed it in Ads Manager and published it yourself.

> ⚠️ Meta's Ads MCP server is a beta product, and menus and commands can change. Always check what Claude created before publishing. This project is not affiliated with Meta or Anthropic.

---

## Route A: Meta's official Ads server (the one in the Reel)

No code, no tokens. Claude talks to your ad account through Meta's official server: `https://mcp.facebook.com/ads`.

### What you need
- [Claude Code](https://claude.com/claude-code) installed.
- Admin or advertiser access to a Meta ad account and the Facebook Page you'll advertise from.
- Your ad images or videos, ready to use (Claude doesn't design creatives).

### Step 1: Add the official Ads server (one command)
```bash
claude mcp add --transport http --scope user meta-ads https://mcp.facebook.com/ads
```
If the login in Step 2 fails with an error like `redirect_uris are not registered`, use the version with your own Meta app instead. It takes 2 minutes and is explained in [`docs/setup-claude-code.md`](docs/setup-claude-code.md):
```bash
claude mcp add --transport http --scope user --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads
```

### Step 2: Log in
Open Claude Code in this folder and type `/mcp`. Choose **meta-ads → Authenticate**, log in with Facebook, and pick your ad account.

### Step 3: One message, 4 campaigns, all paused
1. Fill in [`brief/launch-brief.md`](brief/launch-brief.md).
2. Put your images in `creatives/`.
3. Paste the prompt from [`prompts/01-create-4-campaigns.md`](prompts/01-create-4-campaigns.md).

Claude will:
1. read the brief;
2. show you the full plan;
3. wait for your **yes**;
4. create 4 campaigns, each with its own audience, ad copy and creative, **all PAUSED**;
5. give you a table of everything it created.

You can also use the skill: `/meta-ads-launch`.

### Step 4: Check in Ads Manager, then publish
Open Ads Manager, check budget, audience, placements, creative and links, then switch the campaigns on yourself. The checklist is in [`prompts/02-review-before-publish.md`](prompts/02-review-before-publish.md).

### 🎁 Extra tip: block budget edits
In **Meta Business Suite → Settings → Integrations → Ads MCP server**, choose your ad account and **block "edit budgets"**. Claude can still build ads for you, but it can't raise your budget on its own. Details are in [`docs/safety-business-suite.md`](docs/safety-business-suite.md).

---

## Route B: Python script (for developers)

The same idea, run as a script with the official `facebook-business` SDK and a system-user token. It reads 4 rows from a CSV and creates 4 paused campaigns. By default it only does a **dry run**: it prints the plan and makes no calls to Meta until you add `--live`.

```bash
cd script
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env      # fill in your values, never commit .env
python src/main.py              # dry run: prints the 4 campaigns
python src/main.py --live       # creates them in Meta, all PAUSED
```
More in [`docs/route-b-python.md`](docs/route-b-python.md).

---

## What's in this repo
```
CLAUDE.md                     rules Claude Code follows here (paused only, confirm first, no budget raises)
brief/launch-brief.md         fill-in brief: product, offer, link, 4 audiences, copy, budgets
prompts/                      ready prompts: create 4 campaigns, review before publish, weekly report
creatives/                    put your images or videos here
docs/                         setup help, safety settings, Python route
.claude/skills/               /meta-ads-launch (Route A) and /meta-ads-script (Route B)
script/                       Route B: Python SDK script (dry run by default)
```

## Safety rules built in
- Everything is created **PAUSED**. Claude never publishes, never activates and never raises a budget.
- Claude shows the full plan and waits for your "yes" before creating anything.
- `.env` is git-ignored. Never paste tokens into chat or commit them.

---

Made with ❤️ by **@abdulwarisk.marketing**. Follow for more Claude × Meta Ads tips.
