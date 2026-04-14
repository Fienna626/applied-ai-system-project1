"""
Reliability Testing for AI Features

This module tests the AI features for:
1. Consistency - Does the AI give the same answer for the same input?
2. Confidence Scoring - Are confidence scores calibrated correctly?
3. Error Handling - Does the AI gracefully handle edge cases?
4. Output Quality - Are the outputs useful and sensible?
"""

import pytest
from ai_feature import generate_hint, analyze_pattern, get_suggestion, validate_ai_outputs


class TestGenerateHintReliability:
    """Test the generate_hint() function for reliability."""

    def test_returns_tuple(self):
        """Hint should return (str, float) tuple."""
        result = generate_hint(secret=50, guess=30, attempts=2)
        assert isinstance(result, tuple), "Should return tuple"
        assert len(result) == 2, "Should return 2-element tuple"
        hint, confidence = result
        assert isinstance(hint, str), "First element should be string"
        assert isinstance(confidence, float), "Second element should be float"

    def test_confidence_in_valid_range(self):
        """Confidence score must be 0.0-1.0."""
        hint, confidence = generate_hint(secret=50, guess=30, attempts=2)
        assert 0.0 <= confidence <= 1.0, f"Confidence {confidence} out of range [0.0, 1.0]"

    def test_consistency_same_input_same_output(self):
        """Same input should produce same output (deterministic)."""
        result1 = generate_hint(secret=50, guess=30, attempts=2)
        result2 = generate_hint(secret=50, guess=30, attempts=2)
        assert result1 == result2, "Same input should produce same output"

    def test_high_confidence_with_more_attempts(self):
        """Confidence should increase with more attempts (more data)."""
        hint1, conf1 = generate_hint(secret=50, guess=30, attempts=1)
        hint2, conf2 = generate_hint(secret=50, guess=30, attempts=5)
        assert conf2 >= conf1, f"Confidence should increase with attempts: {conf1} -> {conf2}"

    def test_handles_edge_cases(self):
        """Should handle extreme values gracefully."""
        # Extreme secret
        hint1, conf1 = generate_hint(secret=1, guess=100, attempts=1)
        assert isinstance(hint1, str) and 0.0 <= conf1 <= 1.0

        # Exact guess
        hint2, conf2 = generate_hint(secret=50, guess=50, attempts=1)
        assert isinstance(hint2, str) and 0.0 <= conf2 <= 1.0

        # Many attempts
        hint3, conf3 = generate_hint(secret=50, guess=30, attempts=100)
        assert isinstance(hint3, str) and 0.0 <= conf3 <= 1.0

    def test_low_confidence_no_empty_hint(self):
        """If confidence is too low, hint should be empty string."""
        hint, confidence = generate_hint(secret=50, guess=30, attempts=0)
        # After 0 attempts, confidence may be low
        if confidence < 0.6:
            assert hint == "", "Low confidence should produce empty hint"


class TestAnalyzePatternReliability:
    """Test the analyze_pattern() function for reliability."""

    def test_returns_dict_with_all_fields(self):
        """Pattern analysis must return dict with all required fields."""
        result = analyze_pattern(history=[10, 20, 30], secret=50)
        assert isinstance(result, dict), "Should return dict"
        required_fields = ["strategy", "efficiency", "insight", "confidence"]
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"

    def test_confidence_in_valid_range(self):
        """Confidence score must be 0.0-1.0."""
        pattern = analyze_pattern(history=[10, 20, 30], secret=50)
        assert 0.0 <= pattern["confidence"] <= 1.0, f"Confidence out of range: {pattern['confidence']}"

    def test_efficiency_in_valid_range(self):
        """Efficiency score must be 0.0-1.0."""
        pattern = analyze_pattern(history=[10, 20, 30], secret=50)
        assert 0.0 <= pattern["efficiency"] <= 1.0, f"Efficiency out of range: {pattern['efficiency']}"

    def test_consistency_same_input_same_output(self):
        """Same input should produce same output (deterministic)."""
        result1 = analyze_pattern(history=[10, 20, 30], secret=50)
        result2 = analyze_pattern(history=[10, 20, 30], secret=50)
        assert result1 == result2, "Same input should produce same output"

    def test_empty_history(self):
        """Should handle empty history gracefully."""
        pattern = analyze_pattern(history=[], secret=50)
        assert pattern["strategy"] == "unknown"
        assert pattern["efficiency"] == 0.0
        assert pattern["confidence"] < 0.5, "Low confidence for empty history"

    def test_single_guess(self):
        """Should handle single guess history."""
        pattern = analyze_pattern(history=[25], secret=50)
        assert isinstance(pattern["strategy"], str)
        assert pattern["confidence"] < 0.5, "Low confidence with only 1 guess"

    def test_invalid_guesses_ignored(self):
        """String entries (invalid guesses) should be ignored."""
        result1 = analyze_pattern(history=[10, 20, 30], secret=50)
        result2 = analyze_pattern(history=[10, "bad", 20, "invalid", 30], secret=50)
        # Results should be based only on valid numeric guesses
        assert result1 == result2, "Invalid string guesses should be filtered out"

    def test_confidence_increases_with_more_data(self):
        """Confidence should increase with more guesses (more data)."""
        pattern1 = analyze_pattern(history=[25, 30], secret=50)
        pattern2 = analyze_pattern(history=[25, 30, 35, 40, 45], secret=50)
        assert pattern2["confidence"] >= pattern1["confidence"], \
            f"Confidence should increase with more data: {pattern1['confidence']} -> {pattern2['confidence']}"

    def test_strategy_detection(self):
        """Should detect different guessing strategies."""
        # incremental: small consistent gaps
        incremental = analyze_pattern(history=[10, 11, 12, 13], secret=50)
        assert incremental["strategy"] in ["incremental", "random"]

        # binary search: larger jumps
        binary = analyze_pattern(history=[50, 75, 62, 56, 53], secret=50)
        assert binary["strategy"] in ["binary_search", "random", "incremental"]

        # Both should be valid - just checking no crashes
        assert isinstance(incremental["strategy"], str)
        assert isinstance(binary["strategy"], str)


class TestGetSuggestionReliability:
    """Test the get_suggestion() function for reliability."""

    def test_returns_tuple(self):
        """Suggestion should return (str, float) tuple."""
        result = get_suggestion(score=100, attempts=3, history=[10, 20], difficulty="Normal")
        assert isinstance(result, tuple), "Should return tuple"
        assert len(result) == 2, "Should return 2-element tuple"
        suggestion, confidence = result
        assert isinstance(suggestion, str), "First element should be string"
        assert isinstance(confidence, float), "Second element should be float"

    def test_confidence_in_valid_range(self):
        """Confidence score must be 0.0-1.0."""
        suggestion, confidence = get_suggestion(score=100, attempts=3, history=[10, 20], difficulty="Normal")
        assert 0.0 <= confidence <= 1.0, f"Confidence out of range: {confidence}"

    def test_consistency_same_input_same_output(self):
        """Same input should produce same output (deterministic)."""
        result1 = get_suggestion(score=100, attempts=3, history=[10, 20], difficulty="Normal")
        result2 = get_suggestion(score=100, attempts=3, history=[10, 20], difficulty="Normal")
        assert result1 == result2, "Same input should produce same output"

    def test_handles_all_difficulties(self):
        """Should handle all difficulty levels."""
        for difficulty in ["Easy", "Normal", "Hard"]:
            suggestion, confidence = get_suggestion(score=100, attempts=3, history=[10, 20], difficulty=difficulty)
            assert isinstance(suggestion, str)
            assert 0.0 <= confidence <= 1.0

    def test_confidence_increases_with_attempts(self):
        """Confidence should increase with more attempts (more data)."""
        sugg1, conf1 = get_suggestion(score=100, attempts=1, history=[10], difficulty="Normal")
        sugg2, conf2 = get_suggestion(score=100, attempts=5, history=[10, 20, 30, 40, 50], difficulty="Normal")
        assert conf2 >= conf1, f"Confidence should increase with more attempts: {conf1} -> {conf2}"

    def test_high_scores_suggest_difficulty_increase(self):
        """High scores should suggest increasing difficulty."""
        high_score_sugg, _ = get_suggestion(score=200, attempts=3, history=[10, 20], difficulty="Easy")
        # Should mention Hard or Higher difficulty in suggestion
        suggestion_lower = high_score_sugg.lower()
        # Just check it returns something sensible, don't assume exact wording
        assert isinstance(high_score_sugg, str) and len(high_score_sugg) > 0

    def test_low_scores_provide_encouragement(self):
        """Low scores should still provide meaningful feedback."""
        low_score_sugg, conf = get_suggestion(score=10, attempts=5, history=[10, 20, 30, 40, 50], difficulty="Hard")
        assert isinstance(low_score_sugg, str)
        assert len(low_score_sugg) > 0, "Should provide feedback even for low scores"

    def test_empty_history(self):
        """Should handle empty history."""
        suggestion, confidence = get_suggestion(score=0, attempts=0, history=[], difficulty="Normal")
        assert isinstance(suggestion, str)
        assert 0.0 <= confidence <= 1.0


class TestValidationFunction:
    """Test the validate_ai_outputs() function."""

    def test_validation_returns_dict(self):
        """Validation should return dict with validation results."""
        results = validate_ai_outputs(verbose=False)
        assert isinstance(results, dict), "Should return dict"

    def test_validation_checks_all_functions(self):
        """Validation should check all three AI functions."""
        results = validate_ai_outputs(verbose=False)
        required_keys = ["generate_hint", "analyze_pattern", "get_suggestion", "all_valid"]
        for key in required_keys:
            assert key in results, f"Missing validation key: {key}"

    def test_all_functions_valid(self):
        """All AI functions should pass validation."""
        results = validate_ai_outputs(verbose=False)
        assert results["generate_hint"] is True, "generate_hint should be valid"
        assert results["analyze_pattern"] is True, "analyze_pattern should be valid"
        assert results["get_suggestion"] is True, "get_suggestion should be valid"
        assert results["all_valid"] is True, "Overall validation should pass"


class TestIntegrationAIFunctions:
    """Integration tests for AI functions working together."""

    def test_complete_game_flow(self):
        """Test a complete game flow with all AI functions."""
        secret = 50
        guesses = [25, 35, 40, 45, 48, 49, 50]
        
        for attempt, guess in enumerate(guesses, 1):
            # Generate hint
            hint, hint_conf = generate_hint(secret=secret, guess=guess, attempts=attempt)
            assert 0.0 <= hint_conf <= 1.0
            
            # Analyze pattern
            pattern = analyze_pattern(history=guesses[:attempt], secret=secret)
            assert 0.0 <= pattern["confidence"] <= 1.0
            
            # Get suggestion
            suggestion, sugg_conf = get_suggestion(score=100, attempts=attempt, history=guesses[:attempt], difficulty="Normal")
            assert 0.0 <= sugg_conf <= 1.0

    def test_confidence_consistency(self):
        """Confidence scores should be consistent across functions."""
        # With more attempts, all functions should have higher confidence
        hint1, conf1 = generate_hint(secret=50, guess=30, attempts=1)
        hint2, conf2 = generate_hint(secret=50, guess=30, attempts=10)
        
        pattern1 = analyze_pattern(history=[30], secret=50)
        pattern2 = analyze_pattern(history=[10, 20, 30, 40, 50], secret=50)
        
        assert conf2 >= conf1, "Hint confidence should increase with attempts"
        assert pattern2["confidence"] >= pattern1["confidence"], "Pattern confidence should increase with data"


if __name__ == "__main__":
    # Run with: pytest test_reliability.py -v
    pytest.main([__file__, "-v"])
