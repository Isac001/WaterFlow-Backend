# Django and Python Imports
from django.utils.timezone import now
from datetime import timedelta, datetime
import re
from decimal import Decimal, ROUND_HALF_UP
import logging

# Project imports
from apps.daily_water_consumption.models import DailyWaterConsumption
from .models import AlertWaterConsumption

logger = logging.getLogger(__name__)

# Method to parse date from a label
def parse_date_label(date_label):

        # Try to extract the date from the label
        try:

            # Match the date format 'Dia X de Mês de Ano'
            match = re.match(r"Dia (\d{1,2}) de (\w+) de (\d{4})", date_label)

            # If no match, log a warning and return None
            if not match:

                logger.warning(f"Failed to parse date_label: {date_label}")

                return None

                
            
            # Catch the day, month name, and year from the match
            day = int(match.group(1))
            month_name = match.group(2)
            year = int(match.group(3))

            # Dictionary to map Portuguese month names to numbers
            months_pt = {
                'Janeiro': 1, 'Fevereiro': 2, 'Março': 3,
                'Abril': 4, 'Maio': 5, 'Junho': 6,
                'Julho': 7, 'Agosto': 8, 'Setembro': 9,
                'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
            }

            # Get the month number from the dictionary
            month = months_pt.get(month_name)

            # If month is not found, log a warning and return None
            if not month:

                logger.warning(f"Invalid month name: {month_name} in date_label: {date_label}")
                return None
            # Return the date as a datetime.date object
            return datetime(year, month, day).date()

        # Catch any ValueError or AttributeError during parsing
        except (ValueError, AttributeError) as e:

            logger.error(f"Error parsing date_label '{date_label}': {e}")
            return None
        
# Method to calculate the average water consumption over a specified number of days
def calculate_average_consumption(days=7):
        
        """
        Calculate the average water consumption over the last `days` days.
        Args:
            days (int): Number of days to consider for average calculation. Default is 30.
        Returns:
            Decimal: Average water consumption over the specified period, or None if no valid data is found.
        """
        all_consumptions = DailyWaterConsumption.objects.all()
        valid_consumptions = []

        # 1. Parse all dates and filter valid entries
        for consumption in all_consumptions:
            date = parse_date_label(consumption.date_label)
            if date is not None:
                valid_consumptions.append({
                    'date': date,
                    'total_consumption': consumption.total_consumption
                })

        # 2. Calculate cutoff date (NOW OUTSIDE THE LOOP!)
        cutoff_date = now().date() - timedelta(days=days)

        # 3. Filter consumptions from the last `days` days
        recent_consumptions = [
            item for item in valid_consumptions
            if item['date'] >= cutoff_date
        ]

        # 4. Sort by date (descending) and limit to `days` entries
        recent_consumptions.sort(key=lambda x: x['date'], reverse=True)
        recent_consumptions = recent_consumptions[:days]

        if not recent_consumptions:
            logger.warning("No valid water consumption data found for the specified period.")
            return None

        # 5. Calculate average
        total = sum(item['total_consumption'] for item in recent_consumptions)
        return Decimal(total) / Decimal(len(recent_consumptions))
        
 # Check function   
def check_for_alerts():

        """
        Check if the latest water consumption exceeds the average consumption.
        If it does, create an alert and return it.
        Returns:
            AlertWaterConsumption: The created alert object, or None if no alert is needed.
        """

        # Calculate the average water consumption
        average = calculate_average_consumption()

        # If no valid average is found, log a warning and return None
        if average is None:
            logger.warning("Average water consumption could not be calculated.")
            return None
        
        # Variable to hold the latest consumption and its date
        all_consumptions = DailyWaterConsumption.objects.all()
        latest_consumption = None
        latest_date = None

        # Iterate through all consumptions to find the latest one
        for consumption in all_consumptions:

            # Parse the date from the consumption's date label
            current_date = parse_date_label(consumption.date_label)

            # If the date is valid and is the latest found so far, update the latest variables
            if current_date and (latest_date is None or current_date > latest_date):
                latest_date = current_date
                latest_consumption = consumption

        # If no latest consumption is found, log a warning and return None
        if not latest_consumption:

            logger.warning("No latest water consumption found.")
            
            return None
        
        # Convert average to Decimal for precise calculations
        average = Decimal(average)

        # Calculate the amount by which the latest consumption exceeds the average
        execeeded_amount = Decimal(latest_consumption.total_consumption) - average

        if execeeded_amount <= 0:
            logger.warning("Latest consumption does not exceed the average. No alert created.")
            return None
        
        # Calculate the percentage exceeded
        percentage = (execeeded_amount / average) * 100

        # Round all values to 2 decimal places
        average = average.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        execeeded_amount = execeeded_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        percentage = percentage.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Determine the type of alert based on the percentage exceeded
        if percentage >= 50:
            alert_type = 'EXTREME'
        elif percentage >= 30:
            alert_type = 'VERY_HIGH'
        else:
            alert_type = 'HIGH'

        # Create the alert label
        label = f"ALERTA: CONSUMO DE ÁGUA EXCEDEU {percentage:.2f}% ACIMA DA MÉDIA!"

        # Create and return the alert object
        alert = AlertWaterConsumption.objects.create(
            alert_label=label,
            alert_type=alert_type,
            daily_water_consumption=latest_consumption,
            total_consumption_exceeded=execeeded_amount,
            average_consumption=average,
            percentage_exceeded=percentage
        )

        # If alert creation fails, log an error and return None
        if alert is None:
            logger.error("Failed to create alert.")
            return None

        # Log the successful creation of the alert
        logger.info(f"Alert created: {alert.alert_label} with type {alert_type}")
        return alert