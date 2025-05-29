# from decimal import Decimal
# from django.core.management.base import BaseCommand
# from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption
# from apps.monthly_water_consumption.models import MonthlyWaterConsumption
# from datetime import datetime, timedelta
# import random
# from builtins import Exception
# from core.celery_tasks import bimonthly_water_consumption_task

# class Command(BaseCommand):
#     help = 'Gera dados falsos de consumo mensal para teste de consumo bimestral'

#     def handle(self, *args, **kwargs):
#         try:
#             self.stdout.write("Iniciando a geração de dados de teste bimestral...")
#             self.generate_bimonthly_test_data()
#             self.stdout.write(self.style.SUCCESS("\n✅ Dados de teste criados com sucesso! Iniciando task de consumo bimestral...\n"))

#             async_result = bimonthly_water_consumption_task.delay()
#             self.stdout.write(self.style.SUCCESS(f"✅ Task de consumo bimestral disparada! ID: {async_result.id}"))

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"\n❌ Erro ao executar o comando: {e}"))

#     def generate_bimonthly_test_data(self):
#         """Cria dados para teste bimestral"""
#         today = datetime.now()
#         current_year = today.year

#         first_month_in_period = ((today.month - 1) // 2) * 2 + 1
#         months_in_period = [first_month_in_period, first_month_in_period + 1]

#         total_consumed_in_period = Decimal('0.00')
#         monthly_data = []

#         for month in months_in_period:
#             year = current_year
#             if month > 12:
#                 month -= 12
#                 year += 1

#             first_day = datetime(year, month, 1)
#             last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year + 1, 1, 1) - timedelta(days=1)

#             monthly_consumption = Decimal(random.randint(1000, 5000)).quantize(Decimal('0.01'))

#             monthly_record = MonthlyWaterConsumption.objects.create(
#                 date_label=f"{first_day.strftime('%B')} de {year}",
#                 start_date=first_day,
#                 end_date=last_day,
#                 total_consumption=monthly_consumption
#             )

#             monthly_data.append(monthly_record)
#             total_consumed_in_period += monthly_consumption

#             self.stdout.write(
#                 f"▸ Mês {month:02d}/{year}: {first_day.strftime('%d/%m')} a {last_day.strftime('%d/%m')} → {monthly_consumption} m³"
#             )

#         first_month = monthly_data[0].start_date
#         last_month = monthly_data[-1].end_date

#         BimonthlyWaterConsumption.objects.create(
#             date_label=f"Consumo bimestral entre os meses {first_month.strftime('%m')} e {last_month.strftime('%m')} do ano de {first_month.strftime('%Y')}",
#             start_date=first_month,
#             end_date=last_month,
#             total_consumption=total_consumed_in_period
#         )

#         self.stdout.write(f"\n📊 Total do bimestre: {total_consumed_in_period.quantize(Decimal('0.01'))} L")

from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption
from apps.monthly_water_consumption.models import MonthlyWaterConsumption
from datetime import datetime, timedelta
import random
from core.celery_tasks import bimonthly_water_consumption_task


class Command(BaseCommand):
    help = 'Gera dados falsos de consumo mensal para teste de consumo bimestral'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Iniciando a geração de dados de teste bimestral...")
            self.generate_bimonthly_test_data()
            self.stdout.write(self.style.SUCCESS("\n✅ Dados de teste criados com sucesso! Iniciando task de consumo bimestral...\n"))

            async_result = bimonthly_water_consumption_task.delay()
            self.stdout.write(self.style.SUCCESS(f"✅ Task de consumo bimestral disparada! ID: {async_result.id}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Erro ao executar o comando: {e}"))

    def generate_bimonthly_test_data(self):
        """Cria dados para teste bimestral"""
        today = datetime.now()
        current_year = today.year

        # Define o primeiro mês do bimestre: 1,3,5,7,9,11
        first_month_in_period = ((today.month - 1) // 2) * 2 + 1
        months_in_period = [first_month_in_period, first_month_in_period + 1]

        total_consumed_in_period = Decimal('0.00')
        monthly_data = []

        for month in months_in_period:
            year = current_year
            # Ajuste para meses > 12
            if month > 12:
                month -= 12
                year += 1

            first_day = datetime(year, month, 1)
            if month == 12:
                last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = datetime(year, month + 1, 1) - timedelta(days=1)

            # Gera consumo mensal fake entre 1000 e 5000 (m³ ou L conforme seu sistema)
            monthly_consumption = Decimal(random.randint(1000, 5000)).quantize(Decimal('0.01'))

            monthly_record = MonthlyWaterConsumption.objects.create(
                date_label=f"{first_day.strftime('%B')} de {year}",
                start_date=first_day,
                end_date=last_day,
                total_consumption=monthly_consumption
            )

            monthly_data.append(monthly_record)
            total_consumed_in_period += monthly_consumption

            self.stdout.write(
                f"▸ Mês {month:02d}/{year}: {first_day.strftime('%d/%m')} a {last_day.strftime('%d/%m')} → {monthly_consumption} m³"
            )

        # Cria registro bimestral somando os dois meses
        first_month = monthly_data[0].start_date
        last_month = monthly_data[-1].end_date

        bimonthly_record = BimonthlyWaterConsumption.objects.create(
            date_label=f"Consumo bimestral de {first_month.strftime('%B')} a {last_month.strftime('%B')} de {first_month.year}",
            start_date=first_month,
            end_date=last_month,
            total_consumption=total_consumed_in_period.quantize(Decimal('0.01'))
        )

        self.stdout.write(f"\n📊 Total do bimestre: {total_consumed_in_period.quantize(Decimal('0.01'))} m³")
        self.stdout.write(f"Registro bimestral criado: {bimonthly_record.date_label}")
