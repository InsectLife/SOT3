"""
Simulador de Gerenciamento de Entrada e Saída com Interrupção

Simula o comportamento do gerenciamento de E/S em um sistema operacional,
utilizando interrupções para lidar com eventos de hardware.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
import random
from datetime import datetime


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
        self.tipo_prioridade = "Alta" if prioridade == Prioridade.ALTA else "Média" if prioridade == Prioridade.MEDIA else "Baixa"


class Interrupcao:
    """Representa uma interrupção na fila."""
    
    def __init__(self, prioridade: int, tempo_chegada: int, nome_dispositivo: str, tipo_prioridade: str):
        self.prioridade = prioridade
        self.tempo_chegada = tempo_chegada
        self.nome_dispositivo = nome_dispositivo
        self.tipo_prioridade = tipo_prioridade
    
    def __lt__(self, outro):
        """Comparação para ordenação da fila."""
        if self.prioridade != outro.prioridade:
            return self.prioridade < outro.prioridade
        return self.tempo_chegada < outro.tempo_chegada


class GerenciadorInterrupcoes:
    """Gerencia interrupções com base em prioridades."""
    
    def __init__(self):
        self.fila: List[Interrupcao] = []
        self.contexto_salvo: Optional[Dict[str, Any]] = None
    
    def adicionar_interrupcao(self, tempo: int, dispositivo: Dispositivo) -> bool:
        """
        Adiciona interrupção à fila com ordenação por prioridade.
        
        Returns:
            True se adicionada, False se já existe na fila
        """
        # Verifica se já existe uma interrupção deste dispositivo na mesma unidade de tempo
        ja_existe = any(
            i.nome_dispositivo == dispositivo.nome and 
            i.tempo_chegada == tempo 
            for i in self.fila
        )
        
        if ja_existe:
            return False
        
        interrupcao = Interrupcao(dispositivo.prioridade, tempo, dispositivo.nome, dispositivo.tipo_prioridade)
        self.fila.append(interrupcao)
        
        # Ordena: 1º por prioridade (menor = maior), 2º por tempo de chegada (FIFO)
        self.fila.sort()
        return True
    
    def proximo_interrupcao(self) -> Optional[Interrupcao]:
        """Retorna a próxima interrupção a ser processada."""
        if self.fila:
            return self.fila.pop(0)
        return None
    
    def tem_interrupcoes_pendentes(self) -> bool:
        """Verifica se há interrupções aguardando na fila."""
        return len(self.fila) > 0
    
    def salvar_contexto(self, tempo: int, endereco_pc: int = 0) -> None:
        """Salva contexto do processo interrompido."""
        self.contexto_salvo = {
            "tempo_interrupcao": tempo,
            "pc": endereco_pc,
            "registradores": {"A": 0, "B": 0, "C": 0},  # Simulados
            "status": "salvo"
        }
    
    def restaurar_contexto(self) -> Dict[str, Any]:
        """Restaura contexto salvo."""
        contexto = self.contexto_salvo
        if contexto:
            contexto["status"] = "restaurado"
        self.contexto_salvo = None
        return contexto


class SimuladorIO:
    """Simulador principal de E/S com interrupções."""
    
    DISPOSITIVOS = [
        Dispositivo("Teclado", Prioridade.ALTA),
        Dispositivo("Impressora", Prioridade.MEDIA),
        Dispositivo("Disco", Prioridade.BAIXA),
    ]
    
    def __init__(self, tempo_total: int = 50, arquivo_log: str = "log_simulacao.txt", prob_interrupcao: float = 0.25):
        self.tempo = 0
        self.tempo_total = tempo_total
        self.gerenciador = GerenciadorInterrupcoes()
        self.log = []
        self.arquivo_log = arquivo_log
        self.prob_interrupcao = prob_interrupcao  # Aumentada para testar melhor
        self.tempo_restante_tratamento = 0
        self.interrupcao_atual = None
        self.endereco_pc = 0
        self.ciclos_execucao_normal = 0
        self.estatisticas = {
            "Teclado": 0,
            "Impressora": 0,
            "Disco": 0,
            "total_interrupcoes": 0,
            "tempo_total_tratamento": 0,
            "ciclos_execucao_normal": 0,
            "casos_prioridade_testados": 0
        }
        
    def gerar_interrupcoes(self) -> List[str]:
        """
        Gera interrupções aleatórias.
        
        Returns:
            Lista de nomes de dispositivos que geraram interrupção neste ciclo
        """
        dispositivos_ativados = []
        for dispositivo in self.DISPOSITIVOS:
            if random.random() < self.prob_interrupcao:
                if self.gerenciador.adicionar_interrupcao(self.tempo, dispositivo):
                    dispositivos_ativados.append(dispositivo.nome)
        
        return dispositivos_ativados
    
    def processar_ciclo(self) -> None:
        """Executa um ciclo de simulação."""
        # 1. Tenta gerar novas interrupções neste ciclo
        dispositivos_ativados = self.gerar_interrupcoes()
        
        # Registra múltiplas interrupções simultâneas (caso de teste importante)
        if len(dispositivos_ativados) > 1:
            self.registrar_evento(f"[!] MULTIPLAS INTERRUPCOES simultaneas: {', '.join(dispositivos_ativados)} (teste de prioridade)")
            self.estatisticas["casos_prioridade_testados"] += 1
        elif len(dispositivos_ativados) == 1:
            # Verifica se há outras aguardando (fila não vazia)
            if self.gerenciador.tem_interrupcoes_pendentes() and self.tempo_restante_tratamento == 0:
                self.registrar_evento(f"[+] Interrupcao de {dispositivos_ativados[0]} adicionada a fila.")

        # 2. Verifica se está tratando uma interrupção
        if self.tempo_restante_tratamento > 0:
            self.registrar_evento(f"[>] Continuando tratamento do {self.interrupcao_atual['nome']} ({self.tempo_restante_tratamento} ciclos restantes)")
            self.tempo_restante_tratamento -= 1
            
            # Se terminou o tratamento agora
            if self.tempo_restante_tratamento == 0:
                ctx = self.gerenciador.restaurar_contexto()
                self.registrar_evento(f"[OK] Interrupcao tratada. Restaurando contexto (PC={ctx['pc']}).")
                self.registrar_evento(f"[<] Processo principal retomado (proxima instrucao: {ctx['pc'] + 1})")
                self.interrupcao_atual = None
            return

        # 3. Se não está tratando, verifica fila (Scheduler)
        proxima = self.gerenciador.proximo_interrupcao()
        
        if proxima:
            # Salva estatísticas
            self.estatisticas[proxima.nome_dispositivo] += 1
            self.estatisticas["total_interrupcoes"] += 1
            
            # Salva o contexto atual antes de tratar
            self.gerenciador.salvar_contexto(self.tempo, self.endereco_pc)
            
            # Configura o estado de "Tratando Interrupção"
            self.interrupcao_atual = {
                "nome": proxima.nome_dispositivo,
                "prioridade": proxima.tipo_prioridade,
                "tempo_chegada": proxima.tempo_chegada
            }
            self.tempo_restante_tratamento = random.randint(2, 4)
            self.estatisticas["tempo_total_tratamento"] += self.tempo_restante_tratamento
            
            latencia = self.tempo - proxima.tempo_chegada
            self.registrar_evento(f"[*] Interrupcao: {proxima.nome_dispositivo} (Prioridade: {proxima.tipo_prioridade}) - Latencia: {latencia}u")
            self.registrar_evento(f"    -> Armazenando contexto: PC={self.endereco_pc}, Status='salvo'")
            self.registrar_evento(f"    -> Inicio do tratamento ({self.tempo_restante_tratamento} ciclos estimados)")
        
        else:
            # 4. Se não há interrupções, o processo principal segue
            if self.ciclos_execucao_normal % 5 == 0:  # Log a cada 5 ciclos para não poluir
                self.registrar_evento(f"[ ] Processo principal em execucao (PC={self.endereco_pc})")
            self.endereco_pc += 1  # Simula incremento do PC
            self.ciclos_execucao_normal += 1
            self.estatisticas["ciclos_execucao_normal"] += 1
    
    def registrar_evento(self, evento: str) -> None:
        """Registra evento no log (tela e arquivo)."""
        mensagem = f"[Tempo {self.tempo:02d}] - {evento}"
        self.log.append(mensagem)
        print(mensagem)
    
    def salvar_log_arquivo(self) -> None:
        """Salva o log em arquivo de texto."""
        try:
            with open(self.arquivo_log, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("SIMULAÇÃO DE GERENCIAMENTO DE ENTRADA E SAÍDA COM INTERRUPÇÃO\n")
                f.write("=" * 80 + "\n")
                f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Tempo total de simulação: {self.tempo_total} unidades de tempo\n")
                f.write(f"Probabilidade de interrupção: {self.prob_interrupcao*100:.0f}%\n")
                f.write("=" * 80 + "\n\n")
                
                # Legenda
                f.write("LEGENDA:\n")
                f.write("  [!] = Multiplas interrupcoes simultaneas (teste de prioridade)\n")
                f.write("  [+] = Interrupcao adicionada a fila de espera\n")
                f.write("  [*] = Interrupcao sendo processada\n")
                f.write("  [>] = Continuacao do tratamento\n")
                f.write("  [OK] = Interrupcao finalizada\n")
                f.write("  [<] = Processo retomado\n")
                f.write("  [ ] = Execucao normal (processo principal)\n")
                f.write("=" * 80 + "\n\n")
                
                # Log de eventos
                f.write("LOG DE EVENTOS:\n")
                f.write("-" * 80 + "\n")
                for linha in self.log:
                    f.write(linha + "\n")
                
                # Estatísticas
                f.write("\n" + "=" * 80 + "\n")
                f.write("ESTATÍSTICAS:\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total de interrupções: {self.estatisticas['total_interrupcoes']}\n")
                f.write(f"  • Teclado (Alta prioridade):     {self.estatisticas['Teclado']:3d}\n")
                f.write(f"  • Impressora (Média prioridade): {self.estatisticas['Impressora']:3d}\n")
                f.write(f"  • Disco (Baixa prioridade):      {self.estatisticas['Disco']:3d}\n\n")
                f.write(f"Tempo total de tratamento: {self.estatisticas['tempo_total_tratamento']} unidades\n")
                f.write(f"Ciclos de execução normal: {self.estatisticas['ciclos_execucao_normal']}\n")
                f.write(f"Casos de múltiplas interrupções testados: {self.estatisticas['casos_prioridade_testados']}\n")
                f.write("=" * 80 + "\n")
            
            print(f"\n✓ Log salvo em: {self.arquivo_log}")
        except Exception as e:
            print(f"✗ Erro ao salvar log: {e}")
    
    def executar(self) -> None:
        """Executa a simulação completa."""
        self.registrar_evento("[INIT] Simulacao iniciada.")
        
        while self.tempo < self.tempo_total:
            self.processar_ciclo()
            self.tempo += 1
        
        self.registrar_evento("[END] Simulacao finalizada.")
        self.salvar_log_arquivo()




def main():
    """Função principal."""
    simulador = SimuladorIO(tempo_total=60, prob_interrupcao=0.25)
    simulador.executar()


if __name__ == "__main__":
    main()
