import numpy as np
from typing import List, Dict, Any
from scipy import stats


class StatisticalAnalyzer:
    """Статистический анализ метрик"""

    @staticmethod
    def calculate_descriptive_stats(values: List[float]) -> Dict[str, float]:
        """Описательная статистика"""
        if not values:
            return {}

        arr = np.array(values)

        return {
            'mean': float(np.mean(arr)),
            'median': float(np.median(arr)),
            'std': float(np.std(arr, ddof=1)),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'q1': float(np.percentile(arr, 25)),
            'q3': float(np.percentile(arr, 75)),
            'iqr': float(np.percentile(arr, 75) - np.percentile(arr, 25))
        }

    @staticmethod
    def detect_outliers(values: List[float], method: str = 'iqr') -> Dict:
        """Обнаружение выбросов"""
        if len(values) < 3:
            return {'outliers': [], 'bounds': {}}

        arr = np.array(values)

        if method == 'iqr':
            q1 = np.percentile(arr, 25)
            q3 = np.percentile(arr, 75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers = [float(x) for x in arr if x < lower or x > upper]

            return {
                'outliers': outliers,
                'bounds': {'lower': float(lower), 'upper': float(upper)},
                'method': 'iqr'
            }

    @staticmethod
    def confidence_interval(values: List[float], confidence: float = 0.95) -> Dict:
        """Доверительный интервал"""
        if len(values) < 2:
            return {}

        arr = np.array(values)
        mean = np.mean(arr)
        std = np.std(arr, ddof=1)
        n = len(arr)
        se = std / np.sqrt(n)

        t_value = stats.t.ppf((1 + confidence) / 2, n - 1)
        margin = t_value * se

        return {
            'mean': float(mean),
            'lower': float(mean - margin),
            'upper': float(mean + margin),
            'margin': float(margin)
        }