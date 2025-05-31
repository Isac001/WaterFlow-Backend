from django.core.management import BaseCommand, call_command
from django.db import connections
import psycopg2
import sys
from django.conf import settings

class Command(BaseCommand):
    """
    Command to completely reset the PostgreSQL database in Docker:
    1. Drops current database
    2. Creates new database with proper permissions
    3. Runs all migrations
    """

    help = 'Completely resets the PostgreSQL database (DANGEROUS!)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirms the database reset operation'
        )
        parser.add_argument(
            '--no-migrate',
            action='store_true',
            help='Skips running migrations after reset'
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(self.style.ERROR(
                '🚨 DANGER: This will COMPLETELY DESTROY your database!\n'
                'All data will be permanently lost!\n'
                'Add --confirm to actually execute this operation.\n\n'
                'This will:\n'
                '1. Drop the current database\n'
                '2. Create a new database\n'
                '3. Set up user permissions\n'
                '4. Run all migrations from scratch'
            ))
            sys.exit(1)

        self.stdout.write(self.style.WARNING('Starting PostgreSQL database reset...'))

        try:
            # Get database settings from Django
            db_settings = settings.DATABASES['default']
            db_name = db_settings['NAME']
            db_user = db_settings['USER']
            db_password = db_settings['PASSWORD']
            db_host = db_settings['HOST']
            db_port = db_settings['PORT']

            # Connect to postgres database to perform admin operations
            # Use the same user credentials from settings
            admin_conn = psycopg2.connect(
                dbname='postgres',  # Connect to default admin DB
                user=db_user,        # Use the configured user
                password=db_password,
                host=db_host,
                port=db_port
            )
            admin_conn.autocommit = True  # Required for DB operations
            cursor = admin_conn.cursor()

            # Step 1: Terminate all existing connections
            self.stdout.write(self.style.WARNING('Terminating existing connections...'))
            cursor.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{db_name}'
                AND pid <> pg_backend_pid();
            """)
            self.stdout.write(self.style.SUCCESS('✅ All connections terminated'))

            # Step 2: Drop the database
            self.stdout.write(self.style.WARNING(f'Dropping database {db_name}...'))
            cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
            self.stdout.write(self.style.SUCCESS(f'✅ Database {db_name} dropped'))

            # Step 3: Create new database
            self.stdout.write(self.style.WARNING(f'Creating database {db_name}...'))
            cursor.execute(f'CREATE DATABASE {db_name}')
            self.stdout.write(self.style.SUCCESS(f'✅ Database {db_name} created'))

            # Step 4: Set up user permissions
            self.stdout.write(self.style.WARNING(f'Setting up user {db_user}...'))
            # First grant all privileges on the new database
            cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}')
            # Then grant privileges on public schema
            cursor.execute(f'GRANT ALL PRIVILEGES ON SCHEMA public TO {db_user}')
            self.stdout.write(self.style.SUCCESS('✅ User permissions configured'))

            cursor.close()
            admin_conn.close()

            # Re-establish Django connection
            connections.close_all()

            # Step 5: Run migrations if not skipped
            if not options['no_migrate']:
                self.stdout.write(self.style.WARNING('Running migrations...'))
                call_command('makemigrations', verbosity=0)
                call_command('migrate', verbosity=0)
                self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))

            # Final verification
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                tables = cursor.fetchall()
                self.stdout.write(self.style.SUCCESS(f'✅ Reset complete. Found {len(tables)} tables'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during reset: {str(e)}'))
            sys.exit(1)