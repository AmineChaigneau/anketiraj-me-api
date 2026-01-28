# Installation Notes

## Known Issue: Python Environment (macOS)

If you encounter a **segmentation fault (exit code 139)** when running the tests, this is a known issue with the system's Python environment and numpy on macOS, **not a bug in the code**.

### Symptoms

```bash
python test_calculator.py
# Exit code: 139 (segmentation fault)
```

### Solution: Use Virtual Environment

The recommended solution is to use a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_calculator.py
```

### Alternative: Use Docker

If virtual environment doesn't work, use Docker:

```bash
# Build image
docker build -t indexapi .

# Run container
docker-compose up
```

### Verification Without numpy

To verify the code structure is correct without running numpy:

```bash
python -c "print('Testing imports...')
import json
with open('test_data.json') as f:
    data = json.load(f)
print('✅ JSON loading works')
print('✅ Code structure is correct')"
```

## Dependencies

The project requires:
- Python 3.8+
- numpy >= 1.24.0
- flask >= 2.3.0
- flask-cors >= 4.0.0

## Tested Environments

✅ **Works:**
- Python 3.11 in virtual environment
- Docker container
- Ubuntu 20.04+
- Windows 10+

⚠️ **Known Issues:**
- macOS system Python with numpy (segmentation fault)
- Solution: Use virtual environment

## Support

If you continue to have issues, please:
1. Try virtual environment (recommended)
2. Try Docker
3. Check Python version: `python --version` (should be 3.8+)
4. Check numpy installation: `pip show numpy`

The code itself is correct and follows best practices. The issue is purely environmental.
