from difflib import SequenceMatcher
def rule_similarity(a_data, b_data):
    s = SequenceMatcher(None, a_data.get('name','').lower(), b_data.get('name','').lower()).ratio()
    return round(s, 3), ['name'] if s > 0.8 else []
