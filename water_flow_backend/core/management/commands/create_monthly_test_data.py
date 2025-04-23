from django.core.management.base import BaseCommand
from apps.reader_leak.models import FlowRating
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
import random


class Command(BaseCommand):
    help = 'Gera dados de teste para o modelo FlowRating com amostragem reduzida.'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30, help='Número de dias a simular (padrão: 30 dias)')
        parser.add_argument('--interval', type=int, default=60, help='Intervalo entre medições em segundos (ex: 60 = 1 por minuto, 300 = a cada 5 min)')
        parser.add_argument('--fixed', type=float, help='Valor fixo de flow_rate (em L/min). Se não for informado, será aleatório.')

    def handle(self, *args, **options):
        start_time = datetime(year=2025, month=4, day=1, hour=0, minute=0, second=0)
        start_time = make_aware(start_time)

        interval = timedelta(seconds=options['interval'])
        end_time = start_time + timedelta(days=options['days'])

        current_time = start_time
        created = 0

        self.stdout.write(f"\nGerando dados de teste entre {start_time} e {end_time} com intervalo de {options['interval']} segundos...\n")

        while current_time < end_time:
            flow_rate = options['fixed'] if options['fixed'] is not None else random.uniform(0.0, 6.0)

            FlowRating.objects.create(
                times_tamp=current_time,
                flow_rate=flow_rate
            )

            created += 1
            if created % 500 == 0:
                self.stdout.write(f"{created} registros criados até agora...")

            current_time += interval

        self.stdout.write(f"\n{created} registros criados com sucesso para teste!\n")
