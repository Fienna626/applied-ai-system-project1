"""
AI Feature Module: Clean integration points for AI-powered enhancements.

This module provides hooks for AI features to integrate with the game logic.
AI features should:
  1. Accept only data (not UI state)
  2. Return structured results with confidence scores
  3. Never modify game state directly
  4. Log all outputs for reliability measurement
"""

import logging
from typing import Dict, Tuple

# Configure logging for AI reliability tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ai_logger = logging.getLogger("ai_feature")


def generate_hint(secret: int, guess: int, attempts: int) -> Tuple[str, float]:
    """
    Generate an AI-powered hint based on current game state.
    
    Args:
        secret: The secret number to guess
        guess: The player's current guess
        attempts: Number of attempts made so far
    
    Returns:
        Tuple of (hint_message, confidence_score)
        - hint_message: A hint for the player (empty string if not confident)
        - confidence_score: 0.0-1.0 indicating confidence in the hint
    
    Example:
        hint, confidence = generate_hint(secret=50, guess=30, attempts=2)
        # Could return: ("You're getting closer!", 0.85)
        # Confidence would be low if hints aren't reliable yet
    """
    try:
        # Basic hint logic: distance-based confidence
        distance = abs(secret - guess)
        
        # Confidence decreases if we're uncertain
        # Higher attempts = more data = higher confidence
        confidence = min(0.7 + (attempts * 0.05), 0.95)
        
        # Only give hints if confident enough
        if confidence < 0.6:
            hint = ""
            ai_logger.debug(f"Hint not confident enough (confidence={confidence:.2f})")
        elif distance > 30:
            hint = f"You're {distance} away. Keep searching!"
            ai_logger.info(f"Generated distance-based hint with confidence {confidence:.2f}")
        else:
            hint = "You're very close! Keep narrowing it down."
            ai_logger.info(f"Generated proximity hint with confidence {confidence:.2f}")
        
        ai_logger.debug(f"Hint: '{hint}' (secret={secret}, guess={guess}, confidence={confidence:.2f})")
        return hint, confidence
        
    except Exception as e:
        ai_logger.error(f"Error generating hint: {e}", exc_info=True)
        return "", 0.0


def analyze_pattern(history: list, secret: int) -> Dict:
    """
    Analyze the user's guessing pattern for insights.
    
    Args:
        history: List of all guesses made (ints) or invalid inputs (strings)
        secret: The secret number (for analysis only, not revealed)
    
    Returns:
        Dictionary with pattern insights:
        {
            "strategy": "binary_search" | "random" | "incremental" | "unknown",
            "efficiency": 0.0-1.0,
            "insight": "string description",
            "confidence": 0.0-1.0
        }
    
    Example:
        pattern = analyze_pattern(history=[5, 15, 25, 30, 28], secret=50)
        # Could return: {
        #     "strategy": "incremental",
        #     "efficiency": 0.4,
        #     "insight": "You're guessing in small steps. Try jumping further!",
        #     "confidence": 0.75
        # }
    """
    try:
        if not history:
            return {
                "strategy": "unknown",
                "efficiency": 0.0,
                "insight": "",
                "confidence": 0.0
            }
        
        # Filter out invalid guesses (strings)
        valid_guesses = [g for g in history if isinstance(g, int)]
        
        if len(valid_guesses) < 2:
            ai_logger.debug("Not enough valid guesses to analyze pattern")
            return {
                "strategy": "unknown",
                "efficiency": 0.0,
                "insight": "",
                "confidence": 0.3
            }
        
        # Analyze gaps between guesses
        gaps = [abs(valid_guesses[i+1] - valid_guesses[i]) for i in range(len(valid_guesses)-1)]
        avg_gap = sum(gaps) / len(gaps) if gaps else 0
        
        # Detect strategy
        if all(g < 50 for g in gaps):  # Consistent, small gaps
            strategy = "incremental"
            confidence = 0.8
        elif any(g > 30 for g in gaps):  # Some large jumps
            strategy = "binary_search"
            confidence = 0.7
        else:
            strategy = "random"
            confidence = 0.5
        
        # Calculate efficiency (how close to optimal for finding secret)
        optimal_attempts = 1 + int(__import__('math').log2(100))  # ~7 for range 1-100
        efficiency = min(1.0, optimal_attempts / len(valid_guesses))
        
        # Generate insight
        if strategy == "incremental" and efficiency < 0.5:
            insight = "💡 Try bigger jumps! Binary search is faster."
        elif strategy == "random" and efficiency > 0.7:
            insight = "🎯 Great random strategy! You're lucky or skilled."
        else:
            insight = f"📊 Your strategy: {strategy}"
        
        result = {
            "strategy": strategy,
            "efficiency": round(efficiency, 2),
            "insight": insight,
            "confidence": confidence
        }
        
        ai_logger.info(f"Pattern analysis: strategy={strategy}, efficiency={efficiency:.2f}, confidence={confidence:.2f}")
        return result
        
    except Exception as e:
        ai_logger.error(f"Error analyzing pattern: {e}", exc_info=True)
        return {
            "strategy": "unknown",
            "efficiency": 0.0,
            "insight": "",
            "confidence": 0.0
        }


def get_suggestion(score: int, attempts: int, history: list, difficulty: str) -> Tuple[str, float]:
    """
    Get an AI suggestion for the player's next move or difficulty adjustment.
    
    Args:
        score: Current player score
        attempts: Number of attempts made so far
        history: List of all guesses
        difficulty: Current difficulty level
    
    Returns:
        Tuple of (suggestion_message, confidence_score)
        - suggestion_message: A suggestion for the player
        - confidence_score: 0.0-1.0 indicating confidence in suggestion
    
    Example:
        suggestion, confidence = get_suggestion(score=100, attempts=3, history=[...], difficulty="Normal")
        # Could return: ("You're doing great! Try Hard mode.", 0.82)
    """
    try:
        valid_guesses = [g for g in history if isinstance(g, int)]
        num_guesses = len(valid_guesses)
        
        # Base confidence on data points
        confidence = min(0.5 + (num_guesses * 0.1), 0.9)
        
        # Generate suggestion based on performance
        if score > 150 and difficulty != "Hard":
            suggestion = "🚀 You're crushing it! Try Hard mode for more challenge."
            confidence = min(confidence, 0.85)
        elif score < 50 and num_guesses < 5:
            suggestion = "💪 Keep playing! You'll get better with practice."
            confidence = min(confidence, 0.7)
        elif attempts > 6 and difficulty == "Hard":
            suggestion = "🤔 Hard mode is tough! Normal mode might be more fun."
            confidence = min(confidence, 0.6)
        else:
            suggestion = "📈 Play another round to improve your score!"
            confidence = min(confidence, 0.75)
        
        ai_logger.info(f"Suggestion: '{suggestion}' (confidence={confidence:.2f}, score={score})")
        return suggestion, confidence
        
    except Exception as e:
        ai_logger.error(f"Error generating suggestion: {e}", exc_info=True)
        return "", 0.0


def validate_ai_outputs(verbose: bool = False) -> Dict[str, bool]:
    """
    Validate that all AI features work without errors.
    
    Args:
        verbose: If True, print detailed results
    
    Returns:
        Dictionary with validation results:
        {
            "generate_hint": bool,
            "analyze_pattern": bool,
            "get_suggestion": bool,
            "all_valid": bool
        }
    """
    results = {}
    
    try:
        # Test generate_hint
        hint, conf = generate_hint(secret=50, guess=30, attempts=1)
        assert isinstance(hint, str), "Hint must be string"
        assert 0.0 <= conf <= 1.0, "Confidence must be 0.0-1.0"
        results["generate_hint"] = True
        if verbose:
            print(f"✓ generate_hint: hint='{hint}', confidence={conf:.2f}")
    except Exception as e:
        results["generate_hint"] = False
        if verbose:
            print(f"✗ generate_hint failed: {e}")
        ai_logger.error(f"Validation failed for generate_hint: {e}")
    
    try:
        # Test analyze_pattern
        pattern = analyze_pattern(history=[10, 20, 30, 40], secret=50)
        assert isinstance(pattern, dict), "Pattern must be dict"
        assert "confidence" in pattern, "Pattern must have confidence"
        assert 0.0 <= pattern["confidence"] <= 1.0, "Confidence must be 0.0-1.0"
        results["analyze_pattern"] = True
        if verbose:
            print(f"✓ analyze_pattern: strategy={pattern['strategy']}, confidence={pattern['confidence']:.2f}")
    except Exception as e:
        results["analyze_pattern"] = False
        if verbose:
            print(f"✗ analyze_pattern failed: {e}")
        ai_logger.error(f"Validation failed for analyze_pattern: {e}")
    
    try:
        # Test get_suggestion
        suggestion, conf = get_suggestion(score=100, attempts=2, history=[10, 20], difficulty="Normal")
        assert isinstance(suggestion, str), "Suggestion must be string"
        assert 0.0 <= conf <= 1.0, "Confidence must be 0.0-1.0"
        results["get_suggestion"] = True
        if verbose:
            print(f"✓ get_suggestion: suggestion='{suggestion}', confidence={conf:.2f}")
    except Exception as e:
        results["get_suggestion"] = False
        if verbose:
            print(f"✗ get_suggestion failed: {e}")
        ai_logger.error(f"Validation failed for get_suggestion: {e}")
    
    results["all_valid"] = all([results.get("generate_hint"), results.get("analyze_pattern"), results.get("get_suggestion")])
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"Overall: {'✓ ALL TESTS PASSED' if results['all_valid'] else '✗ SOME TESTS FAILED'}")
        print(f"{'='*50}")
    
    return results
