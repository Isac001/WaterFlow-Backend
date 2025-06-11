# Django and Python Imports
from datetime import datetime, timedelta
from decimal import Decimal
from apps.weekly_water_consumption.models import WeeklyWaterConsumption
import logging
import locale
from builtins import Exception

# Project Imports
from apps.daily_water_consumption.models import DailyWaterConsumption

# Get a logger instance for the current module
logger = logging.getLogger(__name__)

# Set the locale to Brazilian Portuguese for time formatting
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') 

# Define a function to calculate weekly water consumption
def calculate_weekly_water_consumption():

    # Start a try block to handle potential exceptions
    try: 

        # Get the current date and time as the end day of the week
        end_day = datetime.now()

        # Calculate the start day of the week (6 days before the end day)
        start_day = end_day - timedelta(days=6)

        # Initialize an empty list to store relevant daily records
        records = []

        # Iterate over all records in the DailyWaterConsumption table
        for record in DailyWaterConsumption.objects.all():

            # Start an inner try block to handle parsing errors for individual records
            try:

                # Extract the date string from the record's date_label
                date_str = record.date_label.split("dia")[-1].strip()

                # Convert the extracted date string to a datetime.date object
                record_date = datetime.strptime(date_str, "%d de %B de %Y").date()

                # Check if the record's date falls within the calculated week (start_day to end_day)
                if start_day.date() <= record_date <= end_day.date():

                    # If it falls within the week, add the record to the list
                    records.append(record)

                    # Log that the record was added for weekly calculation
                    logger.info(f"Registro {record.date_label} adicionado para o cálculo semanal.")

            # Catch any exception that occurs while processing a single record
            except Exception as e:

                # Log a warning if an error occurs while processing a record's date_label
                logger.warning(f"Erro ao processar o registro {record.date_label}: {e}")

        # Check if no daily records were found for the calculated week
        if not records:

            # Log a warning if no data is found for the period
            logger.warning(f"Nenhum dado encontrado para o período de {start_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')}.")

            # Return None if no records are found
            return None
        
        # Calculate the total water volume by summing up total_consumption from the collected daily records
        total_volume = sum(Decimal(record.total_consumption) for record in records)

        # Check if a weekly consumption record already exists for this specific start and end date
        if WeeklyWaterConsumption.objects.filter(
            start_date=start_day,
            end_date=end_day
        # Check if any such record exists
        ).exists():
            
            # Log a warning if a record for this period already exists
            logger.warning(f"Registro para o período de {start_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')} já existe.")

            # Return None if the record already exists
            return None
        
        # Create and return a new WeeklyWaterConsumption record
        return WeeklyWaterConsumption.objects.create(
            date_label=f"Consumo de água da semana de {start_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')}",
            start_date=start_day,
            end_date=end_day,
            total_consumption=total_volume
        )
    
    # Catch any exception that might occur during the entire process
    except Exception as e:

        # Log the exception with a message
        logger.exception(f"Falha ao calcular consumo semanal: {e}")
        
        # Return None if an exception occurs
        return None