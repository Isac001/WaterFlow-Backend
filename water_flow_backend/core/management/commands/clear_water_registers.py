from itertools import count
from django.core.management import BaseCommand
from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption
from apps.monthly_water_consumption.models import MonthlyWaterConsumption
from apps.reader_leak.models import FlowRating
from apps.weekly_water_consumption.models import WeeklyWaterConsumption


class Command(BaseCommand):
    """
    Coamndo para limpar todos os registros de consumo de água, TODOS!
    """

    help = 'Coamndo para limpar todos os registros de consumo de água, TODOS!'


    def add_arguments(self, parser):

        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirma a exclusão de todos os registros de consumo de água.'
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(self.style.WARNING(
                '⚠️ ATENÇÃO: Este comando apagará TODOS os dados das tabelas de consumo!\n'
                'Adicione --confirm para realmente executar a limpeza.\n'
                'Tabelas afetadas:\n'
                '- FlowRating\n'
                '- WeeklyWaterConsumption\n'
                '- MonthlyWaterConsumption\n'
                '- BiMonthlyWaterConsumption'
            ))

        self.stdout.write(self.style.WARNING('Iniciando a limpeza de dados...'))

        models = [
            ('Leituras de Floxo', FlowRating),
            ('Leitura Semanal de Água', WeeklyWaterConsumption),
            ('Leitura Mensal de Água', MonthlyWaterConsumption),
            ('Leitura Bimestral de Água', BimonthlyWaterConsumption),
        ]

        for model_name, model in models:

            count, _ = model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"✅ {count} registros de {model_name} apagados com sucesso!"))

        self.stdout.write(self.style.SUCCESS('✅ Limpeza de dados concluída com sucesso!'))
      