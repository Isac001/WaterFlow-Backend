
# Django and Python Imports
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
import logging

# Project Imports
from apps.daily_water_consumption.models import DailyWaterConsumption
from apps.weekly_water_consumption.models import WeeklyWaterConsumption

logger = logging.getLogger(__name__)

# ATENÇÃO: A configuração de locale não é mais necessária para esta função,
# mas pode ser útil para outras partes do seu projeto.
# import locale
# locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') 

def calculate_weekly_water_consumption():
    """
    Calcula o consumo da última semana de forma eficiente e segura,
    usando o campo 'date_of_register'.
    """
    try:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6)

        # Verifica se um registro para este período exato já existe
        if WeeklyWaterConsumption.objects.filter(start_date=start_date, end_date=end_date).exists():
            logger.warning(f"Cálculo semanal ignorado: registro para o período de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')} já existe.")
            return None

        # --- LÓGICA CORRIGIDA E EFICIENTE ---
        # 1. Filtra os registros pela data correta, diretamente no banco.
        daily_records_in_range = DailyWaterConsumption.objects.filter(
            date_of_register__range=(start_date, end_date)
        )

        if not daily_records_in_range.exists():
            logger.warning(f"Nenhum dado diário encontrado para a semana de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}.")
            return None

        # 2. Usa a função Sum do Django para calcular o total (muito mais rápido).
        aggregation_result = daily_records_in_range.aggregate(
            total=Sum('total_consumption')
        )
        total_volume = aggregation_result['total'] or Decimal('0.0')
        # ------------------------------------

        # Cria o novo registro semanal
        new_weekly_record = WeeklyWaterConsumption.objects.create(
            date_label=f"Consumo de água da semana de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}",
            start_date=start_date,
            end_date=end_date,
            total_consumption=total_volume
        )
        
        logger.info(f"Registro semanal criado com sucesso para o ID: {new_weekly_record.id}")
        return new_weekly_record

    except Exception as e:
        logger.exception(f"Falha crítica ao calcular consumo semanal: {e}")
        return None