# Django Imports
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Project Imports
from apps.daily_water_consumption.models import DailyWaterConsumption
from apps.weekly_water_consumption.models import WeeklyWaterConsumption 
from core.celery_tasks import weekly_water_consumption_task 

class Command(BaseCommand):
    """
    Comando que cria dados de teste diários e em seguida dispara a task
    para calcular e criar o registro semanal correspondente.
    """
    help = 'Cria dados de teste diários e processa o registro semanal.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days', type=int, default=7,
            help='Define a quantidade de dias de dados de teste a serem gerados.'
        )
        parser.add_argument(
            '--clean', action='store_true',
            help='Limpa todos os dados diários e semanais antes de gerar novos.',
        )

    def handle(self, *args, **options):
        days_to_generate = options['days']
        clean_first = options['clean']

        self.stdout.write(self.style.NOTICE(f"Iniciando processo para gerar {days_to_generate} dias de dados..."))

        if clean_first:
            self.stdout.write("Opção --clean ativada. Limpando dados antigos...")
            daily_count, _ = DailyWaterConsumption.objects.all().delete()
            weekly_count, _ = WeeklyWaterConsumption.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"{daily_count} registros diários e {weekly_count} registros semanais foram apagados."))

        # PASSO 1: Gera os dados de teste diários
        self.generate_test_data(days_to_generate)
        self.stdout.write(self.style.SUCCESS("\n✅ Dados de teste diários criados com sucesso!"))

        # PASSO 2: Chama a task Celery para forçar o cálculo
        self.stdout.write(self.style.NOTICE("\nDisparando a task Celery para calcular o registro semanal..."))
        weekly_water_consumption_task.delay()
        
        self.stdout.write(self.style.SUCCESS("✅ Task agendada! O registro semanal será criado em segundo plano."))
        self.stdout.write(self.style.NOTICE("Verifique os logs do Celery ou o banco de dados em alguns instantes."))


    def generate_test_data(self, num_days):
        try:
            # Gera dados para os últimos `num_days` dias a partir da data de hoje
            end_day = datetime.now().date()
            
            self.stdout.write(f"\nGerando dados para o período de {(end_day - timedelta(days=num_days-1)).strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')}...\n")

            for days_ago in range(num_days):
                current_date = end_day - timedelta(days=days_ago)
                total_consumption = Decimal(random.uniform(500, 1500)).quantize(Decimal('0.00'))

                DailyWaterConsumption.objects.create(
                    date_label=f"Consumo do dia {current_date.strftime('%d/%m/%Y')}",
                    total_consumption=total_consumption,
                    date_of_register=current_date
                )

                self.stdout.write(f"  -> Dia {current_date.strftime('%d/%m/%Y')}: {total_consumption} litros")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Erro ao criar dados de teste: {e}\n"))