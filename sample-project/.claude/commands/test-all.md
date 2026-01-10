---
description: Run all unit tests with detailed reporting
allowed-tools: Bash
---

Run the complete TaskMgr test suite:

1. Execute all tests: `python3 -m unittest discover -s tests -p "test_*.py" -v`
2. Report test results with counts (passed/failed/total)
3. If any tests fail, show failure details and stack traces
4. Suggest fixes for common failure patterns
5. Report final test coverage summary

Expected test modules:
- test_encryption.py (6 tests)
- test_sync.py (6 tests)
- test_export.py (6 tests)
- test_optimize.py (8 tests)
