from typing import List, Dict

def pick_with_confidence(candidates: List[Dict], threshold: float = 0.6):
    """
    Pick top candidate if confidence >= threshold.
    Otherwise abstain.
    """
    if not candidates:
        return None, "no_match"

    # Red-flag rules always win
    redflag = next((c for c in candidates if c["condition"] == "urgent_evaluation"), None)
    if redflag:
        return redflag, "diagnosis"

    top = candidates[0]
    if top["confidence"] >= threshold:
        return top, "diagnosis"
    else:
        return None, "abstain"
