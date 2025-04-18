from src.adapters.input.json_parser import JsonParser
from src.adapters.output.json_formatter import JsonFormatter
from src.domain.ports.input.operacoes_input_port import OperacoesInputPort
from src.domain.ports.output.impostos_output_port import ImpostosOutputPort
from src.domain.services.calcular_imposto_service import CalcularImpostoService


class Container:
    """Container para gerenciar dependências da aplicação."""

    @classmethod
    def get_dependencies(cls):
        """Retorna as dependências configuradas para a aplicação."""
        input_port = cls.get_input_port()
        output_port = cls.get_output_port()
        service = cls.get_service()

        return input_port, service, output_port

    @classmethod
    def get_input_port(cls) -> OperacoesInputPort:
        """Retorna o adaptador de entrada configurado."""
        return JsonParser()

    @classmethod
    def get_output_port(cls) -> ImpostosOutputPort:
        """Retorna o adaptador de saída configurado."""
        return JsonFormatter()

    @classmethod
    def get_service(cls):
        """Retorna o serviço de cálculo de impostos."""
        return CalcularImpostoService()
