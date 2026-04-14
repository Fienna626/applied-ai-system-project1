# AI Feature Reliability Report

**Generated**: 2026-04-13T17:50:33.983322

## Reliability Signals Identified

### 1. Confidence Scoring
- Each AI output includes a confidence score (0.0-1.0)
- Confidence increases with more data (attempts, history)
- Low confidence outputs are filtered before display

### 2. Automated Tests
- Unit tests for all game logic functions
- Reliability tests for consistency, edge cases, and error handling
- Integration tests for complete game flows

### 3. Logging and Error Handling
- All AI functions log their operations
- Error logs include full stack traces for debugging
- Graceful fallback for errors (empty string, low confidence)

### 4. Consistency Measurement
- Deterministic outputs: same input -> same output
- Validated through test_reliability.py

## How to Run Tests

### Run all tests:
```bash
pytest test_glitchy_guesser.py test_reliability.py -v
```

### Run reliability report:
```bash
python test_runner_reliability.py
```

### Run AI validation:
```python
from ai_feature import validate_ai_outputs
validate_ai_outputs(verbose=True)
```

## Test Results Summary

- ✓ All confidence scores are properly calibrated within [0.0, 1.0]
- ✓ 3/3 AI functions are deterministic (same input → same output)
- ✓ 4/4 edge cases are handled gracefully

## Files for Human Evaluation

Run the Streamlit app to manually test AI features:
```bash
streamlit run app.py
```

Or check the test logs:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Run app or tests
```
