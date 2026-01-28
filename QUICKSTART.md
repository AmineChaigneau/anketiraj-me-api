# IndexAPI - Quick Start Guide

Get started with the Index Calculator API in 5 minutes! 🚀

## 1. Installation (30 seconds)

```bash
cd IndexAPI
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed numpy-1.24.0 flask-2.3.0 flask-cors-4.0.0
```

## 2. Test the Calculator (1 minute)

Run the example script to verify everything works:

```bash
python example_usage.py
```

**Expected output:**
```
======================================================================
EXAMPLE 1: Single Question Calculation
======================================================================

Input: Question q1
User: user_001
Selected Response: B

Results:
  SCI (Conflict):     45.20 / 100
  UEI (Engagement):   67.30 / 100
  SEI (Overall):      58.10 / 100

...
```

If you see this output, **everything is working!** ✅

## 3. Use in Your Code (2 minutes)

### Basic Usage

Create a file `my_test.py`:

```python
from index_calculator import IndexCalculator
import json

# Load your data
with open('test_data.json', 'r') as f:
    data = json.load(f)

# Calculate indices
calc = IndexCalculator()
result = calc.calculate_all(data)

# Print results
print(f"SCI: {result['SCI']}")
print(f"UEI: {result['UEI']}")
print(f"SEI: {result['SEI']}")
```

Run it:

```bash
python my_test.py
```

**Expected output:**
```
SCI: 45.2
UEI: 67.3
SEI: 58.1
```

## 4. Start the API Server (1 minute)

```bash
python api.py
```

**Expected output:**
```
 * Serving Flask app 'api'
 * Running on http://0.0.0.0:5001
```

### Test the API

Open a new terminal and run:

```bash
curl -X POST http://localhost:5001/calculate \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

**Expected output:**
```json
{
  "status": "success",
  "data": {
    "SCI": 45.2,
    "UEI": 67.3,
    "SEI": 58.1
  },
  "metadata": {...}
}
```

If you see this, **your API is working!** ✅

## 5. Integration with TestMetrics (30 seconds)

In your JavaScript code (TestMetrics project):

```javascript
// After generating API output
const apiOutput = generateAPIOutput();

// Send to IndexAPI
fetch('http://localhost:5001/calculate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(apiOutput)
})
.then(res => res.json())
.then(data => {
  console.log('SCI:', data.data.SCI);
  console.log('UEI:', data.data.UEI);
  console.log('SEI:', data.data.SEI);
});
```

## Common Use Cases

### Use Case 1: Single Question

```python
calc = IndexCalculator()
result = calc.calculate_all(question_data, update_history=True)
print(f"SCI: {result['SCI']}, UEI: {result['UEI']}, SEI: {result['SEI']}")
```

### Use Case 2: Multiple Questions (Survey)

```python
calc = IndexCalculator()

for question in survey_questions:
    result = calc.calculate_all(question, update_history=True)
    print(f"Q{question['metadata']['questionId']}: SEI={result['SEI']}")
```

### Use Case 3: Batch Processing

```python
calc = IndexCalculator()

results = []
for question in questions:
    result = calc.calculate_all(question, update_history=True)
    results.append(result)

# Final SEI reflects all questions
print(f"Final SEI: {results[-1]['SEI']}")
```

### Use Case 4: API Integration

```bash
# Calculate
curl -X POST http://localhost:5001/calculate \
  -H "Content-Type: application/json" \
  -d @question1.json

# Get history
curl http://localhost:5001/history/user_001

# Reset for new session
curl -X POST http://localhost:5001/reset
```

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'numpy'`

**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### Error: `Address already in use`

**Solution:** Port is already taken
```bash
# By default, the API uses port 5001 (to avoid conflicts with macOS AirPlay on 5000)
# If 5001 is also taken, you can change the port in api.py:
app.run(host='0.0.0.0', port=5002, debug=True)
```

### Error: `KeyError: 'metrics'`

**Solution:** Your JSON is missing required fields. Check the format in `test_data.json`

### API returns 400 error

**Solution:** Validate your JSON format matches the expected structure:
```json
{
  "metadata": {...},
  "trajectory": [...],
  "metrics": {...}
}
```

## Next Steps

1. **Read full documentation:** See `README.md`
2. **Understand the indices:** See `../Analysis/INDICES.md`
3. **View metrics specification:** See `../TestMetrics/METRICS_REPORT.md`
4. **Deploy to production:** Use Gunicorn (see README)

## Need Help?

- **Examples:** Run `python example_usage.py` for 5 detailed examples
- **API Docs:** See `README.md` for all endpoints
- **Index Definitions:** See `../Analysis/INDICES.md`

## Quick Reference

| Task | Command |
|------|---------|
| Install | `pip install -r requirements.txt` |
| Test | `python example_usage.py` |
| Start API | `python api.py` |
| Test API | `curl -X POST http://localhost:5001/calculate -H "Content-Type: application/json" -d @test_data.json` |
| Health Check | `curl http://localhost:5001/health` |

---

**You're ready to go!** 🎉

For more details, see `README.md`.
