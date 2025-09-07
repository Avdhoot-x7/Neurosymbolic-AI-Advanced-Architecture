from engine.rules_engine import fire_rules
from engine.parser import parse_input
import random

def multiple_passes(text: str, n: int = 3):
    """
    Run parser+rules multiple times (simulate variant reasoning).
    Here it's simple: shuffle synonyms or sampling;
    later you can expand with paraphrasing / alt parsing.
    """
    variants = []
    for i in range(n):
        facts = parse_input(text)
        candidates = fire_rules(facts)
        top = candidates[0]["condition"] if candidates else None
        variants.append(top)
    return variants

def critique_agreement(variants):
    """
    Count how often the same condition appears.
    """
    if not variants:
        return None, 0.0
    # Most common
    winner = max(set(variants), key=variants.count)
    score = variants.count(winner) / len(variants)
    return winner, score

def self_check(text: str, threshold: float = 0.7):
    """
    Run multiple passes, check agreement, only accept if strong.
    """
    variants = multiple_passes(text, n=3)
    winner, score = critique_agreement(variants)
    if score >= threshold:
        return {"status": "agree", "condition": winner, "agreement": score, "variants": variants}
    else:
        return {"status": "disagree", "condition": None, "agreement": score, "variants": variants}
