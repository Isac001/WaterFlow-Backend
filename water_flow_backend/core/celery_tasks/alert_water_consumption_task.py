# Django and Python Imports
from celery import shared_task
from django.conf import settings
from datetime import datetime

# Project Imports
from apps.alert_water_consumption.utils import check_for_alerts

# Decorate the function as a shared Celery task with specific configurations
@shared_task(
    bind=True,
    max_retries=3,
    soft_time_limit=300,
    priority=6,
)
# Define the Celery task function
def alert_water_consumption_task(self):

    """
    Celery task to generate water consumption alerts with formatted audit logging.
    """

    # Define the path for the audit log file using Django settings
    audit_log_path = f"{settings.BASE_DIR}/core/logs_audit/alert_logs.txt"
    
    # Define a helper function to write messages to the audit log
    def write_log(message, is_start=False, is_end=False):

        """
        Helper function to write formatted audit logs
        """

        # Getter the timestamp of day and format it
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Open the audit log file in append mode with UTF-8 encoding
        with open(audit_log_path, "a", encoding="utf-8") as audit_file:

            # Check if this log entry marks the start of a task
            if is_start:
                audit_file.write("{\n")
                log_entry = f"      TASK INICIADA: {message} | [{timestamp}]\n"

            # Check if this log entry marks the end of a task
            elif is_end:
                log_entry = f"      TASK FINALIZADA!  | [{timestamp}]\n"
                log_entry += "}\n\n"  

            # For regular log messages within the task
            else:
                log_entry = f"        {message}\n"
            
            # Write the formatted log entry to the file
            audit_file.write(log_entry)

    # Start a try block to handle potential exceptions during task execution
    try:

        # Log the start of the water consumption alert check
        write_log("Verificação de alertas de consumo de água", is_start=True)
        
        # Call the function to check for alerts and get the result
        task_in_working = check_for_alerts() # This variable name seems to imply a status rather than the alert object itself

        # Check if no alert was created (task_in_working is None or False)
        if not task_in_working:

            # Log that no excessive consumption was detected
            write_log("Nenhum consumo excessivo detectado")

            # Log the end of the task
            write_log("", is_end=True)

            # Return a dictionary indicating success and no alert created
            return {
                "status": "success",
                "alert_created": False,
                "message": "No excessive consumption detected",
            }
        
        # If an alert was created, format the alert details for logging
        alert_details = (
            f"ALERTA CRIADO - ID: {task_in_working.id}\n"
            f"        Tipo: {task_in_working.alert_type}\n"
            f"        Excesso: {float(task_in_working.total_consumption_exceeded):.2f}\n"
            f"        Percentual: {float(task_in_working.percentage_exceeded):.2f}%"
        )

        # Write the alert details to the log
        write_log(alert_details)

        # Log the end of the task
        write_log("", is_end=True)

        # Return a dictionary indicating success and details of the created alert
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

    # Catch any exception that occurs during the try block
    except Exception as e:

        # Format an error message including the exception details
        error_messsage = f"Falha na task: {str(e)}. Reagendando nova tentativa..."

        # Write the error message to the log
        write_log(error_messsage)

        # Log the end of the task (even if it failed)
        write_log("", is_end=True)

        # Raise a retry exception to Celery, scheduling a retry with a countdown
        raise self.retry(exc=e, countdown=60)