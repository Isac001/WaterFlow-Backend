# Django and python Imports
from datetime import datetime, timedelta
from decimal import Decimal
import logging
import locale
from builtins import Exception

# Project Imports
from apps.monthly_water_consumption.models import MonthlyWaterConsumption
from apps.weekly_water_consumption.models import WeeklyWaterConsumption

# Get a logger instance for the current module
logger = logging.getLogger(__name__)

# Set the locale to Brazilian Portuguese for time formatting
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# Define a function to calculate monthly water consumption
def monthly_water_consumption():

    # Start a try block to handle potential exceptions
    try:

        # Get the current date and time
        today = datetime.now()

        # Determine the first day of the current month
        first_day = today.replace(day=1)

        # Check if the current month is not December
        if today.month < 12:

            # Calculate the last day of the current month
            last_day = today.replace(month=today.month + 1, day = 1) - timedelta(days=1)

        # If the current month is December
        else:

            # Calculate the last day of December (which is also the last day of the year)
            last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)

        
        # Fetch weekly consumption records that fall within the current month
        records = WeeklyWaterConsumption.objects.filter(
            start_date__gte=first_day,
            end_date__lte=last_day
        # Order the records by their start date
        ).order_by('start_date')

        # Check if no weekly records were found for the month
        if not records.exists():

            # Log a warning if no data is found for the current month
            logger.warning(f"Nenhum dado encontrado para o mês {first_day.strftime('%B')} de {first_day.year}.")

            # Return None if no records are found
            return None
        
        # Calculate the total volume consumed from the fetched weekly records
        total_volume = sum(Decimal(record.total_consumption) for record in records)

        # Check if a monthly record already exists for this period
        if MonthlyWaterConsumption.objects.filter(
            start_date=first_day,
            end_date=last_day
        # Check if any such record exists
        ).exists(): 
            
            # Log a warning if a record for this month already exists
            logger.warning(f"Registro para o mês {first_day.strftime('%B')} de {first_day.year} já existe.")

            # Return None if the record already exists
            return None
        
        # Quantize the total volume to two decimal places
        formatted_consume = total_volume.quantize(Decimal('0.01'))

        # Create and return a new MonthlyWaterConsumption record
        return MonthlyWaterConsumption.objects.create(
            date_label=f"{first_day.strftime('%B')} de {first_day.year}",
            start_date=first_day,
            end_date=last_day,
            total_consumption=formatted_consume
        )

    # Catch any exception that might occur during the process
    except Exception as e:

        # Log the exception with a message
        logger.exception(f'Falha ao calcular consumo mensal: {e}')
        
        # Return None if an exception occurs
        return None