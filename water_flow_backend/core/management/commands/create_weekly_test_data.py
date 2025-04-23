from django.core.management.base import BaseCommand
from apps.reader_leak.models import FlowRating
from datetime import datetime, timedelta
import random
from django.utils.timezone import make_aware

class Command(BaseCommand):

    help = 'Cria dados de teste para o modelo FlowRating'

    def add_arguments(self, parser):
        parser.add_argument('--fixed', type=float, help='Valor fixo de flow_rate (em L/min). Se não for informado, será aleatório.')
        parser.add_argument('--days', type=int, default=7, help='Intervalo entre medições em segundos (ex: 3600 = 1 por hora)')

    def handle(self, *args, **options):

        days = options['days']
        fixed_flow_rate = options['fixed']
        created = 0

        self.stdout.write(f"\nGerando dados de teste para {days} dias...\n")

        for day in range(days):

            base_date = datetime.now() - timedelta(days=day)

            for hour in range(24):

                times_tamp = make_aware(base_date.replace(hour=hour, minute=0, second=0, microsecond=0))
                flow_rate = fixed_flow_rate if fixed_flow_rate is not None else random.uniform(0.5, 5.0)

                FlowRating.objects.create(
                    times_tamp=times_tamp,  
                    flow_rate=flow_rate
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"\n✅ {created} registros criados com sucesso para teste semanal!\n"))