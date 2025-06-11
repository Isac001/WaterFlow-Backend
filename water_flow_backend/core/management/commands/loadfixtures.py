# Django and Python Imports
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

# Define a new management command by inheriting from BaseCommand
class Command(BaseCommand):

    # Define a help string for the command, displayed when running `manage.py help <command_name>`
    help = "Load fixtures from the fixtures directory"

    # Define a method to add command-line arguments to the command
    def add_arguments(self, parser):

        # Add an argument named '--path' to specify the fixtures directory
        parser.add_argument(
            '--path',
            type=str,
            default='water_flow_backend/fixtures/',
            help='Path to the fixtures directory'
        )

    # Define the main logic of the command
    def handle(self, *args, **options):

        # Get the value of the 'path' argument provided by the user or the default value
        fixtures_path = options['path']

        # Initialize an empty list to store the paths of fixture files found
        fixtures_file = []

        # Check if the specified fixtures_path does not exist
        if not os.path.exists(fixtures_path):

            # Write an error message to standard output, styled as an error
            self.stdout.write(self.style.ERROR(f'Path {fixtures_path} does not exist.\n'))

            # Exit the command if the path does not exist
            return
        
        # Iterate over each file and directory name in the specified fixtures_path
        for file_name in os.listdir(fixtures_path):

            # Check if the file name ends with '.json'
            if file_name.endswith('.json'):

                # If it's a JSON file, append its full path to the fixtures_file list
                fixtures_file.append(os.path.join(fixtures_path, file_name))

        # Check if no fixture files were found in the directory
        if not fixtures_file:

            # Write a warning message to standard output, styled as a warning
            self.stdout.write(self.style.WARNING(f'No fixtures found in {fixtures_path}.\n'))
            # Exit the command if no fixtures are found
            return
        
        # Write a message to standard output indicating the start of the fixture loading process
        self.stdout.write(f"Loading fixtures from {fixtures_path}...\n")

        # Iterate over each fixture file found
        for fixture in fixtures_file:

            # Write a message indicating which fixture is currently being loaded
            self.stdout.write(f"Loading fixture {fixture}...\n")

            # Call the 'loaddata' management command to load the current fixture file
            call_command('loaddata', fixture)

        # Write a success message to standard output, styled as success, after all fixtures are loaded
        self.stdout.write(self.style.SUCCESS(f"Fixtures loaded successfully from {fixtures_path}.\n"))