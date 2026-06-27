import unittest

from heuristic import stylometric_heuristic_engine

class TestStylometricHeuristicEngine(unittest.TestCase):

    def test_empty_string(self):
        """Test that empty or whitespace-only strings return a neutral 0.5."""
        self.assertEqual(stylometric_heuristic_engine(""), 0.5)
        self.assertEqual(stylometric_heuristic_engine("   \n\t  "), 0.5)

    def test_single_sentence(self):
        """Test that a single sentence does not crash the variance calculation."""
        text = "This is just one single sentence with no variance."
        score = stylometric_heuristic_engine(text)
        self.assertIsInstance(score, float)
        self.assertTrue(0.0 <= score <= 1.0)

    def test_highly_uniform_ai(self):
        """Test that repetitive, uniform text scores high for AI likelihood."""
        text = (
            "The system provides a clear benefit. The user can log in easily. "
            "The data is processed quickly. The results are shown on the screen. "
            "The application is very secure. The performance is consistently high."
        )
        score = stylometric_heuristic_engine(text)
        # We expect a score heavily leaning toward AI (e.g., > 0.6)
        self.assertGreater(score, 0.6)

    def test_erratic_human(self):
        """Test that varied sentence lengths and rich vocabulary score low (Human)."""
        text = (
            "I've always thought that rain in the city smells entirely different than rain in the woods. "
            "It's metallic, somehow. Sharp. But out here? Out here it just smells like dirt and pine needles, "
            "which is a cliché, I know, but it's true anyway."
        )
        score = stylometric_heuristic_engine(text)
        # We expect a score heavily leaning toward Human (e.g., < 0.4)
        self.assertLess(score, 0.4)

    def test_edge_case_minimalist_poetry(self):
        """
        Test the anticipated edge case: Minimalist poetry with repetitive structures.
        This should artificially inflate the score past 0.40.
        """
        text = (
            "The sun goes down. The moon comes up. The sun goes down. The moon comes up. "
            "We sleep in the dark. We wake in the light. The sun goes down."
        )
        score = stylometric_heuristic_engine(text)
        self.assertGreaterEqual(score, 0.40)

    def test_edge_case_formal_human(self):
        """
        Test the anticipated edge case: Formal human writing (legal/instructional) 
        which intentionally uses uniform patterns and lacks diversity.
        """
        text = (
            "All employees must submit the required documentation by Friday. "
            "Failure to submit documentation will result in a penalty. "
            "The documentation must be signed by a supervisor. "
            "Please review the documentation guidelines prior to submission."
        )
        score = stylometric_heuristic_engine(text)
        # Expect this to falsely lean toward AI due to structural rigidity
        self.assertGreater(score, 0.5)

if __name__ == '__main__':
    unittest.main()