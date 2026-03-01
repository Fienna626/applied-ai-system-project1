import pytest
from glitchy_guesser import get_range_for_difficulty, parse_guess, check_guess, update_score


# ── get_range_for_difficulty ────────────────────────────────────────────────

class TestGetRangeForDifficulty:
    def test_easy_range(self):
        assert get_range_for_difficulty("Easy") == (1, 20)

    def test_normal_range(self):
        assert get_range_for_difficulty("Normal") == (1, 100)

    def test_hard_range_is_wider_than_normal(self):
        """Hard should be harder (wider range), not narrower."""
        _, hard_high = get_range_for_difficulty("Hard")
        _, normal_high = get_range_for_difficulty("Normal")
        assert hard_high > normal_high

    def test_unknown_difficulty_defaults(self):
        assert get_range_for_difficulty("Unknown") == (1, 100)


# ── parse_guess ─────────────────────────────────────────────────────────────

class TestParseGuess:
    def test_valid_integer(self):
        ok, val, err = parse_guess("42")
        assert ok is True
        assert val == 42
        assert err is None

    def test_float_string_truncates(self):
        ok, val, err = parse_guess("7.9")
        assert ok is True
        assert val == 7

    def test_empty_string(self):
        ok, val, err = parse_guess("")
        assert ok is False
        assert val is None
        assert err is not None

    def test_none_input(self):
        ok, val, err = parse_guess(None)
        assert ok is False

    def test_non_numeric_string(self):
        ok, val, err = parse_guess("abc")
        assert ok is False
        assert err == "That is not a number."


# ── check_guess ─────────────────────────────────────────────────────────────

class TestCheckGuess:
    def test_correct_guess(self):
        outcome, msg = check_guess(50, 50)
        assert outcome == "Win"

    def test_guess_too_high_returns_go_lower(self):
        """If guess > secret, player should go LOWER."""
        outcome, msg = check_guess(80, 50)
        assert outcome == "Too High"
        assert "LOWER" in msg          # Bug 2 fix verification

    def test_guess_too_low_returns_go_higher(self):
        """If guess < secret, player should go HIGHER."""
        outcome, msg = check_guess(20, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in msg         # Bug 2 fix verification

    def test_boundary_one_above(self):
        outcome, _ = check_guess(51, 50)
        assert outcome == "Too High"

    def test_boundary_one_below(self):
        outcome, _ = check_guess(49, 50)
        assert outcome == "Too Low"


# ── update_score ─────────────────────────────────────────────────────────────

class TestUpdateScore:
    def test_win_early_gives_high_points(self):
        # attempt 1 → points = 100 - 10*(1+1) = 80
        new_score = update_score(0, "Win", 1)
        assert new_score == 80

    def test_win_score_minimum_is_10(self):
        # attempt 10 → 100 - 110 = -10 → clamped to 10
        new_score = update_score(0, "Win", 10)
        assert new_score == 10

    def test_too_high_even_attempt_adds_5(self):
        new_score = update_score(100, "Too High", 2)   # even attempt
        assert new_score == 105

    def test_too_high_odd_attempt_subtracts_5(self):
        new_score = update_score(100, "Too High", 3)   # odd attempt
        assert new_score == 95

    def test_too_low_always_subtracts_5(self):
        assert update_score(100, "Too Low", 1) == 95
        assert update_score(100, "Too Low", 2) == 95

    def test_unknown_outcome_unchanged(self):
        assert update_score(50, "Banana", 1) == 50