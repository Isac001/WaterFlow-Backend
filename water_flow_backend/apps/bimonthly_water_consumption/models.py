# Import Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Bimonthly water consumption model
class BimonthlyWaterConsumption(models.Model):

    # Bimester label field (text)
    date_label = models.CharField(
        max_length=255,
        verbose_name=_("Rótulo do Bimestre"),
        help_text=_("EX: 'Janeiro e Fevereiro de 2025'")
    )

    # Bimester start date field
    start_date = models.DateField(
        verbose_name=_("Data de Início do Bimestre"),
    )

    # Bimester end date field
    end_date = models.DateField(
        verbose_name=_("Data de Fim do Bimestre")
    )

    # Total consumption field (decimal)
    total_consumption = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_("Consumo Total (L)"),
        help_text=_("Consumo total de água no bimestre em Litros")
    )

    # String representation of the model
    def __str__(self):
        # Retorna a representação em string formatada do modelo
        return f"{self.date_label} - {self.total_consumption} L"
    
    # Meta class for model settings
    class Meta:
        app_label = 'bimonthly_water_consumption'
        db_table = 'bimonthly_water_consumption'
        ordering = ['-start_date']
