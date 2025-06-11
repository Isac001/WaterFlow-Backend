# Django and Python Imports
from datetime import datetime
from decimal import Decimal
import logging

# Project Imports
from apps.flow_rating.models import FlowRating
from apps.daily_water_consumption.models import DailyWaterConsumption

# Get a logger instance for the current module
logger = logging.getLogger(__name__)

# Define a function to calculate daily water consumption
def calculate_daily_water_consumption():

    # Start a try block to handle potential exceptions
    try:

        # Get the current date
        today = datetime.now().date()
        # Format the current date as DD/MM/YYYY
        formatted_date = today.strftime('%d/%m/%Y')
        
        # Check if a daily consumption record already exists for today
        if DailyWaterConsumption.objects.filter(date_label__contains=f"Total de litros consumidos do dia {formatted_date}").exists():

            # Log a warning if the record for today already exists
            logger.warning(f"Registro para o dia {formatted_date} já existe.")

            # Return None if the record already exists
            return None

        # Retrieve all FlowRating records for the current day, ordered by timestamp
        records = FlowRating.objects.filter(
            times_tamp__date=today
        # Order the records by the times_tamp field
        ).order_by('times_tamp')

        # Check if no records were found for the day
        if not records.exists():

            # Log a warning if no data is found for the current day
            logger.warning(f"Nenhum dado encontrado para o dia {formatted_date}.")

            # Return None if no records are found
            return None

        # Initialize total_liters to zero as a Decimal
        total_liters = Decimal('0.00')

        # Get the first record to use as the previous record in the loop
        prev_record = records.first()

        # Iterate through the records starting from the second one
        for record in records[1:]:

            # Define the interval as 1 second, converted to minutes
            interval_min = Decimal('1') / Decimal('60')
            
            # Calculate the average flow rate between the previous and current record
            avg_flow = (Decimal(str(prev_record.flow_rate)) + Decimal(str(record.flow_rate))) / Decimal('2.0')
            
            # Calculate the volume in liters for this interval and add to total_liters
            total_liters += avg_flow * interval_min
            
            # Update prev_record to the current record for the next iteration
            prev_record = record

        # Round the total liters to two decimal places
        total_liters = total_liters.quantize(Decimal('0.00'))

        # Create a new DailyWaterConsumption record
        return DailyWaterConsumption.objects.create(

            # Set the label for the daily record, including the formatted date
            date_label=f"Total de litros consumidos do dia {formatted_date}",

            # Set the total consumption in liters
            total_consumption=total_liters
        )

    # Catch any exception that might occur during the calculation
    except Exception as e:

        # Log the exception with a descriptive message
        logger.exception(f"Falha ao calcular consumo diário: {e}")

        # Return None if an exception occurs
        return None