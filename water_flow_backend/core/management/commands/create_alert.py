# Django and Python Imports
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
import random

# Project Imports
from apps.daily_water_consumption.models import DailyWaterConsumption
from core.celery_tasks.alert_water_consumption_task import alert_water_consumption_task


# Define a new management command by inheriting from BaseCommand
class Command(BaseCommand):

    # Define a help string for the command, displayed when running `manage.py help <command_name>`
    help = "Sempre gera um alerta de consumo de água para testes"

    # Define the main logic of the command
    def handle(self, *args, **options):

        # Start a try block to handle potential exceptions during command execution
        try: 

            # Write a message to standard output indicating the start of the process
            self.stdout.write("Iniciando a criação de alerta de consumo de água...")

            # Call the method to create historical consumption data
            self.create_past_data()

            # Call the method to create a high consumption record for the current day
            self.create_high_consumption()

            # Asynchronously call the alert water consumption Celery task
            alert_water_consumption_task.delay()

            # Write a message to standard output indicating the task has finished
            self.stdout.write("Tarefa finalizada!")
        
        # Catch any exception that occurs during the try block
        except Exception as e:

            # Write an error message to standard output, styled as an error
            self.stdout.write(self.style.ERROR(f"Erro ao gerar dados de teste: {e}"))

            # Re-raise the caught exception
            raise
            
    # Define a method to create past daily water consumption data
    def create_past_data(self):

        # Set a base value for consumption calculation
        base = 1000

        # Get the current date
        today = now().date()

        # Get the first day of the current month
        first_day = today.replace(day=1)

        # Determine the last day of the current month
        # Check if the current month is December
        if today.month == 12:

            # If December, the next month is January of the next year
            next_month = today.replace(year=today.year + 1, month=1, day=1)

        # For any other month
        else:

            # The next month is the current month + 1
            next_month = today.replace(month=today.month + 1, day=1)

        # The last day is the day before the first day of the next month
        last_day = (next_month - timedelta(days=1)).day

        # Loop through each day from 1 to the last day of the month
        for day in range(1, last_day + 1):

            # Create a date object for the current day in the loop
            current_date = first_day.replace(day=day)

            # Check if the current loop date is today or a future date
            if current_date >= today:

                # Skip processing for today and future dates in this historical data generation
                continue  

            # Format the date label for the current date
            date_label = self.format_label(current_date)

            # Calculate a random consumption value based on the base
            consumption = round(base * random.uniform(0.6, 0.8), 2)

            # Write information about the generated data to standard output
            self.stdout.write(f"Dia: {date_label} | Consumo médio: {consumption}")

            # Check if a DailyWaterConsumption record with this date_label already exists
            if not DailyWaterConsumption.objects.filter(
                    date_label=date_label
                ).exists():
                    # If it doesn't exist, create a new DailyWaterConsumption record
                    DailyWaterConsumption.objects.create(
                        date_label=date_label,
                        total_consumption=consumption
                    )

    # Define a method to create a high water consumption record for today
    def create_high_consumption(self):

        # Get the current date
        today = now().date()

        # Calculate a high consumption value, significantly above the base
        high_value = round(1000 * random.uniform(1.7, 2.2), 2)  

        # Format the date label for today
        date_label = self.format_label(today)

        # Write information about the high consumption data to standard output
        self.stdout.write(f"Dia com consumo acima da média: {today} | Consumo: {high_value}")

        # Create and return a new DailyWaterConsumption record with the high value
        return DailyWaterConsumption.objects.create(
            date_label=date_label,
            total_consumption=high_value
        )

    # Define a method to format a date object into a Portuguese string label
    def format_label(self, date):

        # Define a dictionary to map English month names to Portuguese
        meses = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro',
        }

        # Get the English month name from the date object
        nome_mes_ingles = date.strftime('%B')

        # Translate the English month name to Portuguese using the dictionary
        nome_mes = meses[nome_mes_ingles]
        
        # Return the formatted date string in Portuguese
        return f"Dia {date.day} de {nome_mes} de {date.year}"