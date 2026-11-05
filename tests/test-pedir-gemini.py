#!/usr/bin/env python3
"""Regressões offline: erros JSON, banco temporário, timeout e stdin fechado."""
import csv, json, os, pathlib, subprocess, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='test-pedir-') as tmp:
    base = pathlib.Path(tmp)
    fake = base/'gemini-falso'
    fake.write_text('''#!/data/data/com.termux/files/usr/bin/python3
import json, os, sys, time
assert sys.stdin.read() == ''
assert '--settings' in sys.argv
settings = json.load(open(sys.argv[sys.argv.index('--settings')+1]))
assert settings['modelProvider'] == 'gemini'
assert 'command(*)' in settings['permissions']['deny']
assert 'write_file(*)' in settings['permissions']['deny']
assert sys.argv[sys.argv.index('--mode')+1] == 'plan'
case = os.environ['CASO_TESTE']
if case == 'timeout': time.sleep(10)
elif case == '503': print(json.dumps({'error': {'code':503,'message':'UNAVAILABLE key=AIzaFAKE_TEST_ONLY'}}))
elif case == 'search_quota':
 print('Error 429 RESOURCE_EXHAUSTED at WebSearchToolInvocation.execute',file=sys.stderr)
 sys.exit(1)
elif case == 'final_stderr':
 print('Attempt 1 failed: 503 UNAVAILABLE',file=sys.stderr)
 print(json.dumps({'error':{'code':429,'message':'You have exhausted your daily quota on this model.'}}),file=sys.stderr)
elif case == '429': print(json.dumps({'error': {'code':429,'message':'quota exhausted'}}))
elif case == 'status_error': print(json.dumps({'status':'WAITING','response':'partial'}))
elif case == 'error_response': print(json.dumps({'response':'partial','stats':{'models':{'test':{'tokens':{'prompt':14290}}}},'error':{'message':'context length exceeded'}}))
else: print('Aviso antes do JSON\\n'+json.dumps({'status':'SUCCESS','response':'OK','usage':{'input_tokens':100,'output_tokens':10,'thinking_tokens':6,'cache_read_tokens':20},'stats':{'models':{'legacy':{'tokens':{'prompt':900,'candidates':50,'cached':400}}}}}))
''')
    fake.chmod(0o700)
    script = base/'pedir'
    content = pathlib.Path(os.environ.get('PEDIR_TEST_SCRIPT',str(ROOT/'bin/pedir'))).read_text()
    content = content.replace('LOG=$TH/shared/consumo.csv', f'LOG={base}/consumo.csv')
    content = content.replace('ESTADO=$TH/shared/estado-contas.json', f'ESTADO={base}/estado.json')
    content = content.replace('termux_env "$TH/.local/bin/agy" ', f'termux_env {fake} ')
    script.write_text(content); script.chmod(0o700)
    for case, expected, bank in [('ok','ok',False),('503','indisponivel',True),('429','limite',True),('final_stderr','limite',True),('search_quota','limite_pesquisa',False),('error_response','erro',False),('status_error','erro',False),('timeout','tempo',False)]:
        (base/'estado.json').write_text('{}')
        env = dict(os.environ, CASO_TESTE=case, PEDIR_ORIGEM='codex', PEDIR_TIMEOUT='1')
        proc = subprocess.run([str(script),'gemini','-n','teste offline'],env=env,text=True,capture_output=True,timeout=15)
        rows = list(csv.DictReader((base/'consumo.csv').open()))
        assert rows[-1]['estado'] == expected, (case,proc.stderr,rows[-1])
        assert (proc.returncode == 0) == (expected == 'ok'), (case, proc.returncode)
        state = json.loads((base/'estado.json').read_text())
        assert bool(state.get('gemini')) == bank, (case,state)
        if case == 'ok':
            assert [rows[-1][k] for k in ('tok_entrada','tok_saida','tok_cache')] == ['100','10','20']
        if case == 'search_quota':
            assert 'gemini-pesquisa' in state
            skipped = subprocess.run([str(script),'gemini','-n','-t','pesquisa','teste offline'],env=env,text=True,capture_output=True,timeout=5)
            assert skipped.returncode != 0 and 'pesquisa Google' in skipped.stderr
            assert len(list(csv.DictReader((base/'consumo.csv').open()))) == len(rows)
        if case == '503':
            import datetime
            expiry = datetime.datetime.fromisoformat(state['gemini']['limite_ate'])
            assert 13*60 < (expiry-datetime.datetime.now()).total_seconds() <= 15*60
            diag = (base/'diagnosticos/gemini-ultimo-erro.txt').read_text()
            assert 'AIza' not in diag and 'AIza' not in proc.stderr
        print(f'{case}: OK')
print('8 regressões offline passaram; nenhuma chamada a agentes.')
