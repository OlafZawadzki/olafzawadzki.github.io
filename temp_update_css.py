import os, re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update text variables and add gaming color
css = css.replace('--text-secondary: #c8bfb5;', '--text-secondary: #d6cec4;\n    --gaming-color: #3b82f6;')
css = css.replace('--text-muted: #9e9285;', '--text-muted: #b3a79a;')

# 2. Modify specific classes to be neutral
css = re.sub(r'(\.section-eyebrow\s*\{[^\}]*?color:\s*)var\(--secondary-color\)', r'\1var(--text-secondary)', css)

css = re.sub(r'(\.service-notice-pill\s*\{[^\}]*?color:\s*)var\(--primary-color\)', r'\1var(--text-secondary)', css)

css = re.sub(r'(\.blog-card-tag\s*\{[^\}]*?background:\s*)var\(--primary-color\)([^\}]*?color:\s*)#0a0a0a', r'\1rgba(255,255,255,0.1)\2var(--text-secondary)', css)

css = re.sub(
    r'(\.now-tag\s*\{[^\}]*?)background:\s*rgba\(74,\s*222,\s*158,\s*0\.07\);\s*border:\s*1px\s*solid\s*rgba\(74,\s*222,\s*158,\s*0\.18\);\s*color:\s*var\(--secondary-color\);',
    r'\1background: rgba(255, 255, 255, 0.03);\n    border: 1px solid var(--border-color);\n    color: var(--text-secondary);',
    css
)

# 3. Add gaming-btn class and gaming specific overrides
gaming_css = """
.gaming-btn {
    border-color: rgba(59, 130, 246, 0.5) !important;
    background: rgba(59, 130, 246, 0.1) !important;
}
.gaming-btn:hover {
    background: rgba(59, 130, 246, 0.2) !important;
    border-color: var(--gaming-color) !important;
    color: var(--gaming-color) !important;
}
.gaming-btn span {
    color: var(--gaming-color) !important;
}
"""
css += "\n" + gaming_css

# 4. Remove glow from non-CTA (card hover)
# Change --card-shadow-hover to have a less aggressive green glow (or neutral)
css = css.replace('--card-shadow-hover: 0 20px 40px -10px rgba(0, 0, 0, 0.65), 0 0 25px -5px rgba(74, 222, 158, 0.15);', '--card-shadow-hover: 0 20px 40px -10px rgba(0, 0, 0, 0.65), 0 0 25px -5px rgba(255, 255, 255, 0.05);')

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('Updated styles.css')
