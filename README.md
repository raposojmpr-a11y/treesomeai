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
