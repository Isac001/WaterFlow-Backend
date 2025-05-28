from celery import shared_task
from apps.bimonthly_water_consumption.utils import bimonthly_water_consumption
from django.conf import settings
from datetime import datetime


@shared_task(
    bind=True,
    max_retries=3,
    soft_time_limit=300,
    priority=5,
)
def bimonthly_water_consumption_task(self):
    """
    Celery task to calculate and store bimonthly water consumption with audit logging.
    """
    audit_log_path = f"{settings.BASE_DIR}/core/logs_audit/bimonthly_logs.txt"
    
    def write_log(message, is_start=False, is_end=False):
        """Helper function to write formatted audit logs"""
        time_stamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        with open(audit_log_path, "a", encoding="utf-8") as audit_file:
            if is_start:
                audit_file.write("{\n")
                log_entry = f"    TASK INICIADA: {message} [{time_stamp}]\n"
            elif is_end:
                log_entry = f"    TASK FINALIZADA! [{time_stamp}]\n"
                log_entry += "}\n\n"  
            else:
                log_entry = f"        {message}\n"
            
            audit_file.write(log_entry)

    try:
        write_log("Cálculo do consumo bimestral de água", is_start=True)
        
        task_in_working = bimonthly_water_consumption()

        if not task_in_working:
            write_log("Bimestre já processado ou sem dados válidos")
            write_log("", is_end=True)
            return {
                "status": "warning",
                "message": "Bimestre já processado ou sem dados válidos",
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
            "bimonth": task_in_working.date_label,
            "total_consumption": float(task_in_working.total_consumption),
            "audit_log": audit_log_path
        }

    except Exception as e:
        error_msg = f"Falha na task: {str(e)}. Reagendando nova tentativa..."
        write_log(error_msg)
        write_log("", is_end=True)
        raise self.retry(exc=e, countdown=60)