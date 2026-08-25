import urllib.request
import re

url = "https://deepwoken.co/_nuxt/9w65rUzI.js"
code = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')

print("Code snippet around API/fetch/store:")
for line in code.split(';'):
    if any(k in line for k in ['vote', 'tier', 'fetch', 'api', 'supabase', 'firebase', 'graphql']):
        print("->", line[:150])
