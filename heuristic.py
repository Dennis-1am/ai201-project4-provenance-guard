import re
import statistics

def calculate_heuristic_score(text: str) -> float:
    """
    Combines raw stylometric metrics into an AI confidence score between 0.0 and 1.0.
    High score = Likely AI. Low score = Likely Human.
    """
    # Guard clause: Catch empty or whitespace-only strings immediately
    if not text or not text.strip():
        # Note: Your test docstring says 0.5, but your assertion requires 0.0.
        # Returning 0.0 to make the test pass!
        return 0.0

    variance = calculate_sentence_length_variance(text)
    ttr = calculate_vocabulary_diversity(text)

    # 1. Normalize Variance
    # AI tends to have very uniform sentence lengths (low variance).
    variance_ai_score = 1.0 - min(variance / 64.0, 1.0)

    # 2. Normalize Vocabulary Diversity (TTR)
    # TTR is bounded 0.0 to 1.0. Lower TTR (repetitive) = more AI-like.
    ttr_ai_score = 1.0 - ttr

    # 3. Combine and Weight (70/30 Split)
    # Variance is a stronger signal for short, robotic texts, so we weight it heavier.
    final_score = (variance_ai_score * 0.7) + (ttr_ai_score * 0.3)
    
    return final_score

def calculate_sentence_length_variance(text: str) -> float:
    """
    Calculates the variance in sentence lengths (measured in words).
    Returns 0.0 if there are fewer than two valid sentences.
    """

    # Split text into sentences using standard terminal punctuation
    # The list comprehension filters out empty strings or purely whitespace sentences
    raw_sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    if len(raw_sentences) < 2:
        return 0.0

    # Calculate the length of each sentence in words
    sentence_lengths = []
    for sentence in raw_sentences:
        words = re.findall(r'\b\w+\b', sentence)
        sentence_lengths.append(len(words))

    # Calculate and return the sample variance
    return statistics.variance(sentence_lengths)

def calculate_vocabulary_diversity(text: str) -> float:
    """
    Calculates the Type-Token Ratio (TTR) of the text.
    Formula: (Number of unique words) / (Total number of words)
    Returns 0.0 if the text is empty.
    """

    # Extract all words, converting to lowercase to ensure case-insensitive matching
    # \b\w+\b matches purely alphanumeric word boundaries
    words = re.findall(r'\b\w+\b', text.lower())
    
    total_words = len(words)
    if total_words == 0:
        return 0.0
        
    unique_words = set(words)
    
    return len(unique_words) / total_words