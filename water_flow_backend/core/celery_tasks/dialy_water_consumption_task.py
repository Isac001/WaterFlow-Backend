from celery import shared_task
from apps.dialy_water_consumption.utils import daily_water_consumption
import logging
from builtins import Exception

@shared_task(
    bind=True,
    max_retries=3,
    soft_timeout=300,
    priority=5,
)
def daily_water_consumption_task(self):
    """
    Celery task to calculate and store daily water consumption.
    """

    logger = logging.getLogger(__name__)
    logger.info('Iniciando a tarefa de cálculo do consumo diário de água...')

    try:

        resutl = daily_water_consumption()

        if not resutl:
            logger.warning("Dia já processado ou sem dados válidos.")
            return {
                "status": "warning",
                "message": "Dia já processado ou sem dados válidos."
            }
        logger.info("Cálculo do consumo diário de água concluído com sucesso.")

        return {
            "status": "success",
            "day": resutl.date_label,
            "total_consumption": float(resutl.total_consumption),   
        }

    except Exception as e:
        logger.error(f"Erro ao calcular o consumo diário de água: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
    
    finally:
        logger.info("Tarefa de cálculo do consumo diário de água concluída.")