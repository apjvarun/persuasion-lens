"""
PersuasionLens — AI-powered writing persuasiveness analyzer.

Analyzes text across persuasion dimensions (Aristotle's rhetorical triangle +
Cialdini's principles) and returns structured scores, technique identification,
and an improved rewrite.

Built by Varun Gupta | Inspired by US Patent on Persuasiveness of User-Authored Content
"""

import json
import os
from anthropic import Anthropic

client = Anthropic()  # Uses ANTHROPIC_API_KEY env var

ANALYSIS_PROMPT = """You are an expert in persuasion science, combining Aristotle's rhetorical
framework (ethos, pathos, logos) with Cialdini's principles of influence (reciprocity,
scarcity, authority, consistency, liking, consensus/social proof).

Analyze the following text for persuasiveness. Return a JSON object with EXACTLY this structure:

{
  "overall_score": <1-10 integer>,
  "summary": "<2-3 sentence overall assessment>",
  "dimensions": {
    "ethos": {
      "score": <1-10>,
      "evidence": "<specific examples from the text, or what's missing>"
    },
    "pathos": {
      "score": <1-10>,
      "evidence": "<specific examples from the text, or what's missing>"
    },
    "logos": {
      "score": <1-10>,
      "evidence": "<specific examples from the text, or what's missing>"
    },
    "social_proof": {
      "score": <1-10>,
      "evidence": "<specific examples from the text, or what's missing>"
    },
    "scarcity_urgency": {
      "score": <1-10>,
      "evidence": "<specific examples from the text, or what's missing>"
    },
    "clarity": {
      "score": <1-10>,
      "evidence": "<specific examples from the text, or what's missing>"
    }
  },
  "techniques_detected": ["<list of specific persuasion techniques found>"],
  "weaknesses": ["<list of specific weaknesses>"],
  "suggestions": ["<list of 3-5 actionable improvements>"],
  "rewrite": "<improved version of the text that scores higher on persuasiveness>"
}

Return ONLY the JSON object, no other text."""


def analyze(text: str, context: str = "general") -> dict:
    """
    Analyze a piece of text for persuasiveness.

    Args:
        text: The text to analyze
        context: The context/purpose of the text (e.g., "cold email", "linkedin post",
                 "product pitch", "job application")

    Returns:
        dict with scores, analysis, suggestions, and rewrite
    """
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""Context: This text is a {context}.

TEXT TO ANALYZE:
\"\"\"
{text}
\"\"\"

{ANALYSIS_PROMPT}"""
            }
        ]
    )

    # Parse the JSON response
    response_text = message.content[0].text

    # Handle cases where the model wraps JSON in markdown code blocks
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]  # Remove first line
        response_text = response_text.rsplit("```", 1)[0]  # Remove last ```

    return json.loads(response_text)


def compare(text_a: str, text_b: str, context: str = "general") -> dict:
    """
    Compare two versions of text for persuasiveness.
    Useful for A/B testing copy or evaluating before/after edits.
    """
    result_a = analyze(text_a, context)
    result_b = analyze(text_b, context)

    return {
        "version_a": result_a,
        "version_b": result_b,
        "winner": "A" if result_a["overall_score"] >= result_b["overall_score"] else "B",
        "score_delta": abs(result_a["overall_score"] - result_b["overall_score"]),
    }


def print_analysis(result: dict):
    """Pretty-print an analysis result to the console."""
    print(f"\n{'='*60}")
    print(f"  PERSUASION ANALYSIS — Overall Score: {result['overall_score']}/10")
    print(f"{'='*60}\n")

    print(f"  {result['summary']}\n")

    print(f"  {'DIMENSION':<20} {'SCORE':<8} EVIDENCE")
    print(f"  {'-'*56}")
    for dim, data in result["dimensions"].items():
        name = dim.replace("_", " ").title()
        bar = "█" * data["score"] + "░" * (10 - data["score"])
        print(f"  {name:<20} {bar} {data['score']}/10")
        print(f"  {'':20} {data['evidence'][:80]}")
        print()

    print(f"  TECHNIQUES DETECTED:")
    for t in result.get("techniques_detected", []):
        print(f"    • {t}")

    print(f"\n  WEAKNESSES:")
    for w in result.get("weaknesses", []):
        print(f"    ✗ {w}")

    print(f"\n  SUGGESTIONS:")
    for s in result.get("suggestions", []):
        print(f"    → {s}")

    print(f"\n{'='*60}")
    print(f"  SUGGESTED REWRITE")
    print(f"{'='*60}\n")
    print(f"  {result.get('rewrite', 'N/A')}\n")


# --- Run directly from command line ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1]) as f:
            text = f.read()
        context = sys.argv[2] if len(sys.argv) > 2 else "general"
    else:
        # Example: analyze a cold outreach email
        text = """
Hi,

I saw your company is hiring for ML engineers. I have experience in
machine learning and I think I would be a good fit. I have worked at
Amazon for several years and have a master's degree from CMU.

Can we set up a time to chat?

Thanks,
Varun
        """
        context = "cold outreach email to a hiring manager at an AI startup"

    print(f"\n  Analyzing text ({len(text.split())} words) as: {context}")
    print(f"  Calling Claude API...\n")

    result = analyze(text, context)
    print_analysis(result)
