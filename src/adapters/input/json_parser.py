from decimal import Decimal
import json
from typing import List

from src.domain.exceptions.parse_error import ParseError
from src.domain.models.operacao import Operacao, TipoOperacao


class JsonParser:
    """Classe responsável por converter strings JSON em listas de objetos Operacao."""

    @staticmethod
    def parse_operations(json_data: str) -> List[Operacao]:
        """Análise o JSON e retorna uma lista de operações instanciadas no objeto Operacao."""
        try:
            data = json.loads(json_data)

            return [
                Operacao(
                    tipo_operacao=TipoOperacao(item["operation"]),
                    preco_unitario=Decimal(str(item["unit-cost"])),
                    quantidade=int(item["quantity"]),
                )
                for item in data
            ]
        except (json.JSONDecodeError, KeyError, ValueError) as exception:
            raise ParseError(f"Erro ao processar JSON: {str(exception)}")
