from datetime import datetime, timedelta
from django.db.models import Sum
from apps.reader_leak.models import FlowRating
from apps.weekly_water_consumption.models import WeeklyWaterConsumption
import logging
import locale

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') 

def calculate_weekly_water_consumption():
    try:
        end_week = datetime.now().date()
        start_week = end_week - timedelta(days=6)
        
        valid_records = FlowRating.objects.filter(
            timestamp__date__range=[start_week, end_week]
        )
        
        aggregation = valid_records.aggregate(total=Sum('flow_rate'))
        total_flow_rate = aggregation.get('total') or 0.0
        
        if WeeklyWaterConsumption.objects.filter(start_date=start_week, end_date=end_week).exists():
            logger.warning(f"Registro para a semana {start_week} já existe.")
            return None
            
        return WeeklyWaterConsumption.objects.create(
            date_label=f"Semana {start_week.day} a {end_week.day} de {start_week.strftime('%B')} de {start_week.year}",
            start_date=start_week,
            end_date=end_week,
            total_consumption=total_flow_rate
        )
    
    except Exception as e:
        logger.exception(f"Falha ao calcular consumo semanal: {e}")
        return None