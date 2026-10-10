import re

with open('styles.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

GREEN_PATTERNS = ['74, 222, 158', '4ade9e', '22c77a', '6ee7b7']
SKIP_PATTERNS = [
    '--primary-color', '--primary-dark', '--secondary-color',
    '--accent-color', '--gradient-primary', '--gradient-secondary',
    'btn-primary', '/* ', 'var(--primary', 'var(--secondary',
    'var(--gradient', 'var(--accent'
]

results = []
for i, line in enumerate(lines, 1):
    lower = line.lower()
    has_green = any(p in lower for p in GREEN_PATTERNS)
    has_skip = any(p in line for p in SKIP_PATTERNS)
    if has_green and not has_skip:
        results.append(f"{i}: {line.rstrip()}")

for r in results:
    print(r)
print(f"\nTotal: {len(results)} lines")
