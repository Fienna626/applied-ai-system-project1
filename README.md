Phase 1: Functionality Extension (Assign)
TFs should:
[x]Identify which new AI feature will be added to your project.
Reliability or Testing System	You include ways to measure or test how well your AI performs.	A script that checks if your AI gives consistent answers.

[x]Verify the feature is actually used in logic
[x]Detect shallow or fake integrations
added 
[x]Trace data flow end‑to‑end
Input → Processing → Output

User selects difficulty in Streamlit sidebar
get_range_for_difficulty(difficulty) → returns (low, high)
Used to create st.session_state.secret = random.randint(low, high)
User guess flow:

User enters guess → parse_guess(raw_input) → validates input
Result goes to check_guess(guess, secret) → returns outcome
Outcome goes to update_score(current_score, outcome, attempt) → new score

Phase 2: Architecture Diagram (Review)
TFs should:
[x]Create a system diagram or at least understand how adding in a new AI feature will fit into your system. 
[x]Confirm alignment with code
Flag mismatches
- hard coded range 
- logic ui coupling
- missing ai hookpoints :D
- History not analyzed

Phase 3: Documentation (Review)
TFs should:
[x]Understand what is going in the README

Phase 4: Reliability and Testing (Review)
TFs should:
[x]Identify what reliability signal is used
    - Confidence scoring (0.0-1.0): Each AI output includes confidence
    - Determinism: All functions produce same output for same input
    - Logging: All operations logged for traceability
[x]Include at least one way to test or measure its reliability
[x]Automated tests
    - test_reliability.py: 40+ test cases
    - test_glitchy_guesser.py: Game logic tests
[x]Confidence scoring
    - generate_hint() returns (hint, confidence)
    - analyze_pattern() returns {strategy, efficiency, confidence}
    - get_suggestion() returns (suggestion, confidence)
    - Confidence increases with more data
[x]Logging and error handling
    - ai_logger configured in ai_feature.py
    - All AI functions wrapped in try-except
    - Graceful fallbacks for errors
[x]Human evaluation
    - Confidence scores visible in Streamlit UI
    - Outputs human-readable with emojis
    - Users can assess quality directly
[x]Be able to document your findings from your testing
    - reliability_report.json (detailed metrics)
    - RELIABILITY_FINDINGS.md (summary)
    - RELIABILITY_TESTING_COMPLETE.md (full documentation)
