# Import shared_task decorator from Celery for creating asynchronous tasks
from celery import shared_task
# Import the utility function for daily water consumption calculation
from apps.daily_water_consumption.utils import calculate_daily_water_consumption
# Import the base Exception class
from builtins import Exception
# Import Django settings to access project configurations
from django.conf import settings
# Import datetime for handling timestamps
from datetime import datetime

# Decorate the function as a shared Celery task with specific configurations
@shared_task(
    # Bind the task instance (self) to the function
    bind=True,
    # Set the maximum number of retries for the task in case of failure
    max_retries=3,
    # Set a soft time limit for task execution in seconds (Note: parameter name is soft_time_limit, not soft_timeout)
    soft_time_limit=300, # Corrected from soft_timeout to soft_time_limit based on common Celery usage
    # Set the priority of the task
    priority=5,
)
# Define the Celery task function for daily water consumption
def daily_water_consumption_task(self):
    # Add a docstring to describe the Celery task
    """
    Celery task to calculate and store daily water consumption.
    """
    
    # Define the path for the daily audit log file using Django settings
    audit_log_path = f"{settings.BASE_DIR}/core/logs_audit/daily_logs.txt"

    # Define a helper function to write messages to the audit log
    def write_log(message, is_start=False, is_end=False):
        # Get the current timestamp formatted as string
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Open the audit log file in append mode with UTF-8 encoding
        with open(audit_log_path, "a", encoding="utf-8") as audit_file:
            # Check if this log entry marks the start of a task
            if is_start:
                # Write an opening brace for the task log block
                audit_file.write("{\n")
                # Format the log entry for task start
                log_entry = f"      TASK INICIADA: {message} | [{timestamp}]\n"
            
            # Check if this log entry marks the end of a task
            elif is_end:
                # Format the log entry for task end
                log_entry = f"      TASK FINALIZADA! | [{timestamp}]\n"
                # Add a closing brace and newlines for the task log block
                log_entry += "}\n\n"
            
            # For regular log messages within the task
            else:
                # Format a regular log entry
                log_entry = f"      {message}\n"
            
            # Write the formatted log entry to the file
            audit_file.write(log_entry)

    # Start a try block to handle potential exceptions during task execution
    try:
        # Log the start of the daily water consumption task
        write_log("Iniciando a Task de consumo de água diário...", is_start=True)

        # Call the function to calculate daily water consumption
        task_in_working = calculate_daily_water_consumption() # Stores the created DailyWaterConsumption object or None

        # Check if the daily consumption was not processed (e.g., already exists or no data)
        if not task_in_working:
            # Log that the day was already processed or has no valid data
            write_log("Dia já processado ou sem dados válidos.")
            # Log the end of the task
            write_log("", is_end=True)
            
            # Return a warning status and message
            return {
                "status": "warning",
                "message": "Dia já processado ou sem dados válidos."
            }

        # If processing was successful, format the details for logging
        task_details = (
            # Format the ID of the created record
            f"TASK CONCLUÍDA - ID: {task_in_working.id}\n"
            # Format the day label of the reading
            f"           Dia da leitura: {task_in_working.date_label}\n"
            # Format the total water consumption
            f"           Litros de água consumidos: {task_in_working.total_consumption}\n"
            # Format the processing timestamp
            f"           Horário do processamento: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )

        # Write the daily consumption details to the log
        write_log(task_details)
        # Log the end of the task
        write_log("", is_end=True)

        # Return a success status and details of the processed day
        return {
            "status": "success",
            "date_label": task_in_working.date_label,
            # Ensure total consumption is returned as float
            "total_consumption": float(task_in_working.total_consumption),
            "message": "Dia recebido e processado com sucesso!"
        }

    # Catch any exception that occurs during the try block
    except Exception as e:
        # Format an error message including the exception details
        error_message = f"Erro ao calcular o consumo diário de água: {e}"
        # Write the error message to the log
        write_log(error_message)
        # Log the end of the task (even if it failed)
        write_log("", is_end=True)
        # Raise a retry exception to Celery, scheduling a retry with a countdown and max retries
        raise self.retry(exc=e, countdown=60, max_retries=3)