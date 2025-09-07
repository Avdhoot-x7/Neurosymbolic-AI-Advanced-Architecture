from typing import Dict, List

CRITICAL_SLOTS = {
    "duration_days": "How many days have you had these symptoms?",
    "pain_location": "Where exactly is the pain located? (e.g. upper abdomen, lower abdomen)",
    "trigger_foods": "Have you noticed any food or drink that makes it worse?",
}

def find_missing_slots(facts: Dict) -> List[str]:
    """Return list of missing critical slots in the fact table."""
    missing = []
    for slot in CRITICAL_SLOTS:
        if slot not in facts.get("qualifiers", {}):
            missing.append(slot)
    return missing

def generate_questions(missing: List[str]) -> List[str]:
    """Turn missing slots into human-friendly clarifier questions."""
    return [CRITICAL_SLOTS[m] for m in missing if m in CRITICAL_SLOTS]

if __name__ == "__main__":
    # Example: simulate incomplete facts
    facts = {
        "symptoms": {"upper_abdominal_pain"},
        "qualifiers": {"duration_days": 2},
        "red_flags": set()
    }
    miss = find_missing_slots(facts)
    qs = generate_questions(miss)
    print("Missing slots:", miss)
    print("Clarifier questions:", qs)
