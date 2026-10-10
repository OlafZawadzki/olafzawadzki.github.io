import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Extract header and everything before <main>
head_match = re.search(r'(.*?<main>)', idx, re.DOTALL)
head_part = head_match.group(1)

# Modify title and active nav in head_part
head_part = head_part.replace('<title>HEXIT RELY | Olaf Zawadzki — Producent Muzyczny, Sound Designer & Twórca</title>', '<title>O mnie | HEXIT RELY</title>')
head_part = head_part.replace('<li><a href="index.html" class="active">Start</a></li>', '<li><a href="index.html">Start</a></li>')
head_part = head_part.replace('<li><a href="#o-mnie">O mnie</a></li>', '<li><a href="about.html" class="active">O mnie</a></li>')
head_part = head_part.replace('<li><a href="#stream">Stream</a></li>', '')

# Extract footer and everything after </main>
foot_match = re.search(r'(</main>.*)', idx, re.DOTALL)
foot_part = foot_match.group(1)
foot_part = foot_part.replace('<li><a href="#o-mnie">O mnie</a></li>', '<li><a href="about.html">O mnie</a></li>')
foot_part = foot_part.replace('<li><a href="#stream">Stream</a></li>', '')

# 1. Kim jestem
bio_match = re.search(r'(<section class="about-story-section" id="o-mnie">\s*<div class="container">\s*<div class="about-intro-grid">.*?</div>)', idx, re.DOTALL)
bio_html = bio_match.group(1) + '\n\n'

# 2. Stanowisko
stanowisko_intro = """
                <!-- Przejście narracyjne 1 -->
                <div style="margin: var(--space-20) 0 var(--space-8); text-align: center; max-width: 800px; margin-left: auto; margin-right: auto;">
                    <span class="section-eyebrow">Gdzie to wszystko się dzieje</span>
                    <h3 style="font-size: var(--font-size-3xl); font-weight: 800; color: var(--text-primary);">
                        Cała ta praca dzieje się w jednym miejscu — oto moje stanowisko.
                    </h3>
                </div>
"""

stan_img_match = re.search(r'(<!-- Zdjęcie ze stanowiska / studia -->.*?</div>\s*</div>\s*</div>)', idx, re.DOTALL)
stan_img_html = stan_img_match.group(1) + '\n'

setup_match = re.search(r'(<!-- ==========================================================================\s*SEKCJA: MÓJ SETUP.*?</div>\s*</div>\s*</div>)', idx, re.DOTALL)
setup_html = setup_match.group(1) + '\n</div>\n</section>\n'

# Add some comments to the setup
setup_html = setup_html.replace('<li>Interfejs: Behringer UMC 204HD</li>', '<li>Interfejs: Behringer UMC 204HD <br><span style="font-size: 0.85em; color: var(--text-muted);">Niezawodny wół roboczy. Nie potrzebuję sprzętu za miliony, żeby robić dobrze brzmiące rzeczy.</span></li>')
setup_html = setup_html.replace('<li>Biurko: Własnoręcznie z europalet 🪵</li>', '<li>Biurko: Własnoręcznie z europalet 🪵 <br><span style="font-size: 0.85em; color: var(--text-muted);">Zrobione samodzielnie od zera. Najlepszy projekt DIY jaki zrealizowałem.</span></li>')

# 3. Jak mnie oglądać
stream_intro = """
        <section class="stream-section" id="stream" style="padding: var(--space-20) 0; background: var(--bg-primary);">
            <div class="container">
                <div class="section-header-wrap">
                    <span class="section-eyebrow">ZOBACZ TO NA ŻYWO</span>
                    <h2 class="section-title">Jeśli chcesz zobaczyć ten proces na żywo, oto gdzie mnie znajdziesz.</h2>
                    <p class="section-desc">Prowadzę dwa różne kanały, aby każdy znalazł dokładnie to, po co przyszedł.</p>
                </div>
"""

stream_match = re.search(r'<div class="channel-comparison-grid">(.*?</section>)', idx, re.DOTALL)
stream_html = '<div class="channel-comparison-grid">' + stream_match.group(1)

# Assemble about.html
about_content = head_part + '\n' + bio_html + stanowisko_intro + stan_img_html + setup_html + '\n' + stream_intro + stream_html + '\n' + foot_part

# Add a sticky nav pill to about_content
sticky_nav = """
        <!-- Sticky Nav -->
        <div style="position: sticky; top: 100px; z-index: 100; display: flex; justify-content: center; pointer-events: none; margin-bottom: -30px;">
            <div style="background: rgba(10,10,10,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 100px; display: flex; gap: 16px; pointer-events: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
                <a href="#o-mnie" style="color: var(--text-secondary); text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s;">Kim jestem</a>
                <span style="color: var(--border-color);">|</span>
                <a href="#setup" style="color: var(--text-secondary); text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s;">Stanowisko</a>
                <span style="color: var(--border-color);">|</span>
                <a href="#stream" style="color: var(--text-secondary); text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s;">Jak oglądać</a>
            </div>
        </div>
        <style>
            .sticky-nav-link:hover { color: var(--primary-color) !important; }
        </style>
"""
sticky_nav = sticky_nav.replace('style="color', 'class="sticky-nav-link" style="color')

about_content = about_content.replace('<main>', '<main>\n' + sticky_nav)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(about_content)
print('Generated about.html successfully')
