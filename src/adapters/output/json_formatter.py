from decimal import Decimal
import json
from typing import List


class DecimalEncoder(json.JSONEncoder):
    """Classe responsável por converter Decimal para float."""

    def default(self, obj):
        """Converte Decimal para float."""
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class JsonFormatter:
    """Classe responsável por formatar listas de impostos como JSON."""

    @staticmethod
    def formatar_impostos(impostos: List[Decimal]) -> str:
        """Formata lista de impostos como JSON."""
        result = [{"tax": imposto} for imposto in impostos]
        return json.dumps(result, cls=DecimalEncoder, separators=(",", ": "))
