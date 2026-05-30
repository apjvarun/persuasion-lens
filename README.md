# PersuasionLens

AI-powered writing persuasiveness analyzer built on persuasion science — combining Aristotle's rhetorical framework (ethos, pathos, logos) with Cialdini's principles of influence.

Paste any text — cold emails, LinkedIn posts, product pitches, cover letters — and get:
- **Overall persuasiveness score** (1-10)
- **Dimension breakdown** across 6 persuasion axes
- **Technique detection** (what's working)
- **Weakness identification** (what's missing)
- **Actionable suggestions** for improvement
- **AI-generated rewrite** that scores higher

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run the CLI analyzer
python analyzer.py

# Or launch the web app
streamlit run app.py
```

## Usage

### CLI
```python
from analyzer import analyze

result = analyze(
    text="Your email or pitch text here...",
    context="cold outreach email"
)
print(result["overall_score"])  # 1-10
print(result["suggestions"])    # actionable improvements
print(result["rewrite"])        # improved version
```

### A/B Comparison
```python
from analyzer import compare

result = compare(version_a, version_b, context="linkedin post")
print(f"Winner: Version {result['winner']}")
```

## How It Works

The analyzer evaluates text across six dimensions:

| Dimension | What It Measures |
|-----------|-----------------|
| **Ethos** | Credibility, authority, trustworthiness |
| **Pathos** | Emotional appeal, connection, storytelling |
| **Logos** | Logic, evidence, data, reasoning |
| **Social Proof** | References to others' actions, testimonials |
| **Scarcity/Urgency** | Time pressure, limited availability |
| **Clarity** | Readability, structure, call-to-action |

## Background

This project is inspired by peer-reviewed research on quantifying the persuasiveness of user-authored content, published at the International Workshop on Artificial Intelligence in Affective Computing (PMLR, 2019). See [Research Background](docs/research-background.md) for a deep dive into the science behind PersuasionLens and how it evolved from a statistical model analyzing 3 million consumer interactions into an LLM-powered real-time writing assistant.

## License

MIT
