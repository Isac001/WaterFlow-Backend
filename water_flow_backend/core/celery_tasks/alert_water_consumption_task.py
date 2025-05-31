# core/celery_tasks/alert_water_consumption_task.py
from celery import shared_task
import logging
from django.conf import settings
from datetime import datetime
from apps.alert_water_consumption.utils import WaterConsumptionAlertGenerator

@shared_task(
    bind=True,
    max_retries=3,
    soft_time_limit=300,
    priority=6,
)
def alert_water_consumption_task(self):
    """
    Celery task to generate water consumption alerts with formatted audit logging.
    """
    audit_log_path = f"{settings.BASE_DIR}/core/logs_audit/alert_logs.txt"
    
    def write_log(message, is_start=False, is_end=False):
        """Helper function to write formatted audit logs"""
        time_stamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        with open(audit_log_path, "a", encoding="utf-8") as audit_file:
            if is_start:
                audit_file.write("{\n")
                log_entry = f"      TASK INICIADA: {message} [{time_stamp}]\n"
            elif is_end:
                log_entry = f"      TASK FINALIZADA! [{time_stamp}]\n"
                log_entry += "}\n\n"  
            else:
                log_entry = f"        {message}\n"
            
            audit_file.write(log_entry)

    try:
        write_log("Verificação de alertas de consumo de água", is_start=True)
        
        task_in_working = WaterConsumptionAlertGenerator.check_for_alerts()

        if not task_in_working:

            write_log("Nenhum consumo excessivo detectado")
            write_log("", is_end=True)

            return {
                "status": "success",
                "alert_created": False,
                "message": "No excessive consumption detected",
                "audit_log": audit_log_path
            }
        
        alert_details = (
            f"ALERTA CRIADO - ID: {task_in_working.id}\n"
            f"        Tipo: {task_in_working.alert_type}\n"
            f"        Excesso: {float(task_in_working.total_consumption_exceeded):.2f}\n"
            f"        Percentual: {float(task_in_working.percentage_exceeded):.2f}%"
        )
        write_log(alert_details)
        write_log("", is_end=True)

        return {
            "status": "success",
            "alert_created": True,
            "alert_id": task_in_working.id,
            "alert_type": task_in_working.alert_type,
            "exceeded_amount": float(task_in_working.total_consumption_exceeded),
            "percentage": float(task_in_working.percentage_exceeded),
            "message": str(task_in_working),
            "audit_log": audit_log_path
        }

    except Exception as e:
        error_msg = f"Falha na task: {str(e)}. Reagendando nova tentativa..."
        write_log(error_msg)
        write_log("", is_end=True)
        raise self.retry(exc=e, countdown=60)