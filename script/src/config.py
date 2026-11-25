"""Loads .env (repo root) and initialises the Meta SDK. Imported only in --live mode."""
import os, pathlib
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[2]

def init():
    load_dotenv(ROOT / '.env')
    token = os.getenv('META_ACCESS_TOKEN', '').strip()
    acct = os.getenv('META_AD_ACCOUNT_ID', '').strip()
    page = os.getenv('META_PAGE_ID', '').strip()
    missing = [n for n, v in [('META_ACCESS_TOKEN', token), ('META_AD_ACCOUNT_ID', acct), ('META_PAGE_ID', page)] if not v]
    if missing:
        raise SystemExit(f'Missing in .env: {", ".join(missing)} (see docs/route-b-python.md)')
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    app_id, secret = os.getenv('META_APP_ID') or None, os.getenv('META_APP_SECRET') or None
    FacebookAdsApi.init(app_id=app_id, app_secret=secret, access_token=token)
    if not acct.startswith('act_'):
        acct = 'act_' + acct
    return AdAccount(acct), page
