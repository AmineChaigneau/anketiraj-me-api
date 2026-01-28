"""
Index Calculator API
====================

Flask API for calculating SCI, UEI, and SEI indices from mouse tracking data.

Endpoints:
- POST /calculate - Calculate indices for a single question
- POST /calculate_batch - Calculate indices for multiple questions
- POST /reset - Reset history (new survey session)
- GET /history/<user_id> - Get history for a user

Author: Survey Analytics Team
Date: 2026-01-19
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from index_calculator import IndexCalculator
from typing import Dict, List, Any
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize calculator
calculator = IndexCalculator()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Index Calculator API is running'
    }), 200


@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate SCI, UEI, and SEI for a single question.
    
    Request body:
    {
        "metadata": {...},
        "trajectory": [...],
        "metrics": {...}
    }
    
    Response:
    {
        "status": "success",
        "data": {
            "SCI": 45.2,
            "UEI": 67.3,
            "SEI": 58.1
        },
        "metadata": {
            "userId": "...",
            "questionId": "...",
            "timestamp": "..."
        }
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['metadata', 'trajectory', 'metrics']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Calculate indices
        indices = calculator.calculate_all(data, update_history=True)
        
        logger.info(f"Calculated indices for user {data['metadata'].get('userId')}, "
                   f"question {data['metadata'].get('questionId')}: "
                   f"SCI={indices['SCI']}, UEI={indices['UEI']}, SEI={indices['SEI']}")
        
        return jsonify({
            'status': 'success',
            'data': indices,
            'metadata': data['metadata']
        }), 200
        
    except Exception as e:
        logger.error(f"Error calculating indices: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/calculate_batch', methods=['POST'])
def calculate_batch():
    """
    Calculate indices for multiple questions at once.
    
    Request body:
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
    
    Response:
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
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data or 'questions' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No questions array provided'
            }), 400
        
        questions = data['questions']
        
        if not isinstance(questions, list):
            return jsonify({
                'status': 'error',
                'message': 'questions must be an array'
            }), 400
        
        # Calculate indices for each question
        results = []
        for i, question_data in enumerate(questions):
            try:
                indices = calculator.calculate_all(question_data, update_history=True)
                results.append({
                    **indices,
                    'metadata': question_data.get('metadata', {})
                })
            except Exception as e:
                logger.error(f"Error processing question {i}: {str(e)}")
                results.append({
                    'error': str(e),
                    'metadata': question_data.get('metadata', {})
                })
        
        logger.info(f"Batch calculation completed for {len(questions)} questions")
        
        return jsonify({
            'status': 'success',
            'data': results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch calculation: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/reset', methods=['POST'])
def reset():
    """
    Reset the calculator history (for new survey session).
    
    Response:
    {
        "status": "success",
        "message": "History reset successfully"
    }
    """
    try:
        calculator.reset_history()
        logger.info("Calculator history reset")
        
        return jsonify({
            'status': 'success',
            'message': 'History reset successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error resetting history: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id: str):
    """
    Get calculation history for a specific user.
    
    Response:
    {
        "status": "success",
        "data": [
            {
                "sci": 45.2,
                "uei": 67.3,
                "userId": "...",
                "questionId": "...",
                "timestamp": "..."
            },
            ...
        ]
    }
    """
    try:
        history = calculator.get_history(user_id)
        
        return jsonify({
            'status': 'success',
            'data': history
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """
    Get overall statistics about the calculator.
    
    Response:
    {
        "status": "success",
        "data": {
            "total_calculations": 123,
            "unique_users": 45
        }
    }
    """
    try:
        history = calculator.get_history()
        unique_users = len(set(h['userId'] for h in history))
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_calculations': len(history),
                'unique_users': unique_users
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    # Run the API
    # Note: Using port 5001 to avoid conflict with macOS AirPlay Receiver (port 5000)
    app.run(host='0.0.0.0', port=5001, debug=True)
