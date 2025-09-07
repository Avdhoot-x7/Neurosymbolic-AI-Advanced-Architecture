import re
import json
import yaml
from pathlib import Path

# Load ontology
ONTOLOGY = json.load(open(Path(__file__).parents[1] / "ontologies" / "dyspepsia.json"))

# Load rules
with open(Path(__file__).parents[1] / "rules" / "dyspepsia.yaml") as f:
    RULES = yaml.safe_load(f)

def parse_input(text: str):
    """
    Very crude parser: finds symptoms/qualifiers/red_flags in free text.
    Later we’ll add word weights + clarifiers.
    """
    text = text.lower()
    facts = {"symptoms": set(), "qualifiers": {}, "red_flags": set()}

    # symptom detection by keyword
    for s in ONTOLOGY["symptoms"]:
        if s.replace("_", " ") in text:
            facts["symptoms"].add(s)

    # qualifier: duration
    m = re.search(r"(\d+)\s*day", text)
    if m:
        facts["qualifiers"]["duration_days"] = int(m.group(1))

    # pain location
    if "upper" in text and "abdomen" in text:
        facts["qualifiers"]["pain_location"] = "epigastric"

    # trigger foods
    if "spicy" in text:
        facts["qualifiers"]["trigger_foods"] = "spicy"

    # red flags
    if "blood" in text:
        facts["red_flags"].add("blood_in_vomit")
    if "weight loss" in text:
        facts["red_flags"].add("weight_loss")

    return facts


if __name__ == "__main__":
    example = "I have acid reflux for 5 days and upper abdominal pain after spicy food."
    print(parse_input(example))
