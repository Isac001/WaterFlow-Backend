from django.core.management.base import BaseCommand
from apps.flow_rating.models import FlowRating
from datetime import datetime, timedelta
import random
from decimal import Decimal
from django.utils.timezone import make_aware
from apps.dialy_water_consumption.models import DialyWaterConsumption
from core.celery_tasks import weekly_water_consumption_task

class Command(BaseCommand):

    help = 'Cria dados de teste para o modelo FlowRating'

    def handle(self, *args, **options):

        try:

            self.clear_old_data()

            end_day = datetime.now().date()

            start_day = end_day - timedelta(days=6)
            
            self.stdout.write(f"\nGerando dados de teste da semana de {end_day} a {start_day} dias...\n")

            for days_ago in range(7):

                current_date = end_day - timedelta(days_ago)

                total_consumption = Decimal(random.uniform(0, 40000)).quantize(Decimal('0.00'))  

                DialyWaterConsumption.objects.create(
                    date_label=f"Total de litros consumidos do dia {current_date.strftime('%d de %B de %Y')}",
                    total_consumption=total_consumption
                )

            self.stdout.write(
                    f"Dia {current_date.strftime('%d/%m/%Y')}: "
                    f"{total_consumption} litros"
                )

            self.stdout.write(self.style.SUCCESS("\n✅ Dados de teste criados com sucesso! Iniciando task de consumo semanal..\n"))

            result = weekly_water_consumption_task.delay()

            self.stdout.write(self.style.SUCCESS(f"\n✅ Task de consumo semanal iniciada com sucesso! Tarefa: {result.id}\n"))

        except Exception as e:

            self.stdout.write(self.style.ERROR(f"\n❌ Erro ao criar dados de teste: {e}\n"))


    def clear_old_data(self):

        """
        Limpa dados antigos de teste
        """
        self.stdout.write("Limpando dados antigos de teste...")
        DialyWaterConsumption.objects.all().delete()