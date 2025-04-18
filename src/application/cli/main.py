#!/usr/bin/env python3

import sys

from src.application.container import Container


def main() -> None:
    """Ponto de entrada principal para a aplicação CLI para o cálculo de ganho de capital."""

    _, _, _, use_case = Container.get_dependencies()

    for line in sys.stdin:
        if not line.strip():
            break

        try:
            print(use_case.execute(line))
        except Exception as exception:
            raise SystemExit(f"Erro ao processar entrada: {str(exception)}")


if __name__ == "__main__":
    main()
