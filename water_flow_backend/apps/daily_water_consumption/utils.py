from django.db.models import Sum
from datetime import datetime, timedelta
from decimal import Decimal
import logging
from apps.flow_rating.models import FlowRating
from apps.daily_water_consumption.models import DailyWaterConsumption

logger = logging.getLogger(__name__)

def daily_water_consumption():
    try:
        today = datetime.now().date()
        formatted_date = today.strftime('%d/%m/%Y')
        
        # Verifica se já existe registro para hoje
        if DailyWaterConsumption.objects.filter(date_label__contains=f"Total de litros consumidos do dia {formatted_date}").exists():
            logger.warning(f"Registro para o dia {formatted_date} já existe.")
            return None

        # Obtém todos os registros do dia, ordenados por timestamp
        records = FlowRating.objects.filter(
            times_tamp__date=today
        ).order_by('times_tamp')

        if not records.exists():
            logger.warning(f"Nenhum dado encontrado para o dia {formatted_date}.")
            return None

        total_liters = Decimal('0.00')
        prev_record = records.first()

        # Calcula o volume para cada intervalo (1 segundo = 1/60 minutos)
        for record in records[1:]:
            # Intervalo fixo de 1 segundo (convertido para minutos)
            interval_min = Decimal('1') / Decimal('60')
            
            # Média do fluxo entre duas medições (L/min)
            avg_flow = (Decimal(str(prev_record.flow_rate)) + Decimal(str(record.flow_rate))) / Decimal('2.0')
            
            # Volume em litros = fluxo médio (L/min) * tempo (min)
            total_liters += avg_flow * interval_min
            
            prev_record = record

        # Arredonda para 2 casas decimais
        total_liters = total_liters.quantize(Decimal('0.00'))

        # Cria o registro diário com o label formatado
        return DailyWaterConsumption.objects.create(
            date_label=f"Total de litros consumidos do dia {formatted_date}",
            total_consumption=total_liters  # Já está em litros
        )

    except Exception as e:
        logger.exception(f"Falha ao calcular consumo diário: {e}")
        return None