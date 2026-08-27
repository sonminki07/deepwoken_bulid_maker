import os
from pathlib import Path

kb_dir = Path('data/knowledge_base')
suspicious_files = []

for filepath in kb_dir.rglob('*'):
    if filepath.is_file() and filepath.suffix in ['.md', '.txt']:
        if filepath.name in ['INDEX.md', 'README.md']: continue
            
        try:
            content = filepath.read_text(encoding='utf-8')
        except:
            continue
            
        reasons = []
        
        if 'Unnamed Build' in content or 'Unknown Title' in content:
            reasons.append('빌드 이름/영상 제목 누락 (Unnamed/Unknown)')
            
        if 'No summary provided.' in content:
            reasons.append('빌드 요약/코멘트 누락 (No summary provided)')
            
        if content.count('N/A') > 3 or content.count('Unknown') > 3:
            reasons.append('N/A 또는 Unknown 데이터가 4개 이상 포함됨')
            
        if len(content.strip()) < 500:
            reasons.append('파일 내용이 너무 짧음 (500자 미만)')
            
        if filepath.suffix == '.md':
             # stats check: if too many `0`
             if content.count('`0`') > 6:
                  reasons.append('대부분의 스탯(Stats)이 0으로 기록됨')
                  
        if reasons:
            suspicious_files.append((filepath.name, reasons))

if suspicious_files:
    for name, reasons in suspicious_files:
        print(f'- {name}')
        for r in reasons:
            print(f'  * {r}')
else:
    print('No suspicious files found.')
