#!/usr/bin/env python3

import sys

from src.application.container import Container


def main() -> None:
    """Ponto de entrada principal para a aplicação CLI para o cálculo de ganho de capital."""

    input_port, service, output_port = Container.get_dependencies()

    for line in sys.stdin:
        if not line.strip():
            break

        try:
            operacoes = input_port.parse_operations(line)
            impostos = service.calcular_impostos(operacoes)
            print(output_port.formatar_impostos(impostos))
        except Exception as exception:
            raise SystemExit(f"Erro ao processar entrada: {str(exception)}")


if __name__ == "__main__":
    main()
