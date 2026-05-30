# Research Background: The Science Behind PersuasionLens

## Origin Story

PersuasionLens is directly inspired by peer-reviewed research on quantifying persuasiveness of user-authored content, conducted at **Adobe Research** and published at the **3rd International Workshop on Artificial Intelligence in Affective Computing (MLR Press, 2019)**.

> **Paper:** [Persuasion: What Jane Austen Would Have Written](https://proceedings.mlr.press/v122/sinha20a/sinha20a.pdf)
>
> **Authors:** Moumita Sinha, Jennifer Healey, Faran Ahmad, Varun Gupta, Niloy Ganguly
>
> **Venue:** Proceedings of Machine Learning Research, Volume 122, Pages 36-43

---

## What the Research Found

The paper developed an algorithmic approach to computing a real-time **"Persuasion Score"** for digital marketing content, grounded in Aristotle's three modes of persuasion:

| Mode | What It Captures | Features Used in the Study |
|------|-----------------|---------------------------|
| **Pathos** (Emotion) | Emotional connection with the audience | Image memorability, 12 image aesthetics features (symmetry, vivid color, interesting lighting, etc.) |
| **Ethos** (Credibility) | Trustworthiness of the communicator | Text readability, text formality, text sentiment |
| **Logos** (Logic) | Logical structure and reasoning | Image proportion, layout position |

### Key Findings

1. **Text readability and formality matter** — Higher readability and formality scores correlate with higher persuasion scores.
2. **Image position matters** — Content placed higher in the layout is more persuasive; bottom-positioned content has significantly lower engagement.
3. **Image proportion matters** — Larger images relative to the overall content are more persuasive.
4. **Symmetry and lighting** — Images with higher symmetry and interesting lighting are more persuasive.
5. **Consumer context matters** — The same content persuades different consumers differently based on their engagement history (recency of opens, clicks, registration tenure).

### Scale of the Study

- **~3 million** consumer interactions analyzed
- **~400** unique marketing images
- **~14,000** balanced training data points
- Logistic regression model with interaction features between content and consumer attributes

---

## From Research to PersuasionLens

The original research focused on **email marketing content** and required access to consumer interaction data. PersuasionLens takes the core scientific framework and makes it accessible for **any type of writing**:

| Original Research (2019) | PersuasionLens (2026) |
|--------------------------|----------------------|
| Email marketing content only | Any text: emails, pitches, LinkedIn posts, cover letters |
| Required consumer click data | Works on the text alone using LLM reasoning |
| Pathos, Ethos, Logos only | Adds Cialdini's principles: Social Proof, Scarcity/Urgency, Clarity |
| Batch analysis (offline) | Real-time analysis with instant feedback |
| Statistical model (logistic regression) | Claude API for nuanced, context-aware analysis |
| Score only | Score + technique detection + weakness identification + actionable rewrite |

The evolution from a statistical model to an LLM-powered analyzer preserves the scientific rigor of the persuasion framework while making it practical for everyday use.

---

## References

- Sinha, M., Healey, J., Ahmad, F., Gupta, V., & Ganguly, N. (2019). *Persuasion: What Jane Austen Would Have Written.* Proceedings of Machine Learning Research, 122, 36-43.
- Kennedy, G. A. (2008). *The Art of Rhetoric in the Roman World.* Wipf and Stock Publishers.
- Cialdini, R. B. (2006). *Influence: The Psychology of Persuasion.* Harper Business.
- Maslansky, M., West, S., DeMoss, G., & Saylor, D. (2010). *The Language of Trust.* Penguin.
