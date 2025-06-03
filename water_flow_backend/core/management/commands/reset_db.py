# Import BaseCommand and call_command from Django's core management utilities
from django.core.management import BaseCommand, call_command
# Import Django settings to access database configurations
from django.conf import settings
# Import psycopg2 for direct PostgreSQL database interaction
import psycopg2
# Import sys for system-specific parameters and functions, like sys.exit
import sys


# Define a new management command by inheriting from BaseCommand
class Command(BaseCommand):
    # Add a docstring to describe the command's functionality and warnings
    """
    Django management command to hard reset a PostgreSQL database:
    1. Drops the existing database (DESTRUCTIVE)
    2. Creates a new database with the same name
    3. Runs all Django migrations

    WARNING: This will permanently delete all existing data.
    """

    # Define a help string for the command, displayed when running `manage.py help <command_name>`
    help = '⚠️ Apaga e recria completamente o banco de dados (DROP → CREATE → MIGRATE)'

    # Define a method to add command-line arguments to the command
    def add_arguments(self, parser):
        # Add a '--confirm' argument, which is a boolean flag
        parser.add_argument(
            # Argument name
            '--confirm',
            # Action to store 'true' if the flag is present
            action='store_true',
            # Help text for this argument, warning the user
            help='⚠️ VOCÊ TEM CERTEZA QUE QUER APAGAR O BANCO E RECRIAR? Use esta flag para confirmar.'
        )

    # Define the main logic of the command
    def handle(self, *args, **options):
        # Get the default database configuration from Django settings
        db_config = settings.DATABASES['default']

        # Check if the '--confirm' flag was not provided
        if not options['confirm']:
            # Write an error message to standard output, styled as an error
            self.stdout.write(self.style.ERROR(
                '🚫 OPERAÇÃO CANCELADA.\n'
                'Esta operação é DESTRUTIVA e apagará todos os dados permanentemente.\n'
                'Se deseja continuar, execute com a flag: --confirm'
            ))
            # Exit the command if confirmation is not given
            return

        # Start a try block to handle potential exceptions during the reset process
        try:
            # Write a warning message for the first step: dropping the database
            self.stdout.write(self.style.WARNING('🛑 ETAPA 1/3: Apagando banco de dados...'))
            # Call the internal method to drop the database
            self._drop_database(db_config)

            # Write a warning message for the second step: creating the database
            self.stdout.write(self.style.WARNING('🛠️ ETAPA 2/3: Criando novo banco de dados...'))
            # Call the internal method to create the database
            self._create_database(db_config)

            # Write a warning message for the third step: running migrations
            self.stdout.write(self.style.WARNING('🔁 ETAPA 3/3: Executando migrações...'))
            # Call the 'migrate' management command with verbosity level 1
            call_command('migrate', verbosity=1)

            # Write a success message after all steps are completed
            self.stdout.write(self.style.SUCCESS('✅ Banco de dados recriado e migrado com sucesso!'))

        # Catch any exception that occurs during the try block
        except Exception as e:
            # Write an error message to standard error, styled as an error
            self.stderr.write(self.style.ERROR(f'❌ Erro durante o processo: {e}'))
            # Exit the script with an error code
            sys.exit(1)

    # Define an internal method to drop the database
    def _drop_database(self, db_config):
        # Add a docstring to describe the method's functionality
        """
        Drops the current database after terminating all active connections.
        """
        # Initialize the connection variable to None
        connection = None
        # Start a try block for database operations
        try:
            # Connect to the 'postgres' database (a default maintenance database)
            connection = psycopg2.connect(
                # Database name to connect initially
                dbname='postgres', 
                # User from the Django settings
                user=db_config['USER'],
                # Password from the Django settings
                password=db_config['PASSWORD'],
                # Host from the Django settings
                host=db_config['HOST'],
                # Port from the Django settings
                port=db_config['PORT']
            )
            # Set autocommit to True to execute commands immediately without a transaction block
            connection.autocommit = True
            # Create a cursor object to execute SQL commands
            cursor = connection.cursor()

            # SQL command to terminate active connections to the target database
            # This is necessary before dropping the database
            cursor.execute("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s AND pid <> pg_backend_pid();
            """, (db_config['NAME'],)) # Pass the target database name as a parameter

            # SQL command to drop the target database if it exists
            # Use f-string for the database name, ensure it's quoted if it contains special characters or case sensitivity matters
            cursor.execute(f'DROP DATABASE IF EXISTS "{db_config["NAME"]}"')

        # Catch psycopg2 specific errors
        except psycopg2.Error as e:
            # Raise a new exception with a custom error message
            raise Exception(f"Erro ao apagar banco de dados: {e}")
        # Define a finally block to ensure resources are released
        finally:
            # Check if the connection was established
            if connection:
                # Close the database connection
                connection.close()

    # Define an internal method to create the database
    def _create_database(self, db_config):
        # Add a docstring to describe the method's functionality
        """
        Creates a new database with the same name.
        """
        # Initialize the connection variable to None
        connection = None
        # Start a try block for database operations
        try:
            # Connect to the 'postgres' database
            connection = psycopg2.connect(
                # Database name to connect initially
                dbname='postgres',
                # User from the Django settings
                user=db_config['USER'],
                # Password from the Django settings
                password=db_config['PASSWORD'],
                # Host from the Django settings
                host=db_config['HOST'],
                # Port from the Django settings
                port=db_config['PORT']
            )
            # Set autocommit to True
            connection.autocommit = True
            # Create a cursor object
            cursor = connection.cursor()

            # SQL command to create the new database
            # Use f-string for the database name, quoting it to preserve case or handle special characters
            cursor.execute(f'CREATE DATABASE "{db_config["NAME"]}"')

        # Catch psycopg2 specific errors
        except psycopg2.Error as e:
            # Raise a new exception with a custom error message
            raise Exception(f"Erro ao criar banco de dados: {e}")
        # Define a finally block
        finally:
            # Check if the connection was established
            if connection:
                # Close the database connection
                connection.close()