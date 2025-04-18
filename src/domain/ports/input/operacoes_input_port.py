from typing import List

from src.domain.models.operacao import Operacao


class OperacoesInputPort:
    """Interface para leitura de operações financeiras."""

    def parse_operations(self, data: str) -> List[Operacao]:
        """Método para converter dados externos em operações do domínio."""
        pass
