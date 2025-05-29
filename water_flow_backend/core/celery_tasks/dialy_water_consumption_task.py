from celery import shared_task
from apps.daily_water_consumption.utils import calculate_daily_water_consumption
import logging
from builtins import Exception
from django.conf import settings
from datetime import datetime

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
    
    audit_log_path = f"{settings.BASE_DIR}/core/logs_audit/daily_logs.txt"

    def write_log(message, is_start=False, is_end=True):
        time_stamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        with open(audit_log_path, "a", encoding="utf-8") as audit_log:
            if is_start:
                audit_log.write("{\n")
                log_entry = f"      TASK INICIADA: {message} | [{time_stamp}]"
            
            elif is_end:
                log_entry = f"      TASK FINALIZADA! | [{time_stamp}]"
                log_entry += "}\n\n"
            
            else:
                log_entry = f"  {message}\n"
            
            audit_log.write(log_entry)

    try:
        write_log("Iniciando a Task de consumo de água diario", is_start=True)

        task_in_working = calculate_daily_water_consumption()

        if not task_in_working:
            write_log("Dia já processada ou sem dados válidos.")
            write_log(is_end=True)
            
            return {
                "status": "warning",
                "message": "Dia já processada ou sem dados válidos."
            }

        write_log(
            f"TASK CONCLUÍDA!"
            f"           Dia da leitura: {task_in_working.date_label}"
            f"           Litros de água consumidos: {task_in_working.total_consumption}"
        )
        
        write_log("", is_end=True)

        return {
            "status": "success",
            "date_label": task_in_working.date_label,
            "total_consumption": float(task_in_working.total_consumption),
        }

    except Exception as e:
        error_message = f"Erro ao calcular o consumo diario de água: {e}"
        write_log(error_message)
        write_log("", is_end=True)
        raise self.retry(exc=e, countdown=60, max_retries=3)