# Simulador de Gerenciamento de Entrada e Saída com Interrupção

## Sobre o Projeto

Este projeto é um simulador desenvolvido em Python para estudar e visualizar o funcionamento do gerenciamento de Entrada e Saída (E/S) em Sistemas Operacionais. Ele implementa o mecanismo de interrupções de hardware, demonstrando como o processador lida com eventos externos, prioridades e a preservação do estado dos processos.

O objetivo é ilustrar de forma clara como o sistema operacional pausa um processo em execução para atender requisições de dispositivos (Teclado, Impressora, Disco), realiza a troca de contexto e posteriormente retoma a execução original.

## Funcionalidades

- **Simulação de Dispositivos**: Geração aleatória de interrupções vindas de diferentes periféricos (Teclado, Impressora e Disco).
- **Gerenciamento de Prioridades**: Tratamento de requisições simultâneas ou concorrentes baseado na hierarquia de importância do dispositivo.
- **Troca de Contexto**: Simulação do armazenamento (salvamento) e recuperação do estado do processo interrompido.
- **Log de Eventos**: Geração de um registro detalhado (na tela ou arquivo) mostrando o fluxo temporal, desde a interrupção até a retomada do processo.

## Como Executar

O projeto consiste em um script principal. Para executá-lo:

1. Certifique-se de ter o Python 3 instalado em sua máquina.
2. Baixe o código fonte (arquivo .py).
3. No terminal, execute o comando:

```bash
python simulador_io.py
```


## Mecanismos Implementados

### 1. Sistema de Interrupções

O simulador reproduz o comportamento de hardware onde dispositivos externos sinalizam à CPU que precisam de atenção.

**Funcionamento**: O processo principal executa continuamente. Quando uma interrupção ocorre, o fluxo é pausado. O sistema "salva" onde parou (contexto), executa a rotina de tratamento do dispositivo específico e, ao finalizar, "restaura" o contexto para continuar o processo principal.

**Analogia**: Você está lendo um livro (processo) e o telefone toca (interrupção). Você marca a página (salva contexto), atende o telefone (trata interrupção) e depois volta a ler da página marcada (restaura contexto).

### 2. Hierarquia de Prioridades

Para garantir que eventos críticos sejam atendidos primeiro, o simulador define níveis de prioridade para cada dispositivo. Se duas interrupções ocorrerem na mesma unidade de tempo, a de maior prioridade é atendida primeiro.

A simulação utiliza a seguinte configuração de dispositivos:

| Dispositivo | Prioridade | Tipo de Prioridade |
|-------------|------------|-------------------|
| Teclado     | 1          | Alta              |
| Impressora  | 2          | Média             |
| Disco       | 3          | Baixa             |

## Exemplo de Log de Execução

Abaixo, um exemplo do formato de saída gerado pelo simulador, demonstrando o fluxo de interrupção e retomada:

```text
[Tempo 0]  - Processo principal em execução.
[Tempo 10] - Interrupção: Teclado - Prioridade: Alta - Armazenando contexto do processo principal.
[Tempo 11] - Tratando a interrupção do teclado.
[Tempo 15] - Interrupção tratada. Restaurando o contexto do processo principal.
[Tempo 16] - Processo principal retomado.
...
