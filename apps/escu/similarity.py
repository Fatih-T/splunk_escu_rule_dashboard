from difflib import SequenceMatcher

FIELD_WEIGHTS = {
    "mitre_technique_id": 0.40,
    "name":               0.25,
    "mitre_tactic":       0.15,
    "data_source":        0.10,
    "description":        0.10,
}

def field_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    a, b = str(a).lower().strip(), str(b).lower().strip()
    if a == b:
        return 1.0
    return SequenceMatcher(None, a, b).ratio()

def rule_similarity(rule_a_data: dict, rule_b_data: dict) -> tuple[float, list]:
    """
    Returns: (score 0.0–1.0, list of matched field names)
    """
    total, matched_fields = 0.0, []
    for field, weight in FIELD_WEIGHTS.items():
        score = field_similarity(
            rule_a_data.get(field, ""),
            rule_b_data.get(field, "")
        )
        total += score * weight
        if score >= 0.8:
            matched_fields.append(field)
    return round(total, 3), matched_fields
