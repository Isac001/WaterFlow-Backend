from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from apps.flow_rating.models import FlowRating
from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption
import logging
import locale
from apps.monthly_water_consumption.models import MonthlyWaterConsumption 


logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
def bimonthly_water_consumption():
        
    try:

        today = datetime.now().date()
        current_month = today.month
        current_year = today.year

        first_month = ((current_month - 1) // 2) * 2 + 1
        first_day = datetime(current_year, first_month, 1).date()

        if first_month == 11:

            last_day = datetime(current_year, 12, 31).date()

        elif first_month == 12:

            last_day = datetime(current_year + 1, 1, 31).date()

        else:
        
            last_day = (datetime(current_year, first_month + 2, 1).date() - timedelta(days=1))

        records = MonthlyWaterConsumption.objects.filter(
            start_date__gte=first_day,
            end_date__lte=last_day
        ).order_by('start_date')

        if not records.exists():
            logger.warning(f"Nenhum dado encontrado para o bimestre {first_day.strftime('%B')} de {first_day.year}.")
            return None
        
        total_volume = sum(Decimal(record.total_consumption) for record in records)

        if BimonthlyWaterConsumption.objects.filter(
            start_date=first_day,
            end_date=last_day
        ).exists():
            logger.warning(f"Registro para o bimestre {first_day.strftime('%B')} de {first_day.year} já existe.")
            return None
        
        month_names = [
            first_day.strftime('%B').capitalize(),
            last_day.strftime('%B').capitalize()
        ]
        
        return BimonthlyWaterConsumption.objects.create(
            date_label=f"Consumo bimestral de {month_names[0]} a {month_names[1]} de {current_year}",
            start_date=first_day,
            end_date=last_day,
            total_consumption=total_volume.quantize(Decimal('0.01'))
        )

    except Exception as e:

        logger.exception(f"Falha ao calcular consumo bimestral: {e}")
        return None
