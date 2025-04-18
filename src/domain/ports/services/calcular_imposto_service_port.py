from decimal import Decimal
from typing import List

from src.domain.models.operacao import Operacao


class CalcularImpostoServicePort:
    """Interface para serviço de cálculo de impostos."""

    def calcular_impostos(self, operacoes: List[Operacao]) -> List[Decimal]:
        """Calcula os impostos para uma lista de operações."""
        pass
