# from celery import shared_task
# from apps.bimonthly_water_consumption.utils import bimonthly_water_consumption
# from django.conf import settings
# from datetime import datetime


# @shared_task(
#     bind=True,
#     max_retries=3,
#     soft_time_limit=300,
#     priority=5,
# )
# def bimonthly_water_consumption_task(self):
#     """
#     Celery task to calculate and store bimonthly water consumption with audit logging.
#     """
#     audit_log_path = f"{settings.BASE_DIR}/core/logs_audit/bimonthly_logs.txt"
    
#     def write_log(message, is_start=False, is_end=False, is_concluded=False):
#         """Helper function to write formatted audit logs"""
#         time_stamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
#         with open(audit_log_path, "a", encoding="utf-8") as audit_file:
#             if is_start:
#                 audit_file.write("{\n")
#                 log_entry = f"      TASK INICIADA: {message} | [{time_stamp}]\n"
#             elif is_end:
#                 log_entry = f"      TASK FINALIZADA! | [{time_stamp}]\n"
#                 log_entry += "}\n\n"  
#             elif is_concluded:
#                 log_entry = f"      TASK CONCLUÍDA!\n"
#             else:
#                 log_entry = f"           {message}\n"
            
#             audit_file.write(log_entry)

#     try:
#         write_log("Iniciando task de consumo bimestral...", is_start=True)
        
#         task_in_working = bimonthly_water_consumption()

#         if not task_in_working:
#             write_log("Bimestre já processado ou sem dados válidos")
#             write_log("", is_end=True)
#             return {
#                 "status": "warning",
#                 "message": "Bimestre já processado ou sem dados válidos",
#             }

#         write_log("", is_concluded=True)
#         write_log(f"Período da leitura: {task_in_working.date_label}")
#         write_log(f"Litros de água consumidos: {task_in_working.total_consumption}")
#         write_log(f"Data do início da leitura: {task_in_working.start_date.strftime('%d/%m/%Y')}")
#         write_log(f"Data do fim da leitura: {task_in_working.end_date.strftime('%d/%m/%Y')}")
        
#         write_log("", is_end=True)

#         return {
#             "status": "success",
#             "bimonth": task_in_working.date_label,
#             "total_consumption": float(task_in_working.total_consumption),
#             "start_date": task_in_working.start_date.strftime('%d/%m/%Y'),
#             "end_date": task_in_working.end_date.strftime('%d/%m/%Y')
#         }

#     except Exception as e:
#         error_msg = f"Falha na task: {str(e)}. Reagendando nova tentativa..."
#         write_log(error_msg)
#         write_log("", is_end=True)
#         raise self.retry(exc=e, countdown=60)

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
    
    def write_log(message, is_start=False, is_end=False, is_concluded=False):
        time_stamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open(audit_log_path, "a", encoding="utf-8") as audit_file:
            if is_start:
                audit_file.write("{\n")
                log_entry = f"      TASK INICIADA: {message} | [{time_stamp}]\n"
            elif is_end:
                log_entry = f"      TASK FINALIZADA! | [{time_stamp}]\n"
                log_entry += "}\n\n"  
            elif is_concluded:
                log_entry = f"      TASK CONCLUÍDA!\n"
            else:
                log_entry = f"           {message}\n"
            audit_file.write(log_entry)

    try:
        write_log("Iniciando task de consumo bimestral...", is_start=True)
        
        task_result = bimonthly_water_consumption()

        if not task_result:
            write_log("Bimestre já processado ou sem dados válidos")
            write_log("", is_end=True)
            return {
                "status": "warning",
                "message": "Bimestre já processado ou sem dados válidos",
            }

        write_log("", is_concluded=True)
        write_log(f"Período da leitura: {task_result.date_label}")
        write_log(f"Litros de água consumidos: {task_result.total_consumption}")
        write_log(f"Data do início da leitura: {task_result.start_date.strftime('%d/%m/%Y')}")
        write_log(f"Data do fim da leitura: {task_result.end_date.strftime('%d/%m/%Y')}")
        
        write_log("", is_end=True)

        return {
            "status": "success",
            "bimonth": task_result.date_label,
            "total_consumption": float(task_result.total_consumption),
            "start_date": task_result.start_date.strftime('%d/%m/%Y'),
            "end_date": task_result.end_date.strftime('%d/%m/%Y')
        }

    except Exception as e:
        error_msg = f"Falha na task: {str(e)}. Reagendando nova tentativa..."
        write_log(error_msg)
        write_log("", is_end=True)
        raise self.retry(exc=e, countdown=60)
