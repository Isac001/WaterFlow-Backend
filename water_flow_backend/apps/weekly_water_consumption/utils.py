from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from apps.reader_leak.models import FlowRating
from apps.weekly_water_consumption.models import WeeklyWaterConsumption
import logging
import locale

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') 

def calculate_weekly_water_consumption():
    try: 

        end_day = datetime.now()
        frist_day = end_day - timedelta(days=7)

        records = FlowRating.objects.filter(
            times_tamp__date__range=[frist_day.date(), end_day.date()]
        ).order_by('times_tamp')

        if not records.exists():

            logger.warning(f"Nenhum dado encontrado para o período de {frist_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')}.")
            return None
        
        total_volume = Decimal('0.00')
        prev_record = None 

        for record in records:

            if prev_record:
                total_volume += record.flow_rate

            prev_record = record

        if WeeklyWaterConsumption.objects.filter(
            start_date=frist_day,
            end_date=end_day
        ).exists():
            logger.warning(f"Registro para o período de {frist_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')} já existe.")
            return None
        
        return WeeklyWaterConsumption.objects.create(
            date_label=f"{frist_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')}",
            start_date=frist_day,
            end_date=end_day,
            total_consumption=total_volume
        )
    except Exception as e:

        logger.exception(f"Falha ao calcular consumo semanal: {e}")
        return None