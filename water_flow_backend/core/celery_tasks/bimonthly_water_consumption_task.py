# Import shared_task decorator from Celery for creating asynchronous tasks
from celery import shared_task
# Import the utility function for bimonthly water consumption calculation
from apps.bimonthly_water_consumption.utils import bimonthly_water_consumption
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
    # Set a soft time limit for task execution in seconds
    soft_time_limit=300,
    # Set the priority of the task
    priority=5,
)
# Define the Celery task function for bimonthly water consumption
def bimonthly_water_consumption_task(self):
    # Add a docstring to describe the Celery task
    """
    Celery task to calculate and store bimonthly water consumption.
    """

    # Define the path for the bimonthly audit log file using Django settings
    audit_log_path = f"{settings.BASE_DIR}/core/logs_audit/bimonthly_logs.txt"
    
    # Define a helper function to write messages to the audit log
    def write_log(message, is_start=False, is_end=False):
        # Add a docstring to describe the helper function
        """Helper function to write formatted audit logs"""
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
        # Log the start of the bimonthly consumption task
        write_log("Iniciando task de consumo bimestral...", is_start=True)
        
        # Call the function to calculate bimonthly water consumption
        task_in_working = bimonthly_water_consumption() # Stores the created BimonthlyWaterConsumption object or None

        # Check if the bimonthly consumption was not processed (e.g., already exists or no data)
        if not task_in_working:
            # Log that the bimester was already processed or has no valid data
            write_log("Bimestre já processado ou sem dados válidos.")
            # Log the end of the task
            write_log("", is_end=True)
            # Return a warning status and message
            return {
                "status": "warning",
                "message": "Bimestre já processado ou sem dados válidos."
            }

        # If processing was successful, format the details for logging
        bimonthly_details = (
            # Format the ID of the created record
            f"TASK CONCLUÍDA - ID: {task_in_working.id}\n"
            # Format the period label of the reading
            f"           Período da leitura: {task_in_working.date_label}\n"
            # Format the total water consumption
            f"           Litros de água consumidos: {task_in_working.total_consumption}\n"
            # Format the start date of the reading
            f"           Data do início da leitura: {task_in_working.start_date.strftime('%d-%m-%Y %H:%M:%S')}\n"
            # Format the end date of the reading
            f"           Data do fim da leitura: {task_in_working.end_date.strftime('%d-%m-%Y %H:%M:%S')}"
        )

        # Write the bimonthly consumption details to the log
        write_log(bimonthly_details)
        # Log the end of the task
        write_log("", is_end=True)

        # Return a success status and details of the processed bimester
        return {
            "status": "success",
            "bimonth": task_in_working.date_label,
            # Ensure total consumption is returned as float
            "total_consumption": float(task_in_working.total_consumption),
            "start_date": task_in_working.start_date.strftime('%d-%m-%Y %H:%M:%S'),
            "end_date": task_in_working.end_date.strftime('%d-%m-%Y %H:%M:%S')
        }

    # Catch any exception that occurs during the try block
    except Exception as e:
        # Format an error message including the exception details
        error_message = f"Erro ao calcular o consumo bimestral de água: {e}"
        # Write the error message to the log
        write_log(error_message)
        # Log the end of the task (even if it failed)
        write_log("", is_end=True)
        # Raise a retry exception to Celery, scheduling a retry with a countdown and max retries
        raise self.retry(exc=e, countdown=60, max_retries=3)