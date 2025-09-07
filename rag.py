from pathlib import Path

# Load snippets from knowledge base
SNIPPETS = (Path(__file__).parents[1] / "knowledge" / "dyspepsia_guidelines.txt").read_text().splitlines()

def retrieve_support(condition: str):
    """Return snippet(s) that mention the condition keyword."""
    hits = [s for s in SNIPPETS if condition.lower() in s.lower()]
    return hits[:2]  # top 2 matches
