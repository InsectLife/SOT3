# Trabalho Prático 3 - Simulador de Gerenciamento de Entrada e Saída

**Disciplina:** Sistemas Operacionais  
**Instituição:** Universidade Federal do Pampa (UNIPAMPA)

## 📌 Sobre o Projeto

Este projeto consiste em um simulador desenvolvido em Python para demonstrar o funcionamento do **Subsistema de Entrada e Saída (E/S)** de um Sistema Operacional. O foco principal é a implementação do mecanismo de **interrupções de hardware**, ilustrando como o processador lida com eventos externos, respeita hierarquias de prioridade e preserva o estado (contexto) dos processos.

O software simula o ciclo de vida de uma interrupção:
1. Pausa do processo em execução (Salvar Contexto).
2. Arbitragem de prioridade (Scheduler de Interrupções).
3. Execução da rotina de tratamento.
4. Retorno ao processo original (Restaurar Contexto).

## 🚀 Funcionalidades

* **Gerador de Eventos Aleatórios:** Simulação de interrupções vindas de periféricos distintos (Teclado, Impressora e Disco) em momentos aleatórios.
* **Arbitragem de Prioridade:** Implementação de uma fila de prioridades que garante que dispositivos críticos (ex: Teclado) sejam atendidos antes de dispositivos de baixa prioridade, mesmo em casos de **interrupções simultâneas**.
* **Troca de Contexto:** Simulação do salvamento de registradores (PC, status) e posterior restauração.
* **Log Detalhado:** Geração automática do arquivo `log_simulacao.txt` contendo o registro temporal de todos os eventos e estatísticas finais.

## 🛠️ Tecnologias e Estrutura

* **Linguagem:** Python 3.x (Bibliotecas padrão: `random`, `enum`, `typing`, `datetime`).
* **Arquitetura:**
    * `Dispositivo`: Define as características dos periféricos.
    * `Interrupcao`: Objeto comparável para ordenação na fila de prioridades.
    * `GerenciadorInterrupcoes`: Controla a fila, o salvamento de contexto e a lógica de escalonamento.
    * `SimuladorIO`: Classe principal que orquestra o loop de tempo (clock) e o fluxo de execução.

## 📋 Hierarquia de Prioridades

O simulador utiliza a seguinte tabela de prioridades para o tratamento de eventos:

| Dispositivo | Prioridade | Nível  | Comportamento |
|:-----------:|:----------:|:------:|:--------------|
| **Teclado** | 1          | Alta   | Atendimento Imediato |
| **Impressora**| 2        | Média  | Aguarda Alta prioridade |
| **Disco** | 3          | Baixa  | Aguarda Alta e Média |

## ⚙️ Como Executar

O projeto não requer instalação de bibliotecas externas. Para rodar a simulação:

1. Certifique-se de ter o Python 3 instalado.
2. Execute o arquivo principal no terminal:

```bash
python simulador_io.py
```
3. Ao final da execução, verifique o arquivo gerado log_simulacao.txt no mesmo diretório para ver o relatório completo.

## 📄 Entendendo o Log (Legenda)

O simulador gera logs visuais para facilitar o rastreamento do fluxo de execução. Abaixo, o significado de cada tag:

* [!] : Colisão de Interrupções. Indica que múltiplos dispositivos solicitaram atenção ao mesmo tempo (teste de prioridade).

* [+] : Interrupção adicionada à fila de espera (aguardando tratamento).

* [*] : Início do processamento da interrupção (Contexto salvo).

* [>] : Ciclo de tratamento da interrupção em andamento.

* [OK]: Interrupção finalizada (Contexto restaurado).

* [<] : Retorno ao processo principal (User mode)

## 🔍 Exemplo de Saída


[Tempo 08] - [ ] Processo principal em execucao (PC=8)
[Tempo 09] - [!] MULTIPLAS INTERRUPCOES simultaneas: Teclado, Disco (teste de prioridade)
[Tempo 09] - [*] Interrupcao: Teclado (Prioridade: Alta) - Latencia: 0u
[Tempo 09] -     -> Armazenando contexto: PC=9, Status='salvo'
[Tempo 09] -     -> Inicio do tratamento (3 ciclos estimados)
[Tempo 10] - [>] Continuando tratamento do Teclado (3 ciclos restantes)
...
[Tempo 12] - [OK] Interrupcao tratada. Restaurando contexto (PC=9).
[Tempo 12] - [<] Processo principal retomado (proxima instrucao: 10)