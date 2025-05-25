from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption
from apps.monthly_water_consumption.models import MonthlyWaterConsumption
from datetime import datetime, timedelta
import random
from builtins import Exception
class Command(BaseCommand):
    help = 'Gera dados falsos de consumo mensal para teste de consumo bimestral'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando a geração de dados de teste bimestral...")
        self.generate_bimonthly_test_data()

    def clear_old_data(self):
        """Limpa dados antigos de teste"""
        self.stdout.write("Limpando dados antigos de teste...")
        count, _ = BimonthlyWaterConsumption.objects.all().delete()
        self.stdout.write(f"Removidos {count} registros bimestrais antigos")

    def generate_bimonthly_test_data(self):
        """Cria dados para teste bimestral"""
        try:
            today = datetime.now()
            current_year = today.year
            
            # Determina o primeiro mês do bimestre atual
            first_month_in_period = ((today.month - 1) // 2) * 2 + 1
            months_in_period = [first_month_in_period, first_month_in_period + 1]
            
            self.clear_old_data()
            
            total_consumed_in_period = Decimal('0.00')
            monthly_data = []
            
            # Gera dados para cada mês do bimestre
            for month in months_in_period:
                year = current_year
                if month > 12:
                    month -= 12
                    year += 1
                
                first_day = datetime(year, month, 1)
                last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 \
                          else datetime(year + 1, 1, 1) - timedelta(days=1)
                
                # Gera um valor aleatório para o mês entre 1000 e 5000
                monthly_consumption = Decimal(random.randint(1000, 5000)).quantize(Decimal('0.01'))
                
                # Cria registro mensal (se necessário para o cálculo)
                monthly_record = MonthlyWaterConsumption.objects.create(
                    date_label=f"{first_day.strftime('%B')} de {year}",
                    start_date=first_day,
                    end_date=last_day,
                    total_consumption=monthly_consumption
                )
                
                monthly_data.append(monthly_record)
                total_consumed_in_period += monthly_consumption
                
                self.stdout.write(
                    f"▸ Mês {month:02d}/{year}: {first_day.strftime('%d/%m')} a {last_day.strftime('%d/%m')} "
                    f"→ {monthly_consumption} m³"
                )
            
            # Cria registro bimestral
            first_month = monthly_data[0].start_date
            last_month = monthly_data[-1].end_date
            
            BimonthlyWaterConsumption.objects.create(
                date_label=f"Bimestre {first_month.strftime('%m/%Y')}-{last_month.strftime('%m/%Y')}",
                start_date=first_month,
                end_date=last_month,
                total_consumption=total_consumed_in_period
            )
            
            self.stdout.write(f"\n✅ Dados gerados com sucesso para o bimestre!")
            self.stdout.write(f"📊 Total do bimestre: {total_consumed_in_period.quantize(Decimal('0.01'))} m³")
            self.stdout.write("\nPróximos passos:")
            self.stdout.write("1. Verifique os dados no admin ou no banco de dados")
            self.stdout.write("2. Execute o processamento bimestral se necessário")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Erro durante a geração de dados: {str(e)}"))
            raise