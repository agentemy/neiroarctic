from fastapi import APIRouter, HTTPException
from ..db.data_extraction import get_all_physiological_by_individual
from ..analytics.stats import StatisticalAnalyzer

router = APIRouter(prefix="/charts", tags=["charts"])
analyzer = StatisticalAnalyzer()


@router.get("/{individual_number}")
async def get_chart_data(individual_number: str):
    """Получить данные для построения графиков"""
    data = await get_all_physiological_by_individual(individual_number)

    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    # Разделяем по метрикам
    fatigue_values = [d['fatigue'] for d in data if d.get('fatigue') is not None]
    stress_values = [d['stress'] for d in data if d.get('stress') is not None]
    concentration_values = [d['concentration'] for d in data if d.get('concentration') is not None]
    relax_values = [d['relax'] for d in data if d.get('relax') is not None]

    return {
        "individual_number": individual_number,
        "total_records": len(data),
        "charts": {
            "fatigue": {
                "values": fatigue_values,
                "stats": analyzer.calculate_descriptive_stats(fatigue_values),
                "outliers": analyzer.detect_outliers(fatigue_values)
            },
            "stress": {
                "values": stress_values,
                "stats": analyzer.calculate_descriptive_stats(stress_values),
                "outliers": analyzer.detect_outliers(stress_values)
            },
            "concentration": {
                "values": concentration_values,
                "stats": analyzer.calculate_descriptive_stats(concentration_values),
                "outliers": analyzer.detect_outliers(concentration_values)
            },
            "relax": {
                "values": relax_values,
                "stats": analyzer.calculate_descriptive_stats(relax_values),
                "outliers": analyzer.detect_outliers(relax_values)
            }
        }
    }


@router.get("/{individual_number}/statistics")
async def get_statistics(individual_number: str):
    """Получить статистику"""
    data = await get_all_physiological_by_individual(individual_number)

    result = {"individual_number": individual_number, "overall": {}}

    for metric in ['fatigue', 'stress', 'concentration', 'relax']:
        values = [d[metric] for d in data if d.get(metric) is not None]
        if values:
            result['overall'][metric] = {
                "stats": analyzer.calculate_descriptive_stats(values),
                "confidence_interval": analyzer.confidence_interval(values),
                "outliers": analyzer.detect_outliers(values)
            }

    return result