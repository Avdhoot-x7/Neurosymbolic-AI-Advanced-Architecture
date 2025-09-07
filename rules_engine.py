import yaml
from pathlib import Path
from typing import Dict, Any, List

with open(Path(__file__).parents[1] / "rules" / "dyspepsia.yaml", "r") as f:
    RULES: List[Dict[str, Any]] = yaml.safe_load(f)

def _check_clause(facts: Dict[str, Any], clause: Dict[str, Any]) -> bool:
    # supports three clause types: symptom, qualifier, red_flag
    if "symptom" in clause:
        return clause["symptom"] in facts["symptoms"]

    if "red_flag" in clause:
        return clause["red_flag"] in facts["red_flags"]

    if "qualifier" in clause:
        q = clause["qualifier"]
        name = q["name"]
        if name not in facts["qualifiers"]:
            return False
        val = facts["qualifiers"][name]
        if "equals" in q:
            return val == q["equals"]
        if "gte" in q:
            try:
                return float(val) >= float(q["gte"])
            except Exception:
                return False
        if "includes" in q:
            # val can be str or list
            if isinstance(val, str):
                return q["includes"] in val
            if isinstance(val, list):
                return q["includes"] in val
            return False
    return False

def _check_logic(facts: Dict[str, Any], logic: Dict[str, Any]) -> bool:
    # logic is either {"all": [clauses]} or {"any": [clauses]} or empty
    if not logic:
        return True
    if "all" in logic:
        return all(_check_clause(facts, c) for c in logic["all"])
    if "any" in logic:
        return any(_check_clause(facts, c) for c in logic["any"])
    return False

def fire_rules(facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return list of fired rules with provenance and scores."""
    fired = []
    for r in RULES:
        if _check_logic(facts, r.get("if", {})) and not _check_logic(facts, r.get("unless", {})):
            result = {
                "rule_id": r["id"],
                "condition": r["then"]["condition"],
                "recommendation": r["then"]["recommendation"],
                "confidence": float(r["then"]["confidence"]),
                "source": r["then"]["source"]
            }
            fired.append(result)
    # sort highest confidence first
    fired.sort(key=lambda x: x["confidence"], reverse=True)
    return fired
