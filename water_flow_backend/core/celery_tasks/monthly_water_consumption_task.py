# apps/monthly_water_consumption/tasks.py

from celery import shared_task
from apps.monthly_water_consumption.utils import monthly_water_consumption
import logging
from django.conf import settings
from datetime import datetime


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

    audit_logs_path = f"{settings.BASE_DIR}/core/logs_audit/monthly_logs.txt"

    def write_log(message, is_start=False, is_end=False):

        with open(audit_logs_path, "a", encoding="utf-8") as audit_logs:
            if is_start:
                audit_logs.write("{\n")
                log_entry = f"      TASK INICIADA: {message} | [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]"

            elif is_end:
                log_entry = f"      TASK FINALIZADA! | [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]"
                log_entry += "}\n\n"

            else:
                log_entry = f"      {message}\n"


    try:

        write_log("Iniciando task de consumo mensal...", is_start=True)

        task_in_working = monthly_water_consumption()

        if not task_in_working:
            write_log("Mês já processado ou sem dados válidos.")
            write_log("", is_end=True)
            return {
                "status": "warning",
                "message": "Mês já processado ou sem dados válidos."
                }
        
        write_log(
            f"TASK CONCLUIDA!"
            f"           Época da leitura: {task_in_working.date_label}"
            f"           Litros de água consumidos: {task_in_working.total_consumption}"
            f"           Data do início da leitura: {task_in_working.start_date}"
            f"           Data do fim da leitura: {task_in_working.end_date}"
            )
        write_log("", is_end=True)
        
        return {
            "status": "success",
            "month": task_in_working.date_label,
            "total_consumption": float(task_in_working.total_consumption),
            "start_date": task_in_working.start_date,
            "end_date": task_in_working.end_date
        }

    except Exception as e:
        error_message = f"Erro ao calcular o consumo diário de água: {e}"
        write_log(error_message)
        write_log("", is_end=True)
        raise self.retry(exc=e, countdown=60, max_retries=3)

   