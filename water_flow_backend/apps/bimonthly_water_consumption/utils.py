# # Django and Python Imports
# from datetime import datetime, timedelta
# from decimal import Decimal
# import logging
# import locale

# # Project Imports
# from apps.monthly_water_consumption.models import MonthlyWaterConsumption
# from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption

# # Get a logger and locale instance for the current module
# logger = logging.getLogger(__name__)
# locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# # Define a function to calculate bimonthly water consumption
# def bimonthly_water_consumption():

#     # Start a try block to handle potential exceptions
#     try:

#         # Get the current date
#         today = datetime.now().date()

#         # Get the current month from today's date
#         current_month = today.month

#         # Get the current year from today's date
#         current_year = today.year

#         # Calculate the first month of the bimester (1, 3, 5, 7, 9, 11)
#         first_month = ((current_month - 1) // 2) * 2 + 1

#         # Determine the first day of the bimester
#         first_day = datetime(current_year, first_month, 1).date()

#         # Check if the first month of the bimester is November
#         if first_month == 11:

#             # If it's November, the last day is December 31st
#             last_day = datetime(current_year, 12, 31).date()
            
#         # For other bimesters
#         else:
#             # Get the first day of the month after the bimester and subtract one day
#             last_day = (datetime(current_year, first_month + 2, 1).date() - timedelta(days=1))

#         # Fetch monthly records that intersect with the bimester period
#         records = MonthlyWaterConsumption.objects.filter(
#             start_date__lte=last_day,
#             end_date__gte=first_day
#         # Order the records by their start date
#         ).order_by('start_date')

#         # Check if no records were found for the bimester
#         if not records.exists():

#             # Log a warning if no data is found
#             logger.warning(f"Nenhum dado encontrado para o bimestre {first_day.strftime('%B')} de {first_day.year}.")

#             # Return None if no records are found
#             return None
        
#         # Calculate the total volume consumed from the fetched records
#         total_volume = sum(Decimal(record.total_consumption) for record in records)

#         # Check if a bimonthly record already exists for this period
#         if BimonthlyWaterConsumption.objects.filter(
#             start_date=first_day,
#             end_date=last_day
#         ).exists():
            
#             # Log a warning if a record for this bimester already exists
#             logger.warning(f"Registro para o bimestre {first_day.strftime('%B')} de {first_day.year} já existe.")
            
#             # Return None if the record already exists
#             return None

#         # Create a list of month names for the bimester label
#         month_names = [
#             first_day.strftime('%B').capitalize(),
#             last_day.strftime('%B').capitalize()
#         ]

#         # Create and return a new BimonthlyWaterConsumption record
#         return BimonthlyWaterConsumption.objects.create(
#             date_label=f"Consumo bimestral de {month_names[0]} a {month_names[1]} de {current_year}",
#             start_date=first_day,
#             end_date=last_day,
#             total_consumption=total_volume.quantize(Decimal('0.01'))
#         )
    
#     # Catch any exception that might occur during the process
#     except Exception as e:

#         # Log the exception and your error
#         logger.exception(f"Falha ao calcular consumo bimestral: {e}")

#         # Return None if an exception occurs
#         return None

# Em um arquivo como /apps/bimonthly_water_consumption/utils.py
# Em /apps/bimonthly_water_consumption/utils.py

# Django and Python Imports
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
import locale
import logging

# Project Imports
from apps.monthly_water_consumption.models import MonthlyWaterConsumption
from apps.bimonthly_water_consumption.models import BimonthlyWaterConsumption

# Inicializa o logger para registrar informações e erros
logger = logging.getLogger(__name__)

# Configura o locale para nomes de meses em português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, '') # Fallback para o locale padrão do sistema

def bimonthly_water_consumption():
    """
    Calcula o consumo do bimestre com base no último registro mensal encontrado.
    Esta função é autônoma e não necessita de parâmetros.
    """
    try:
        # <> LÓGICA INTELIGENTE: Encontra o registro mensal mais recente para usar como referência.
        latest_month = MonthlyWaterConsumption.objects.order_by('-end_date').first()

        if not latest_month:
            logger.warning("Nenhum registro mensal encontrado. O cálculo bimestral não pode prosseguir.")
            return None

        # <> Usa a data do último registro mensal como ponto de partida.
        calculation_date = latest_month.end_date
        logger.info(f"Último mês encontrado termina em {calculation_date}. Verificando o bimestre correspondente.")

        # Determina o bimestre a ser processado a partir da data de referência
        current_year = calculation_date.year
        current_month = calculation_date.month
        first_month_of_bimester = ((current_month - 1) // 2) * 2 + 1
        first_day = datetime(current_year, first_month_of_bimester, 1).date()

        if first_month_of_bimester == 11:
            last_day = datetime(current_year, 12, 31).date()
        else:
            last_day = (datetime(current_year, first_month_of_bimester + 2, 1).date() - timedelta(days=1))

        # Checagem de idempotência: se o registro para este bimestre já existe, para a execução.
        if BimonthlyWaterConsumption.objects.filter(start_date=first_day, end_date=last_day).exists():
            logger.warning(f"Registro para o bimestre de {first_day.strftime('%B de %Y')} já existe.")
            return None

        # Busca os registros mensais contidos no período exato do bimestre
        records = MonthlyWaterConsumption.objects.filter(
            start_date__gte=first_day,
            end_date__lte=last_day
        )

        # Garante que existem exatamente 2 meses para o cálculo ser válido
        if records.count() != 2:
            logger.warning(f"Não foram encontrados os 2 registros mensais para o bimestre de {first_day.strftime('%B de %Y')}.")
            return None

        # Usa aggregate para somar o consumo total de forma eficiente no banco de dados
        total_volume = records.aggregate(total=Sum('total_consumption'))['total'] or Decimal('0.0')

        # Cria o rótulo com os nomes dos meses em português
        month_names = sorted(list(set(r.start_date.strftime('%B').capitalize() for r in records)))
        date_label = f"Consumo de {' e '.join(month_names)} de {current_year}"

        # Cria e retorna o novo registro bimestral
        new_bimonthly_record = BimonthlyWaterConsumption.objects.create(
            date_label=date_label,
            start_date=first_day,
            end_date=last_day,
            total_consumption=total_volume.quantize(Decimal('0.01'))
        )
        
        logger.info(f"Registro bimestral criado com sucesso. ID: {new_bimonthly_record.id}")
        return new_bimonthly_record

    except Exception as e:
        logger.exception(f'Falha crítica ao calcular consumo bimestral: {e}')
        return None