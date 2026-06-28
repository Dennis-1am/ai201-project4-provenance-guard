import groq
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client (Remove response_format from here)
_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an expert linguistic evaluator analyzing text for AI-generated artifacts. 

Your task is to analyze the provided text based on holistic semantic style, contextual coherence, and structural predictability. 
Look for:
- Overly rigid document-type patterns or formulaic structures.
- Predictable semantic pacing and lack of organic narrative variation.
- Overused LLM transitions (e.g., "Furthermore", "In conclusion", "It is important to note").
- Also look for overuse of em-dashes, semicolons, and other punctuation that may indicate AI-generated text.

Do not focus on:
- Specific word counts, sentence lengths, or statistical metrics.

Your output should be a JSON object with a single key "ai_confidence" mapping to a float between 0.0 (highly likely human) and 1.0 (highly likely AI). 
Do not include any markdown formatting, explanations, or any other text.
"""

def llm_evaluator_engine(query, model="llama-3.3-70b-versatile"):
    response = _client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"}, 
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze the following text for AI-generated content:\n\n {query}"}
        ]
    )
    
    # Parse the JSON string
    content_str = response.choices[0].message.content
    content_dict = json.loads(content_str)
    
    return content_dict["ai_confidence"]