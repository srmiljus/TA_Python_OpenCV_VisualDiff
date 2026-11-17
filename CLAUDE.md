# visual-diff - Project Rules

## Technology Stack
- **Language**: Python 3.11+
- **Testing**: pytest
- **Image Processing**: opencv-python, numpy
- **No real screenshots**: Tests use generated images (numpy arrays only)

## Development Environment
- **Virtual Environment**: Always use `.venv` folder in project root
- **Shell**: Git Bash (use forward slashes `/`)
- **Python Commands**: Use `.venv/Scripts/python` (NOT bare `python`)
- **Dependencies**: Specified in `requirements.txt`
  - Install with: `.venv/Scripts/python -m pip install -r requirements.txt`
  - Run tests with: `.venv/Scripts/python -m pytest -v`

## Development Workflow - TDD (Test-Driven Development)
1. **Write tests first** — always
2. **Run tests** to confirm they fail (red)
3. **Implement code** to make tests pass (green)
4. **Never modify existing tests** to make them pass
   - Exception: Only if explicitly approved by user
5. **Run all tests after each change** — verify nothing breaks
6. **No auto-commits** — user handles all git commits

## Testing Guidelines
- Tests are derived from requirements, never from the existing implementation
- Generated images: Use `numpy.ndarray` to create test images, never screenshot()
- Fast feedback: Tests must run quickly
- Coverage: All visual-diff functionality tested

## Code Style & Quality
- Follow PEP 8
- Clear, descriptive names
- Minimal comments (explain WHY, not WHAT)
- No unnecessary abstraction before needed

---

**Status**: Project initialization in progress
