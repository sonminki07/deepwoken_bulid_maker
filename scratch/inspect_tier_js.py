import urllib.request
import re

url = "https://deepwoken.co/_nuxt/9w65rUzI.js"
code = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')

# Search for tier definitions S, A, B, C, D or fetch calls
print("Length of tier JS:", len(code))
endpoints = re.findall(r'fetch\([^\)]+\)|axios\.[a-z]+\([^\)]+\)|\$fetch\([^\)]+\)', code)
print("Fetch calls:", endpoints[:10])

# Look for keywords like "tier", "vote", "rank", "rating"
words = re.findall(r'[a-zA-Z0-9_\-\.\/]+', code)
matches = [w for w in words if any(k in w.lower() for k in ['tier', 'ranking', 'score', 'vote', 'supabase', 'firebase'])]
print("Sample matched keywords:", matches[:25])
