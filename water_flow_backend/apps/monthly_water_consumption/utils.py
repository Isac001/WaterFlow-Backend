from datetime import datetime, timedelta
from django.db.models import Sum
from apps.reader_leak.models import FlowRating
from apps.monthly_water_consumption.models import MonthlyWaterConsumption
import logging
import locale

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def monthly_water_consumption():

    try:

        end_month = datetime.now().date()
        start_month = end_month.replace(month=1)

        valid_records = FlowRating.objects.filter(
            timestamp__date__range=[start_month, end_month]
        )

        aggregation = valid_records.aggregate(total=Sum('flow_rate'))

        total_flow_rate = aggregation.get('total') or 0.0

        if MonthlyWaterConsumption.objects.filter(start_date=start_month, end_date=end_month).exists():

            logger.warning(f"Registro para o mês {start_month} já existe.")
            return None
        
        return MonthlyWaterConsumption.objects.create(
            date_label=f"Mês de {start_month.strftime('%B')} de {start_month.year}",
            start_date=start_month,
            end_date=end_month,
            total_consumption=total_flow_rate
        )

    except Exception as e:
        
        logger.exception(f"Falha ao calcular consumo mensal: {e}")
        return None
