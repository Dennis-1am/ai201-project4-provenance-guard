import re
import statistics

def stylometric_heuristic_engine(text: str) -> float:
    """
    Analyzes sentence length variance and vocabulary diversity.
    Returns a confidence score between 0.0 (Human) and 1.0 (AI).
    """
    if not text.strip():
        return 0.5  # Neutral/Uncertain for empty strings
    
    # 1. Tokenization and Setup
    words = re.findall(r'\b\w+\b', text.lower())
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    if len(words) == 0 or len(sentences) == 0:
        return 0.5
        
    # 2. Vocabulary Diversity (Type-Token Ratio)
    # TTR = Unique Words / Total Words
    unique_words = set(words)
    ttr = len(unique_words) / len(words)
    
    # Invert TTR for AI confidence: Lower diversity -> Higher AI likelihood
    ai_score_ttr = 1.0 - ttr 

    # 3. Sentence Length Variance
    sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    
    if len(sentence_lengths) > 1:
        variance = statistics.variance(sentence_lengths)
    else:
        variance = 0.0
        
    # Normalize variance to a 0-1 scale. 
    # (Note: 40.0 is an initial baseline threshold for high variance, tune as needed during testing)
    normalized_variance = min(variance / 40.0, 1.0)
    
    # Invert Variance for AI confidence: Lower variance -> Higher AI likelihood
    ai_score_variance = 1.0 - normalized_variance
    
    # 4. Final Calculation: Average of both metrics
    confidence_score = (ai_score_ttr + ai_score_variance) / 2.0
    
    return round(confidence_score, 4)