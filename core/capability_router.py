# Module docstring
"""
Capability Router
"""

# ===== Added for main.py integration =====
def is_capability_question(text: str) -> bool:
    keywords = ["capability", "abilities", "what can you do", "features", "skills", "can you"]
    return any(k in text.lower() for k in keywords)

def capability_response() -> str:
    return (
        "I am Nova-X, a self-evolving cognitive architecture.\n"
        "I can reason, learn, and improve my own code.\n"
        "Current features:\n"
        "  • Groq-powered reasoning\n"
        "  • Self-scanning and patching\n"
        "  • Automatic pull requests via GitHub\n"
        "  • Living cycle daemon for continuous reflection\n"
        "  • Dynamic capability routing\n"
        "  • And I'm growing every day!"
    )
