from django.core.management.base import BaseCommand
from apps.flow_rating.models import FlowRating
from datetime import datetime, timedelta
import random
from django.utils.timezone import make_aware
from core.celery_tasks.dialy_water_consumption_task import daily_water_consumption_task

class Command(BaseCommand):

    help = 'Cria dados de teste para o modelo FlowRating para o dia atual'

    def handle(self, *args, **options):

        self.generate_flow_rating()

        result = daily_water_consumption_task.delay()

        self.stdout.write(f"Iniciando a tarefa de cálculo do consumo diário de água: {result.id}")

    def generate_flow_rating(self):

        today = datetime.now().date()

        start_time = make_aware(datetime.combine(today, datetime.min.time()))

        for second in range(84600):

            times_tamp = start_time + timedelta(seconds=second)

            flow_rate = round(random.uniform(0.0, 100.0), 2)

            FlowRating.objects.create(
                times_tamp=times_tamp,
                flow_rate=flow_rate
            )

            if second % 10000 == 0:
                self.stdout.write(f"Criado registro {second}/86400 - {times_tamp.strftime('%H:%M:%S')}")        