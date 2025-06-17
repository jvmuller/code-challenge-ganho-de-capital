from decimal import Decimal
import json
from typing import List

from src.domain.ports.output.impostos_output_port import ImpostosOutputPort


class DecimalEncoder(json.JSONEncoder):
    """Classe responsável por converter Decimal para float."""

    def default(self, obj):
        """Converte Decimal para float."""
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class JsonFormatter(ImpostosOutputPort):
    """Classe responsável por formatar listas de impostos como JSON."""

    @staticmethod
    def formatar_impostos(impostos: List[Decimal]) -> str:
        """Formata lista de impostos como JSON."""
        result = [{"error": imposto} if isinstance(imposto, str) else {"tax": imposto} for imposto in impostos]
        return json.dumps(result, cls=DecimalEncoder, separators=(",", ": "))
