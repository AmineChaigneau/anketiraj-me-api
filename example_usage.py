"""
Example Usage of Index Calculator
==================================

This file demonstrates how to use the IndexCalculator class
to calculate SCI, UEI, and SEI from mouse tracking data.

Author: Survey Analytics Team
Date: 2026-01-19
"""

from index_calculator import IndexCalculator
import json

# Example data (from TestMetrics API output format)
example_data = {
    "metadata": {
        "userId": "user_001",
        "surveyId": "survey_123",
        "questionId": "q1",
        "timestamp": "2026-01-19T12:00:00.000Z",
        "selectedResponse": "B"
    },
    "trajectory": [
        {"x": 0.0, "y": 0.0, "step": 0, "normalizedTime": 0.0},
        {"x": 0.05, "y": 0.05, "step": 1, "normalizedTime": 0.0526},
        {"x": 0.10, "y": 0.12, "step": 2, "normalizedTime": 0.1053},
        {"x": 0.15, "y": 0.20, "step": 3, "normalizedTime": 0.1579},
        {"x": 0.20, "y": 0.30, "step": 4, "normalizedTime": 0.2105},
        {"x": 0.25, "y": 0.42, "step": 5, "normalizedTime": 0.2632},
        {"x": 0.30, "y": 0.55, "step": 6, "normalizedTime": 0.3158},
        {"x": 0.35, "y": 0.68, "step": 7, "normalizedTime": 0.3684},
        {"x": 0.40, "y": 0.80, "step": 8, "normalizedTime": 0.4211},
        {"x": 0.42, "y": 0.85, "step": 9, "normalizedTime": 0.4737},
        {"x": 0.44, "y": 0.88, "step": 10, "normalizedTime": 0.5263},
        {"x": 0.46, "y": 0.91, "step": 11, "normalizedTime": 0.5789},
        {"x": 0.48, "y": 0.93, "step": 12, "normalizedTime": 0.6316},
        {"x": 0.50, "y": 0.95, "step": 13, "normalizedTime": 0.6842},
        {"x": 0.51, "y": 0.96, "step": 14, "normalizedTime": 0.7368},
        {"x": 0.52, "y": 0.97, "step": 15, "normalizedTime": 0.7895},
        {"x": 0.53, "y": 0.98, "step": 16, "normalizedTime": 0.8421},
        {"x": 0.54, "y": 0.99, "step": 17, "normalizedTime": 0.8947},
        {"x": 0.55, "y": 0.995, "step": 18, "normalizedTime": 0.9474},
        {"x": 0.56, "y": 1.0, "step": 19, "normalizedTime": 1.0}
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

# Example with change of mind (more complex trajectory)
example_data_complex = {
    "metadata": {
        "userId": "user_001",
        "surveyId": "survey_123",
        "questionId": "q2",
        "timestamp": "2026-01-19T12:01:00.000Z",
        "selectedResponse": "C"
    },
    "trajectory": [
        {"x": 0.0, "y": 0.0, "step": 0, "normalizedTime": 0.0},
        {"x": 0.05, "y": 0.05, "step": 1, "normalizedTime": 0.0526},
        {"x": 0.15, "y": 0.15, "step": 2, "normalizedTime": 0.1053},
        {"x": 0.25, "y": 0.20, "step": 3, "normalizedTime": 0.1579},
        {"x": 0.30, "y": 0.18, "step": 4, "normalizedTime": 0.2105},  # Change direction
        {"x": 0.20, "y": 0.25, "step": 5, "normalizedTime": 0.2632},
        {"x": 0.15, "y": 0.35, "step": 6, "normalizedTime": 0.3158},
        {"x": 0.25, "y": 0.45, "step": 7, "normalizedTime": 0.3684},
        {"x": 0.35, "y": 0.55, "step": 8, "normalizedTime": 0.4211},
        {"x": 0.40, "y": 0.65, "step": 9, "normalizedTime": 0.4737},
        {"x": 0.35, "y": 0.70, "step": 10, "normalizedTime": 0.5263},  # Another change
        {"x": 0.45, "y": 0.75, "step": 11, "normalizedTime": 0.5789},
        {"x": 0.55, "y": 0.80, "step": 12, "normalizedTime": 0.6316},
        {"x": 0.65, "y": 0.85, "step": 13, "normalizedTime": 0.6842},
        {"x": 0.70, "y": 0.88, "step": 14, "normalizedTime": 0.7368},
        {"x": 0.73, "y": 0.91, "step": 15, "normalizedTime": 0.7895},
        {"x": 0.76, "y": 0.94, "step": 16, "normalizedTime": 0.8421},
        {"x": 0.78, "y": 0.96, "step": 17, "normalizedTime": 0.8947},
        {"x": 0.79, "y": 0.98, "step": 18, "normalizedTime": 0.9474},
        {"x": 0.80, "y": 1.0, "step": 19, "normalizedTime": 1.0}
    ],
    "metrics": {
        "deviation": {
            "maxDeviationPositive": 78.5,
            "maxDeviationNegative": -45.2,
            "aucPositive": 234.5,
            "aucNegative": -89.3
        },
        "velocity": {
            "maximalVelocity": 0.890,
            "averageVelocity": 0.423,
            "maximalVelocityPxPerSec": 890.0,
            "averageVelocityPxPerSec": 423.0
        },
        "complexity": {
            "angleEntropy": 3.124,
            "initiationTimeMs": 245
        },
        "hover": {
            "hoverCounts": {
                "A": 3,
                "B": 2,
                "C": 1,
                "D": 2
            },
            "totalHovers": 8
        }
    }
}


def example_1_single_calculation():
    """Example 1: Calculate indices for a single question."""
    print("=" * 70)
    print("EXAMPLE 1: Single Question Calculation")
    print("=" * 70)
    
    # Initialize calculator
    calc = IndexCalculator()
    
    # Calculate indices
    result = calc.calculate_all(example_data, update_history=True)
    
    print(f"\nInput: Question {example_data['metadata']['questionId']}")
    print(f"User: {example_data['metadata']['userId']}")
    print(f"Selected Response: {example_data['metadata']['selectedResponse']}")
    print(f"\nResults:")
    print(f"  SCI (Conflict):     {result['SCI']:.2f} / 100")
    print(f"  UEI (Engagement):   {result['UEI']:.2f} / 100")
    print(f"  SEI (Overall):      {result['SEI']:.2f} / 100")
    print()


def example_2_multiple_questions():
    """Example 2: Calculate indices for multiple questions (cumulative SEI)."""
    print("=" * 70)
    print("EXAMPLE 2: Multiple Questions with Cumulative SEI")
    print("=" * 70)
    
    # Initialize calculator
    calc = IndexCalculator()
    
    # Question 1
    result1 = calc.calculate_all(example_data, update_history=True)
    print(f"\nQuestion 1: {example_data['metadata']['questionId']}")
    print(f"  SCI: {result1['SCI']:.2f}, UEI: {result1['UEI']:.2f}, SEI: {result1['SEI']:.2f}")
    
    # Question 2
    result2 = calc.calculate_all(example_data_complex, update_history=True)
    print(f"\nQuestion 2: {example_data_complex['metadata']['questionId']}")
    print(f"  SCI: {result2['SCI']:.2f}, UEI: {result2['UEI']:.2f}, SEI: {result2['SEI']:.2f}")
    
    print(f"\n📊 SEI Evolution:")
    print(f"  After Q1: {result1['SEI']:.2f}")
    print(f"  After Q2: {result2['SEI']:.2f} (cumulative, based on Q1 + Q2)")
    
    # Get history
    history = calc.get_history(user_id="user_001")
    print(f"\n📋 History for user_001:")
    for i, h in enumerate(history, 1):
        print(f"  Q{i}: SCI={h['sci']:.2f}, UEI={h['uei']:.2f}")
    print()


def example_3_api_format():
    """Example 3: Using data directly from TestMetrics API."""
    print("=" * 70)
    print("EXAMPLE 3: Direct API Integration")
    print("=" * 70)
    
    # Simulate receiving JSON from API
    api_response = json.dumps(example_data, indent=2)
    
    print("\n📥 Received JSON from TestMetrics API:")
    print(api_response[:200] + "...\n")
    
    # Parse and calculate
    data = json.loads(api_response)
    calc = IndexCalculator()
    result = calc.calculate_all(data, update_history=False)
    
    print("📤 Output to send to database/frontend:")
    output = {
        "userId": data['metadata']['userId'],
        "questionId": data['metadata']['questionId'],
        "indices": result,
        "timestamp": data['metadata']['timestamp']
    }
    print(json.dumps(output, indent=2))
    print()


def example_4_batch_processing():
    """Example 4: Batch processing multiple questions."""
    print("=" * 70)
    print("EXAMPLE 4: Batch Processing")
    print("=" * 70)
    
    # Initialize calculator
    calc = IndexCalculator()
    
    # Process multiple questions
    questions = [example_data, example_data_complex]
    results = []
    
    for i, question in enumerate(questions, 1):
        result = calc.calculate_all(question, update_history=True)
        results.append(result)
        print(f"\nQuestion {i}: SCI={result['SCI']:.2f}, UEI={result['UEI']:.2f}, SEI={result['SEI']:.2f}")
    
    print(f"\n📊 Summary:")
    print(f"  Total questions processed: {len(results)}")
    print(f"  Average SCI: {sum(r['SCI'] for r in results) / len(results):.2f}")
    print(f"  Average UEI: {sum(r['UEI'] for r in results) / len(results):.2f}")
    print(f"  Final SEI: {results[-1]['SEI']:.2f}")
    print()


def example_5_interpretation():
    """Example 5: Interpreting the results."""
    print("=" * 70)
    print("EXAMPLE 5: Result Interpretation")
    print("=" * 70)
    
    calc = IndexCalculator()
    result = calc.calculate_all(example_data_complex, update_history=True)
    
    print(f"\nQuestion: {example_data_complex['metadata']['questionId']}")
    print(f"Selected: {example_data_complex['metadata']['selectedResponse']}")
    print(f"\nScores:")
    print(f"  SCI: {result['SCI']:.2f}")
    print(f"  UEI: {result['UEI']:.2f}")
    print(f"  SEI: {result['SEI']:.2f}")
    
    print(f"\n📊 Interpretation:")
    
    # SCI interpretation
    sci = result['SCI']
    if sci < 20:
        sci_interp = "Fluid decision, minimal conflict"
    elif sci < 40:
        sci_interp = "Low conflict, generally confident"
    elif sci < 60:
        sci_interp = "Moderate conflict, weighing options"
    elif sci < 80:
        sci_interp = "High conflict, significant hesitation"
    else:
        sci_interp = "Maximal conflict, multiple choice changes"
    print(f"  SCI ({sci:.1f}): {sci_interp}")
    
    # UEI interpretation
    uei = result['UEI']
    if uei < 20:
        uei_interp = "No engagement, mechanical behavior"
    elif uei < 40:
        uei_interp = "Low engagement, minimal interaction"
    elif uei < 60:
        uei_interp = "Moderate engagement, typical pattern"
    elif uei < 80:
        uei_interp = "High engagement (confident or exploratory)"
    else:
        uei_interp = "Maximal engagement, strong involvement"
    print(f"  UEI ({uei:.1f}): {uei_interp}")
    
    # SEI interpretation
    sei = result['SEI']
    if sei < 30:
        sei_interp = "Poor quality, likely speeding"
    elif sei < 50:
        sei_interp = "Below average, inconsistent attention"
    elif sei < 70:
        sei_interp = "Moderate quality, acceptable"
    elif sei < 85:
        sei_interp = "High quality, consistent engagement"
    else:
        sei_interp = "Excellent quality, sustained attention"
    print(f"  SEI ({sei:.1f}): {sei_interp}")
    
    # Data quality flag
    if uei < 30:
        print(f"\n⚠️  Data Quality Flag: Low UEI indicates potential speeding/inattention")
    elif sci > 80 and uei < 40:
        print(f"\n⚠️  Data Quality Flag: High conflict + low engagement = confused and rushed")
    else:
        print(f"\n✅ Data Quality: Acceptable")
    print()


if __name__ == "__main__":
    # Run all examples
    example_1_single_calculation()
    example_2_multiple_questions()
    example_3_api_format()
    example_4_batch_processing()
    example_5_interpretation()
    
    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
