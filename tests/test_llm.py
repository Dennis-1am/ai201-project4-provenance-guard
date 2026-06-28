import json
from unittest.mock import patch, MagicMock

# Import the function from your file (assuming your file is named llm.py)
from llm import llm_evaluator_engine

def create_mock_groq_response(confidence_score):
    """
    Helper function to simulate the exact object structure 
    returned by the Groq Python SDK.
    """
    mock_response = MagicMock()
    mock_message = MagicMock()
    
    # Simulate the JSON string that the LLM would return
    mock_message.content = json.dumps({"ai_confidence": confidence_score})
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    return mock_response

class TestLLMEvaluatorEngine:

    @patch('llm._client.chat.completions.create')
    def test_evaluator_returns_correct_float(self, mock_create):
        """Test that the function correctly parses a standard response."""
        # Arrange: Setup the mock to return a simulated response of 0.85
        mock_create.return_value = create_mock_groq_response(0.85)
        test_query = "Furthermore, in conclusion, this is an AI text."

        # Act
        result = llm_evaluator_engine(test_query)

        # Assert
        assert isinstance(result, float)
        assert result == 0.85
        mock_create.assert_called_once()

    @patch('llm._client.chat.completions.create')
    def test_evaluator_api_parameters(self, mock_create):
        """Test that the function passes the correct parameters to the Groq API."""
        mock_create.return_value = create_mock_groq_response(0.1)
        test_query = "Just some normal human text here."
        custom_model = "llama-3.1-8b-instant"

        # Act
        llm_evaluator_engine(test_query, model=custom_model)

        # Assert: Check that the API was called with the exact right model and messages
        mock_create.assert_called_once()
        call_kwargs = mock_create.call_args.kwargs
        
        assert call_kwargs["model"] == custom_model
        assert len(call_kwargs["messages"]) == 2
        assert call_kwargs["messages"][0]["role"] == "system"
        assert "Analyze the following text" in call_kwargs["messages"][1]["content"]

    @patch('llm._client.chat.completions.create')
    def test_evaluator_handles_zero_confidence(self, mock_create):
        """Test boundary condition: 0.0 confidence"""
        mock_create.return_value = create_mock_groq_response(0.0)
        
        result = llm_evaluator_engine("Total human.")
        
        assert result == 0.0

    @patch('llm._client.chat.completions.create')
    def test_evaluator_handles_max_confidence(self, mock_create):
        """Test boundary condition: 1.0 confidence"""
        mock_create.return_value = create_mock_groq_response(1.0)
        
        result = llm_evaluator_engine("Total AI.")
        
        assert result == 1.0