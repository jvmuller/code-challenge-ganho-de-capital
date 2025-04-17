#!/usr/bin/env python3
"""
Ponto de entrada principal da aplicação para o cálculo de ganho de capital.
"""

import sys

from src.adapters.input.json_parser import JsonParser
from src.adapters.output.json_formatter import JsonFormatter
from src.domain.services.calcular_imposto_service import CalcularImpostoService


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            break

        try:
            operacoes = JsonParser.parse_operations(line)
            impostos = CalcularImpostoService().calcular_impostos(operacoes)
            print(JsonFormatter.formatar_impostos(impostos))
        except Exception as exception:
            raise SystemExit(f"Erro ao processar entrada: {str(exception)}")


if __name__ == "__main__":
    main()
