"""
Simulador de Gerenciamento de Entrada e Saída com Interrupção
"""

from enum import Enum
from typing import List, Optional
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
        # Cria a tupla com os dados da interrupção
        interrupcao = (dispositivo.prioridade, tempo, dispositivo.nome)
        self.fila.append(interrupcao)
        
        # Ordena a fila: 
        # 1º critério: Prioridade (menor valor = maior prioridade)
        # 2º critério: Tempo de chegada (FIFO para prioridades iguais)
        self.fila.sort(key=lambda x: (x[0], x[1]))
    
    def proximo_interrupcao(self) -> Optional[tuple]:
        """Retorna a próxima interrupção a ser processada."""
        if self.fila:
            return self.fila.pop(0)
        return None
    
    def salvar_contexto(self, tempo: int) -> None:
        """Salva contexto do processo."""
        # Armazena um "snapshot" simples do processo (PC simulado e tempo)
        self.contexto_salvo = {
            "pc": f"instrucao_no_tempo_{tempo}",
            "status": "executando"
        }
    
    def restaurar_contexto(self) -> dict:
        """Restaura contexto salvo."""
        contexto = self.contexto_salvo
        self.contexto_salvo = None  # Limpa o contexto salvo
        return contexto


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
        self.tempo_restante_tratamento = 0
        self.interrupcao_atual_nome = None
        
    def gerar_interrupcoes(self) -> None:
        """Gera interrupções aleatórias."""
        # Chance de interrupção (ex: 15% por dispositivo por ciclo)
        for dispositivo in self.DISPOSITIVOS:
            if random.random() < 0.15: 
                self.gerenciador.adicionar_interrupcao(self.tempo, dispositivo)
    
    def processar_ciclo(self) -> None:
        """Executa um ciclo de simulação."""
        # 1. Tenta gerar novas interrupções neste ciclo
        self.gerar_interrupcoes()

        # 2. Verifica se já estamos tratando uma interrupção (Processador Ocupado com IO)
        if self.tempo_restante_tratamento > 0:
            self.registrar_evento(f"Tratando a interrupção do {self.interrupcao_atual_nome}...")
            self.tempo_restante_tratamento -= 1
            
            # Se terminou o tratamento agora
            if self.tempo_restante_tratamento == 0:
                ctx = self.gerenciador.restaurar_contexto()
                self.registrar_evento(f"Interrupção tratada. Restaurando o contexto do processo principal.")
                self.interrupcao_atual_nome = None
            return

        # 3. Se não estamos ocupados, verificamos se há algo na fila (Scheduler)
        proxima = self.gerenciador.proximo_interrupcao()
        
        if proxima:
            prioridade, tempo_origem, nome_disp = proxima
            
            # Salva o contexto atual antes de tratar
            self.gerenciador.salvar_contexto(self.tempo)
            
            # Configura o estado de "Tratando Interrupção"
            self.interrupcao_atual_nome = nome_disp
            # Define um tempo de duração baseado na prioridade (opcional, mas didático)
            # Ex: Alta prioridade resolve rápido (3 ticks), Baixa demora mais (5 ticks)
            # Ou fixo para simplificar. Vamos usar um valor aleatório entre 2 e 4.
            self.tempo_restante_tratamento = random.randint(2, 4)
            
            msg_prio = "Alta" if prioridade == 1 else "Média" if prioridade == 2 else "Baixa"
            self.registrar_evento(f"Interrupção: {nome_disp} - Prioridade: {msg_prio} - Armazenando contexto do processo principal.")
        
        else:
            # 4. Se não há interrupções, o processo principal segue (CPU User Mode)
            self.registrar_evento("Processo principal em execução.")
    
    def registrar_evento(self, evento: str) -> None:
        """Registra evento no log."""
        mensagem = f"[Tempo {self.tempo:02d}] - {evento}"
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
