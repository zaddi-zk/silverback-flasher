import requests, time
owner='kirui58-sy'; repo='silverback-flasher'; pat='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'
headers={'Authorization':f'token {pat}','Accept':'application/vnd.github+json'}

def latest_run():
    r=requests.get(f'https://api.github.com/repos/{owner}/{repo}/actions/runs?branch=main', headers=headers)
    r.raise_for_status()
    runs=r.json().get('workflow_runs', [])
    if not runs:
        print('No workflow runs found')
        return None
    return runs[0]

run=latest_run()
if not run:
    raise SystemExit(0)
print('Latest run:', run['id'], run['status'], run['conclusion'])
print('URL:', run['html_url'])

for _ in range(30):
    r=requests.get(run['url'], headers=headers)
    r.raise_for_status()
    s=r.json()
    print('Status:', s['status'], 'Conclusion:', s.get('conclusion'))
    if s['status']=='completed':
        print('Finished with conclusion:', s.get('conclusion'))
        break
    time.sleep(5)
