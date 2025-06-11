# Django and Python Imports
from celery import shared_task
from django.conf import settings
from datetime import datetime

# Project Impors
from apps.weekly_water_consumption.utils import calculate_weekly_water_consumption

# Decorate the function as a shared Celery task with specific configurations
@shared_task(
    bind=True,
    max_retries=3,
    soft_timeout=300,
    priority=5,
)
# Define the Celery task function for weekly water consumption
def weekly_water_consumption_task(self):

    """
    Celery task to calculate and store weekly water consumption.
    """

    # Define the path for the weekly audit log file using Django settings
    audit_logs_path = f"{settings.BASE_DIR}/core/logs_audit/weekly_logs.txt"

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
        
        # Log the start of the weekly consumption task
        write_log("Iniciando task de consumo semanal...", is_start=True)

        # Call the function to calculate weekly water consumption
        task_in_working = calculate_weekly_water_consumption() # Stores the created WeeklyWaterConsumption object or None

        # Check if the weekly consumption was not processed (e.g., already exists or no data)
        if not task_in_working:

            # Log that the week was already processed or has no valid data
            write_log("Semana já processada ou sem dados válidos.")

            # Log the end of the task
            write_log("", is_end=True)

            # Return a warning status and message
            return {
                "status": "warning",
                "message": "Semana já processada ou sem dados válidos."
            }
        
        # If processing was successful, format the details for logging
        weekly_details = (
            f"TASK CONCLUÍDA - ID: {task_in_working.id}\n"
            f"           Período da leitura: {task_in_working.date_label}\n"
            f"           Litros de água consumidos: {task_in_working.total_consumption}\n"
            f"           Data do início da leitura: {task_in_working.start_date.strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"           Data do fim da leitura: {task_in_working.end_date.strftime('%d-%m-%Y %H:%M:%S')}"
        )

        # Write the weekly consumption details to the log
        write_log(weekly_details)

        # Log the end of the task
        write_log("", is_end=True)
        
        # Return a success status and details of the processed week
        return {
            "status": "success",
            "week": task_in_working.date_label,
            "total_consumption": float(task_in_working.total_consumption),
            "start_date": task_in_working.start_date.strftime('%d-%m-%Y %H:%M:%S'),
            "end_date": task_in_working.end_date.strftime('%d-%m-%Y %H:%M:%S')
        }

    # Catch any exception that occurs during the try block
    except Exception as e:

        # Format an error message including the exception details
        error_message = f"Erro ao calcular o consumo semanal de água: {e}"

        # Write the error message to the log
        write_log(error_message)

        # Log the end of the task (even if it failed)
        write_log("", is_end=True)
        
        # Raise a retry exception to Celery, scheduling a retry with a countdown and max retries
        raise self.retry(exc=e, countdown=60, max_retries=3)