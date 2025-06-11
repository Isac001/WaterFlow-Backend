# Django and Python Imports
from datetime import datetime, timedelta
from decimal import Decimal
import logging
import locale

# Project Imports
from apps.monthly_water_consumption.models import MonthlyWaterConsumption
from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption

# Get a logger and locale instance for the current module
logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# Define a function to calculate bimonthly water consumption
def bimonthly_water_consumption():

    # Start a try block to handle potential exceptions
    try:

        # Get the current date
        today = datetime.now().date()

        # Get the current month from today's date
        current_month = today.month

        # Get the current year from today's date
        current_year = today.year

        # Calculate the first month of the bimester (1, 3, 5, 7, 9, 11)
        first_month = ((current_month - 1) // 2) * 2 + 1

        # Determine the first day of the bimester
        first_day = datetime(current_year, first_month, 1).date()

        # Check if the first month of the bimester is November
        if first_month == 11:

            # If it's November, the last day is December 31st
            last_day = datetime(current_year, 12, 31).date()
            
        # For other bimesters
        else:
            # Get the first day of the month after the bimester and subtract one day
            last_day = (datetime(current_year, first_month + 2, 1).date() - timedelta(days=1))

        # Fetch monthly records that intersect with the bimester period
        records = MonthlyWaterConsumption.objects.filter(
            start_date__lte=last_day,
            end_date__gte=first_day
        # Order the records by their start date
        ).order_by('start_date')

        # Check if no records were found for the bimester
        if not records.exists():

            # Log a warning if no data is found
            logger.warning(f"Nenhum dado encontrado para o bimestre {first_day.strftime('%B')} de {first_day.year}.")

            # Return None if no records are found
            return None
        
        # Calculate the total volume consumed from the fetched records
        total_volume = sum(Decimal(record.total_consumption) for record in records)

        # Check if a bimonthly record already exists for this period
        if BimonthlyWaterConsumption.objects.filter(
            start_date=first_day,
            end_date=last_day
        ).exists():
            
            # Log a warning if a record for this bimester already exists
            logger.warning(f"Registro para o bimestre {first_day.strftime('%B')} de {first_day.year} já existe.")
            
            # Return None if the record already exists
            return None

        # Create a list of month names for the bimester label
        month_names = [
            first_day.strftime('%B').capitalize(),
            last_day.strftime('%B').capitalize()
        ]

        # Create and return a new BimonthlyWaterConsumption record
        return BimonthlyWaterConsumption.objects.create(
            date_label=f"Consumo bimestral de {month_names[0]} a {month_names[1]} de {current_year}",
            start_date=first_day,
            end_date=last_day,
            total_consumption=total_volume.quantize(Decimal('0.01'))
        )
    
    # Catch any exception that might occur during the process
    except Exception as e:

        # Log the exception and your error
        logger.exception(f"Falha ao calcular consumo bimestral: {e}")

        # Return None if an exception occurs
        return None