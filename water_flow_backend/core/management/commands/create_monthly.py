from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.weekly_water_consumption.models import WeeklyWaterConsumption
from datetime import datetime, timedelta
import random
from core.celery_tasks import monthly_water_consumption_task

class Command(BaseCommand):

    help = 'Gera dados falsos de consumo de água semanal para teste de consumo mensal'

    def handle(self, *args, **kwargs):

        self.stdout.write("Iniciando a geração de dados de teste...")

        self.generate_monthly_test_data()

    def generate_monthly_test_data(self):

        """
        Criando dados para teste mensal
        """

        self.stdout.write("Gerando dados de teste mensal...")

        try: 
            today = datetime.now()
            first_day_in_month = today.replace(day=1)

            if today.month == 12:
                last_day_in_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)

            else:

                last_day_in_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
            weeks = []

            start_week = first_day_in_month

            while start_week <= last_day_in_month:

                date_end_week = start_week + timedelta(days=6)

                if date_end_week > last_day_in_month:
                    date_end_week = last_day_in_month

                weeks.append((start_week, date_end_week))

                start_week = date_end_week + timedelta(days=1)

            total_consumed_in_month = Decimal('0.00')

            for i, (start_week, end_week) in enumerate(weeks):

                weekly_consumption = Decimal(random.randint(500, 1500)).quantize(Decimal('0.01'))

                WeeklyWaterConsumption.objects.create(
                    date_label=f"{start_week.strftime('%d/%m/%Y')} a {end_week.strftime('%d/%m/%Y')}",
                    start_date=start_week,
                    end_date=end_week,
                    total_consumption=weekly_consumption
                )

                total_consumed_in_month += weekly_consumption

                self.stdout.write(
                    f"Semana {i}: {start_week.strftime('%d/%m/%Y')} a {end_week.strftime('%d/%m/%Y')}, Consumo: {weekly_consumption} L/min"
                )

            monthly_water_consumption_task.delay()
            self.stdout.write(f"\n✅ Dados gerados com sucesso para {len(weeks)} semanas!")
            self.stdout.write(f"📊 Total do mês: {total_consumed_in_month.quantize(Decimal('0.01'))} L/min")
            

        except Exception as e:

            self.stdout.write(self.style.ERROR(f"Erro ao gerar dados de teste: {e}"))

            raise