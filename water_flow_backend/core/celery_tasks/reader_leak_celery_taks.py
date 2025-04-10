from celery import shared_task
from apps.weekly_water_consumption.utils import calculate_weekly_water_consumption
import logging

logger = logging.getLogger(__name__)
@shared_task(
        bind=True,
    max_retries=3,
    soft_timeout=300,
    priority=5,
)
def weekly_water_consumption_task(self):
    """
    Celery task to calculate and store weekly water consumption.
    """

    logger.info("Iniciando tarefa de cálculo do consumo semanal de água.")

    try:

        result = calculate_weekly_water_consumption()

        if not result:
            logger.warning("Semana já processada ou sem dados válidos.")
            return {"status": "warning", "message": "Semana já processada ou sem dados válidos."}
        
        logger.info("Cálculo do consumo semanal de água concluído com sucesso.")

        return {
            "status": "success",
            "week": result.date_label,
            "total_consumption": float(result.total_consumption),
        }

    except Exception as e:

        logger.error(f"Erro ao calcular o consumo semanal de água: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
    
    finally:
        
        logger.info("Tarefa de cálculo do consumo semanal de água concluida.")


