#!/usr/bin/env python3
"""
Ponto de entrada principal da aplicação para o cálculo de ganho de capital.
"""

from pathlib import Path
import sys

# Adiciona o diretório src ao PYTHONPATH
src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from adapters.input.json_parser import JsonParser
from adapters.output.json_formatter import JsonFormatter
from domain.services.calcular_imposto_service import CalcularImpostoService


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
