# # Django and python Imports
# from datetime import datetime, timedelta
# from decimal import Decimal
# import logging
# import locale
# from calendar import monthrange

# # Project Imports
# from apps.monthly_water_consumption.models import MonthlyWaterConsumption
# from apps.weekly_water_consumption.models import WeeklyWaterConsumption

# # Get a logger instance for the current module
# logger = logging.getLogger(__name__)

# # Define a locale instance for the current module
# locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# # Function to calculate monthly water consumption
# def monthly_water_consumption():
#     """
#     Calcula o consumo do mês com base no último registro semanal encontrado.
#     Esta função é projetada para ser chamada sem parâmetros por uma task do Celery.
#     """
#     try:
#         # --- LÓGICA INTELIGENTE ---
#         # 1. Encontra o registro semanal mais recente para saber qual mês processar.
#         latest_week = WeeklyWaterConsumption.objects.order_by('-end_date').first()

#         if not latest_week:
#             logger.warning("Nenhum registro semanal encontrado. O cálculo mensal não pode prosseguir.")
#             return None

#         # 2. Usa a data do último registro semanal como nossa data de referência.
#         calculation_date = latest_week.end_date
#         logger.info(f"Última semana encontrada termina em {calculation_date}. Calculando para o mês de {calculation_date.strftime('%B de %Y')}.")
#         # ---------------------------

#         # Determina o primeiro e o último dia do mês de referência
#         first_day = calculation_date.replace(day=1)
#         _, num_days = monthrange(calculation_date.year, calculation_date.month)
#         last_day = first_day + timedelta(days=num_days - 1)
        
#         # Verifica se um registro mensal para este período já existe
#         if MonthlyWaterConsumption.objects.filter(start_date=first_day, end_date=last_day).exists(): 
#             logger.warning(f"Registro para o mês {first_day.strftime('%B de %Y')} já existe.")
#             return None
        
#         # Busca todos os registros semanais que pertencem a este mês
#         records_in_month = WeeklyWaterConsumption.objects.filter(
#             start_date__year=first_day.year,
#             start_date__month=first_day.month
#         ).order_by('start_date')

#         if not records_in_month.exists():
#             logger.warning(f"Nenhum dado semanal encontrado para o mês {first_day.strftime('%B de %Y')}.")
#             return None
        
#         # Calcula o volume total somando os registros semanais do mês
#         total_volume = sum(record.total_consumption for record in records_in_month)
        
#         # Formata o consumo para duas casas decimais
#         formatted_consume = total_volume.quantize(Decimal('0.01'))

#         # Cria o novo registro mensal
#         new_monthly_record = MonthlyWaterConsumption.objects.create(
#             date_label=f"Consumo de {first_day.strftime('%B de %Y')}",
#             start_date=first_day,
#             end_date=last_day,
#             total_consumption=formatted_consume
#         )

#         logger.info(f"Registro mensal criado com sucesso para o ID: {new_monthly_record.id}")
#         return new_monthly_record

#     except Exception as e:
#         logger.exception(f'Falha crítica ao calcular consumo mensal: {e}')
#         return None




from datetime import datetime, timedelta
from decimal import Decimal
import logging
import locale
from calendar import monthrange

from .models import MonthlyWaterConsumption
from apps.weekly_water_consumption.models import WeeklyWaterConsumption

logger = logging.getLogger(__name__)

# Configura o locale para nomes de meses em português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, '') # Fallback para o locale padrão do sistema

def monthly_water_consumption():

    try:

        # Captura o mês a ser calculado pela semana
        latest_week = WeeklyWaterConsumption.objects.filter().order_by('end_date').first()

        # Tratamento caso não tiver registros de semanas
        if latest_week is None:
            logger.warning('Nenhum registro semanal encontrado. Cálculo mensal não poderá ser realizado')
            return None

        # Usa o último registro semanal como refência para calcular-mos o mês
        calculation_date = latest_week.end_date
        logger.info(f"Útlima semana encontrada: {calculation_date}, calculando o mês de {calculation_date.strftime('%B de %Y')}")

        # Calculando o primeiro dia do mês
        first_day = calculation_date.replace(day=1)
        _, num_days = monthrange(calculation_date.year, calculation_date.month)

        # Calculando o primeiro dia do mês
        last_day = first_day + timedelta(days=num_days -1)

        # Tratamento para caso o mês já esteja calculado
        if MonthlyWaterConsumption.objects.filter(start_date=first_day, end_date=last_day).exists():
            logger.warning(f"Registro para o mês {first_day.strftime('%B de %Y')} já existe no banco de dados")
            return None
        
        records_in_month = WeeklyWaterConsumption.objects.filter(
            start_date__year = first_day.year,
            start_date__month = first_day.month
        ).order_by('start_date')

        if not records_in_month.exists():

            logger.warning(f"Nenhum dado semanal encontrado para o mês {first_day.strftime('%B de %Y')}.")
            return None
        
        total_volume = sum(record.total_consumption for record in records_in_month)

        formatted_consumption = total_volume.quantize(Decimal('0.01'))

        new_monthly_record = MonthlyWaterConsumption.objects.create(
            date_label = f"Consumo de {first_day.strftime('%B de %Y')}",
            start_date=first_day,
            end_date=last_day,
            total_volume=formatted_consumption
        )

        logger.info(f'Registro mensal criado para o ID: {new_monthly_record.id}')

        return new_monthly_record

    except Exception as e:

        logger.error(f"Erro fatal {str(e)} | Cálculo não realizado")
        return None        

