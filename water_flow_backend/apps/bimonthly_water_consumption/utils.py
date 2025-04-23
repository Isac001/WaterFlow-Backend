from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from apps.reader_leak.models import FlowRating
from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption
import logging
import locale


logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
def bimonthly_water_consumption():
        
    try:

        today = datetime.now().date()
        current_month = today.month
        current_year = today.year

        first_month = current_month - 1 if current_month % 2 == 0 else current_month
        first_day = datetime(current_year, first_month, 1).date()

        if first_month == 11:

            last_day = datetime(current_year, 12, 31).date()

        elif first_month == 12:

            last_day = datetime(current_year + 1, 1, 31).date()

        else:
        
            last_day = (datetime(current_year, first_month + 2, 1).date() - timedelta(days=1))

        records = FlowRating.objects.filter(
            times_tamp__date__range=[first_day, last_day]
        ).order_by('times_tamp')

        if not records.exists():
            logger.warning(f"Nenhum dado encontrado para o bimestre {first_day.strftime('%B')} de {first_day.year}.")
            return None
        
        total_volume = Decimal('0.00')
        prev_record = None

        for record in records:

            if prev_record:
                total_volume += Decimal(prev_record.flow_rate)

            prev_record = record

        if BimonthlyWaterConsumption.objects.filter(
            start_date=first_day,
            end_date=last_day
        ).exists():
            logger.warning(f"Registro para o bimestre {first_day.strftime('%B')} de {first_day.year} já existe.")
            return None
        
        return BimonthlyWaterConsumption.objects.create(
            date_label=f"Consumo bimestral de {first_day.strftime('%B')} a {last_day.strftime('%B')} {first_day.year}",
            start_date=first_day,
            end_date=last_day,
            total_consumption=total_volume.quantize(Decimal('0.01'))
        )



    except Exception as e:

        logger.exception(f"Falha ao calcular consumo bimestral: {e}")
        return None
