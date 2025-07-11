from decimal import Decimal, InvalidOperation
import json
from typing import List

from src.domain.exceptions.parse_error import ParseError
from src.domain.models.operacao import Operacao, TipoOperacao
from src.domain.ports.input.operacoes_input_port import OperacoesInputPort


class JsonParser(OperacoesInputPort):
    """Classe responsável por converter strings JSON em listas de objetos Operacao."""

    @staticmethod
    def parse_operations(json_data: str) -> List[Operacao]:
        """Análise o JSON e retorna uma lista de operações instanciadas no objeto Operacao."""
        try:
            # Remove quebras de linha e espaços extras
            json_data = json_data.strip().replace("\n", "").replace("  ", " ")
            data = json.loads(json_data)

            return [
                Operacao(
                    tipo_operacao=TipoOperacao(item["operation"]),
                    preco_unitario=Decimal(str(item["unit-cost"])),
                    quantidade=int(item["quantity"]),
                )
                for item in data
            ]
        except (json.JSONDecodeError, KeyError, ValueError, InvalidOperation) as exception:
            raise ParseError(f"Erro ao processar JSON: {str(exception)}")
