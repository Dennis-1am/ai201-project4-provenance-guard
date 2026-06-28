## Architecture Narrative

A single piece of text will first be sent via a `POST /submit` request to the Flask API Gateway. Before the text is processed, the request will hit the **Defensive Layer**, which consists solely of *Flask-Limiter*. It will evaluate the request and, if it exceeds the threshold, reject it immediately and log the failure.

If cleared, the gateway will forward the entire payload to the **Multi-Signal Detection Pipeline**. Inside the pipeline, the text is parsed by two components: the **GROQ LLM Evaluator**, which analyzes the semantic style and returns an AI confidence score, and the **Stylometric Heuristic Engine**, a cheap and fast function that uses sentence length variance and vocabulary diversity to output its own confidence score.

These two scores are then passed to the **Scoring Engine**, which blends them into a final calibrated confidence percentage. This score is then passed to the **Label Mapping** function, which returns the appropriate label against defined thresholds.

Once a final transparency label is outputted alongside the submitted text, the user can submit a structured request containing the text they want to appeal, their appeal reason, and what it was originally labeled as. Each submission endpoint response is logged, the system will log the final label decision, confidence score, signals used, and any appeals. These logs can be retrieved via the `GET /log` endpoint.

&nbsp;
### API Surface
---

Endpoint | Accepts (JSON Payload) | Returns (JSON Response)
:--- | :--- | :---
`POST /submit` | `text`: string <br> `creator_id`: string | `content_id`: string <br> `attribution`: string <br> `confidence`: float <br> `label`: string
`POST /appeal` | `content_id`: string <br> `creator_reasoning`: string | `status`: "under_review" <br> `message`: string
`GET /log` | _Not Applicable_ | `entries`: array of log objects <br> *(Each: timestamp, content_id, scores, status, appeal)*

&nbsp;
### Architecture Diagram
---
Flow 1: Submission Flow
```mermaid
graph TD
    %% Flow 1: Submission Flow
    A[POST /submit] -->|&nbsp;Raw Text&nbsp;| B(Signal 1: Stylometric Heuristics Engine)
    A --> |&nbsp;Raw Text&nbsp;| C(Signal 2: GROQ LLM)
    B --> |&nbsp;Signal Score&nbsp;| D(Scoring Engine)
    C --> |&nbsp;Signal Score&nbsp;| D
    D --> |&nbsp;Combined Score&nbsp;| E(Label Mapping)
    E --> |&nbsp;Transparency Label&nbsp;| F(Audit Log)
    F --> |&nbsp;JSON Response&nbsp;| G[User View]
```

Flow 2: Appeal Flow
```mermaid
graph TD
    %% Flow 2: Appeal Flow
    H[POST /appeal] -->|&nbsp;Content ID + Reason&nbsp;| I(Update Status to 'under_review')
    I -->|&nbsp;Log Appeal Data&nbsp;| J(Audit Log)
    J -->|&nbsp;JSON Response&nbsp;| K[User View]
```

&nbsp;
### Detection Signals
---

1. **Stylometric Heuristic Engine**
* **What it measures:** Sentence length variance and vocabulary diversity (Type-Token Ratio).
* **Why it differs:** AI-generated text tends to be highly uniform and statistically consistent, leading to lower sentence length variance and less vocabulary diversity. Human writing is naturally more erratic, varied, and structurally unpredictable.
* **Blind Spots:** It completely lacks semantic understanding. It fails on highly structured, formal human writing—such as legal documentation, instruction manuals, or textbooks—which are intentionally uniform and repetitive, leading to false positives.
* **Output:** A confidence score between 0 - 1, calculated by the average of the sentence length variance & vocabulary diversity.

2. **GROQ LLM Evaluator**
* **What it measures:** Holistic semantic style, contextual coherence, and document-type patterns.
* **Why it differs:** It acts as a holistic evaluator, identifying complex, high-level structural artifacts, overused transitions, and predictable semantic pacing common to LLM outputs.
* **Blind Spots:** It struggles with precise statistical breakdowns. It cannot accurately calculate exact numerical variances on the fly and can easily be fooled by lightly edited AI content or unusually rigid, template-driven human writing.
* **Output:** A confidence score between 0 - 1

&nbsp;
### Rate Limiting

* Run this code in terminal to test the rate limit
```
for i in $(seq 1 12); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:5000/submit \
    -H "Content-Type: application/json" \
    -d '{"text": "This is a test submission for rate limit testing purposes only.", "creator_id": "ratelimit-test"}'
done
```

* Should expect this output
```
200
200
200
200
200
200
200
200
200
200
429
429
```

## Log Entries

```json
{
    "entries": [
        {
            "appeal_reasoning": null,
            "content_id": "eeb009f2-a360-47b1-affd-df491c9b9f71",
            "creator_id": "test-user-ai-1",
            "label": "\ud83e\udd16 *Automated System Verdict:* \"Highly likely to be AI-generated.\"",
            "scores": {
                "final": 0.717498183139535,
                "groq_llm": 0.8,
                "heuristic": 0.24998788759689916
            },
            "status": "High-Confidence AI",
            "timestamp": "2026-06-28T19:19:41.396377+00:00"
        },
        {
            "appeal_reasoning": "I believe my submission was incorrectly flagged as AI-generated. I would like to request a review of",
            "content_id": "ff0f3df6-a975-431e-a7a6-121771e28d1d",
            "creator_id": "test-user-me",
            "label": "\u26a0\ufe0f *Uncertain:* \"Mixed signals detected. This content is under review.\"",
            "scores": {
                "final": 0.5450121268656717,
                "groq_llm": 0.6,
                "heuristic": 0.2334141791044776
            },
            "status": "Under Review",
            "timestamp": "2026-06-28T19:05:43.049348+00:00"
        },
        {
            "appeal_reasoning": null,
            "content_id": "ff0f3df6-a975-431e-a7a6-121771e28d1d",
            "creator_id": "test-user-me",
            "label": "\u26a0\ufe0f *Uncertain:* \"Mixed signals detected. This content is under review.\"",
            "scores": {
                "final": 0.5450121268656717,
                "groq_llm": 0.6,
                "heuristic": 0.2334141791044776
            },
            "status": "Uncertain",
            "timestamp": "2026-06-28T19:04:35.132733+00:00"
        }
    ]
}
```
