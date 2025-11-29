"""
Simulador de Gerenciamento de Entrada e Saída com Interrupção
"""

from enum import Enum
from typing import List
import random


class Prioridade(Enum):
    """Níveis de prioridade dos dispositivos."""
    ALTA = 1
    MEDIA = 2
    BAIXA = 3


class Dispositivo:
    """Representa um dispositivo de E/S."""
    
    def __init__(self, nome: str, prioridade: Prioridade):
        self.nome = nome
        self.prioridade = prioridade.value


class GerenciadorInterrupcoes:
    """Gerencia interrupções com base em prioridades."""
    
    def __init__(self):
        self.fila: List[tuple] = []  # (prioridade, tempo, dispositivo_nome)
        self.contexto_salvo = None
    
    def adicionar_interrupcao(self, tempo: int, dispositivo: Dispositivo) -> None:
        """Adiciona interrupção à fila."""
        # TODO: Adicionar à fila mantendo ordem de prioridade
        pass
    
    def proximo_interrupcao(self) -> tuple:
        """Retorna a próxima interrupção a ser processada."""
        # TODO: Retornar interrupção de maior prioridade
        pass
    
    def salvar_contexto(self, tempo: int) -> None:
        """Salva contexto do processo."""
        # TODO: Armazenar tempo e estado do processo
        pass
    
    def restaurar_contexto(self) -> dict:
        """Restaura contexto salvo."""
        # TODO: Retornar contexto armazenado
        pass


class SimuladorIO:
    """Simulador principal de E/S com interrupções."""
    
    DISPOSITIVOS = [
        Dispositivo("Teclado", Prioridade.ALTA),
        Dispositivo("Impressora", Prioridade.MEDIA),
        Dispositivo("Disco", Prioridade.BAIXA),
    ]
    
    def __init__(self, tempo_total: int = 50):
        self.tempo = 0
        self.tempo_total = tempo_total
        self.gerenciador = GerenciadorInterrupcoes()
        self.log = []
    
    def gerar_interrupcoes(self) -> None:
        """Gera interrupções aleatórias."""
        # TODO: Simular geração aleatória de interrupções
        pass
    
    def processar_ciclo(self) -> None:
        """Executa um ciclo de simulação."""
        # TODO: Gerar interrupções, processar fila e registrar evento
        pass
    
    def registrar_evento(self, evento: str) -> None:
        """Registra evento no log."""
        mensagem = f"[Tempo {self.tempo}] - {evento}"
        self.log.append(mensagem)
        print(mensagem)
    
    def executar(self) -> None:
        """Executa a simulação."""
        self.registrar_evento("Simulação iniciada.")
        
        while self.tempo < self.tempo_total:
            self.processar_ciclo()
            self.tempo += 1
        
        self.registrar_evento("Simulação finalizada.")


def main():
    """Função principal."""
    simulador = SimuladorIO(tempo_total=50)
    simulador.executar()


if __name__ == "__main__":
    main()
