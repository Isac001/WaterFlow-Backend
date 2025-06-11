# Django and Python Imports
from decimal import Decimal
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random

# Project Imports
from core.celery_tasks import bimonthly_water_consumption_task
from apps.monthly_water_consumption.models import MonthlyWaterConsumption


# Define a new management command by inheriting from BaseCommand
class Command(BaseCommand):
    
    # Define a help string for the command
    help = 'Gera dados falsos de consumo mensal para teste de consumo bimestral'

    # Define the main logic of the command
    def handle(self, *args, **kwargs):
        
        # Write a message to standard output indicating the start of the process
        self.stdout.write("Iniciando a geração de dados de testes....")

        # Call the method to generate bimonthly test data
        self.generate_bimonthly_test_data()

    # Define a method to generate test data for bimonthly consumption
    def generate_bimonthly_test_data(self):

        # Start a try block to handle potential exceptions
        try: 
           
            # Get the current date and time
            today = datetime.now()

            # Get the current year
            current_year = today.year

            # Calculate the first month of the current bimester (e.g., if today is June (month 6), first_month is 5 (May))
            first_month_in_period = ((today.month - 1) // 2) * 2 + 1

            # Create a list containing the two months of the current bimester
            months_in_period = [first_month_in_period, first_month_in_period + 1]

            # Initialize the total consumed in the period to zero
            total_consumed_in_period = Decimal('0.00')

            # Initialize an empty list to store created monthly data (optional, not used later in this version)
            monthly_data = []

            # Loop through each month in the calculated bimester period
            for month in months_in_period:

                # Set the initial year for the current month
                year = current_year

                # Determine the first day of the current month in the loop
                first_day = datetime(year, month, 1)

                # Determine the last day of the current month
                # If the current month is December
                if month == 12:

                    # The last day is December 31st
                    last_day = datetime(year, 12, 31) # Simpler way: datetime(year + 1, 1, 1) - timedelta(days=1)

                # For any other month
                else:

                    # The last day is the day before the first day of the next month
                    last_day = datetime(year, month + 1, 1) - timedelta(days=1)

                # Generate a random monthly consumption value between 1000 and 5000
                monthly_consumption = Decimal(random.randint(1000, 5000)).quantize(Decimal('0.01'))

                # Create a new MonthlyWaterConsumption record
                monthly_record = MonthlyWaterConsumption.objects.create(
                    date_label=f"{first_day.strftime('%B')} de {year}",
                    start_date=first_day,
                    end_date=last_day,
                    total_consumption=monthly_consumption
                )

                # Append the created record to the monthly_data list (optional)
                monthly_data.append(monthly_record)

                # Add the current month's consumption to the total for the bimester
                total_consumed_in_period += monthly_consumption

                # Write information about the generated monthly data to standard output
                self.stdout.write(
                    # Format the output string (Note: m³ might be a typo if consumption is in Liters elsewhere)
                    f"Mês {month:02d}/{year}: {first_day.strftime('%d/%m')} a {last_day.strftime('%d/%m')} → {monthly_consumption} m³"
                )

            # Asynchronously call the Celery task to calculate bimonthly consumption based on the created monthly data
            bimonthly_water_consumption_task.delay()
            
            # Write the total consumption for the generated bimester to standard output
            self.stdout.write(f"\n📊 Total do bimestre: {total_consumed_in_period.quantize(Decimal('0.01'))} m³")

        # Catch any exception that occurs during the try block
        except Exception as e:

            # Write an error message to standard output, styled as an error
            self.stdout.write(self.style.ERROR(f"Erro ao gerar dados de teste: {e}"))

            # Re-raise the caught exception
            raise