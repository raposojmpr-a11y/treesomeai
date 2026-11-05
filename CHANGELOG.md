# Changelog — TreeSomeAI
Formato: [Keep a Changelog](https://keepachangelog.com/pt-PT/1.1.0/). Datas AAAA-MM-DD. Autor entre parênteses.
Regra: cada alteração ao código entra aqui, no mesmo commit.

## [Por lançar]
### Adicionado
- README: secção "O que faz"; repositório publicado no GitHub. (claude)

## [0.1.0] — 2026-11-05
### Adicionado
- Repositório git TreeSomeAI em `~/shared` (só `bin/`, `tests/`, `policies/`, docs). (claude)
- `pedir -m <modelo>`: modelo por chamada, só no agente pedido. (claude, ideia gemini)
- `pedir -c`: continua a última conversa com o agente (claude `--resume`, codex `exec resume`, agy `--conversation`). (claude, ideia gemini)
- Repetição automática quando a ligação do agente é interrompida. (claude)
- Testes offline: sinais, stream interrompido, continuação de conversa (11 no total). (claude)
### Corrigido
- `saldo`: lock e escrita atómica; medições paralelas já não se atropelam. (claude, codex)
- `saldo codex`: recua para sessões anteriores quando a atual ainda não tem limites. (claude)
- `saldo`: timeouts nos comandos tmux. (codex)
- `pedir`: limpeza por sinais (agente, vigia e temporários). (codex)
- `pedir`: escrita atómica do estado do banco. (codex)
- `pedir`: braçadeira antecipada só salta o titular se houver substituto elegível (incl. quota de pesquisa). (codex)
- `pedir`: em modo escrita, limite atingido já não passa a tarefa a outro agente. (codex)
- `pedir`: `--estado`/`--livre` devolvem o código de erro real; `-t` validado. (codex, claude)
- `rever-consumo`: procura sessões do Claude em todas as raízes. (claude)
