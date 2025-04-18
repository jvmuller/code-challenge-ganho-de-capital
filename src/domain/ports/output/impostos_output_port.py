from decimal import Decimal
from typing import List


class ImpostosOutputPort:
    """Interface para formatação de impostos."""

    def formatar_impostos(self, impostos: List[Decimal]) -> str:
        """Método para formatar impostos para saída."""
        pass
