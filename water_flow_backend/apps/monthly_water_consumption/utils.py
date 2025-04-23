from datetime import datetime, timedelta
from decimal import Decimal
import logging
import locale

from apps.reader_leak.models import FlowRating
from apps.monthly_water_consumption.models import MonthlyWaterConsumption

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


def monthly_water_consumption():
    try:
        today = datetime.now()
        first_day = today.replace(day=1)

        # Calcula o último dia do mês
        if today.month < 12:
            last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        else:
            last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)

        # Busca os registros dentro do mês
        records = FlowRating.objects.filter(
            times_tamp__date__range=[first_day, last_day]
        ).order_by('times_tamp')

        if not records.exists():
            logger.warning(f"Nenhum dado encontrado para o mês {first_day.strftime('%B')} de {first_day.year}.")
            return None

        total_volume = Decimal('0.00')
        liters_per_second = Decimal('0.0166667')  # Se flow_rate está em L/min

        for record in records:
            liters = Decimal(record.flow_rate) * liters_per_second
            total_volume += liters

        # Verifica se já existe um registro para o mês
        if MonthlyWaterConsumption.objects.filter(
            start_date=first_day,
            end_date=last_day
        ).exists():
            logger.warning(f"Registro para o mês {first_day.strftime('%B')} de {first_day.year} já existe.")
            return None

        formatted_consume = total_volume.quantize(Decimal('0.01'))

        # Cria e retorna o novo registro de consumo mensal
        return MonthlyWaterConsumption.objects.create(
            date_label=f"{first_day.strftime('%B')} de {first_day.year}",
            start_date=first_day,
            end_date=last_day,
            total_consumption=formatted_consume
        )

    except Exception as e:
        logger.exception(f"Falha ao calcular consumo mensal: {e}")
        return None
