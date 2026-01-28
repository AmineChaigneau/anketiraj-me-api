"""
Index Calculator Module
=======================

Calculates SCI, UEI, and SEI indices from mouse tracking data.

Input: JSON format from TestMetrics API output
Output: Dictionary with SCI, UEI, SEI scores [0-100]

Author: Survey Analytics Team
Date: 2026-01-19
"""

import numpy as np
from typing import Dict, List, Any, Optional
import math


class IndexCalculator:
    """
    Calculates Survey Indices (SCI, UEI, SEI) from mouse tracking data.
    """
    
    def __init__(self):
        """Initialize the calculator."""
        self.history = []  # Store history for SEI calculation
    
    # =========================================================================
    # HELPER FUNCTIONS
    # =========================================================================
    
    @staticmethod
    def normalize_0_1(values: List[float]) -> List[float]:
        """Normalize values to [0, 1] range."""
        if not values:
            return []
        min_val = min(values)
        max_val = max(values)
        if max_val == min_val:
            return [0.5] * len(values)
        return [(v - min_val) / (max_val - min_val) for v in values]
    
    @staticmethod
    def calculate_trajectory_metrics(trajectory: List[Dict[str, float]]) -> Dict[str, float]:
        """
        Calculate additional metrics from trajectory that are not in the input.
        
        Args:
            trajectory: List of trajectory points with x, y, step
        
        Returns:
            Dictionary with calculated metrics (xFlips, yFlips, avgDeviation, etc.)
        """
        if len(trajectory) < 2:
            return {
                'xFlips': 0,
                'yFlips': 0,
                'averageDeviation': 0.0,
                'trajectoryLength': 0.0,
                'trajectorySmoothness': 1.0
            }
        
        # Extract coordinates
        x_coords = [p['x'] for p in trajectory]
        y_coords = [p['y'] for p in trajectory]
        
        # Calculate X-Flips (direction changes in X)
        x_flips = 0
        for i in range(1, len(x_coords) - 1):
            dx1 = x_coords[i] - x_coords[i-1]
            dx2 = x_coords[i+1] - x_coords[i]
            if dx1 * dx2 < 0:  # Sign change
                x_flips += 1
        
        # Calculate Y-Flips (direction changes in Y)
        y_flips = 0
        for i in range(1, len(y_coords) - 1):
            dy1 = y_coords[i] - y_coords[i-1]
            dy2 = y_coords[i+1] - y_coords[i]
            if dy1 * dy2 < 0:  # Sign change
                y_flips += 1
        
        # Calculate Average Deviation from ideal straight line
        # Ideal line: from (0, 0) to (x_end, y_end)
        x_start, y_start = x_coords[0], y_coords[0]
        x_end, y_end = x_coords[-1], y_coords[-1]
        
        deviations = []
        line_length = math.sqrt((x_end - x_start)**2 + (y_end - y_start)**2)
        
        if line_length > 0:
            for i in range(1, len(trajectory) - 1):
                x, y = x_coords[i], y_coords[i]
                # Perpendicular distance from point to line
                numerator = abs((y_end - y_start) * x - (x_end - x_start) * y + 
                              x_end * y_start - y_end * x_start)
                distance = numerator / line_length
                deviations.append(distance)
        
        avg_deviation = np.mean(deviations) if deviations else 0.0
        
        # Calculate trajectory length
        trajectory_length = 0.0
        for i in range(1, len(trajectory)):
            dx = x_coords[i] - x_coords[i-1]
            dy = y_coords[i] - y_coords[i-1]
            trajectory_length += math.sqrt(dx**2 + dy**2)
        
        # Calculate trajectory smoothness (angle consistency)
        angles = []
        for i in range(1, len(trajectory)):
            dx = x_coords[i] - x_coords[i-1]
            dy = y_coords[i] - y_coords[i-1]
            angle = math.atan2(dy, dx)
            angles.append(angle)
        
        # Smoothness based on angle variance
        if len(angles) > 1:
            angle_changes = [abs(angles[i] - angles[i-1]) for i in range(1, len(angles))]
            angle_sd = np.std(angle_changes)
            smoothness = max(0, 1 - (angle_sd / math.pi))
        else:
            smoothness = 1.0
        
        return {
            'xFlips': x_flips,
            'yFlips': y_flips,
            'averageDeviation': avg_deviation,
            'trajectoryLength': trajectory_length,
            'trajectorySmoothness': smoothness
        }
    
    # =========================================================================
    # SCI CALCULATION
    # =========================================================================
    
    def calculate_sci(self, data: Dict[str, Any]) -> float:
        """
        Calculate Survey Conflictuality Index (SCI).
        
        SCI measures cognitive conflict during decision-making.
        
        Args:
            data: Dictionary with trajectory and metrics
        
        Returns:
            SCI score [0-100]
        """
        metrics = data.get('metrics', {})
        trajectory = data.get('trajectory', [])
        metadata = data.get('metadata', {})
        
        # Extract metrics
        deviation = metrics.get('deviation', {})
        velocity = metrics.get('velocity', {})
        hover = metrics.get('hover', {})
        
        max_dev_pos = deviation.get('maxDeviationPositive', 0)
        max_dev_neg = abs(deviation.get('maxDeviationNegative', 0))
        auc_pos = deviation.get('aucPositive', 0)
        auc_neg = abs(deviation.get('aucNegative', 0))
        avg_velocity = velocity.get('averageVelocityPxPerSec', 0)
        
        # Calculate additional metrics from trajectory
        traj_metrics = self.calculate_trajectory_metrics(trajectory)
        x_flips = traj_metrics['xFlips']
        y_flips = traj_metrics['yFlips']
        avg_deviation = traj_metrics['averageDeviation']
        
        # Calculate hover non-selected ratio
        hover_counts = hover.get('hoverCounts', {})
        selected_response = metadata.get('selectedResponse', '')
        
        if hover_counts:
            total_hovers = sum(hover_counts.values())
            selected_hovers = hover_counts.get(selected_response, 0)
            non_selected_hovers = total_hovers - selected_hovers
            hover_ratio = non_selected_hovers / total_hovers if total_hovers > 0 else 0
        else:
            hover_ratio = 0
        
        # Total metrics
        total_max_dev = max_dev_pos + max_dev_neg
        total_auc = auc_pos + auc_neg
        total_flips = x_flips + y_flips
        
        # Normalize components (using conceptual ranges)
        # These ranges are based on typical observed values
        norm_max_dev = min(total_max_dev / 100, 1.0)  # Max ~100px
        norm_auc = min(total_auc / 500, 1.0)           # Max ~500
        norm_flips = min(total_flips / 20, 1.0)        # Max ~20 flips
        norm_avg_dev = min(avg_deviation / 50, 1.0)    # Max ~50px
        norm_velocity = 1 - min(avg_velocity / 2000, 1.0)  # Lower velocity = more time
        norm_hover = hover_ratio  # Already in [0, 1]
        
        # SCI Formula (weighted sum)
        sci_raw = (
            0.25 * norm_flips +         # 25%: Direction changes
            0.20 * norm_max_dev +       # 20%: Maximum deviation
            0.20 * norm_auc +           # 20%: Area under curve
            0.15 * norm_avg_dev +       # 15%: Average deviation
            0.10 * norm_velocity +      # 10%: Time spent
            0.10 * norm_hover           # 10%: Hover on non-selected
        )
        
        # Scale to [0, 100]
        sci = sci_raw * 100
        
        return sci
    
    # =========================================================================
    # UEI CALCULATION
    # =========================================================================
    
    def calculate_uei(self, data: Dict[str, Any]) -> float:
        """
        Calculate User Engagement Index (UEI).
        
        UEI measures cognitive engagement using a Dual Engagement Model:
        - Confident Engagement: fast, direct, smooth, decisive
        - Exploratory Engagement: complex, deliberate
        
        Args:
            data: Dictionary with trajectory and metrics
        
        Returns:
            UEI score [0-100]
        """
        metrics = data.get('metrics', {})
        trajectory = data.get('trajectory', [])
        
        # Extract metrics
        deviation = metrics.get('deviation', {})
        velocity = metrics.get('velocity', {})
        complexity = metrics.get('complexity', {})
        
        max_dev_pos = deviation.get('maxDeviationPositive', 0)
        max_dev_neg = abs(deviation.get('maxDeviationNegative', 0))
        auc_pos = deviation.get('aucPositive', 0)
        auc_neg = abs(deviation.get('aucNegative', 0))
        
        avg_velocity = velocity.get('averageVelocityPxPerSec', 500)
        max_velocity = velocity.get('maximalVelocityPxPerSec', 1000)
        
        angle_entropy = complexity.get('angleEntropy', 1.0)
        initiation_time = complexity.get('initiationTimeMs', 200)
        
        # Calculate trajectory metrics
        traj_metrics = self.calculate_trajectory_metrics(trajectory)
        trajectory_length = traj_metrics['trajectoryLength']
        smoothness = traj_metrics['trajectorySmoothness']
        
        # Total metrics
        total_max_dev = max_dev_pos + max_dev_neg
        total_auc = auc_pos + auc_neg
        
        # === ENGAGEMENT TYPE 1: CONFIDENT (fast + direct + smooth + decisive) ===
        
        # Directness: inverse of deviation (normalize to typical range)
        directness = 1 - min(total_max_dev / 100, 1.0)
        
        # Smoothness: already calculated
        smoothness_norm = smoothness if smoothness is not None else 0.5
        
        # Appropriate speed: not too slow (normalize avg velocity)
        not_too_slow = min(avg_velocity / 1000, 1.0)
        
        # Decisiveness: high max velocity (normalize)
        decisiveness = min(max_velocity / 2000, 1.0)
        
        # Confident engagement score
        confident_engagement = (directness + smoothness_norm + not_too_slow + decisiveness) / 4
        
        # === ENGAGEMENT TYPE 2: EXPLORATORY (complex + deliberate) ===
        
        # Exploration: entropy, AUC, length (normalize each)
        norm_entropy = min(angle_entropy / 3.0, 1.0)
        norm_auc = min(total_auc / 500, 1.0)
        norm_length = min(trajectory_length / 5.0, 1.0)
        
        exploration = (norm_entropy + norm_auc + norm_length) / 3
        
        # Deliberation: not too fast (inverse of velocity)
        deliberation = 1 - min(avg_velocity / 1000, 1.0)
        
        # Exploratory engagement score
        exploratory_engagement = (exploration * 0.7 + deliberation * 0.3)
        
        # === FINAL UEI: Maximum of both types ===
        uei_raw = max(confident_engagement, exploratory_engagement)
        
        # Speed penalty for instant response (<100ms = suspicious)
        if initiation_time < 100:
            speed_penalty = 0.7
        else:
            speed_penalty = 1.0
        
        # Apply penalty and scale to [0, 100]
        uei = uei_raw * speed_penalty * 100
        
        # Clamp to [0, 100]
        uei = max(0, min(100, uei))
        
        return uei
    
    # =========================================================================
    # SEI CALCULATION (requires history)
    # =========================================================================
    
    def add_to_history(self, sci: float, uei: float, metadata: Dict[str, Any]) -> None:
        """
        Add a question's SCI/UEI scores to history for SEI calculation.
        
        Args:
            sci: SCI score for the question
            uei: UEI score for the question
            metadata: Question metadata (userId, questionId, etc.)
        """
        self.history.append({
            'sci': sci,
            'uei': uei,
            'userId': metadata.get('userId', ''),
            'questionId': metadata.get('questionId', ''),
            'timestamp': metadata.get('timestamp', '')
        })
    
    def calculate_sei(self, user_id: Optional[str] = None) -> float:
        """
        Calculate Survey Engagement Index (SEI) - Dynamic/Cumulative.
        
        SEI is calculated cumulatively based on all questions answered so far.
        
        Args:
            user_id: Optional user ID to filter history (if None, uses all history)
        
        Returns:
            SEI score [0-100] based on cumulative engagement
        """
        # Filter history by user_id if provided
        if user_id:
            history = [h for h in self.history if h['userId'] == user_id]
        else:
            history = self.history
        
        if not history:
            return 50.0  # Neutral score if no history
        
        # Extract SCI and UEI values
        sci_values = [h['sci'] for h in history]
        uei_values = [h['uei'] for h in history]
        
        # === PRIMARY COMPONENTS ===
        cumulative_mean_uei = np.mean(uei_values)
        cumulative_mean_sci = np.mean(sci_values)
        
        # === SECONDARY: Consistency and Quality ===
        if len(uei_values) > 1:
            cumulative_sd_uei = np.std(uei_values, ddof=1)
            cumulative_cv_uei = cumulative_sd_uei / cumulative_mean_uei if cumulative_mean_uei > 0 else 0
        else:
            cumulative_cv_uei = 0
        
        consistency = 1 / (1 + cumulative_cv_uei)
        
        # High engagement ratio (UEI > 60)
        high_engagement_ratio = sum(1 for u in uei_values if u > 60) / len(uei_values)
        
        # Low engagement penalty (UEI < 30)
        low_engagement_ratio = sum(1 for u in uei_values if u < 30) / len(uei_values)
        
        # Engaged despite conflict (SCI > 50 AND UEI > 60)
        balance = sum(1 for s, u in zip(sci_values, uei_values) if s > 50 and u > 60) / len(uei_values)
        
        # === NORMALIZATION ===
        # Normalize to [0, 1] using typical ranges
        norm_uei = cumulative_mean_uei / 100
        norm_sci = cumulative_mean_sci / 100
        norm_consistency = consistency  # Already in [0, 1]
        norm_high_ratio = high_engagement_ratio
        norm_low_penalty = 1 - low_engagement_ratio
        norm_balance = balance
        
        # === FINAL SEI CALCULATION ===
        sei_raw = (
            0.40 * norm_uei +           # Average engagement (40%)
            0.20 * norm_sci +           # Conflict/cognitive effort (20%)
            0.15 * norm_consistency +   # Consistency (15%)
            0.10 * norm_high_ratio +    # High engagement ratio (10%)
            0.10 * norm_balance +       # Engaged despite conflict (10%)
            0.05 * norm_low_penalty     # Low engagement penalty (5%)
        )
        
        # Scale to [0, 100]
        sei = sei_raw * 100
        
        return sei
    
    # =========================================================================
    # MAIN CALCULATION METHOD
    # =========================================================================
    
    def calculate_all(self, data: Dict[str, Any], update_history: bool = True) -> Dict[str, float]:
        """
        Calculate all indices (SCI, UEI, SEI) from input data.
        
        Args:
            data: Dictionary with metadata, trajectory, and metrics
            update_history: If True, adds SCI/UEI to history for SEI calculation
        
        Returns:
            Dictionary with 'SCI', 'UEI', 'SEI' scores [0-100]
        """
        # Calculate SCI and UEI
        sci = self.calculate_sci(data)
        uei = self.calculate_uei(data)
        
        # Add to history if requested
        if update_history:
            metadata = data.get('metadata', {})
            self.add_to_history(sci, uei, metadata)
        
        # Calculate SEI (cumulative)
        user_id = data.get('metadata', {}).get('userId')
        sei = self.calculate_sei(user_id)
        
        return {
            'SCI': round(sci, 2),
            'UEI': round(uei, 2),
            'SEI': round(sei, 2)
        }
    
    def reset_history(self) -> None:
        """Reset the history (useful for new survey session)."""
        self.history = []
    
    def get_history(self, user_id: Optional[str] = None) -> List[Dict]:
        """
        Get history of SCI/UEI scores.
        
        Args:
            user_id: Optional user ID to filter history
        
        Returns:
            List of history entries
        """
        if user_id:
            return [h for h in self.history if h['userId'] == user_id]
        return self.history
