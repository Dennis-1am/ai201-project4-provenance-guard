from heuristic import calculate_heuristic_score, calculate_sentence_length_variance, calculate_vocabulary_diversity
from llm import llm_evaluator_engine

heuristic_weight = 0.15
llm_weight = 0.85

def score_text(text: str) -> float:
    """
    Scores the text based on a combination of heuristic and LLM evaluations.
    Returns a float score between 0.0 and 1.0.
    """
    if not text or not text.strip():
        return 0.0

    heuristic_score = calculate_heuristic_score(text)
    groq_confidence = llm_evaluator_engine(text)
    
    # Use weighted average for now, but could be adjusted in the future
    final_confidence = (heuristic_score * heuristic_weight) + (groq_confidence * llm_weight)

    return heuristic_score, groq_confidence, final_confidence

def get_status_label(score: float) -> dict:
    """Map the AI confidence score to its status and label."""
    if score >= 0.70:
        return {
            "status": "High-Confidence AI",
            "label": '🤖 *Automated System Verdict:* "Highly likely to be AI-generated."'
        }
    elif score >= 0.40:
        return {
            "status": "Uncertain",
            "label": '⚠️ *Uncertain:* "Mixed signals detected. This content is under review."'
        }
    else:
        return {
            "status": "High-Confidence Human",
            "label": '✍️ *Verified Style:* "Highly likely to be original human writing."'
        }