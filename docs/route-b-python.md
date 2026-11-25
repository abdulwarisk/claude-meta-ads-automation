# Route B: Python script (developers)

This uses the official `facebook-business` SDK and a **system-user token** (Business settings → Users → System users → Add assets → Generate token with `ads_management`). Prefer an expiring token and rotate it. Never commit it.

## Setup
```bash
cd script
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # fill in META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_PAGE_ID
```

## Plan your 4 campaigns
Edit `script/ad_plan.csv`. One row is one campaign, with columns for its ad set and ad:
`campaign_name, country, cities, age_min, age_max, interest_keyword, daily_budget_minor, headline, primary_text, description, cta, image_file, link`

- `daily_budget_minor` is in the smallest unit of your account currency (50000 = 500.00).
- `cities` is optional. Separate several cities with `;`. They're looked up by name in the country.
- `image_file` is a file inside `creatives/`.

## Run
```bash
python src/main.py           # DRY RUN: prints the plan, makes no calls to Meta
python src/main.py --live    # creates 4 campaigns, ad sets and ads, all PAUSED
```
Objective: OUTCOME_TRAFFIC, optimised for LINK_CLICKS, lowest-cost bidding. Everything is PAUSED. Check in Ads Manager and publish yourself.
