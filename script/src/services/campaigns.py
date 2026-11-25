"""Creates campaign, ad set, image, creative and ad. Everything is PAUSED."""
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.ad import Ad

PAUSED = 'PAUSED'

def campaign(account, name):
    return account.create_campaign(params={
        'name': name, 'objective': 'OUTCOME_TRAFFIC', 'status': PAUSED,
        'special_ad_categories': [], 'is_adset_budget_sharing_enabled': False,
    })

def adset(account, campaign_id, name, budget_minor, targeting):
    return account.create_ad_set(params={
        'name': name, 'campaign_id': campaign_id, 'status': PAUSED,
        'daily_budget': int(budget_minor), 'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'LINK_CLICKS', 'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
        'destination_type': 'WEBSITE', 'targeting': targeting,
    })

def image(account, path):
    img = AdImage(parent_id=account.get_id())
    img[AdImage.Field.filename] = str(path)
    img.remote_create()
    return img[AdImage.Field.hash]

def creative(account, page_id, image_hash, row):
    return account.create_ad_creative(params={
        'name': f"{row['campaign_name']} | creative",
        'object_story_spec': {'page_id': page_id, 'link_data': {
            'image_hash': image_hash, 'link': row['link'], 'message': row['primary_text'],
            'name': row['headline'], 'description': row['description'],
            'call_to_action': {'type': row['cta'], 'value': {'link': row['link']}},
        }},
    })

def ad(account, adset_id, creative_id, name):
    return account.create_ad(params={'name': name, 'adset_id': adset_id, 'creative': {'creative_id': creative_id}, 'status': PAUSED})
