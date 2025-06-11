# Django and Python Imports
from decimal import Decimal
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random

# Project Imports
from apps.weekly_water_consumption.models import WeeklyWaterConsumption
from core.celery_tasks import monthly_water_consumption_task

# Define a new management command by inheriting from BaseCommand
class Command(BaseCommand):

    # Define a help string for the command
    help = 'Gera dados falsos de consumo de água semanal para teste de consumo mensal'

    # Define the main logic of the command
    def handle(self, *args, **kwargs):

        # Write a message to standard output indicating the start of the process
        self.stdout.write("Iniciando a geração de dados de teste...")

        # Call the method to generate test data for monthly consumption calculation
        self.generate_monthly_test_data()

    # Define a method to generate weekly test data for an entire month
    def generate_monthly_test_data(self):

        # Write a message to standard output indicating the start of this specific data generation step
        self.stdout.write("Gerando dados de teste mensal...")

        # Start a try block to handle potential exceptions
        try: 

            # Get the current date and time
            today = datetime.now()

            # Determine the first day of the current month
            first_day_in_month = today.replace(day=1)

            # Determine the last day of the current month
            # Check if the current month is December
            if today.month == 12:

                # If December, the last day is December 31st
                last_day_in_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)

            # For any other month
            else:

                # The last day is the day before the first day of the next month
                last_day_in_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
            # Initialize an empty list to store week start and end date tuples
            weeks = []

            # Set the start of the first week to the first day of the month
            start_week = first_day_in_month

            # Loop as long as the start_week is within the current month
            while start_week <= last_day_in_month:

                # Calculate the potential end of the current week (6 days after start)
                date_end_week = start_week + timedelta(days=6)

                # If the calculated end_week goes beyond the last day of the month, cap it
                if date_end_week > last_day_in_month:

                    # Set the end_week to the last day of the month
                    date_end_week = last_day_in_month

                # Add the (start_week, end_week) tuple to the list of weeks
                weeks.append((start_week, date_end_week))

                # Set the start of the next week to the day after the current end_week
                start_week = date_end_week + timedelta(days=1)

            # Initialize the total consumed in the month to zero
            total_consumed_in_month = Decimal('0.00')

            # Loop through each calculated week with an index
            for i, (start_week, end_week) in enumerate(weeks):

                # Generate a random weekly consumption value between 500 and 1500
                weekly_consumption = Decimal(random.randint(500, 1500)).quantize(Decimal('0.01'))

                # Create a new WeeklyWaterConsumption record for the current week
                WeeklyWaterConsumption.objects.create(
                    date_label=f"{start_week.strftime('%d/%m/%Y')} a {end_week.strftime('%d/%m/%Y')}",
                    start_date=start_week,
                    end_date=end_week,
                    total_consumption=weekly_consumption
                )

                # Add the current week's consumption to the total for the month
                total_consumed_in_month += weekly_consumption

                # Write information about the generated weekly data to standard output
                self.stdout.write(
                    f"Semana {i+1}: {start_week.strftime('%d/%m/%Y')} a {end_week.strftime('%d/%m/%Y')}, Consumo: {weekly_consumption} L/min" # Corrected index to i+1 for 1-based week number
                )

            # Asynchronously call the Celery task to calculate monthly consumption based on the generated weekly data
            monthly_water_consumption_task.delay()

            # Write a success message indicating the number of weeks generated
            self.stdout.write(f"\n✅ Dados gerados com sucesso para {len(weeks)} semanas!")
            
            # Write the total consumption for the generated month to standard output
            self.stdout.write(f"📊 Total do mês: {total_consumed_in_month.quantize(Decimal('0.01'))} L/min")
            

        # Catch any exception that occurs during the try block
        except Exception as e:

            # Write an error message to standard output, styled as an error
            self.stdout.write(self.style.ERROR(f"Erro ao gerar dados de teste: {e}"))

            # Re-raise the caught exception
            raise