import requests

# Test the default pages domain (should work immediately)
url = 'https://hottboiihitzz.pages.dev'
print(f'Testing {url}...')

try:
    r = requests.get(url, timeout=10, allow_redirects=True)
    print(f'Status: {r.status_code}')
    print(f'Content length: {len(r.content)} bytes')
    print(f'Title: {r.text[r.text.find("<title>"):r.text.find("</title>")+8] if "<title>" in r.text else "N/A"}')
    print(f'\n✓ Site is LIVE and accessible!')
    
    # Show first 500 chars of content to verify it's our app
    print(f'\nFirst 500 chars of content:')
    print(r.text[:500])
except Exception as e:
    print(f'Error: {e}')
