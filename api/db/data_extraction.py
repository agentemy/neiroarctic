from sqlalchemy import select
from typing import List, Dict, Any

from .database import Base
from .database import async_session_maker

async def get_all_physiological_by_individual(
    individual_number: str,
) -> List[Dict[str, Any]]:
    PhysiologicalMetrics = Base.classes.physiological_metrics
    async with async_session_maker() as session:
        result = await session.scalars(
            select(PhysiologicalMetrics)
            .where(PhysiologicalMetrics.individual_number == individual_number)
        )

        return [
            {
                "session": r.session,
                "relax": r.relax,
                "fatigue": r.fatigue,
                "concentration": r.concentration,
                "stress": r.stress,
            }
            for r in result
        ]
