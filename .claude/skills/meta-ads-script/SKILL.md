---
name: meta-ads-script
description: Route B. Run the Python SDK script in script/ to create 4 paused campaigns from script/ad_plan.csv: dry run first, live only after the user's yes.
---

1. Check that `.env` exists in the repo root with a token, ad account and page. If not, stop and point to `docs/route-b-python.md`. Never print the token.
2. If the user wants changes, edit `script/ad_plan.csv` only.
3. Run `cd script && python src/main.py` (dry run) and show the plan.
4. Only after an explicit yes to that plan, run `python src/main.py --live`.
5. Report the created IDs and statuses. Everything should be PAUSED.
