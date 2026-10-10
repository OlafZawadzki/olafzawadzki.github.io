import os, glob, re

# 1. Fix Hub Icons and gaming-btn style in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

idx = re.sub(
    r'<span class="now-tag" style="[^"]*">🎮 Its Hexit IRL</span>',
    r'<span>🎮 Its Hexit IRL (VOD)</span>',
    idx
)
# wait, it was inside `<a class="hub-btn gaming-btn">` which has `<span>🎮 Its Hexit IRL (VOD)</span>`
idx = idx.replace('style="background: rgba(59, 130, 246, 0.1); border-color: rgba(59, 130, 246, 0.3); color: #60a5fa;"', '')

# Replace emojis with SVGs
svg_game = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="hub-icon"><path d="M1.5 4A1.5 1.5 0 0 0 0 5.5v5A1.5 1.5 0 0 0 1.5 12h13a1.5 1.5 0 0 0 1.5-1.5v-5A1.5 1.5 0 0 0 14.5 4h-13zM6 8.5H4.5V10h-1V8.5H2v-1h1.5V6h1v1.5H6v1zM10.5 7a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm2.5 2.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/></svg>'
svg_music = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="hub-icon"><path d="M9 13c0 1.105-1.12 2-2.5 2S4 14.105 4 13s1.12-2 2.5-2 2.5.895 2.5 2z"/><path fill-rule="evenodd" d="M9 3v10H8V3h1z"/><path d="M8 2.82a1 1 0 0 1 .804-.98l3-.6A1 1 0 0 1 13 2.22V4L8 5V2.82z"/></svg>'
svg_laptop = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="hub-icon"><path d="M13.5 3a.5.5 0 0 1 .5.5V11H2V3.5a.5.5 0 0 1 .5-.5h11zm-11-1A1.5 1.5 0 0 0 1 3.5V12h14V3.5A1.5 1.5 0 0 0 13.5 2h-11zM0 12.5h16a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 12.5z"/></svg>'
svg_chat = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="hub-icon"><path d="M2.678 11.894a1 1 0 0 1 .287.801 10.97 10.97 0 0 1-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 0 1 .71-.074A8.06 8.06 0 0 0 8 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894zm-.493 3.905a21.682 21.682 0 0 1-.713.129c-.2.032-.352-.176-.273-.362a9.68 9.68 0 0 0 .244-.637l.003-.01c.248-.72.45-1.548.524-2.319C.743 11.37 0 9.76 0 8c0-3.866 3.582-7 8-7s8 3.134 8 7-3.582 7-8 7a9.06 9.06 0 0 1-2.347-.306c-.52.263-1.639.742-3.468 1.105z"/></svg>'

idx = idx.replace('<span>🎮 Its Hexit IRL (VOD)</span>', f'{svg_game}\n                                    <span>Its Hexit IRL (VOD)</span>')
idx = idx.replace('<span>🎵 Portfolio NOX</span>', f'{svg_music}\n                                    <span>Portfolio NOX</span>')
idx = idx.replace('<span>💻 Samplix</span>', f'{svg_laptop}\n                                    <span>Samplix</span>')
idx = idx.replace('<span>💬 Discord</span>', f'{svg_chat}\n                                    <span>Discord</span>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

# 2. Fix Navigation on all pages (excluding index.html where it should stay relative if needed, but actually index.html#projekty works everywhere including index.html)
for html_file in glob.glob("*.html"):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common nav replacements for ALL pages (including subpages)
    content = content.replace('href="#projekty"', 'href="index.html#projekty"')
    content = content.replace('href="#kontakt"', 'href="index.html#kontakt"')
    content = content.replace('href="#o-mnie"', 'href="about.html"')
    content = content.replace('href="#stream"', 'href="about.html#stream"')
    content = content.replace('href="index.html#o-mnie"', 'href="about.html"')
    
    # Fix the active class on index.html if it was mistakenly set to about.html#projekty (just in case)
    if html_file == 'index.html':
        pass # we actually want index.html#projekty in index.html as well, it behaves correctly in modern browsers (just scrolls down). But let's leave index.html#projekty.

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Clean up styles.css removing the .gaming-btn glow
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'\.gaming-btn\s*\{[^}]*\}', '', css)
css = re.sub(r'\.gaming-btn:hover\s*\{[^}]*\}', '', css)
css = re.sub(r'\.gaming-btn\s*span\s*\{[^}]*\}', '', css)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Done')
