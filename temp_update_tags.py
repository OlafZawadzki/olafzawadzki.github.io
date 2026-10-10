import re

for fname in ['index.html', 'about.html']:
    if not __import__('os').path.exists(fname): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Style gaming tags specifically
    content = content.replace('<span class="now-tag">🎮 Its Hexit IRL</span>', '<span class="now-tag" style="background: rgba(59, 130, 246, 0.1); border-color: rgba(59, 130, 246, 0.3); color: #60a5fa;">🎮 Its Hexit IRL</span>')

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
print('Updated gaming tags')
