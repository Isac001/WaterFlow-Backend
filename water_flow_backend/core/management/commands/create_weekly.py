# Django and Python Imports
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Project Imports
from apps.daily_water_consumption.models import DailyWaterConsumption
from core.celery_tasks import weekly_water_consumption_task

# Define a new management command by inheriting from BaseCommand
class Command(BaseCommand):

    # Define a help string for the command (Note: help string says FlowRating, but code generates DailyWaterConsumption)
    help = 'Cria dados de teste para o modelo FlowRating' # Should be 'Cria dados de teste para DailyWaterConsumption para cálculo semanal'

    # Define the main logic of the command
    def handle(self, *args, **options):
       
        # Write a message to standard output indicating the start of the process
        self.stdout.write("Iniciando a geração de dados de teste...")

        # Call the method to generate test data for weekly consumption calculation
        self.generate_weekly_test_data()

    # Define a method to generate daily test data for the past week
    def generate_weekly_test_data(self):

        # Write a message to standard output indicating the start of this specific data generation step
        self.stdout.write("Gerando dados de teste semanal...")

        # Start a try block to handle potential exceptions
        try:

            # Get the current date as the end day for the data generation period
            end_day = datetime.now().date()

            # Calculate the start day for the data generation period (6 days before the end_day, making a 7-day period)
            start_day = end_day - timedelta(days=6)
            
            # Write a message indicating the date range for which data is being generated
            self.stdout.write(f"\nGerando dados de teste da semana de {start_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')}...\n") # Corrected order of dates in log

            # Loop 7 times to generate data for 7 days, including today
            for days_ago in range(7):

                # Calculate the specific date for the current iteration (from end_day backwards)
                current_date = end_day - timedelta(days=days_ago)

                # Generate a random total consumption value between 0 and 40000, quantized to two decimal places
                total_consumption = Decimal(random.uniform(0, 40000)).quantize(Decimal('0.00'))  

                # Create a new DailyWaterConsumption record for the current date
                DailyWaterConsumption.objects.create(
                    date_label=f"Total de litros consumidos do dia {current_date.strftime('%d de %B de %Y')}", 
                    total_consumption=total_consumption
                )

                # Write information about the generated daily data to standard output
                self.stdout.write(
                    f"Dia {current_date.strftime('%d/%m/%Y')}: {total_consumption} litros"
                )

            # Write a success message to standard output, styled as success
            self.stdout.write(self.style.SUCCESS("\n✅ Dados de teste criados com sucesso! Iniciando task de consumo semanal..\n"))

            # Asynchronously call the Celery task to calculate weekly consumption based on the generated daily data
            weekly_water_consumption_task.delay()

        # Catch any exception that occurs during the try block
        except Exception as e:
            
            # Write an error message to standard output, styled as error
            self.stdout.write(self.style.ERROR(f"\n❌ Erro ao criar dados de teste: {e}\n"))