from src.domain.ports.input.operacoes_input_port import OperacoesInputPort
from src.domain.ports.output.impostos_output_port import ImpostosOutputPort
from src.domain.ports.services.calcular_imposto_service_port import CalcularImpostoServicePort


class CalcularImpostosUseCase:
    """Caso de uso para cálculo de impostos."""

    def __init__(
        self,
        operacoes_input: OperacoesInputPort,
        imposto_service: CalcularImpostoServicePort,
        impostos_output: ImpostosOutputPort,
    ):
        self._operacoes_input = operacoes_input
        self._imposto_service = imposto_service
        self._impostos_output = impostos_output

    def execute(self, input_data: str) -> str:
        """Executa o fluxo completo de cálculo de impostos com entrada e saída formatadas."""
        operacoes = self._operacoes_input.parse_operations(input_data)
        impostos = self._imposto_service.calcular_impostos(operacoes)
        return self._impostos_output.formatar_impostos(impostos)
