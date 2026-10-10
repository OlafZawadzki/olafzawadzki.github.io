import os, re

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# 1. Update Nav
idx = idx.replace('<li><a href="#o-mnie">O mnie</a></li>', '<li><a href="about.html">O mnie</a></li>')
idx = idx.replace('<li><a href="#stream">Stream</a></li>', '')

# 2. Shorten Bio
bio_replacement = """
                        <span class="section-eyebrow">Moja droga i filozofia</span>
                        <h2 class="hero-title" style="margin-bottom: var(--space-4); font-size: var(--font-size-3xl);">Cześć, tu Olaf.</h2>
                        <p>
                            W sieci funkcjonuję jako <strong>HEXIT RELY</strong>. Od ponad 7 lat zgłębiam dźwięk, a swoją pasją do sound designu i tworzenia muzyki dzielę się na żywo podczas streamów.
                        </p>
                        <div style="margin-top: var(--space-6);">
                            <a href="about.html" class="btn btn-secondary">Poznaj mnie bliżej &rarr;</a>
                        </div>
"""
idx = re.sub(r'(<div class="about-story-text">).*?(</div>\s*<div class="about-story-image">)', r'\1\n' + bio_replacement + r'\2', idx, flags=re.DOTALL)

# 3. Remove Setup (and the image)
# We want to remove from "<!-- Zdjęcie ze stanowiska / studia -->" to the end of Setup section.
idx = re.sub(r'<!-- Zdjęcie ze stanowiska / studia -->.*?<!-- ==========================================================================\s*SEKCJA EKOSYSTEM', r'<!-- ==========================================================================\n             SEKCJA EKOSYSTEM', idx, flags=re.DOTALL)

# 4. Remove Stream section
idx = re.sub(r'<!-- ==========================================================================\s*SEKCJA STREAMING I FORMATY TRANSMISJI\s*========================================================================== -->\s*<section class="stream-section" id="stream".*?</section>', '', idx, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print('Updated index.html')
