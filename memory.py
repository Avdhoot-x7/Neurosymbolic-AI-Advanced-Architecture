class ConversationMemory:
    def __init__(self):
        # store last known facts across turns
        self.facts = {"symptoms": set(), "qualifiers": {}, "red_flags": set()}

    def update(self, new_facts: dict):
        """Merge new facts into memory"""
        # merge symptoms
        self.facts["symptoms"].update(new_facts.get("symptoms", []))

        # merge qualifiers (overwrite if repeated)
        for k, v in new_facts.get("qualifiers", {}).items():
            self.facts["qualifiers"][k] = v

        # merge red flags
        self.facts["red_flags"].update(new_facts.get("red_flags", []))

        return self.facts

    def get(self):
        return self.facts

    def reset(self):
        self.facts = {"symptoms": set(), "qualifiers": {}, "red_flags": set()}
