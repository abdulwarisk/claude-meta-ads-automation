"""Create one PAUSED traffic campaign per row of ad_plan.csv.

  python src/main.py          dry run (default): validate + print the plan, no calls to Meta
  python src/main.py --live   create everything in Meta, all PAUSED
"""
import csv, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE.parent
ROOT = SCRIPT.parent
PLAN = SCRIPT / 'ad_plan.csv'
CREATIVES = ROOT / 'creatives'
CTAS = {'LEARN_MORE', 'SHOP_NOW', 'SIGN_UP', 'ORDER_NOW', 'BOOK_TRAVEL', 'CONTACT_US', 'DOWNLOAD', 'GET_OFFER', 'SUBSCRIBE', 'APPLY_NOW', 'WHATSAPP_MESSAGE'}
REQ = ['campaign_name', 'country', 'age_min', 'age_max', 'daily_budget_minor', 'headline', 'primary_text', 'cta', 'image_file', 'link']

def load(live):
    rows = list(csv.DictReader(open(PLAN, encoding='utf-8')))
    problems = []
    for n, r in enumerate(rows, 1):
        for k in REQ:
            if not (r.get(k) or '').strip():
                problems.append(f'row {n}: {k} is empty')
        if (r.get('cta') or '').strip() not in CTAS:
            problems.append(f"row {n}: cta '{r.get('cta')}' not in {sorted(CTAS)}")
        try:
            if int(r['daily_budget_minor']) <= 0: raise ValueError
        except Exception:
            problems.append(f'row {n}: daily_budget_minor must be a whole number > 0')
        if not (CREATIVES / (r.get('image_file') or '')).is_file():
            problems.append(f"row {n}: creatives/{r.get('image_file')} not found")
        if live and 'your-site.com' in (r.get('link') or ''):
            problems.append(f'row {n}: replace the sample link with your real page')
    return rows, problems

def show(rows):
    print(f'\n{len(rows)} campaign(s) planned, objective OUTCOME_TRAFFIC, everything PAUSED:\n')
    for n, r in enumerate(rows, 1):
        print(f"{n}. {r['campaign_name']}")
        print(f"   audience : {r['country']} {('(' + r['cities'] + ')') if r.get('cities') else ''} age {r['age_min']}-{r['age_max']} interest '{r.get('interest_keyword', '')}'")
        print(f"   budget   : {int(r['daily_budget_minor']) / 100:.2f}/day (account currency)")
        print(f"   ad       : {r['headline']} | {r['primary_text'][:60]}... | {r['cta']}")
        print(f"   creative : creatives/{r['image_file']}  link: {r['link']}\n")

def main():
    live = '--live' in sys.argv
    rows, problems = load(live)
    show(rows)
    if problems:
        print('Fix these first:\n  - ' + '\n  - '.join(problems)); sys.exit(1)
    if not live:
        print('DRY RUN only. Nothing was sent to Meta. Run with --live to create these as PAUSED.'); return
    sys.path.insert(0, str(SCRIPT))
    from src.config import init
    from src.services import targeting, campaigns as C
    account, page_id = init()
    out = SCRIPT / 'output'; out.mkdir(exist_ok=True)
    results = []
    for n, r in enumerate(rows, 1):
        try:
            t, city_keys, interest = targeting.build(r)
            camp = C.campaign(account, r['campaign_name'])
            aset = C.adset(account, camp.get_id(), r['campaign_name'] + ' | ad set', r['daily_budget_minor'], t)
            h = C.image(account, CREATIVES / r['image_file'])
            cr = C.creative(account, page_id, h, r)
            a = C.ad(account, aset.get_id(), cr.get_id(), r['campaign_name'] + ' | ad')
            results.append([n, r['campaign_name'], camp.get_id(), aset.get_id(), a.get_id(), 'PAUSED', ''])
            print(f"✓ {n}. {r['campaign_name']}  campaign {camp.get_id()}  ad set {aset.get_id()}  ad {a.get_id()}  PAUSED")
        except Exception as e:
            msg = getattr(e, 'api_error_message', lambda: str(e))()
            results.append([n, r['campaign_name'], '', '', '', 'FAILED', msg])
            print(f"✗ {n}. {r['campaign_name']} failed: {msg}")
    with open(out / 'created.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows([['row', 'name', 'campaign_id', 'adset_id', 'ad_id', 'status', 'error']] + results)
    print(f"\nSaved {out / 'created.csv'}. Review in Ads Manager and publish yourself.")

if __name__ == '__main__':
    main()
