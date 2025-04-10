from django.core.management.base import BaseCommand
from apps.reader_leak.models import FlowRating
from datetime import datetime, timedelta
import random
from django.utils.timezone import make_aware

class Command(BaseCommand):

    help = 'Cria dados de teste para o modelo FlowRating'

    def handle(self, *args, **options):
        # Define o intervalo de datas para a última semana

        for day in range(7):

            date = make_aware(datetime.now() - timedelta(days=day))  # Torna aware

            for hour in range(24):

                FlowRating.objects.create(
                    timestamp= date.replace(hour=hour, minute=0, second=0),
                    flow_rate=random.uniform(0.5, 5.0)
                )


        self.stdout.write(self.style.SUCCESS('Dados de teste criados com sucesso!'))