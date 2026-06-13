import requests
owner='kirui58-sy'; repo='silverback-flasher'; job_id='81189689878'
pat='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'
headers={'Authorization':f'token {pat}','Accept':'application/vnd.github+json'}
url=f'https://api.github.com/repos/{owner}/{repo}/actions/jobs/{job_id}/logs'
resp=requests.get(url, headers=headers)
print('status', resp.status_code)
open('logs.zip','wb').write(resp.content)
print('Saved logs.zip')
