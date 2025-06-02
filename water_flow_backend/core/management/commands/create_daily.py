# Import BaseCommand for creating custom management commands
from django.core.management.base import BaseCommand
# Import the FlowRating model
from apps.flow_rating.models import FlowRating
# Import datetime and timedelta for date and time manipulations
from datetime import datetime, timedelta
# Import random for generating random numbers
import random
# Import make_aware to create timezone-aware datetime objects
from django.utils.timezone import make_aware
# Import the celery task
from core.celery_tasks.daily_water_consumption_task import daily_water_consumption_task

# Define a new management command by inheriting from BaseCommand
class Command(BaseCommand):

    # Define a help string for the command
    help = 'Cria dados de teste para o modelo FlowRating para o dia atual'

    # Define the main logic of the command
    def handle(self, *args, **options):

        # Write a message to standard output indicating the start of the task
        self.stdout.write(f"Iniciando a tarefa de cálculo do consumo diário de água...") # Message implies calculation, but command generates data first

        # Call the method to generate flow rating data
        self.generate_flow_rating()

    # Define a method to generate flow rating data
    def generate_flow_rating(self):

        # Start a try block to handle potential exceptions
        try: 

            # Get the current date
            today = datetime.now().date()

            # Create a timezone-aware datetime object for the beginning of today (00:00:00)
            start_time = make_aware(datetime.combine(today, datetime.min.time()))

            # Loop for each second in a day (Note: 86400 seconds in a day, 84600 is slightly less)
            for second in range(84600): # Consider using 86400 for a full day

                # Calculate the timestamp for the current second
                times_tamp = start_time + timedelta(seconds=second)

                # Generate a random flow rate between 0.0 and 100.0, rounded to 2 decimal places
                flow_rate = round(random.uniform(0.0, 100.0), 2)

                # Create a new FlowRating object with the generated timestamp and flow rate
                FlowRating.objects.create(
                    times_tamp=times_tamp,
                    flow_rate=flow_rate
                )

                # Check if the current second is a multiple of 10000 to provide progress feedback
                if second % 10000 == 0:
                    # Write a progress message to standard output
                    self.stdout.write(f"Criado registro {second}/86400 - {times_tamp.strftime('%H:%M:%S')}") # Using 86400 in log

            # Asynchronously call the Celery task to calculate daily water consumption based on the generated data
            daily_water_consumption_task.delay()

            # Write a success message to standard output
            self.stdout.write(f"\n DADOS GERADOS COM SUCESSO")

        # Catch any exception that occurs during the try block
        except Exception as e:

            # Write an error message to standard output, styled as an error
            self.stdout.write(self.style.ERROR(f"Erro ao gerar dados de teste: {e}"))

            # Re-raise the caught exception
            raise