from django.core.management import BaseCommand, call_command
from django.conf import settings
import psycopg2
import sys


class Command(BaseCommand):
    """
    Django management command to hard reset a PostgreSQL database:
    1. Drops the existing database (DESTRUCTIVE)
    2. Creates a new database with the same name
    3. Runs all Django migrations

    WARNING: This will permanently delete all existing data.
    """

    help = '⚠️ Apaga e recria completamente o banco de dados (DROP → CREATE → MIGRATE)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='⚠️ VOCÊ TEM CERTEZA QUE QUER APAGAR O BANCO E RECRIAR? Use esta flag para confirmar.'
        )

    def handle(self, *args, **options):
        db_config = settings.DATABASES['default']

        if not options['confirm']:
            self.stdout.write(self.style.ERROR(
                '🚫 OPERAÇÃO CANCELADA.\n'
                'Esta operação é DESTRUTIVA e apagará todos os dados permanentemente.\n'
                'Se deseja continuar, execute com a flag: --confirm'
            ))
            return

        try:
            self.stdout.write(self.style.WARNING('🛑 ETAPA 1/3: Apagando banco de dados...'))
            self._drop_database(db_config)

            self.stdout.write(self.style.WARNING('🛠️ ETAPA 2/3: Criando novo banco de dados...'))
            self._create_database(db_config)

            self.stdout.write(self.style.WARNING('🔁 ETAPA 3/3: Executando migrações...'))
            call_command('migrate', verbosity=1)

            self.stdout.write(self.style.SUCCESS('✅ Banco de dados recriado e migrado com sucesso!'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Erro durante o processo: {e}'))
            sys.exit(1)

    def _drop_database(self, db_config):
        """
        Drops the current database after terminating all active connections.
        """
        connection = None
        try:
            connection = psycopg2.connect(
                dbname='postgres',
                user=db_config['USER'],
                password=db_config['PASSWORD'],
                host=db_config['HOST'],
                port=db_config['PORT']
            )
            connection.autocommit = True
            cursor = connection.cursor()

            # Termina conexões ativas com o banco alvo
            cursor.execute("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s AND pid <> pg_backend_pid();
            """, (db_config['NAME'],))

            # Apaga o banco
            cursor.execute(f'DROP DATABASE IF EXISTS "{db_config["NAME"]}"')

        except psycopg2.Error as e:
            raise Exception(f"Erro ao apagar banco de dados: {e}")
        finally:
            if connection:
                connection.close()

    def _create_database(self, db_config):
        """
        Creates a new database with the same name.
        """
        connection = None
        try:
            connection = psycopg2.connect(
                dbname='postgres',
                user=db_config['USER'],
                password=db_config['PASSWORD'],
                host=db_config['HOST'],
                port=db_config['PORT']
            )
            connection.autocommit = True
            cursor = connection.cursor()

            # Cria o banco com nome entre aspas duplas para preservar maiúsculas se existirem
            cursor.execute(f'CREATE DATABASE "{db_config["NAME"]}"')

        except psycopg2.Error as e:
            raise Exception(f"Erro ao criar banco de dados: {e}")
        finally:
            if connection:
                connection.close()
