# Django Imports
from django.core.management.base import BaseCommand
from django.db.models import Sum
from datetime import datetime, timedelta
from calendar import monthrange
import random
from decimal import Decimal

# Models
from apps.daily_water_consumption.models import DailyWaterConsumption
from apps.weekly_water_consumption.models import WeeklyWaterConsumption
from apps.monthly_water_consumption.models import MonthlyWaterConsumption

# Celery Task (Apenas a mensal é necessária agora)
from core.celery_tasks import monthly_water_consumption_task

class Command(BaseCommand):
    """
    Comando para gerar um conjunto de dados completo (diário e semanal) para um mês
    e, ao final, disparar a task de cálculo mensal.
    """
    help = 'Gera dados diários e semanais, e então dispara a task de cálculo mensal.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--month',
            type=str,
            help='Define o mês para gerar dados (formato YYYY-MM). Ex: --month 2025-06. Se não for fornecido, usa o mês anterior.',
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Limpa todos os dados (diários, semanais, mensais) antes de gerar novos.',
        )

    def handle(self, *args, **options):
        # --- PASSO 1: Determinar o mês e as datas ---
        self.stdout.write(self.style.NOTICE("🚀 Iniciando geração de dados mocados..."))
        
        today = datetime.now().date()
        if options['month']:
            try:
                first_day_of_month = datetime.strptime(options['month'], '%Y-%m').date()
            except ValueError:
                self.stdout.write(self.style.ERROR("Formato de data inválido. Use YYYY-MM."))
                return
        else:
            first_day_of_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)

        _, num_days_in_month = monthrange(first_day_of_month.year, first_day_of_month.month)
        last_day_of_month = first_day_of_month + timedelta(days=num_days_in_month - 1)

        self.stdout.write(self.style.NOTICE(f"Mês alvo: {first_day_of_month.strftime('%B de %Y')}"))

        # --- PASSO 2: Limpar dados antigos ---
        if options['clean']:
            self.stdout.write("Opção --clean ativada. Limpando todos os dados antigos...")
            daily_count, _ = DailyWaterConsumption.objects.all().delete()
            weekly_count, _ = WeeklyWaterConsumption.objects.all().delete()
            monthly_count, _ = MonthlyWaterConsumption.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"{daily_count} diários, {weekly_count} semanais e {monthly_count} mensais foram apagados."))

        # --- PASSO 3: Gerar novos dados diários ---
        self.stdout.write(self.style.NOTICE(f"\nGerando {num_days_in_month} registros diários..."))
        self._generate_daily_data(first_day_of_month, last_day_of_month)
        self.stdout.write(self.style.SUCCESS("✅ Dados diários criados com sucesso!"))

        # --- PASSO 4: Calcular e criar os registros semanais DIRETAMENTE ---
        self.stdout.write(self.style.NOTICE("\nCalculando e criando os registros semanais..."))
        self._calculate_and_create_weekly_data(first_day_of_month, last_day_of_month)
        
        # --- PASSO 5: Disparar task para o cálculo mensal ---
        self.stdout.write(self.style.NOTICE("\nDisparando task para o cálculo mensal..."))
        monthly_water_consumption_task.delay()
        self.stdout.write(self.style.SUCCESS(f"✅ Task mensal para {first_day_of_month.strftime('%B de %Y')} disparada."))

        self.stdout.write(self.style.SUCCESS("\n🎉 Processo concluído! Verifique os logs do Celery para acompanhar o cálculo mensal."))

    def _generate_daily_data(self, start_date, end_date):
        """Cria registros diários para um intervalo de datas."""
        current_date = start_date
        while current_date <= end_date:
            # Evita duplicatas se a opção --clean não for usada
            if not DailyWaterConsumption.objects.filter(date_of_register=current_date).exists():
                total_consumption = Decimal(random.uniform(500, 1500)).quantize(Decimal('0.00'))
                DailyWaterConsumption.objects.create(
                    date_label=f"Consumo do dia {current_date.strftime('%d/%m/%Y')}",
                    total_consumption=total_consumption,
                    date_of_register=current_date
                )
            current_date += timedelta(days=1)

    def _calculate_and_create_weekly_data(self, first_day, last_day):
        """
        Calcula e cria os registros semanais com base nos dados diários existentes.
        Este método substitui a necessidade de tasks semanais.
        """
        week_start_date = first_day
        current_date = first_day
        
        while current_date <= last_day:
            # Uma semana termina no Domingo (weekday == 6) ou no último dia do mês
            if current_date.weekday() == 6 or current_date == last_day:
                week_end_date = current_date

                # Filtra os dias da semana atual
                daily_records = DailyWaterConsumption.objects.filter(
                    date_of_register__range=(week_start_date, week_end_date)
                )

                if daily_records.exists():
                    # Calcula o total usando a agregação do Django (muito eficiente)
                    total_volume = daily_records.aggregate(total=Sum('total_consumption'))['total'] or Decimal('0.0')

                    # Cria o registro semanal
                    WeeklyWaterConsumption.objects.create(
                        date_label=f"Consumo da semana de {week_start_date.strftime('%d/%m/%Y')} a {week_end_date.strftime('%d/%m/%Y')}",
                        start_date=week_start_date,
                        end_date=week_end_date,
                        total_consumption=total_volume
                    )
                    self.stdout.write(self.style.SUCCESS(f"  -> Semana de {week_start_date.strftime('%d/%m')} a {week_end_date.strftime('%d/%m')} criada."))

                # Prepara a data de início para a próxima semana
                week_start_date = current_date + timedelta(days=1)

            current_date += timedelta(days=1)