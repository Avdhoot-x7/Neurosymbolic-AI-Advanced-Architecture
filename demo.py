from pprint import pprint
from copy import deepcopy

from engine.parser import parse_input
from engine.rules_engine import fire_rules
from engine.clarifier import find_missing_slots, generate_questions
from engine.rag import retrieve_support
from engine.confidence import pick_with_confidence
from engine.memory import ConversationMemory
from engine.diff import diff_facts
from engine.self_critique import self_check

memory = ConversationMemory()  # global memory for a conversation


def infer(text: str):
    # Snapshot old facts before update (deep copy to avoid shared sets/dicts)
    old_facts = deepcopy(memory.get())

    # Parse new input into facts and merge into memory
    new_facts = parse_input(text)
    facts = memory.update(new_facts)

    # Track what changed this turn
    changes = diff_facts(old_facts, facts)

    # Step 1: Clarify if critical info is missing
    missing = find_missing_slots(facts)
    if missing:
        return {
            "status": "need_more_info",
            "input": text,
            "facts": facts,
            "questions": generate_questions(missing),
            "changes": changes
        }

    # Step 2: Apply rules
    candidates = fire_rules(facts)

    # Step 3: Confidence & abstain layer
    top, status = pick_with_confidence(candidates, threshold=0.6)

    # Step 4: Self-critique (agreement across passes) before finalizing
    if status == "diagnosis" and top:
        critique = self_check(text)  # checks agreement of multiple passes
        if critique.get("status") == "disagree":
            return {
                "status": "abstain",
                "input": text,
                "facts": facts,
                "message": "Model reasoning disagreed across passes.",
                "critique": critique,
                "changes": changes
            }

        # If critique agrees, attach citations and return diagnosis
        top["citations"] = retrieve_support(top["condition"])
        return {
            "status": "diagnosis",
            "input": text,
            "facts": facts,
            "top": top,
            "all_candidates": candidates,
            "critique": critique,
            "changes": changes
        }

    if status == "abstain":
        return {
            "status": "abstain",
            "input": text,
            "facts": facts,
            "message": "Not enough confidence to answer safely.",
            "changes": changes
        }

    return {
        "status": "no_match",
        "input": text,
        "facts": facts,
        "changes": changes
    }


if __name__ == "__main__":
    # Simulate multi-turn conversation
    case1 = "I have bloating and nausea."
    print("\n=== Turn 1 ===")
    pprint(infer(case1))

    case2 = "It has been 4 days."
    print("\n=== Turn 2 ===")
    pprint(infer(case2))

    case3 = "And the pain is in my upper abdomen after spicy food."
    print("\n=== Turn 3 ===")
    pprint(infer(case3))
