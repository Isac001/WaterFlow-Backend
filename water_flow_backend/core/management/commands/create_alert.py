from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
import random

from apps.alert_water_consumption.utils import WaterConsumptionAlertGenerator
from apps.daily_water_consumption.models import DailyWaterConsumption
from core.celery_tasks.alert_water_consumption_task import alert_water_consumption_task


class Command(BaseCommand):
    help = "Sempre gera um alerta de consumo de água para testes"

    def handle(self, *args, **options):
        self.stdout.write("Criando dados de consumo baixo dos últimos 30 dias...")
        self.create_past_data()

        self.stdout.write("Criando consumo alto para hoje...")
        consumo_hoje = self.create_high_consumption()

        self.stdout.write(self.style.SUCCESS(f"Consumo de hoje: {consumo_hoje.total_consumption}L"))

        self.stdout.write("Executando tarefa Celery de alerta...")
        result = alert_water_consumption_task.apply().get()

        if result.get("alert_created"):
            self.stdout.write(self.style.SUCCESS(f"✅ Alerta criado com sucesso! ID: {result['alert_id']}"))
            self.stdout.write(f"🔔 Tipo: {result['alert_type']}")
            self.stdout.write(f"📈 Excesso: {float(result['exceeded_amount']):.2f}L")
            self.stdout.write(f"📊 Porcentagem: {float(result['percentage']):.2f}%")
        else:
            self.stdout.write(self.style.WARNING(result.get("message", "Nenhum alerta gerado")))

    def create_past_data(self):
        base = 1000
        today = now().date()
        first_day = today.replace(day=1)

        # Descobrir último dia do mês atual
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        last_day = (next_month - timedelta(days=1)).day

        for day in range(1, last_day + 1):
            current_date = first_day.replace(day=day)
            if current_date >= today:
                continue  # Ignora hoje e dias futuros

            date_label = self.format_label(current_date)
            if not DailyWaterConsumption.objects.filter(date_label=date_label).exists():
                consumo = round(base * random.uniform(0.6, 0.8), 2)
                DailyWaterConsumption.objects.create(
                    date_label=date_label,
                    total_consumption=consumo
                )

    def create_high_consumption(self):
        today = now().date()
        high_value = round(1000 * random.uniform(1.7, 2.2), 2)  # Força o excesso
        date_label = self.format_label(today)

        return DailyWaterConsumption.objects.create(
            date_label=date_label,
            total_consumption=high_value
        )

    def format_label(self, date):
        meses = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro',
        }
        nome_mes = meses[date.strftime('%B')]
        return f"Dia {date.day} de {nome_mes} de {date.year}"
