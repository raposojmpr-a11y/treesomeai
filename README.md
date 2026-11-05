# TreeSomeAI

Equipa de três agentes de IA (🟠 Claude · 🟢 Codex · 🔵 Gemini/Antigravity) a trabalhar em conjunto
num Nothing Phone (1): Termux + Ubuntu (proot-distro).

| Ferramenta | Função |
|---|---|
| `bin/pedir` | um agente chama outro, com registo de consumo e "braçadeira" (substituição automática quando um fica sem tokens) |
| `bin/saldo` | quanto resta das contas de cada agente, sem gastar tokens |
| `bin/rever-consumo` | resumo do consumo de tokens |
| `policies/` | permissões do Antigravity/Gemini por modo (leitura/escrita) |
| `tests/` | testes de regressão offline |

Memória partilhada (fora do repositório): `MEMORIA.md` + `temas/`.

## O que faz

### 📨 `pedir`: um agente chama outro
`pedir <codex|gemini|claude|auto> [-t tipo] [-w] [-n] [-m modelo] [-c] "pedido"`
- É a forma única de um agente pedir trabalho a outro. Por omissão só leitura; com `-w` pode escrever.
- `-t` indica o tipo de tarefa; com `auto`, a cadeia escolhe quem a faz:

| Tipo | Cadeia |
|---|---|
| pesquisa, documento | Gemini → Claude → Codex |
| termux, rede, codigo | Codex → Claude → Gemini |
| revisao | Codex → Gemini → Claude |
| outro | Claude → Codex → Gemini |

- **Braçadeira automática:** se o agente bate no limite (ou está a ≥90%), o pedido passa ao próximo da cadeia e o agente fica "no banco" (Claude/Codex 5 h, Gemini 12 h). Ver com `pedir --estado`.
- `-m` escolhe o modelo para essa chamada; `-c` continua a conversa anterior sem reenviar contexto.
- Se a ligação cai a meio, repete uma vez. Cada chamada fica registada em `consumo.csv`.

### 📊 `saldo`: quanto resta de cada conta, com 0 tokens
- Claude: lê o ecrã `/usage` numa sessão tmux escondida (~15 s).
- Codex: lê os limites gravados na última sessão.
- Gemini: ainda sem medição.
- Guarda em `saldo.json`, que o `pedir` usa para passar a braçadeira **antes** do limite.

### 📈 `rever-consumo`: relatório de gastos
- Junta as chamadas entre agentes e as sessões do Claude/Codex (últimos 7 dias por omissão).
- Serve para ajustar as cadeias de encaminhamento.

### 🛡️ Por trás
- Políticas de sandbox (leitura/escrita) para o Antigravity e o Gemini.
- 11 testes automáticos offline.
- Histórico de alterações em [`CHANGELOG.md`](CHANGELOG.md).

## Uso rápido
```
pedir codex -t revisao "revê bin/x:10-40"      # chamada nova, só leitura
pedir codex -c "e a linha 55?"                  # continua a mesma conversa (sem reenviar contexto)
pedir claude -m haiku "resume este log"         # modelo por chamada
pedir --estado                                  # quem está no banco
python3 tests/test-pedir-gemini.py              # regressões offline (sem gastar tokens)
```
