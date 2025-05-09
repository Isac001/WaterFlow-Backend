# apps/monthly_water_consumption/tasks.py

from celery import shared_task
from apps.monthly_water_consumption.utils import monthly_water_consumption
import logging

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    soft_timeout=300,
    priority=5,
)
def monthly_water_consumption_task(self):
    """
    Celery task to calculate and store monthly water consumption.
    """

    logger.info("Iniciando tarefa de cálculo do consumo mensal de água.")

    try:
        result = monthly_water_consumption()

        if not result:
            logger.warning("Mês já processado ou sem dados válidos.")
            return {"status": "warning", "message": "Mês já processado ou sem dados válidos."}
        
        logger.info("Cálculo do consumo mensal de água concluído com sucesso.")

        return {
            "status": "success",
            "month": result.data_label,
            "total_consumption": float(result.total_consumption),
        }

    except Exception as e:
        logger.error(f"Erro ao calcular o consumo mensal de água: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

    finally:
        logger.info("Tarefa de cálculo do consumo mensal de água concluída.")
