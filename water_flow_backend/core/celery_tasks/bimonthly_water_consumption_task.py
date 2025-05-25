from celery import shared_task
from apps.bimonthly_water_consumption.utils import bimonthly_water_consumption
import logging
from builtins import Exception

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    soft_timeout=300,
    priority=5,
)
def bimonthly_water_consumption_task(self):
    """
    Celery task to calculate and store bimonthly water consumption.
    """

    logger.info("Iniciando tarefa de cálculo do consumo bimestral de água.")

    try:
        result = bimonthly_water_consumption()

        if not result:
            logger.warning("Bimestre já processado ou sem dados válidos.")
            return {
                "status": "warning",
                "message": "Bimestre já processado ou sem dados válidos."
            }

        logger.info("Cálculo do consumo bimestral de água concluído com sucesso.")

        return {
            "status": "success",
            "bimonth": result.date_label,
            "total_consumption": float(result.total_consumption),
        }

    except Exception as e:
        logger.error(f"Erro ao calcular o consumo bimestral de água: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

    finally:
        logger.info("Tarefa de cálculo do consumo bimestral de água concluída.")
