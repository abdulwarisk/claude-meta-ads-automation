"""Looks up interest IDs and city keys by name."""
from facebook_business.adobjects.targetingsearch import TargetingSearch

def interest(keyword):
    if not keyword:
        return None
    res = TargetingSearch.search(params={'type': 'adinterest', 'q': keyword, 'limit': 5})
    return {'id': res[0]['id'], 'name': res[0]['name']} if res else None

def city(name, country):
    res = TargetingSearch.search(params={'type': 'adgeolocation', 'location_types': ['city'], 'q': name, 'country_code': country, 'limit': 1})
    return res[0]['key'] if res else None

def build(row):
    cc = row['country'].strip().upper()
    cities = [c.strip() for c in (row.get('cities') or '').split(';') if c.strip()]
    geo = {'countries': [cc]}
    keys = [k for k in (city(c, cc) for c in cities) if k]
    if keys:
        geo = {'cities': [{'key': k, 'radius': 17, 'distance_unit': 'kilometer'} for k in keys]}
    t = {
        'geo_locations': geo,
        'age_min': int(row['age_min']), 'age_max': int(row['age_max']),
        'publisher_platforms': ['facebook', 'instagram'],
        'targeting_automation': {'advantage_audience': 0},
    }
    i = interest(row.get('interest_keyword', '').strip())
    if i:
        t['flexible_spec'] = [{'interests': [i]}]
    return t, keys, i
