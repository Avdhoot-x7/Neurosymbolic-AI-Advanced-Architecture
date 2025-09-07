from typing import Dict, List

def diff_facts(old: Dict, new: Dict) -> List[str]:
    """Compare two fact dicts and return a list of changes."""
    changes = []

    # Symptoms
    added_symptoms = new["symptoms"] - old["symptoms"]
    if added_symptoms:
        changes.append(f"Added symptoms: {', '.join(added_symptoms)}")

    # Qualifiers
    for k, v in new["qualifiers"].items():
        if k not in old["qualifiers"]:
            changes.append(f"Added qualifier {k}={v}")
        elif old["qualifiers"][k] != v:
            changes.append(f"Updated qualifier {k}: {old['qualifiers'][k]} → {v}")

    # Red flags
    added_red = new["red_flags"] - old["red_flags"]
    if added_red:
        changes.append(f"Added red flags: {', '.join(added_red)}")

    return changes
