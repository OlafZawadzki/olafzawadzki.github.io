import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The main content is broken - let's extract head, nav, footer and rebuild main
head_match = re.search(r'(.*?<main>)', content, re.DOTALL)
head_part = head_match.group(1)

foot_match = re.search(r'(</main>.*)', content, re.DOTALL)
foot_part = foot_match.group(1)

# Rebuild the main content cleanly
main_content = """
        <!-- Sticky mini-nav -->
        <div style="position: sticky; top: 88px; z-index: 100; display: flex; justify-content: center; pointer-events: none; padding: 16px 0 0; margin-bottom: 8px;">
            <div style="background: rgba(10,10,10,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 100px; display: flex; gap: 20px; pointer-events: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
                <a href="#o-mnie" style="color: var(--text-secondary); text-decoration: none; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; transition: color 0.2s;" onmouseover="this.style.color='var(--primary-color)'" onmouseout="this.style.color='var(--text-secondary)'">Kim jestem</a>
                <span style="color: var(--border-color);">|</span>
                <a href="#setup" style="color: var(--text-secondary); text-decoration: none; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; transition: color 0.2s;" onmouseover="this.style.color='var(--primary-color)'" onmouseout="this.style.color='var(--text-secondary)'">Stanowisko</a>
                <span style="color: var(--border-color);">|</span>
                <a href="#stream" style="color: var(--text-secondary); text-decoration: none; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; transition: color 0.2s;" onmouseover="this.style.color='var(--primary-color)'" onmouseout="this.style.color='var(--text-secondary)'">Jak oglądać</a>
            </div>
        </div>

        <!-- =============================================
             SEKCJA 1: Kim jestem
             ============================================= -->
        <section class="about-story-section" id="o-mnie" style="padding: var(--space-20) 0;">
            <div class="container">
                <div class="about-intro-grid">
                    <div class="about-story-text">
                        <span class="section-eyebrow">Moja droga i filozofia</span>
                        <h1 class="hero-title" style="margin-bottom: var(--space-4); font-size: var(--font-size-3xl);">Cześć, tu Olaf.</h1>
                        <p style="color: var(--text-secondary); line-height: 1.75; margin-bottom: var(--space-4);">
                            W sieci funkcjonuję jako <strong style="color: var(--text-primary);">HEXIT RELY</strong>. Nie traktuję tej strony jako sztywnego CV czy kolejnego cennika usług — to miejsce, w którym chcę pokazać Ci, kim naprawdę jestem jako twórca i czym na co dzień żyje moja głowa.
                        </p>
                        <p style="color: var(--text-secondary); line-height: 1.75; margin-bottom: var(--space-4);">
                            Od ponad 7 lat zgłębiam dźwięk. Zaczynałem od chaotycznych eksperymentów z syntezatorami w domowym pokoju, a z czasem przerodziło się to w pełną pasję do sound designu gier, kompozycji i miksu. W pewnym momencie poczułem jednak, że zamykanie się na miesiące w ciemnym studio sam na sam z monitorem to za mało — brakowało mi kontaktu z ludźmi, wymiany energii i dzielenia się procesem.
                        </p>
                        <p style="color: var(--text-secondary); line-height: 1.75;">
                            Tak narodził się pomysł na streaming. Zamiast pokazywać wyłącznie "wypolerowany efekt końcowy", odpaliłem kamerę i zacząłem streamować cały proces: błędy, poszukiwania brzmień, układanie perkusji od zera i rozkładanie projektów na czynniki pierwsze.
                        </p>
                    </div>
                    <div class="about-story-image">
                        <div class="hero-avatar-wrap">
                            <img src="hexit/Fotos26/hexit-face.jpg" alt="Olaf Zawadzki - Hexit Rely">
                            <div class="hero-status-pill">
                                <span>🎧 Muzyka • Streaming • Rzemiosło</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- =============================================
             SEKCJA 2: Moje stanowisko
             ============================================= -->
        <section id="setup" style="padding: var(--space-20) 0; background: var(--bg-secondary);">
            <div class="container">
                <!-- Narracyjne przejście -->
                <div style="text-align: center; max-width: 800px; margin: 0 auto var(--space-16);">
                    <span class="section-eyebrow">Gdzie to wszystko się dzieje</span>
                    <h2 style="font-size: var(--font-size-3xl); font-weight: 800; color: var(--text-primary); margin-top: var(--space-3);">
                        Cała ta praca dzieje się w jednym miejscu — oto moje stanowisko.
                    </h2>
                </div>

                <!-- Zdjęcie stanowiska + opis -->
                <div class="content-card" style="margin-bottom: var(--space-12);">
                    <div style="display: grid; grid-template-columns: 1.1fr 0.9fr; gap: var(--space-10); align-items: center;">
                        <div>
                            <span class="section-eyebrow">Moje codzienne stanowisko</span>
                            <h3 style="font-size: var(--font-size-2xl); font-weight: 800; margin-bottom: var(--space-4); margin-top: var(--space-2); color: var(--text-primary);">
                                Miejsce, w którym powstaje wszystko
                            </h3>
                            <p style="color: var(--text-secondary); line-height: 1.7; margin-bottom: var(--space-4);">
                                To tutaj nagrywam streamy, produkuję muzykę, testuję kolejne wersje oprogramowania Samplix i planuję kolejne projekty DIY.
                            </p>
                            <p style="color: var(--text-secondary); line-height: 1.7;">
                                Kluczem do dobrego brzmienia nie są drogie wtyczki, ale zbalansowane warunki odsłuchowe, wygoda pracy i narzędzia, które nie przeszkadzają w przepływie kreatywnym.
                            </p>
                        </div>
                        <div>
                            <img src="hexit/Fotos26/hexit-stanowisko.jpg" alt="Stanowisko studyjne Hexit Rely" style="width: 100%; border-radius: var(--radius-xl, 20px); box-shadow: var(--shadow-xl); border: 1px solid var(--border-color);">
                        </div>
                    </div>
                </div>

                <!-- Setup grid -->
                <div class="section-header-wrap" style="margin-bottom: var(--space-8);">
                    <span class="section-eyebrow">Sprzęt &amp; Narzędzia</span>
                    <h3 class="section-title">Mój Setup w 2024 / 2026</h3>
                    <p class="section-desc">Dokładna lista sprzętu, na którym na co dzień nagrywam, gram, produkuję i streamuję.</p>
                </div>

                <div class="setup-grid">
                    <div class="setup-card">
                        <h4>🎹 Interfejsy &amp; Audio</h4>
                        <ul>
                            <li>DAW: Ableton Live Suite &amp; FL Studio</li>
                            <li>Interfejs: Behringer UMC 204HD<br><span style="font-size: 0.85em; color: var(--text-muted);">Niezawodny wół roboczy. Nie potrzebuję sprzętu za miliony, żeby robić dobrze brzmiące rzeczy.</span></li>
                            <li>Interfejs mobilny: Swiftsonic Audio 2</li>
                            <li>Mikrofon: Behringer XM 8500 ×2</li>
                        </ul>
                    </div>
                    <div class="setup-card">
                        <h4>🖥️ Monitory &amp; Odsłuch</h4>
                        <ul>
                            <li>Monitory studyjne: Yamaha HS5 + HS8S (subwoofer)</li>
                            <li>Słuchawki: Sony MDR-7506, Audio-Technica ATH-M40x</li>
                        </ul>
                    </div>
                    <div class="setup-card">
                        <h4>💻 Komputer &amp; Peryferiale</h4>
                        <ul>
                            <li>CPU: AMD Ryzen 5 5600X</li>
                            <li>RAM: 32 GB DDR4</li>
                            <li>GPU: NVIDIA RTX 3060 Ti</li>
                            <li>Dyski: NVMe 1 TB + HDD 4 TB</li>
                        </ul>
                    </div>
                    <div class="setup-card">
                        <h4>🎹 Kontrolery MIDI</h4>
                        <ul>
                            <li>MIDI: Arturia MiniLab MkII</li>
                            <li>Kontroler: Launchpad X</li>
                        </ul>
                    </div>
                    <div class="setup-card">
                        <h4>🪵 Studio DIY</h4>
                        <ul>
                            <li>Biurko: Własnoręcznie z europalet 🪵<br><span style="font-size: 0.85em; color: var(--text-muted);">Zrobione samodzielnie od zera. Najlepszy projekt DIY jaki zrealizowałem.</span></li>
                            <li>Panele akustyczne: DIY z wełny mineralnej w drewnianych ramach</li>
                            <li>Kamera: Logitech C920 Pro HD</li>
                        </ul>
                    </div>
                    <div class="setup-card">
                        <h4>🎬 Streaming</h4>
                        <ul>
                            <li>Oprogramowanie: OBS Studio z własną scenografią</li>
                            <li>Oswietlenie: Ring light + Elgato Key Light</li>
                            <li>Kontroler Stream: Elgato Stream Deck MK.2</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- =============================================
             SEKCJA 3: Jak mnie oglądać
             ============================================= -->
        <section class="stream-section" id="stream" style="padding: var(--space-20) 0; background: var(--bg-primary);">
            <div class="container">
                <div class="section-header-wrap">
                    <span class="section-eyebrow">ZOBACZ TO NA ŻYWO</span>
                    <h2 class="section-title">Jeśli chcesz zobaczyć ten proces na żywo, oto gdzie mnie znajdziesz.</h2>
                    <p class="section-desc">Prowadzę dwa różne kanały, aby każdy znalazł dokładnie to, po co przyszedł.</p>
                </div>

                <div class="channel-comparison-grid">
                    <!-- Kanał Główny -->
                    <div class="channel-card">
                        <div>
                            <span class="channel-card-badge badge-main-channel">Kanał Główny: Muzyka &amp; Edycja</span>
                            <h3 style="font-size: var(--font-size-2xl); font-weight: 700; margin-bottom: var(--space-3); color: var(--text-primary);">
                                Hexit Rely (Main)
                            </h3>
                            <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: var(--space-4);">
                                Miejsce skupione na czystym rzemiośle audio:
                            </p>
                            <ul style="list-style: none; padding: 0; margin-bottom: var(--space-6);">
                                <li style="padding: 6px 0; color: var(--text-secondary); display: flex; align-items: center; gap: 8px;">
                                    <span style="color: #ef4444;">▶</span> Sesje tworzenia utworów w DAW na żywo
                                </li>
                                <li style="padding: 6px 0; color: var(--text-secondary); display: flex; align-items: center; gap: 8px;">
                                    <span style="color: #ef4444;">▶</span> Montowane materiały zza kulis i poradniki
                                </li>
                                <li style="padding: 6px 0; color: var(--text-secondary); display: flex; align-items: center; gap: 8px;">
                                    <span style="color: #ef4444;">▶</span> Sound design do gier i testowanie wtyczek
                                </li>
                            </ul>
                        </div>
                        <div>
                            <a href="https://www.youtube.com/channel/UCIpPTE3HsmUSAb-yfNybvSA" target="_blank" rel="noopener" class="btn btn-primary" style="width: 100%;">
                                Przejdź do Kanału Głównego ↗
                            </a>
                        </div>
                    </div>

                    <!-- Kanał Drugi: Its Hexit IRL -->
                    <div class="channel-card">
                        <div>
                            <span class="channel-card-badge badge-second-channel">Kanał Gamingowy: Długie Formaty &amp; VOD</span>
                            <h3 style="font-size: var(--font-size-2xl); font-weight: 700; margin-bottom: var(--space-3); color: var(--text-primary);">
                                Its Hexit IRL <span style="font-size: var(--font-size-lg); font-weight: 500; color: var(--text-muted);">(Minecraft &amp; VOD)</span>
                            </h3>
                            <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: var(--space-4);">
                                Survival w Minecraft, autorskie pluginy, nocne transmisje i pełne zapisy VOD:
                            </p>
                            <ul style="list-style: none; padding: 0; margin-bottom: var(--space-6);">
                                <li style="padding: 6px 0; color: var(--text-secondary); display: flex; align-items: center; gap: 8px;">
                                    <span style="color: #3b82f6;">▶</span> Survival z widzami, tworzenie pluginów i skryptów serwerowych
                                </li>
                                <li style="padding: 6px 0; color: var(--text-secondary); display: flex; align-items: center; gap: 8px;">
                                    <span style="color: #3b82f6;">▶</span> Wielogodzinne streamy nocne bez cięć i luźne rozmowy o devie
                                </li>
                                <li style="padding: 6px 0; color: var(--text-secondary); display: flex; align-items: center; gap: 8px;">
                                    <span style="color: #3b82f6;">▶</span> Kompletne archiwum VOD dla każdego, kto przegapił live
                                </li>
                            </ul>
                        </div>
                        <div>
                            <a href="https://www.youtube.com/@HexitIrl" target="_blank" rel="noopener" class="btn btn-secondary" style="width: 100%;">
                                Przejdź do Its Hexit IRL (@HexitIrl) ↗
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Discord -->
                <div class="content-card" style="margin-top: var(--space-12);">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-10); align-items: center;">
                        <div>
                            <span class="creator-tag" style="margin-bottom: var(--space-3); display: inline-block;">Serwer Discord</span>
                            <h3 style="font-size: var(--font-size-2xl); font-weight: 800; margin-bottom: var(--space-3); color: var(--text-primary);">
                                Dołącz do społeczności HEXIT RELY
                            </h3>
                            <p style="color: var(--text-secondary); line-height: 1.7; margin-bottom: var(--space-4);">
                                Wymiana feedbacku do kawałków, testy presetów, wspólne granie i powiadomienia o każdym live bez kaprysów algorytmów.
                            </p>
                            <a href="https://discord.gg/BbrtEFCeJb" target="_blank" rel="noopener" class="btn btn-primary">
                                Dołącz na Discord ↗
                            </a>
                        </div>
                        <div class="info-pill-box">
                            <h4 style="font-size: var(--font-size-base); font-weight: 700; color: var(--text-primary); margin-bottom: var(--space-2);">
                                📜 Kultura czatu:
                            </h4>
                            <p style="color: var(--text-secondary); font-size: var(--font-size-sm); line-height: 1.6; margin: 0;">
                                Szacunek do innych, merytoryczna dyskusja o muzyce i kodzie, brak toksyczności i spamowania. Wpadaj z dobrą energią!
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
"""

new_content = head_part + '\n' + main_content + '\n' + foot_part

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('about.html rebuilt successfully')
