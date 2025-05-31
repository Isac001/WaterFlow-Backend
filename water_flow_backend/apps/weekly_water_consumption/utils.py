from datetime import datetime, timedelta
from decimal import Decimal
from apps.flow_rating.models import FlowRating
from apps.weekly_water_consumption.models import WeeklyWaterConsumption
import logging
import locale
from builtins import Exception
from apps.daily_water_consumption.models import DailyWaterConsumption

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') 

def calculate_weekly_water_consumption():
    try: 

        end_day = datetime.now()
        start_day = end_day - timedelta(days=6)
        records = []

        for record in DailyWaterConsumption.objects.all():
            try:

                date_str = record.date_label.split("dia")[-1].strip()
                record_date = datetime.strptime(date_str, "%d de %B de %Y").date()

                if start_day.date() <= record_date <= end_day.date():
                    records.append(record)
                    logger.info(f"Registro {record.date_label} adicionado para o cálculo semanal.")

            except Exception as e:

                logger.warning(f"Erro ao processar o registro {record.date_label}: {e}")

        if not records:

            logger.warning(f"Nenhum dado encontrado para o período de {start_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')}.")
            return None
        
        total_volume = sum(Decimal(record.total_consumption) for record in records)

        if WeeklyWaterConsumption.objects.filter(
            start_date=start_day,
            end_date=end_day
        ).exists():
            logger.warning(f"Registro para o período de {start_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')} já existe.")
            return None
        
        return WeeklyWaterConsumption.objects.create(
            date_label=f"Consumo de água da semana de {start_day.strftime('%d/%m/%Y')} a {end_day.strftime('%d/%m/%Y')}",
            start_date=start_day,
            end_date=end_day,
            total_consumption=total_volume
        )
    except Exception as e:

        logger.exception(f"Falha ao calcular consumo semanal: {e}")
        return None