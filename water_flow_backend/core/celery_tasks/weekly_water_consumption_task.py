from celery import shared_task
from apps.weekly_water_consumption.utils import calculate_weekly_water_consumption
from builtins import Exception

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


    try:

        result = calculate_weekly_water_consumption()

        if not result:
            return {"status": "warning", "message": "Semana já processada ou sem dados válidos."}
        

        return {
            "status": "success",
            "week": result.date_label,
            "total_consumption": float(result.total_consumption),
        }

    except Exception as e:

        raise self.retry(exc=e, countdown=60, max_retries=3)
    