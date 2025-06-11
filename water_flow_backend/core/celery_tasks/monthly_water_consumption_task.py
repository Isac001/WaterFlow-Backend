# Django and Python Imports
from celery import shared_task
from django.conf import settings
from datetime import datetime

# Project Imports
from apps.monthly_water_consumption.utils import monthly_water_consumption


# Decorate the function as a shared Celery task with specific configurations
@shared_task(
    bind=True,
    max_retries=3,
    soft_timeout=300,
    priority=5,
)
# Define the Celery task function for monthly water consumption
def monthly_water_consumption_task(self):

    """
    Celery task to calculate and store monthly water consumption.
    """

    # Define the path for the monthly audit log file using Django settings
    audit_logs_path = f"{settings.BASE_DIR}/core/logs_audit/monthly_logs.txt"

    # Define a helper function to write messages to the audit log
    def write_log(message, is_start=False, is_end=False):

        # Get the current timestamp formatted as string
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Open the audit log file in append mode with UTF-8 encoding
        with open(audit_logs_path, "a", encoding="utf-8") as audit_file:

            # Check if this log entry marks the start of a task
            if is_start:
                audit_file.write("{\n")
                log_entry = f"      TASK INICIADA: {message} | [{timestamp}]\n"

            # Check if this log entry marks the end of a task
            elif is_end:
                log_entry = f"      TASK FINALIZADA! | [{timestamp}]\n"
                log_entry += "}\n\n"

            # For regular log messages within the task
            else:

                # Format a regular log entry
                log_entry = f"      {message}\n"

            # Write the formatted log entry to the file
            audit_file.write(log_entry)

    # Start a try block to handle potential exceptions during task execution
    try:

        # Log the start of the monthly consumption task
        write_log("Iniciando task de consumo mensal...", is_start=True)

        # Call the function to calculate monthly water consumption
        task_in_working = monthly_water_consumption() 

        # Check if the monthly consumption was not processed (e.g., already exists or no data)
        if not task_in_working:

            # Log that the month was already processed or has no valid data
            write_log("Mês já processado ou sem dados válidos.")
            # Log the end of the task
            write_log("", is_end=True)

            # Return a warning status and message
            return {
                "status": "warning",
                "message": "Mês já processado ou sem dados válidos."
                }
        
        # If processing was successful, format the details for logging
        task_details = (
            # Format the ID of the created record
            f"TASK CONCLUIDA - ID: {task_in_working.id}\n"
            # Format the period label of the reading
            f"           Época da leitura: {task_in_working.date_label}\n"
            # Format the total water consumption
            f"           Litros de água consumidos: {task_in_working.total_consumption}\n"
            # Format the start date of the reading
            f"           Data do início da leitura: {task_in_working.start_date.strftime("%d-%m-%Y %H:%M:%S")}\n" # Note: start_date is DateField, %H:%M:%S might be 00:00:00
            # Format the end date of the reading
            f"           Data do fim da leitura: {task_in_working.end_date.strftime("%d-%m-%Y %H:%M:%S")}" # Note: end_date is DateField, %H:%M:%S might be 00:00:00
            )
        
        # Write the monthly consumption details to the log
        write_log(task_details)
        # Log the end of the task
        write_log("", is_end=True)
        
        # Return a success status and details of the processed month
        return {
            "status": "success",
            "month": task_in_working.date_label,
            # Ensure total consumption is returned as float
            "total_consumption": float(task_in_working.total_consumption),
            "start_date": task_in_working.start_date,
            "end_date": task_in_working.end_date
        }

    # Catch any exception that occurs during the try block
    except Exception as e:
        # Format an error message including the exception details (Note: message says "diário" but task is "mensal")
        error_message = f"Erro ao calcular o consumo diário de água: {e}" # Consider changing "diário" to "mensal"
        # Write the error message to the log
        write_log(error_message)
        # Log the end of the task (even if it failed)
        write_log("", is_end=True)
        # Raise a retry exception to Celery, scheduling a retry with a countdown and max retries
        raise self.retry(exc=e, countdown=60, max_retries=3)