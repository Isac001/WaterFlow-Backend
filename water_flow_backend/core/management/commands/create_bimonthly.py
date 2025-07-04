# # Django and Python Imports
# from decimal import Decimal
# from django.core.management.base import BaseCommand
# from datetime import datetime, timedelta
# import random

# # Project Imports
# from core.celery_tasks import bimonthly_water_consumption_task
# from apps.monthly_water_consumption.models import MonthlyWaterConsumption


# # Define a new management command by inheriting from BaseCommand
# class Command(BaseCommand):
    
#     # Define a help string for the command
#     help = 'Gera dados falsos de consumo mensal para teste de consumo bimestral'

#     # Define the main logic of the command
#     def handle(self, *args, **kwargs):
        
#         # Write a message to standard output indicating the start of the process
#         self.stdout.write("Iniciando a geração de dados de testes....")

#         # Call the method to generate bimonthly test data
#         self.generate_bimonthly_test_data()

#     # Define a method to generate test data for bimonthly consumption
#     def generate_bimonthly_test_data(self):

#         # Start a try block to handle potential exceptions
#         try: 
           
#             # Get the current date and time
#             today = datetime.now()

#             # Get the current year
#             current_year = today.year

#             # Calculate the first month of the current bimester (e.g., if today is June (month 6), first_month is 5 (May))
#             first_month_in_period = ((today.month - 1) // 2) * 2 + 1

#             # Create a list containing the two months of the current bimester
#             months_in_period = [first_month_in_period, first_month_in_period + 1]

#             # Initialize the total consumed in the period to zero
#             total_consumed_in_period = Decimal('0.00')

#             # Initialize an empty list to store created monthly data (optional, not used later in this version)
#             monthly_data = []

#             # Loop through each month in the calculated bimester period
#             for month in months_in_period:

#                 # Set the initial year for the current month
#                 year = current_year

#                 # Determine the first day of the current month in the loop
#                 first_day = datetime(year, month, 1)

#                 # Determine the last day of the current month
#                 # If the current month is December
#                 if month == 12:

#                     # The last day is December 31st
#                     last_day = datetime(year, 12, 31) # Simpler way: datetime(year + 1, 1, 1) - timedelta(days=1)

#                 # For any other month
#                 else:

#                     # The last day is the day before the first day of the next month
#                     last_day = datetime(year, month + 1, 1) - timedelta(days=1)

#                 # Generate a random monthly consumption value between 1000 and 5000
#                 monthly_consumption = Decimal(random.randint(1000, 5000)).quantize(Decimal('0.01'))

#                 # Create a new MonthlyWaterConsumption record
#                 monthly_record = MonthlyWaterConsumption.objects.create(
#                     date_label=f"{first_day.strftime('%B')} de {year}",
#                     start_date=first_day,
#                     end_date=last_day,
#                     total_consumption=monthly_consumption
#                 )

#                 # Append the created record to the monthly_data list (optional)
#                 monthly_data.append(monthly_record)

#                 # Add the current month's consumption to the total for the bimester
#                 total_consumed_in_period += monthly_consumption

#                 # Write information about the generated monthly data to standard output
#                 self.stdout.write(
#                     # Format the output string (Note: m³ might be a typo if consumption is in Liters elsewhere)
#                     f"Mês {month:02d}/{year}: {first_day.strftime('%d/%m')} a {last_day.strftime('%d/%m')} → {monthly_consumption} m³"
#                 )

#             # Asynchronously call the Celery task to calculate bimonthly consumption based on the created monthly data
#             bimonthly_water_consumption_task.delay()
            
#             # Write the total consumption for the generated bimester to standard output
#             self.stdout.write(f"\n📊 Total do bimestre: {total_consumed_in_period.quantize(Decimal('0.01'))} m³")

#         # Catch any exception that occurs during the try block
#         except Exception as e:

#             # Write an error message to standard output, styled as an error
#             self.stdout.write(self.style.ERROR(f"Erro ao gerar dados de teste: {e}"))

#             # Re-raise the caught exception
#             raise


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
from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption

# Celery Task
from core.celery_tasks import bimonthly_water_consumption_task

class Command(BaseCommand):
    """
    Comando para gerar um conjunto de dados completo para um bimestre (diário, semanal e mensal)
    e, ao final, disparar a task de cálculo bimestral.
    """
    help = 'Gera dados para um bimestre e dispara a task de cálculo bimestral.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--month',
            type=str,
            help='Define o PRIMEIRO mês do bimestre (formato YYYY-MM). Ex: --month 2025-05 para o bimestre Maio/Junho.',
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Limpa todos os dados (diários, semanais, mensais, bimestrais) antes de gerar novos.',
        )

    def handle(self, *args, **options):
        # --- PASSO 1: Determinar o bimestre e as datas ---
        self.stdout.write(self.style.NOTICE("🚀 Iniciando geração de dados mocados para o BIMESTRE..."))
        
        today = datetime.now().date()
        if options['month']:
            try:
                first_day_of_bimester = datetime.strptime(options['month'], '%Y-%m').date()
            except ValueError:
                self.stdout.write(self.style.ERROR("Formato de data inválido. Use YYYY-MM."))
                return
        else:
            # Lógica para pegar o bimestre anterior ao atual
            current_bimester_start_month = ((today.month - 1) // 2) * 2 + 1
            first_day_of_current_bimester = today.replace(month=current_bimester_start_month, day=1)
            # Pega o primeiro dia do bimestre anterior
            first_day_of_bimester = (first_day_of_current_bimester - timedelta(days=60)).replace(day=1)

        # Determina as datas para os dois meses do bimestre
        month1_start = first_day_of_bimester
        _, num_days_m1 = monthrange(month1_start.year, month1_start.month)
        month1_end = month1_start + timedelta(days=num_days_m1 - 1)

        month2_start = month1_end + timedelta(days=1)
        _, num_days_m2 = monthrange(month2_start.year, month2_start.month)
        month2_end = month2_start + timedelta(days=num_days_m2 - 1)

        self.stdout.write(self.style.NOTICE(f"Bimestre alvo: {month1_start.strftime('%B')} e {month2_start.strftime('%B')} de {month1_start.year}"))

        # --- PASSO 2: Limpar dados antigos ---
        if options['clean']:
            self.stdout.write("Opção --clean ativada. Limpando todos os dados antigos...")
            daily_count, _ = DailyWaterConsumption.objects.all().delete()
            weekly_count, _ = WeeklyWaterConsumption.objects.all().delete()
            monthly_count, _ = MonthlyWaterConsumption.objects.all().delete()
            bimonthly_count, _ = BimonthlyWaterConsumption.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"{daily_count} diários, {weekly_count} semanais, {monthly_count} mensais e {bimonthly_count} bimestrais foram apagados."))

        # --- PASSO 3: Gerar dados para o MÊS 1 ---
        self.stdout.write(self.style.NOTICE(f"\n--- Gerando dados para {month1_start.strftime('%B de %Y')} ---"))
        self._generate_daily_data(month1_start, month1_end)
        self._calculate_and_create_weekly_data(month1_start, month1_end)
        self._create_monthly_record(month1_start, month1_end)

        # --- PASSO 4: Gerar dados para o MÊS 2 ---
        self.stdout.write(self.style.NOTICE(f"\n--- Gerando dados para {month2_start.strftime('%B de %Y')} ---"))
        self._generate_daily_data(month2_start, month2_end)
        self._calculate_and_create_weekly_data(month2_start, month2_end)
        self._create_monthly_record(month2_start, month2_end)
        
        # --- PASSO 5: Disparar task para o cálculo BIMESTRAL ---
        self.stdout.write(self.style.NOTICE("\nDisparando task para o cálculo bimestral..."))
        bimonthly_water_consumption_task.delay()
        self.stdout.write(self.style.SUCCESS("✅ Task bimestral disparada."))

        self.stdout.write(self.style.SUCCESS("\n🎉 Processo concluído! Verifique os logs do Celery para acompanhar o cálculo bimestral."))

    def _generate_daily_data(self, start_date, end_date):
        """Cria registros diários para um intervalo de datas."""
        self.stdout.write(f"Gerando registros diários de {start_date.strftime('%d/%m')} a {end_date.strftime('%d/%m')}...")
        current_date = start_date
        while current_date <= end_date:
            if not DailyWaterConsumption.objects.filter(date_of_register=current_date).exists():
                DailyWaterConsumption.objects.create(
                    date_label=f"Consumo do dia {current_date.strftime('%d/%m/%Y')}",
                    total_consumption=Decimal(random.uniform(500, 1500)).quantize(Decimal('0.00')),
                    date_of_register=current_date
                )
            current_date += timedelta(days=1)
        self.stdout.write(self.style.SUCCESS("  -> Dados diários criados."))

    def _calculate_and_create_weekly_data(self, first_day, last_day):
        """Calcula e cria os registros semanais com base nos dados diários de um mês."""
        self.stdout.write("Calculando e criando registros semanais...")
        week_start_date = first_day
        current_date = first_day
        while current_date <= last_day:
            if current_date.weekday() == 6 or current_date == last_day:
                week_end_date = current_date
                daily_records = DailyWaterConsumption.objects.filter(date_of_register__range=(week_start_date, week_end_date))
                if daily_records.exists():
                    total_volume = daily_records.aggregate(total=Sum('total_consumption'))['total'] or Decimal('0.0')
                    WeeklyWaterConsumption.objects.create(
                        date_label=f"Consumo da semana de {week_start_date.strftime('%d/%m/%Y')} a {week_end_date.strftime('%d/%m/%Y')}",
                        start_date=week_start_date,
                        end_date=week_end_date,
                        total_consumption=total_volume
                    )
                week_start_date = current_date + timedelta(days=1)
            current_date += timedelta(days=1)
        self.stdout.write(self.style.SUCCESS("  -> Dados semanais criados."))

    def _create_monthly_record(self, start_date, end_date):
        """Cria o registro mensal consolidado para um mês específico."""
        self.stdout.write(f"Criando registro mensal para {start_date.strftime('%B de %Y')}...")
        # Evita duplicatas se a opção --clean não for usada
        if not MonthlyWaterConsumption.objects.filter(start_date=start_date).exists():
            total_volume = DailyWaterConsumption.objects.filter(
                date_of_register__range=(start_date, end_date)
            ).aggregate(total=Sum('total_consumption'))['total'] or Decimal('0.0')

            MonthlyWaterConsumption.objects.create(
                date_label=f"Consumo de {start_date.strftime('%B de %Y')}",
                start_date=start_date,
                end_date=end_date,
                total_consumption=total_volume
            )
            self.stdout.write(self.style.SUCCESS("  -> Registro mensal criado."))
        else:
            self.stdout.write(self.style.WARNING("  -> Registro mensal já existente. Pulando."))