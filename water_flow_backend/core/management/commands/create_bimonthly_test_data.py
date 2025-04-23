from django.core.management.base import BaseCommand
from apps.reader_leak.models import FlowRating
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
import random
import calendar

class Command(BaseCommand):

    help = 'Cria dados de teste para a tabela de consumo bimestral'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=3600, help='Intervalo entre medições em segundos (ex: 3600 = 1 por hora)')
        parser.add_argument('--fixed', type=float, help='Valor fixo de flow_rate (em L/min). Se não for informado, será aleatório.')

    def handle(self, *args, **options):

        now = datetime.now()
        current_month = now.month
        current_year = now.year

        first_month = current_month -1 if current_month % 2 == 0 else current_month

        months = [first_month, first_month + 1]

        interval = timedelta(seconds=options['interval'])
        created = 0

        for month in months:

            year = current_year if month <= 12 else current_year + 1
            real_month = month if month <= 12 else month - 12
            days_in_month = calendar.monthrange(year, real_month)[1]

            for day in range(1, days_in_month + 1):
                for hour in range(0, 24):
                    for minute in range(0, 60, interval.seconds // 60):
                        dt = datetime(year, real_month, day, hour, minute, 0)
                        timestamp = make_aware(dt)

                        flow_rate = options['fixed'] if options['fixed'] is not None else random.uniform(0.5, 5.0)

                        FlowRating.objects.create(
                            times_tamp=timestamp,
                            flow_rate=flow_rate
                        )

                        created += 1
                        if created % 500 == 0:
                            self.stdout.write(f"{created} registros criados até agora...")

        self.stdout.write(self.style.SUCCESS(f"\n✅ {created} registros criados com sucesso para o bimestre!\n"))