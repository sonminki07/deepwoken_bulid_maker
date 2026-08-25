import sys
import re
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
req = urllib.request.Request('https://deepwoken.co/tier-lists', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

scripts = re.findall(r'href="([^"]+\.js)"', html) + re.findall(r'src="([^"]+\.js)"', html)
for s in set(scripts):
    js_url = 'https://deepwoken.co' + s if s.startswith('/') else s
    try:
        jscode = urllib.request.urlopen(urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
        matches = re.findall(r'/(?:api|server)/[a-zA-Z0-9_\-\/]+', jscode)
        if matches:
            print(f"File {s}: API routes -> {set(matches)}")
        full_urls = re.findall(r'https?://[a-zA-Z0-9_\-\.:]+/[a-zA-Z0-9_\-\/]+', jscode)
        relevant = [u for u in set(full_urls) if 'api' in u or 'deepwoken' in u]
        if relevant:
            print(f"File {s}: Full URLs -> {relevant}")
    except Exception as e:
        pass
