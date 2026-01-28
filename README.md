# Index Calculator API

Python API for calculating **SCI**, **UEI**, and **SEI** indices from mouse tracking data.

## 📊 Overview

This API calculates three survey quality indices based on mouse trajectory analysis:

| Index | Name | Level | Description |
|-------|------|-------|-------------|
| **SCI** | Survey Conflictuality Index | Micro (per question) | Measures cognitive conflict and hesitation |
| **UEI** | User Engagement Index | Micro (per question) | Measures cognitive engagement and attention |
| **SEI** | Survey Engagement Index | Macro (cumulative) | Measures sustained engagement across questions |

## 🚀 Quick Start

### Installation

```bash
cd IndexAPI
pip install -r requirements.txt
```

### Basic Usage (Python)

```python
from index_calculator import IndexCalculator

# Initialize calculator
calc = IndexCalculator()

# Your data from TestMetrics API
data = {
    "metadata": {...},
    "trajectory": [...],
    "metrics": {...}
}

# Calculate all indices
result = calc.calculate_all(data)
print(result)  # {'SCI': 45.2, 'UEI': 67.3, 'SEI': 58.1}
```

### Run API Server

```bash
python api.py
```

The API will be available at `http://localhost:5001`

### Run Examples

```bash
python example_usage.py
```

## 📥 Input Format

The API expects JSON data in the **TestMetrics API output format**:

```json
{
  "metadata": {
    "userId": "string",
    "surveyId": "string",
    "questionId": "string",
    "timestamp": "ISO8601 string",
    "selectedResponse": "string"
  },
  "trajectory": [
    {
      "x": 0.0,
      "y": 0.0,
      "step": 0,
      "normalizedTime": 0.0
    }
    // ... 20 points total
  ],
  "metrics": {
    "deviation": {
      "maxDeviationPositive": 45.2,
      "maxDeviationNegative": -12.5,
      "aucPositive": 123.4,
      "aucNegative": -34.5
    },
    "velocity": {
      "maximalVelocity": 1.234,
      "averageVelocity": 0.567,
      "maximalVelocityPxPerSec": 1234.0,
      "averageVelocityPxPerSec": 567.0
    },
    "complexity": {
      "angleEntropy": 2.345,
      "initiationTimeMs": 123
    },
    "hover": {
      "hoverCounts": {
        "A": 2,
        "B": 1,
        "C": 0,
        "D": 1
      },
      "totalHovers": 4
    }
  }
}
```

## 📤 Output Format

```json
{
  "SCI": 45.2,
  "UEI": 67.3,
  "SEI": 58.1
}
```

All scores are in the range **[0, 100]**.

## 🌐 API Endpoints

### `POST /calculate`

Calculate indices for a single question.

**Request:**
```json
{
  "metadata": {...},
  "trajectory": [...],
  "metrics": {...}
}
```

**Response:**
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

### `POST /calculate_batch`

Calculate indices for multiple questions at once.

**Request:**
```json
{
  "questions": [
    {
      "metadata": {...},
      "trajectory": [...],
      "metrics": {...}
    },
    ...
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "SCI": 45.2,
      "UEI": 67.3,
      "SEI": 58.1,
      "metadata": {...}
    },
    ...
  ]
}
```

### `POST /reset`

Reset calculator history (for new survey session).

**Response:**
```json
{
  "status": "success",
  "message": "History reset successfully"
}
```

### `GET /history/<user_id>`

Get calculation history for a specific user.

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "sci": 45.2,
      "uei": 67.3,
      "userId": "user_001",
      "questionId": "q1",
      "timestamp": "..."
    },
    ...
  ]
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Index Calculator API is running"
}
```

### `GET /stats`

Get overall statistics.

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_calculations": 123,
    "unique_users": 45
  }
}
```

## 📊 Index Definitions

### SCI - Survey Conflictuality Index

**Measures:** Cognitive conflict and hesitation during decision-making

**Components:**
- Direction changes (X/Y flips) - 25%
- Maximum deviation - 20%
- Area under curve - 20%
- Average deviation - 15%
- Time spent - 10%
- Hover on non-selected options - 10%

**Interpretation:**
- **0-20:** Fluid decision, minimal conflict
- **21-40:** Low conflict, generally confident
- **41-60:** Moderate conflict, weighing options
- **61-80:** High conflict, significant hesitation
- **81-100:** Maximal conflict, multiple choice changes

### UEI - User Engagement Index

**Measures:** Cognitive engagement and attention (Dual Model)

**Two types of engagement:**
1. **Confident:** Fast, direct, smooth, decisive
2. **Exploratory:** Complex, deliberate, thorough

**Components:**
- Confident: Directness + Smoothness + Speed + Decisiveness
- Exploratory: Complexity + Deliberation
- Final UEI = MAX(Confident, Exploratory)

**Interpretation:**
- **0-20:** No engagement, mechanical behavior
- **21-40:** Low engagement, minimal interaction
- **41-60:** Moderate engagement, typical pattern
- **61-80:** High engagement (confident OR exploratory)
- **81-100:** Maximal engagement, strong involvement

### SEI - Survey Engagement Index

**Measures:** Sustained engagement across the entire survey (cumulative)

**Calculation:** Dynamic/cumulative after each question
- After Q1: SEI based on Q1
- After Q2: SEI based on Q1-Q2
- After Q3: SEI based on Q1-Q3
- etc.

**Components:**
- Average UEI - 40%
- Average SCI - 20%
- Consistency - 15%
- High engagement ratio - 10%
- Engaged despite conflict - 10%
- Low engagement penalty - 5%

**Interpretation:**
- **0-30:** Poor quality, likely speeding
- **31-50:** Below average, inconsistent attention
- **51-70:** Moderate quality, acceptable
- **71-85:** High quality, consistent engagement
- **86-100:** Excellent quality, sustained attention

## 🔧 Advanced Usage

### Multiple Questions (Cumulative SEI)

```python
calc = IndexCalculator()

# Question 1
result1 = calc.calculate_all(data_q1, update_history=True)
print(f"Q1 - SEI: {result1['SEI']}")  # Based on Q1 only

# Question 2
result2 = calc.calculate_all(data_q2, update_history=True)
print(f"Q2 - SEI: {result2['SEI']}")  # Based on Q1+Q2

# Question 3
result3 = calc.calculate_all(data_q3, update_history=True)
print(f"Q3 - SEI: {result3['SEI']}")  # Based on Q1+Q2+Q3
```

### Get History

```python
# Get history for a specific user
history = calc.get_history(user_id="user_001")

for entry in history:
    print(f"Q{entry['questionId']}: SCI={entry['sci']}, UEI={entry['uei']}")
```

### Reset History

```python
# Reset for new survey session
calc.reset_history()
```

### Single Calculation (No History)

```python
# Calculate without updating history
result = calc.calculate_all(data, update_history=False)
```

## 📋 Example cURL Requests

### Calculate Single Question

```bash
curl -X POST http://localhost:5001/calculate \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

### Batch Calculation

```bash
curl -X POST http://localhost:5001/calculate_batch \
  -H "Content-Type: application/json" \
  -d '{"questions": [...]}'
```

### Get History

```bash
curl http://localhost:5001/history/user_001
```

### Reset History

```bash
curl -X POST http://localhost:5001/reset
```

## 📁 Project Structure

```
IndexAPI/
├── index_calculator.py   # Core calculation logic
├── api.py                # Flask API server
├── example_usage.py      # Usage examples
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── test_data.json       # Sample test data
```

## 🧪 Testing

Run the example script to test all functionality:

```bash
python example_usage.py
```

This will run 5 example scenarios:
1. Single question calculation
2. Multiple questions with cumulative SEI
3. Direct API integration
4. Batch processing
5. Result interpretation

## 📊 Data Quality Flags

The API automatically flags potential data quality issues:

- **⚠️ UEI < 30:** Potential speeding or inattention
- **⚠️ High SCI + Low UEI:** Confused and rushed
- **✅ Otherwise:** Acceptable quality

## 🔗 Integration with TestMetrics

This API is designed to work seamlessly with the **TestMetrics** JavaScript project:

1. **TestMetrics** captures mouse trajectories
2. **TestMetrics** calculates basic metrics
3. **TestMetrics** sends JSON to this API
4. **IndexAPI** calculates SCI, UEI, SEI
5. Results saved to database

**Workflow:**
```
User Interaction → TestMetrics (JS) → JSON → IndexAPI (Python) → Database
```

## 📖 Documentation

For detailed documentation on the indices, see:
- `../Analysis/INDICES.md` - Complete index definitions
- `../TestMetrics/METRICS_REPORT.md` - Input metrics specification

## 🚀 Deployment

### Production Deployment

For production, use a proper WSGI server like **Gunicorn**:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 api:app
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5001
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "api:app"]
```

## 📝 License

MIT License - See main project README

## 👥 Authors

Survey Analytics Team - 2026

## 🤝 Contributing

See main project CONTRIBUTING.md

## 📧 Support

For issues or questions, open an issue on the main repository.
