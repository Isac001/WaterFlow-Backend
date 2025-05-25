from datetime import datetime, timedelta
from decimal import Decimal
import logging
import locale

from apps.monthly_water_consumption.models import MonthlyWaterConsumption
from apps.weekly_water_consumption.models import WeeklyWaterConsumption
from builtins import Exception

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def monthly_water_consumption():
    try:

        today = datetime.now()
        first_day = today.replace(day=1)

        if today.month < 12:
            last_day = today.replace(month=today.month + 1, day = 1) - timedelta(days=1)

        else:

            last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)

        
        records = WeeklyWaterConsumption.objects.filter(
            start_date__gte=first_day,
            end_date__lte=last_day
        ).order_by('start_date')

        if not records.exists():

            logger.warning(f"Nenhum dado encontrado para o mês {first_day.strftime('%B')} de {first_day.year}.")

            return None
        
        total_volume = sum(Decimal(record.total_consumption) for record in records)

        if MonthlyWaterConsumption.objects.filter(
            start_date=first_day,
            end_date=last_day
        ).exists(): 
            logger.warning(f"Registro para o mês {first_day.strftime('%B')} de {first_day.year} já existe.")
            return None
        
        formatted_consume = total_volume.quantize(Decimal('0.01'))

        return MonthlyWaterConsumption.objects.create(
            date_label=f"{first_day.strftime('%B')} de {first_day.year}",
            start_date=first_day,
            end_date=last_day,
            total_consumption=formatted_consume
        )

    except Exception as e:
        logger.exception(f'Falha ao calcular consumo mensal: {e}')
        return None