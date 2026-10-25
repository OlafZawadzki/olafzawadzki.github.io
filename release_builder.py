#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HEXIT RELY — Generator & Edytor Wydań Muzycznych (Release Builder Studio)
Aplikacja z interfejsem graficznym do tworzenia i edytowania podstron wydań,
zarządzania plikami audio / bezpośrednimi linkami URL, dynamicznymi stemsami,
tapetami oraz aktualizacji katalogu wydań (wydania.html).
"""

import os
import sys
import json
import shutil
import re
import html
from pathlib import Path

# Ustalenie katalogu roboczego (root projektu)
PROJECT_ROOT = Path(__file__).resolve().parent

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False


def slugify(text: str) -> str:
    """Tworzy bezpieczny identyfikator URL ze stringa."""
    text = text.lower().strip()
    polish_chars = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'
    }
    for pl, en in polish_chars.items():
        text = text.replace(pl, en)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-') or 'wydanie'


def get_available_releases() -> list[dict]:
    """Zwraca listę wszystkich dostępnych wydań zapisanych w hexit/releases/."""
    releases_dir = PROJECT_ROOT / "hexit" / "releases"
    releases = []
    if not releases_dir.is_dir():
        return releases

    for folder in sorted(releases_dir.iterdir()):
        if folder.is_dir():
            data_file = folder / "release_data.json"
            if data_file.is_file():
                try:
                    data = json.loads(data_file.read_text(encoding="utf-8"))
                    releases.append({
                        "slug": folder.name,
                        "title": data.get("title", folder.name),
                        "data_file": data_file,
                        "data": data
                    })
                except Exception:
                    releases.append({
                        "slug": folder.name,
                        "title": folder.name,
                        "data_file": data_file,
                        "data": None
                    })
            else:
                # Sprawdź czy istnieje wydanie-<slug>.html
                html_file = PROJECT_ROOT / f"wydanie-{folder.name}.html"
                if html_file.is_file():
                    releases.append({
                        "slug": folder.name,
                        "title": folder.name.capitalize(),
                        "data_file": None,
                        "data": None
                    })
    return releases


def resolve_asset(val: str, slug: str, dest_folder: Path, fallback_rel: str) -> tuple[str, str, bool]:
    """
    Sprawdza czy wartość to:
    1. Zewnętrzny link URL (http/https)
    2. Plik lokalny do skopiowania
    3. Już istniejąca relatywna ścieżka w projekcie
    Zwraca: (sciezka_lub_url, nazwa_pliku, czy_to_url)
    """
    val = val.strip()
    if not val:
        return fallback_rel, Path(fallback_rel).name if fallback_rel else "", False

    if val.startswith(("http://", "https://")):
        filename = val.split("/")[-1].split("?")[0] or "download"
        return val, filename, True

    path_obj = Path(val)
    if path_obj.is_file():
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_file = dest_folder / path_obj.name
        # Jeśli plik nie jest już w miejscu docelowym, kopiujemy go
        if path_obj.resolve() != dest_file.resolve():
            shutil.copy2(path_obj, dest_file)
        rel_path = os.path.relpath(dest_file, PROJECT_ROOT).replace("\\", "/")
        return rel_path, dest_file.name, False

    # Jeśli podano istniejącą relatywną ścieżkę w projekcie
    proj_file = PROJECT_ROOT / val
    if proj_file.is_file():
        return val.replace("\\", "/"), proj_file.name, False

    return fallback_rel, Path(fallback_rel).name if fallback_rel else "", False


def generate_release(data: dict) -> tuple[bool, str]:
    """
    Główna funkcja generująca stronę wydania, kopiująca pliki / obsługująca linki,
    zapisująca release_data.json oraz aktualizująca wydania.html.
    """
    try:
        title = data.get("title", "").strip()
        if not title:
            return False, "Błąd: Tytuł wydania jest wymagany!"

        slug = data.get("slug", "").strip() or slugify(title)
        artist = data.get("artist", "Hexit Rely").strip() or "Hexit Rely"
        year = data.get("year", "2026").strip() or "2026"
        bpm = data.get("bpm", "128 BPM").strip() or "128 BPM"
        key = data.get("key", "C Minor").strip() or "C Minor"
        duration = data.get("duration", "3:30").strip() or "3:30"
        quality = data.get("quality", "48 kHz / 24-bit").strip() or "48 kHz / 24-bit"
        genre = data.get("genre", "Elektronika").strip() or "Elektronika"

        # Flaga opcjonalnego linku w bio
        enable_bio = bool(data.get("enable_bio", True))

        # Tagi / Badge
        badge_main = data.get("badge_main", "Nowy Singiel").strip()
        badge_stems = data.get("badge_stems", "Stems ZIP & Arty").strip()
        badge_meta1 = f"{bpm} • {key}"
        badge_meta2 = genre
        youtube_safe = bool(data.get("youtube_safe", True))
        badge_youtube = data.get("badge_youtube", "No Copyright Music").strip() or "No Copyright Music"

        # Tłumaczenia (EN)
        translations_en = data.get("translations_en", {})
        badge_main_en = translations_en.get("badge_main", "").strip() or "New Single"
        badge_youtube_en = translations_en.get("badge_youtube", "").strip() or "No Copyright Music"
        short_desc_en = translations_en.get("short_desc", "").strip()
        full_desc_1_en = translations_en.get("full_desc_1", "").strip()
        full_desc_2_en = translations_en.get("full_desc_2", "").strip()
        license_notice_en = translations_en.get("license_notice", "").strip()

        if youtube_safe:
            youtube_badge_release_html = f"""                            <span class="release-pill pill-youtube" title="Content ID Free • Dozwolone bezpłatnie w filmach na platformie YouTube">
                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.022.26-.01.104c-.048.519-.119 1.023-.22 1.402a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.04.018-.256.008-.105c.05-.572.124-1.141.235-1.558a2.007 2.007 0 0 1 1.415-1.42c.487-.132 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/></svg>
                                <span data-pl="{html.escape(badge_youtube)}" data-en="{html.escape(badge_youtube_en)}">{html.escape(badge_youtube)}</span>
                                <span class="pill-yt-tag">Free on YouTube</span>
                            </span>"""
            youtube_safe_box_html = f"""                            <!-- YouTube Content ID Free Callout Box -->
                            <div class="youtube-safe-box">
                                <div class="youtube-safe-icon" aria-hidden="true">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.022.26-.01.104c-.048.519-.119 1.023-.22 1.402a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.04.018-.256.008-.105c.05-.572.124-1.141.235-1.558a2.007 2.007 0 0 1 1.415-1.42c.487-.132 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/></svg>
                                </div>
                                <div class="youtube-safe-content">
                                    <span class="youtube-safe-title">
                                        <span class="lang-content-pl">Content ID Free &bull; Muzyka bez roszczeń (Tylko na YouTube)</span>
                                        <span class="lang-content-en" style="display:none;">Content ID Free &bull; Royalty-Free on YouTube</span>
                                    </span>
                                    <span style="color: var(--text-secondary);">
                                        <span class="lang-content-pl">Utwór jest w 100% bezpieczny od roszczeń praw autorskich dla twórców wideo — możesz bez obaw używać go jako darmowy podkład w swoich materiałach na platformie YouTube (wystarczy podać w opisie: <em>Muzyka: {html.escape(artist)} — {html.escape(title)}</em>).</span>
                                        <span class="lang-content-en" style="display:none;">This track is 100% free of Content ID claims for video creators — you can safely use it as free background music in your YouTube content (just credit in description: <em>Music: {html.escape(artist)} — {html.escape(title)}</em>).</span>
                                    </span>
                                </div>
                            </div>"""
            youtube_badge_card_html = f"""                                <span class="release-pill pill-youtube" title="Content ID Free • Darmowe na YouTube">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16"><path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.022.26-.01.104c-.048.519-.119 1.023-.22 1.402a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.04.018-.256.008-.105c.05-.572.124-1.141.235-1.558a2.007 2.007 0 0 1 1.415-1.42c.487-.132 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/></svg>
                                    <span data-pl="{html.escape(badge_youtube)}" data-en="{html.escape(badge_youtube_en)}">{html.escape(badge_youtube)}</span>
                                    <span class="pill-yt-tag">YouTube</span>
                                </span>"""
        else:
            youtube_badge_release_html = ""
            youtube_safe_box_html = ""
            youtube_badge_card_html = ""

        # Opisy
        short_desc = data.get("short_desc", "").strip() or f"Autorski singiel {title} w wykonaniu {artist}."
        full_desc_1 = data.get("full_desc_1", "").strip() or f"{title} to autorska kompozycja łącząca przestrzenne syntezatory z głębokim basem."
        full_desc_2 = data.get("full_desc_2", "").strip() or "Utwór wyprodukowany w Ableton Live Suite & FL Studio z użyciem hybrydowych łańcuchów efektowych."
        license_notice = data.get("license_notice", "").strip() or (
            f"Licencja Creative Commons (CC BY-NC 4.0): Masz pełne prawo do bezpłatnego pobierania, "
            f"cięcia sampli, tworzenia remiksów, grania w setach DJ-skich oraz wykorzystywania jako podkład "
            f"w swoich filmach na YouTube/Twitchu. Wystarczy podać w opisie: Muzyka: {artist} — {title}."
        )

        # Linki Streamingowe (Smartlink)
        link_spotify = data.get("link_spotify", "https://open.spotify.com/artist/4hcXADTFvPXtRxVTGYXW4I").strip()
        link_youtube = data.get("link_youtube", "https://www.youtube.com/channel/UCIpPTE3HsmUSAb-yfNybvSA").strip()
        link_apple = data.get("link_apple", "").strip() or link_spotify
        link_soundcloud = data.get("link_soundcloud", "").strip() or link_spotify
        link_tiktok = data.get("link_tiktok", "https://www.tiktok.com/@hexit_official").strip()

        # Foldery docelowe
        rel_folder = PROJECT_ROOT / "hexit" / "releases" / slug
        rel_folder.mkdir(parents=True, exist_ok=True)

        downloads_folder = PROJECT_ROOT / "hexit" / "downloads"
        downloads_folder.mkdir(parents=True, exist_ok=True)

        # 1. Audio Preview
        audio_input = data.get("audio_file", "")
        audio_rel_path, _, audio_is_url = resolve_asset(audio_input, slug, rel_folder, "Sounds/Harmony.mp3")

        # 2. Cover Art
        cover_input = data.get("cover_file", "")
        cover_rel_path, _, cover_is_url = resolve_asset(cover_input, slug, rel_folder, "hexit/harmony-cover.jpg")

        # 3. Paczka STEMS ZIP
        stems_zip_input = data.get("stems_zip_file", "")
        stems_zip_rel_path, stems_zip_filename, stems_zip_is_url = resolve_asset(
            stems_zip_input, slug, downloads_folder, ""
        )
        if not stems_zip_filename:
            stems_zip_filename = f"{artist}_{title}_Stems.zip".replace(" ", "_")

        # 4. Osobne Ścieżki STEMS (Dynamiczne - plik lub link URL)
        stems_individual = data.get("stems_individual", [])
        stems_html_items = []
        for idx, stem in enumerate(stems_individual, 1):
            s_name = stem.get("name", f"Ścieżka {idx}").strip() or f"Ścieżka {idx}"
            s_file_input = stem.get("file", "").strip()

            s_rel_path, s_filename, s_is_url = resolve_asset(
                s_file_input, slug, rel_folder, stems_zip_rel_path or audio_rel_path
            )
            if not s_filename:
                s_filename = f"{slug}_stem_{idx}.wav"

            if s_is_url:
                download_btn = f'<a href="{s_rel_path}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm" style="padding: 4px 12px; font-size: 0.75rem;">Pobierz ↗</a>'
            else:
                download_btn = f'<a href="{s_rel_path}" download="{s_filename}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm" style="padding: 4px 12px; font-size: 0.75rem;">Pobierz</a>'

            stems_html_items.append(f"""
                        <div class="stem-track-pill" style="justify-content: space-between;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M9 13c0 1.105-1.12 2-2.5 2S4 14.105 4 13s1.12-2 2.5-2 2.5.895 2.5 2z"/><path fill-rule="evenodd" d="M9 3v10H8V3h1z"/><path d="M8 2.82a1 1 0 0 1 .804-.98l3-.6A1 1 0 0 1 13 2.22V4L8 5V2.82z"/></svg>
                                <span>{html.escape(s_name)}</span>
                            </div>
                            {download_btn}
                        </div>""")

        stems_list_rendered = "\n".join(stems_html_items)

        # 5. Grafiki / Tapety (Dynamiczna lista materiałów)
        visual_assets_input = data.get("visual_assets", [])
        if not visual_assets_input:
            # Fallback dla starszych zapisów wydań
            visual_assets_input = []
            if cover_input or cover_rel_path:
                visual_assets_input.append({
                    "title": "Oficjalna Okładka Utworu",
                    "format": "Format 1:1",
                    "desc": "Oryginalny artwork singla w bezstratnej jakości.",
                    "file": cover_input or cover_rel_path
                })
            pc_wall_input = data.get("pc_wall_file", "")
            if pc_wall_input:
                visual_assets_input.append({
                    "title": "Tapeta na Pulpit Komputera",
                    "format": "Format 16:9",
                    "desc": "Szerokokątna grafika wysokiej rozdzielczości na monitor.",
                    "file": pc_wall_input
                })
            phone_wall_input = data.get("phone_wall_file", "")
            if phone_wall_input:
                visual_assets_input.append({
                    "title": "Tapeta na Smartfon (Ekran blokady)",
                    "format": "Format 9:16",
                    "desc": "Dedykowana tapeta pionowa na ekrany telefonów (iOS / Android).",
                    "file": phone_wall_input
                })

        visual_cards_html = []
        for idx, v in enumerate(visual_assets_input, 1):
            v_title = v.get("title", f"Grafika {idx}").strip() or f"Grafika {idx}"
            v_format = v.get("format", "Format 16:9").strip() or "Grafika"
            v_desc = v.get("desc", "").strip() or "Materiały graficzne wysokiej rozdzielczości do pobrania."
            v_file = v.get("file", "").strip()

            v_rel, v_filename, _ = resolve_asset(v_file, slug, rel_folder, cover_rel_path)
            if not v_filename:
                v_filename = f"{artist}_{title}_art_{idx}.png".replace(" ", "_")

            card = f"""                        <!-- Grafika / Tapeta: {html.escape(v_title)} -->
                        <div class="visual-asset-card">
                            <div class="visual-asset-preview-wrap" onclick="openLightbox('{v_rel}')" title="Kliknij, aby powiększyć podgląd">
                                <span class="visual-format-pill">{html.escape(v_format)}</span>
                                <img src="{v_rel}" alt="{html.escape(v_title)}" class="visual-asset-preview" loading="lazy">
                                <div class="visual-quick-zoom" aria-hidden="true" title="Powiększ">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"/><path d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"/><path d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"/></svg>
                                </div>
                            </div>
                            <div class="visual-asset-info">
                                <h4>{html.escape(v_title)}</h4>
                                <p>{html.escape(v_desc)}</p>
                                <div class="visual-asset-actions">
                                    <button type="button" class="btn btn-secondary btn-sm visual-zoom-btn" onclick="openLightbox('{v_rel}')">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"/><path d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"/><path d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z"/></svg>
                                        Powiększ
                                    </button>
                                    <a href="{v_rel}" download="{v_filename}" target="_blank" rel="noopener" class="btn btn-primary btn-sm visual-dl-btn">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>
                                        Pobierz &darr;
                                    </a>
                                </div>
                            </div>
                        </div>"""
            visual_cards_html.append(card)

        visuals_rendered = "\n".join(visual_cards_html)

        # 6. Przygotowanie kodu HTML
        release_filename = f"wydanie-{slug}.html"
        release_filepath = PROJECT_ROOT / release_filename

        # Przycisk pobrania ZIP stemsów (zawsze target="_blank")
        if stems_zip_rel_path:
            if stems_zip_is_url:
                stems_zip_btn_html = f'<a href="{stems_zip_rel_path}" target="_blank" rel="noopener" class="btn btn-primary btn-large" style="display: inline-flex; align-items: center; gap: 10px; flex-shrink: 0;"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>Pobierz Paczkę STEMS (.ZIP) ↗</a>'
            else:
                stems_zip_btn_html = f'<a href="{stems_zip_rel_path}" download="{stems_zip_filename}" target="_blank" rel="noopener" class="btn btn-primary btn-large" style="display: inline-flex; align-items: center; gap: 10px; flex-shrink: 0;"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>Pobierz Paczkę STEMS (.ZIP)</a>'
        else:
            stems_zip_btn_html = ""

        # Opcjonalne zakładki Bio / Smartlink
        tabs_html = ""
        bio_mode_section_html = ""
        js_bio_tab_setup = ""

        if enable_bio:
            tabs_html = """
            <div style="text-align: center; margin-bottom: var(--space-8);">
                <div class="view-mode-tabs" role="tablist">
                    <button type="button" class="view-mode-btn active" id="tabFullPage" role="tab" aria-selected="true">
                        Pełna Strona Wydania &amp; STEMS
                    </button>
                    <button type="button" class="view-mode-btn" id="tabBioMode" role="tab" aria-selected="false">
                        Widok Smartlink / Bio (Smartfony) ↗
                    </button>
                </div>
            </div>
"""
            bio_mode_section_html = f"""
            <!-- WIDOK: WERSJA SMARTLINK / BIO DLA WYDANIA -->
            <div id="bioModeView" style="display: none;">
                <div class="release-bio-container">
                    <div class="release-bio-card">
                        <img src="{cover_rel_path}" alt="{html.escape(title)} Cover" class="bio-track-cover">
                        <h2 style="font-size: var(--font-size-2xl); font-weight: 800; color: var(--text-primary); margin-bottom: 4px;">{html.escape(title)}</h2>
                        <span style="color: var(--primary-color); font-weight: 600; font-size: var(--font-size-sm); display: block; margin-bottom: var(--space-4);">
                            {html.escape(artist)} &bull; {html.escape(year)} &bull; {html.escape(bpm)}
                        </span>

                        <!-- Mini Player wewnątrz Bio -->
                        <div class="custom-audio-hub" style="margin: var(--space-4) 0; padding: 12px 16px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <button type="button" class="btn-play-release" id="bioPlayBtn" aria-label="Odtwórz {html.escape(title)}" data-audio-src="{audio_rel_path}" style="width: 40px; height: 40px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" id="bioPlayIcon">
                                        <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/>
                                    </svg>
                                </button>
                                <div class="release-progress-wrap">
                                    <div class="release-track-bar" id="bioTrackBar">
                                        <div class="release-track-fill" id="bioTrackFill"></div>
                                    </div>
                                    <div class="release-player-meta">
                                        <span id="bioCurrentTime">0:00</span>
                                        <span>Podgląd utworu</span>
                                        <span>{html.escape(duration)}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: var(--space-4);">
                            Wybierz swoją ulubioną platformę streamingową:
                        </p>

                        <!-- Przyciski Platform Streamingowych -->
                        <div class="bio-platform-links">
                            <a href="{link_spotify}" target="_blank" rel="noopener" class="bio-platform-btn">
                                <div class="bio-platform-left">
                                    <div class="bio-platform-icon"><img src="spotify.svg" alt="Spotify" style="width: 20px; height: 20px;"></div>
                                    <span>Spotify</span>
                                </div>
                                <span class="bio-action-tag">Odtwórz</span>
                            </a>
                            <a href="{link_youtube}" target="_blank" rel="noopener" class="bio-platform-btn">
                                <div class="bio-platform-left">
                                    <div class="bio-platform-icon"><img src="youtube.webp" alt="YouTube" style="width: 20px; height: 20px;"></div>
                                    <span>YouTube &amp; Music</span>
                                </div>
                                <span class="bio-action-tag">Oglądaj</span>
                            </a>
                            <a href="{link_apple}" target="_blank" rel="noopener" class="bio-platform-btn">
                                <div class="bio-platform-left">
                                    <div class="bio-platform-icon" style="color: #ff3b5c;">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M11.182.008C11.148-.03 9.923.023 8.857 1.18c-1.066 1.156-.902 2.482-.878 2.516.024.034 1.52.087 2.475-1.258.955-1.345.762-2.391.728-2.43zm3.314 11.733c-.048-.096-2.325-1.234-2.113-3.422.212-2.189 1.675-2.789 1.698-2.854.023-.065-.597-.79-1.254-1.157a3.692 3.692 0 0 0-1.563-.434c-.108-.003-.483-.095-1.254.116-.508.139-1.653.589-1.968.607-.315.018-1.256-.522-2.267-.665-.947-.133-1.872.247-2.428.875C1.88 5.348 1.48 6.64 1.48 8.08c0 3.298 2.089 6.262 3.636 6.326.77.032 1.257-.428 2.274-.428 1.018 0 1.34.428 2.27.428 1.536 0 3.328-2.33 3.328-2.33s-.492-.338-.492-.338z"/></svg>
                                    </div>
                                    <span>Apple Music</span>
                                </div>
                                <span class="bio-action-tag">Odsłuchaj</span>
                            </a>
                            <a href="{link_soundcloud}" target="_blank" rel="noopener" class="bio-platform-btn">
                                <div class="bio-platform-left">
                                    <div class="bio-platform-icon" style="color: #ff5500;">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M13.684 6.75a2.825 2.825 0 0 1 1.766 2.656C15.45 10.97 14.19 12 12.637 12H7.2V5.597c.504-.576 1.248-.947 2.08-.947.625 0 1.2.206 1.667.556.368-.262.82-.416 1.306-.416.48 0 .927.15 1.288.406.05.034.098.07.143.107v.447zM6.4 5.92v6.08H5.6V6.784a3.1 3.1 0 0 1 .8-.864zm-1.6 1.44v4.64h-.8V7.84a3.15 3.15 0 0 1 .8-.48zm-1.6.8v3.84h-.8V8.64a3.1 3.1 0 0 1 .8-.48zm-1.6.8v3.04H.8V9.32a3.1 3.1 0 0 1 .8-.36zm-1.6.8v2.24H0v-1.88a3.1 3.1 0 0 1 0-.36z"/></svg>
                                    </div>
                                    <span>SoundCloud</span>
                                </div>
                                <span class="bio-action-tag">Stream</span>
                            </a>
                            <a href="{link_tiktok}" target="_blank" rel="noopener" class="bio-platform-btn">
                                <div class="bio-platform-left">
                                    <div class="bio-platform-icon"><img src="tiktok.webp" alt="TikTok" style="width: 20px; height: 20px;"></div>
                                    <span>TikTok Audio</span>
                                </div>
                                <span class="bio-action-tag">Użyj</span>
                            </a>
                        </div>

                        <div style="margin-top: var(--space-6); padding-top: var(--space-4); border-top: 1px solid var(--border-color);">
                            <button type="button" class="btn btn-primary" id="btnSwitchToFull" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>
                                Pobierz STEMS &amp; Grafiki (Strona Wydania) &rarr;
                            </button>
                        </div>
                    </div>
                </div>
            </div>
"""
            js_bio_tab_setup = f"""
            const tabFullPage = document.getElementById('tabFullPage');
            const tabBioMode = document.getElementById('tabBioMode');
            const fullPageView = document.getElementById('fullPageView');
            const bioModeView = document.getElementById('bioModeView');
            const btnSwitchToFull = document.getElementById('btnSwitchToFull');
            const bioPlayBtn = document.getElementById('bioPlayBtn');
            const bioPlayIcon = document.getElementById('bioPlayIcon');
            const bioTrackBar = document.getElementById('bioTrackBar');
            const bioTrackFill = document.getElementById('bioTrackFill');
            const bioCurrentTime = document.getElementById('bioCurrentTime');

            const setViewMode = (mode) => {{
                if (mode === 'bio') {{
                    if (tabBioMode) {{ tabBioMode.classList.add('active'); tabBioMode.setAttribute('aria-selected', 'true'); }}
                    if (tabFullPage) {{ tabFullPage.classList.remove('active'); tabFullPage.setAttribute('aria-selected', 'false'); }}
                    if (fullPageView) fullPageView.style.display = 'none';
                    if (bioModeView) bioModeView.style.display = 'block';
                    history.replaceState(null, null, '#bio-mode');
                }} else {{
                    if (tabFullPage) {{ tabFullPage.classList.add('active'); tabFullPage.setAttribute('aria-selected', 'true'); }}
                    if (tabBioMode) {{ tabBioMode.classList.remove('active'); tabBioMode.setAttribute('aria-selected', 'false'); }}
                    if (fullPageView) fullPageView.style.display = 'block';
                    if (bioModeView) bioModeView.style.display = 'none';
                    if (window.location.hash === '#bio-mode') {{
                        history.replaceState(null, null, '{release_filename}');
                    }}
                }}
            }};

            if (tabFullPage) tabFullPage.addEventListener('click', () => setViewMode('full'));
            if (tabBioMode) tabBioMode.addEventListener('click', () => setViewMode('bio'));
            if (btnSwitchToFull) btnSwitchToFull.addEventListener('click', () => setViewMode('full'));

            if (window.location.hash === '#bio-mode') {{
                setViewMode('bio');
            }}

            if (bioPlayBtn) bioPlayBtn.addEventListener('click', togglePlay);
            if (bioTrackBar) bioTrackBar.addEventListener('click', (e) => handleSeek(e, bioTrackBar));
"""

        html_content = f"""<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- SEO Meta Tags -->
    <title>{html.escape(artist)} — {html.escape(title)} | Wydanie, Streaming, STEMS &amp; Grafiki</title>
    <meta name="description"
        content="Oficjalna strona wydania utworu '{html.escape(title)}' od {html.escape(artist)}. Odsłuchaj w streamingach, pobierz bezpłatnie wielościeżkowe STEMS oraz oficjalne grafiki.">
    <meta name="keywords" content="{html.escape(artist)}, {html.escape(title)}, utwór, singiel, stems, pobierz stemsy, tapety, okładka, remix, {html.escape(genre)}">
    <meta name="author" content="{html.escape(artist)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://hexitrely.pl/{release_filename}">

    <!-- Open Graph -->
    <meta property="og:type" content="music.song">
    <meta property="og:title" content="{html.escape(artist)} — {html.escape(title)}">
    <meta property="og:description" content="{html.escape(short_desc)}">
    <meta property="og:image" content="https://hexitrely.pl/{cover_rel_path}">
    <meta property="og:url" content="https://hexitrely.pl/{release_filename}">

    <!-- Stylesheets & Fonts -->
    <link rel="stylesheet" href="styles.css?v=20261024">
    <link rel="icon" type="image/ico" href="logohexit.ico">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        .view-mode-tabs {{
            display: inline-flex;
            background: rgba(18, 16, 14, 0.85);
            border: 1px solid var(--border-color);
            padding: 4px;
            border-radius: 999px;
            gap: 4px;
            margin-bottom: var(--space-8);
            backdrop-filter: blur(12px);
        }}
        .view-mode-btn {{
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-size: var(--font-size-sm);
            font-weight: 600;
            padding: 8px 18px;
            border-radius: 999px;
            cursor: pointer;
            transition: all 0.25s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        .view-mode-btn.active {{
            background: var(--gradient-primary);
            color: #12100e;
            box-shadow: 0 4px 14px rgba(74, 222, 158, 0.35);
        }}
        .release-bio-container {{
            max-width: 480px;
            margin: 0 auto;
            text-align: center;
            padding: var(--space-6) var(--space-4) var(--space-12);
        }}
        .release-bio-card {{
            background: linear-gradient(145deg, rgba(28, 25, 22, 0.95) 0%, rgba(18, 16, 14, 0.98) 100%);
            border: 1px solid rgba(74, 222, 158, 0.25);
            border-radius: 24px;
            padding: var(--space-8) var(--space-6);
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6), 0 0 30px rgba(74, 222, 158, 0.08);
            backdrop-filter: blur(16px);
        }}
        .bio-track-cover {{
            width: 180px;
            height: 180px;
            border-radius: 18px;
            object-fit: cover;
            margin: 0 auto 18px;
            display: block;
            border: 2px solid rgba(74, 222, 158, 0.4);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(74, 222, 158, 0.2);
            transition: transform 0.3s ease;
        }}
        .bio-platform-links {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: var(--space-6);
        }}
        .bio-platform-btn {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 18px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            color: var(--text-primary);
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 600;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .bio-platform-btn:hover {{
            transform: translateY(-2px);
            border-color: var(--primary-color);
            background: rgba(74, 222, 158, 0.08);
            color: var(--primary-color);
            box-shadow: 0 6px 18px rgba(74, 222, 158, 0.15);
        }}
        .bio-platform-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .bio-platform-icon {{
            width: 22px;
            height: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .bio-action-tag {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-muted);
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}
        .bio-platform-btn:hover .bio-action-tag {{
            background: var(--primary-color);
            color: #12100e;
        }}
        .custom-audio-hub {{
            background: rgba(18, 16, 14, 0.85);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 16px 20px;
            margin: var(--space-6) 0;
        }}
        .audio-wave-anim {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            height: 24px;
            margin-bottom: 8px;
        }}
        .wave-bar {{
            width: 3px;
            height: 6px;
            background: var(--primary-color);
            border-radius: 2px;
            transition: height 0.2s ease;
        }}
        .is-playing .wave-bar {{
            animation: waveBounce 1.2s ease-in-out infinite alternate;
        }}
        .is-playing .wave-bar:nth-child(2) {{ animation-delay: 0.15s; }}
        .is-playing .wave-bar:nth-child(3) {{ animation-delay: 0.3s; }}
        .is-playing .wave-bar:nth-child(4) {{ animation-delay: 0.45s; }}
        .is-playing .wave-bar:nth-child(5) {{ animation-delay: 0.2s; }}
        .is-playing .wave-bar:nth-child(6) {{ animation-delay: 0.35s; }}
        @keyframes waveBounce {{
            0% {{ height: 4px; }}
            50% {{ height: 22px; }}
            100% {{ height: 8px; }}
        }}
        .image-lightbox {{
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.92);
            z-index: 9999;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .image-lightbox.active {{
            display: flex;
        }}
        .lightbox-img {{
            max-width: 90vw;
            max-height: 85vh;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .lightbox-close {{
            position: absolute;
            top: 24px;
            right: 24px;
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            font-size: 1.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s ease;
        }}
        .lightbox-close:hover {{
            background: var(--primary-color);
            color: #000;
        }}
    </style>
</head>

<body>
    <!-- Header & Nawigacja -->
    <header class="modern-header">
        <nav class="nav-container" aria-label="Główna nawigacja">
            <a href="index.html" class="nav-brand">
                <img src="logohexit.webp" alt="Hexit Rely Logo" class="logo">
                <span class="brand-title">HEXIT <span class="brand-accent">RELY</span></span>
            </a>

            <ul class="nav-menu" id="navMenu">
                <li><a href="index.html">Start</a></li>
                <li><a href="about.html">O mnie</a></li>
                <li><a href="wydania.html" class="active">Wydania</a></li>
                <li><a href="index.html#projekty">Projekty</a></li>
                <li><a href="index.html#kontakt">Kontakt</a></li>
                <li class="nav-dropdown">
                    <button type="button" class="nav-dropdown-toggle" aria-haspopup="true" aria-expanded="false">
                        Portfolio ↗ <span class="dropdown-arrow">▼</span>
                    </button>
                    <ul class="nav-dropdown-menu">
                        <li>
                            <a href="https://noxaudios.github.io/portfolio.html" target="_blank" rel="noopener">
                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16" style="vertical-align: -2px; margin-right: 6px;"><path d="M1.5 4A1.5 1.5 0 0 0 0 5.5v5A1.5 1.5 0 0 0 1.5 12h13a1.5 1.5 0 0 0 1.5-1.5v-5A1.5 1.5 0 0 0 14.5 4h-13zM6 8.5H4.5V10h-1V8.5H2v-1h1.5V6h1v1.5H6v1zM10.5 7a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm2.5 2.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/></svg>Game Dev
                            </a>
                        </li>
                        <li>
                            <a href="https://noxaudios.github.io/portfolio-muzyczne.html" target="_blank" rel="noopener">
                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16" style="vertical-align: -2px; margin-right: 6px;"><path d="M9 13c0 1.105-1.12 2-2.5 2S4 14.105 4 13s1.12-2 2.5-2 2.5.895 2.5 2z"/><path fill-rule="evenodd" d="M9 3v10H8V3h1z"/><path d="M8 2.82a1 1 0 0 1 .804-.98l3-.6A1 1 0 0 1 13 2.22V4L8 5V2.82z"/></svg>Muzyka
                            </a>
                        </li>
                    </ul>
                </li>
            </ul>

            <div class="nav-actions">
                <div class="lang-switch" role="group" aria-label="Wybór języka / Language selection">
                    <button class="lang-btn active" data-lang="pl" type="button" aria-pressed="true">PL</button>
                    <span class="lang-sep">/</span>
                    <button class="lang-btn" data-lang="en" type="button" aria-pressed="false">EN</button>
                </div>
                <div class="nav-socials">
                    <a href="https://www.youtube.com/channel/UCIpPTE3HsmUSAb-yfNybvSA" target="_blank" rel="noopener" class="social-link" title="YouTube">
                        <img src="youtube.webp" alt="YouTube" class="social-icon">
                    </a>
                    <a href="https://open.spotify.com/artist/4hcXADTFvPXtRxVTGYXW4I" target="_blank" rel="noopener" class="social-link" title="Spotify">
                        <img src="spotify.svg" alt="Spotify" class="social-icon">
                    </a>
                    <a href="https://www.tiktok.com/@hexit_official" target="_blank" rel="noopener" class="social-link" title="TikTok">
                        <img src="tiktok.webp" alt="TikTok" class="social-icon">
                    </a>
                    <a href="https://www.instagram.com/hexit_official" target="_blank" rel="noopener" class="social-link" title="Instagram">
                        <img src="instagram.webp" alt="Instagram" class="social-icon">
                    </a>
                </div>

                <button class="nav-toggle" id="navToggle" aria-label="Otwórz menu nawigacji">
                    <span></span><span></span><span></span>
                </button>
            </div>
        </nav>
    </header>
    <div class="nav-overlay" id="navOverlay"></div>

    <main style="padding-top: 100px; padding-bottom: var(--space-20);">
        <div class="container">
            <!-- Okruszki chleba -->
            <div style="display: flex; gap: 8px; align-items: center; margin-bottom: var(--space-6);">
                <a href="wydania.html" style="color: var(--text-muted); text-decoration: none; font-size: var(--font-size-sm);">&larr; Wszystkie Wydania &amp; STEMS</a>
                <span style="color: var(--border-color);">&bull;</span>
                <span style="color: var(--primary-color); font-size: var(--font-size-sm); font-weight: 600;">{html.escape(title)}</span>
            </div>

{tabs_html}

            <!-- WIDOK: PEŁNA STRONA WYDANIA -->
            <div id="fullPageView">
                <div class="release-hero-grid" style="display: grid; grid-template-columns: minmax(280px, 420px) 1fr; gap: var(--space-12); align-items: start; margin-bottom: var(--space-16);">
                    <!-- Lewa Kolumna: Okładka i Specyfikacja Techniczna -->
                    <div>
                        <div class="release-cover-frame" style="position: relative; border-radius: 20px; overflow: hidden; border: 1px solid rgba(74, 222, 158, 0.3); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6); aspect-ratio: 1/1; background: #0a0908;">
                            <img src="{cover_rel_path}" alt="Okładka {html.escape(title)}" style="width: 100%; height: 100%; object-fit: cover; display: block;" id="mainCoverImg">
                            <button type="button" class="zoom-cover-btn" id="btnZoomCover" aria-label="Powiększ okładkę" style="position: absolute; bottom: 12px; right: 12px; background: rgba(0,0,0,0.7); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 6px 12px; color: #fff; font-size: 0.75rem; cursor: pointer; backdrop-filter: blur(8px);">
                                Powiększ &oplus;
                            </button>
                        </div>

                        <!-- Parametry techniczne utworu -->
                        <div class="track-specs-card" style="margin-top: var(--space-6); background: rgba(18, 16, 14, 0.7); border: 1px solid var(--border-color); border-radius: 16px; padding: var(--space-4) var(--space-6);">
                            <h4 style="font-size: var(--font-size-xs); color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">Metadane Studyjne</h4>
                            <div class="spec-item">
                                <span class="spec-label">Tempo</span>
                                <span class="spec-val">{html.escape(bpm)}</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Tonacja</span>
                                <span class="spec-val">{html.escape(key)}</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Długość</span>
                                <span class="spec-val">{html.escape(duration)}</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Jakość Mastera</span>
                                <span class="spec-val">{html.escape(quality)}</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Gatunek</span>
                                <span class="spec-val">{html.escape(genre)}</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Producent</span>
                                <span class="spec-val">{html.escape(artist)}</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Format STEMS</span>
                                <span class="spec-val">WAV / MP3</span>
                            </div>
                        </div>
                    </div>

                    <!-- Prawa Kolumna: Tytuł, Odtwarzacz, Opis i Linki -->
                    <div>
                        <div class="release-badge-row" style="margin-bottom: var(--space-3); display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
                            <span class="release-pill pill-primary" data-pl="{html.escape(badge_main)}" data-en="{html.escape(badge_main_en)}">{html.escape(badge_main)}</span>
                            <span class="release-pill pill-stems">{html.escape(badge_stems)}</span>
{youtube_badge_release_html}
                            <span class="release-pill pill-meta">{html.escape(badge_meta1)}</span>
                            <span class="release-pill pill-meta">{html.escape(badge_meta2)}</span>
                        </div>

                        <h1 class="hero-title" style="font-size: var(--font-size-4xl); margin-bottom: 4px;">{html.escape(title)}</h1>
                        <span style="font-size: var(--font-size-lg); color: var(--primary-color); font-weight: 700; display: block; margin-bottom: var(--space-4);">
                            {html.escape(artist)} &bull; {html.escape(year)}
                        </span>

                        <!-- Główny Zaawansowany Audio Player Utworu -->
                        <div class="custom-audio-hub" id="mainAudioPlayerCard">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <div>
                                    <strong style="color: var(--text-primary); font-size: var(--font-size-sm); display: block;">{html.escape(title)} &bull; Pełny Odsłuch Audio</strong>
                                    <span style="color: var(--text-muted); font-size: var(--font-size-xs);">Plik preview w wysokiej jakości</span>
                                </div>
                                <div class="audio-wave-anim" id="waveVisualizer">
                                    <div class="wave-bar"></div><div class="wave-bar"></div><div class="wave-bar"></div>
                                    <div class="wave-bar"></div><div class="wave-bar"></div><div class="wave-bar"></div>
                                </div>
                            </div>

                            <div style="display: flex; align-items: center; gap: 16px;">
                                <button type="button" class="btn-play-release" id="pagePlayBtn" aria-label="Odtwórz lub wstrzymaj {html.escape(title)}" data-audio-src="{audio_rel_path}">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16" id="pagePlayIcon">
                                        <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/>
                                    </svg>
                                </button>
                                <div class="release-progress-wrap">
                                    <div class="release-track-bar" id="pageTrackBar">
                                        <div class="release-track-fill" id="pageTrackFill"></div>
                                    </div>
                                    <div class="release-player-meta">
                                        <span id="pageCurrentTime">0:00</span>
                                        <span>{html.escape(key)} &bull; {html.escape(bpm)}</span>
                                        <span id="pageTotalDuration">{html.escape(duration)}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Opis Utworu & Zamysł -->
                        <div style="margin: var(--space-6) 0;">
                            <h3 style="font-size: var(--font-size-lg); font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">
                                <span class="lang-content-pl">O utworze &amp; Procesie Produkcji</span>
                                <span class="lang-content-en" style="display:none;">About the Track &amp; Production Process</span>
                            </h3>
                            <div class="lang-content-pl">
                                <p style="color: var(--text-secondary); line-height: 1.7; font-size: var(--font-size-base); margin-bottom: 12px; white-space: pre-line;">
                                    {html.escape(full_desc_1)}
                                </p>
                                <p style="color: var(--text-secondary); line-height: 1.7; font-size: var(--font-size-base); margin-bottom: var(--space-4); white-space: pre-line;">
                                    {html.escape(full_desc_2)}
                                </p>
                            </div>
                            <div class="lang-content-en" style="display:none;">
                                <p style="color: var(--text-secondary); line-height: 1.7; font-size: var(--font-size-base); margin-bottom: 12px; white-space: pre-line;">
                                    {html.escape(full_desc_1_en or full_desc_1)}
                                </p>
                                <p style="color: var(--text-secondary); line-height: 1.7; font-size: var(--font-size-base); margin-bottom: var(--space-4); white-space: pre-line;">
                                    {html.escape(full_desc_2_en or full_desc_2)}
                                </p>
                            </div>
{youtube_safe_box_html}
                        </div>

                        <!-- Szybkie Skróty do Sekcji -->
                        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                            <a href="#stems-sekcja" class="btn btn-primary" style="display: inline-flex; align-items: center; gap: 8px;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>
                                Pobierz STEMS &darr;
                            </a>
                            <a href="#grafiki-sekcja" class="btn btn-secondary" style="display: inline-flex; align-items: center; gap: 8px;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/><path d="M2.002 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2h-12zm12 1a1 1 0 0 1 1 1v6.5l-3.777-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12V3a1 1 0 0 1 1-1h12z"/></svg>
                                Grafiki &amp; Tapety &darr;
                            </a>
                        </div>
                    </div>
                </div>

                <!-- SEKCJA: POBIERZ STEMS & MATERIAŁY AUDIO DLA TWÓRCÓW -->
                <div class="stems-package-card" id="stems-sekcja">
                    <div class="stems-package-header">
                        <div>
                            <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                                <span class="release-pill pill-stems">Multitrack</span>
                                <span class="release-pill pill-meta">Stems Paczka</span>
                            </div>
                            <h2 class="stems-package-title">Pobierz STEMS (Do Remiksów)</h2>
                            <p style="color: var(--text-secondary); margin: 0; font-size: var(--font-size-sm);">
                                Pobierz kompletną paczkę wielościeżkową lub pobieraj pojedyncze ścieżki osobno poniżej:
                            </p>
                        </div>
                        {stems_zip_btn_html}
                    </div>

                    <!-- Lista ścieżek zawartych w paczce -->
                    <div style="margin-bottom: 8px;">
                        <span style="font-size: var(--font-size-xs); color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700;">
                            Pobierz pojedyncze ścieżki osobno (WAV / MP3):
                        </span>
                    </div>
                    <div class="stems-items-list">
{stems_list_rendered}
                    </div>

                    <div class="stems-license-notice">
                        <div class="lang-content-pl">{html.escape(license_notice)}</div>
                        <div class="lang-content-en" style="display:none;">{html.escape(license_notice_en or license_notice)}</div>
                    </div>
                </div>

                <!-- SEKCJA: GRAFIKI, ARTY & TAPETY (DO POBRANIA) -->
                <div style="margin-bottom: var(--space-16);" id="grafiki-sekcja">
                    <div class="section-header-wrap" style="text-align: left; margin-bottom: var(--space-6);">
                        <span class="section-eyebrow">Visual Assets &bull; Grafiki &amp; Tapety</span>
                        <h2 class="section-title">Oficjalne Arty i Tapety do Pobrania</h2>
                        <p class="section-desc" style="margin-left: 0;">
                            Pobierz oficjalne materiały wizualne w pełnej rozdzielczości: okładkę albumu, tapetę na komputer oraz grafikę pionową na ekran blokady smartfona.
                        </p>
                    </div>

                    <div class="visuals-download-grid">
{visuals_rendered}
                    </div>
                </div>
            </div>

{bio_mode_section_html}
        </div>
    </main>

    <!-- Lightbox Modal -->
    <div class="image-lightbox" id="imageLightbox">
        <button type="button" class="lightbox-close" id="lightboxClose" aria-label="Zamknij podgląd">&times;</button>
        <img src="" alt="Podgląd grafiki" class="lightbox-img" id="lightboxImg">
    </div>

    <!-- Footer -->
    <footer class="modern-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 {html.escape(artist)}. Wszelkie prawa zastrzeżone.</p>
                <div class="footer-links">
                    <a href="wydania.html">Wszystkie Wydania</a>
                    <a href="bio.html">Oficjalne Bio Linki</a>
                    <a href="polityka.html">Polityka Prywatności</a>
                    <a href="index.html#kontakt">Kontakt</a>
                </div>
            </div>
        </div>
    </footer>

    <!-- Wspólny element Audio -->
    <audio id="releaseAudioElement" src="{audio_rel_path}" preload="metadata"></audio>

    <script src="scripts.js?v=20261024"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {{
            const audio = document.getElementById('releaseAudioElement');
            const pagePlayBtn = document.getElementById('pagePlayBtn');
            const pagePlayIcon = document.getElementById('pagePlayIcon');
            const pageTrackBar = document.getElementById('pageTrackBar');
            const pageTrackFill = document.getElementById('pageTrackFill');
            const pageCurrentTime = document.getElementById('pageCurrentTime');
            const pageTotalDuration = document.getElementById('pageTotalDuration');
            const waveVisualizer = document.getElementById('waveVisualizer');

            const playSvg = '<path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/>';
            const pauseSvg = '<path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/>';

            const formatTime = (seconds) => {{
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${{mins}}:${{secs < 10 ? '0' : ''}}${{secs}}`;
            }};

            const togglePlay = () => {{
                if (audio.paused) {{
                    audio.play().then(() => {{
                        updatePlayIcons(true);
                        if (waveVisualizer) waveVisualizer.classList.add('is-playing');
                    }}).catch(err => console.log('Audio error:', err));
                }} else {{
                    audio.pause();
                    updatePlayIcons(false);
                    if (waveVisualizer) waveVisualizer.classList.remove('is-playing');
                }}
            }};

            const updatePlayIcons = (isPlaying) => {{
                const icon = isPlaying ? pauseSvg : playSvg;
                if (pagePlayIcon) pagePlayIcon.innerHTML = icon;
                const bIcon = document.getElementById('bioPlayIcon');
                if (bIcon) bIcon.innerHTML = icon;
            }};

            if (pagePlayBtn) pagePlayBtn.addEventListener('click', togglePlay);

            audio.addEventListener('timeupdate', () => {{
                if (!audio.duration) return;
                const pct = (audio.currentTime / audio.duration) * 100;
                const formatted = formatTime(audio.currentTime);
                if (pageTrackFill) pageTrackFill.style.width = pct + '%';
                const bFill = document.getElementById('bioTrackFill');
                if (bFill) bFill.style.width = pct + '%';
                if (pageCurrentTime) pageCurrentTime.textContent = formatted;
                const bCurrent = document.getElementById('bioCurrentTime');
                if (bCurrent) bCurrent.textContent = formatted;
            }});

            audio.addEventListener('loadedmetadata', () => {{
                if (pageTotalDuration && audio.duration) {{
                    pageTotalDuration.textContent = formatTime(audio.duration);
                }}
            }});

            audio.addEventListener('ended', () => {{
                updatePlayIcons(false);
                if (waveVisualizer) waveVisualizer.classList.remove('is-playing');
                if (pageTrackFill) pageTrackFill.style.width = '0%';
                const bFill = document.getElementById('bioTrackFill');
                if (bFill) bFill.style.width = '0%';
            }});

            const handleSeek = (e, bar) => {{
                if (!audio.duration) return;
                const rect = bar.getBoundingClientRect();
                const pos = (e.clientX - rect.left) / rect.width;
                audio.currentTime = pos * audio.duration;
            }};

            if (pageTrackBar) pageTrackBar.addEventListener('click', (e) => handleSeek(e, pageTrackBar));

{js_bio_tab_setup}

            const lightbox = document.getElementById('imageLightbox');
            const lightboxImg = document.getElementById('lightboxImg');
            const lightboxClose = document.getElementById('lightboxClose');

            window.openLightbox = (src) => {{
                if (lightbox && lightboxImg) {{
                    lightboxImg.src = src;
                    lightbox.classList.add('active');
                }}
            }};

            if (lightboxClose) {{
                lightboxClose.addEventListener('click', () => lightbox.classList.remove('active'));
            }}
            if (lightbox) {{
                lightbox.addEventListener('click', (e) => {{
                    if (e.target === lightbox) lightbox.classList.remove('active');
                }});
            }}

            const btnZoomCover = document.getElementById('btnZoomCover');
            if (btnZoomCover) {{
                btnZoomCover.addEventListener('click', () => openLightbox('{cover_rel_path}'));
            }}
        }});
    </script>
</body>
</html>
"""
        release_filepath.write_text(html_content, encoding="utf-8")

        # 7. Zapis danych wydania do JSON (umożliwia późniejszą edycję!)
        data_to_save = dict(data)
        data_to_save["slug"] = slug
        data_to_save["enable_bio"] = enable_bio
        data_to_save["youtube_safe"] = youtube_safe
        data_to_save["badge_youtube"] = badge_youtube
        data_to_save["visual_assets"] = visual_assets_input
        data_to_save["translations_en"] = translations_en
        data_file = rel_folder / "release_data.json"
        data_file.write_text(json.dumps(data_to_save, ensure_ascii=False, indent=2), encoding="utf-8")

        # 8. Dodanie / Aktualizacja wydania w wydania.html
        wydania_path = PROJECT_ROOT / "wydania.html"
        if wydania_path.is_file():
            wydania_content = wydania_path.read_text(encoding="utf-8")

            # Przyciski akcji na kafelku
            if enable_bio:
                actions_html = f"""                                <a href="{release_filename}" class="btn btn-primary btn-sm" style="flex: 1; text-align: center;">
                                    <span data-pl="Strona Wydania &rarr;" data-en="Release Page &rarr;">Strona Wydania &rarr;</span>
                                </a>
                                <a href="{release_filename}#bio-mode" class="btn btn-secondary btn-sm" title="Widok Smartlink / Bio">
                                    Smartlink ↗
                                </a>"""
            else:
                actions_html = f"""                                <a href="{release_filename}" class="btn btn-primary btn-sm" style="width: 100%; text-align: center;">
                                    <span data-pl="Strona Wydania &rarr;" data-en="Release Page &rarr;">Strona Wydania &rarr;</span>
                                </a>"""

            new_card_html = f"""                    <!-- Wydanie Muzyczne: {html.escape(title)} -->
                    <div class="content-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;" data-release-slug="{slug}">
                        <div style="position: relative; overflow: hidden; aspect-ratio: 1/1; background: #0a0908;">
                            <a href="{release_filename}">
                                <img src="{cover_rel_path}" alt="{html.escape(title)} - {html.escape(artist)}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            </a>
                            <div style="position: absolute; top: 14px; left: 14px; display: flex; gap: 6px; flex-wrap: wrap;">
                                <span class="release-pill pill-primary" data-pl="{html.escape(badge_main)}" data-en="{html.escape(badge_main_en)}">{html.escape(badge_main)}</span>
                                <span class="release-pill pill-stems">{html.escape(badge_stems)}</span>
{youtube_badge_card_html}
                            </div>
                        </div>
                        <div style="padding: var(--space-6); display: flex; flex-direction: column; flex: 1;">
                            <span style="font-size: var(--font-size-xs); color: var(--primary-color); font-weight: 600; text-transform: uppercase; margin-bottom: 4px;">{html.escape(genre)} &bull; {html.escape(bpm)} &bull; {html.escape(key)} &bull; {html.escape(year)}</span>
                            <h3 style="font-size: var(--font-size-xl); font-weight: 800; color: var(--text-primary); margin-bottom: 8px;">
                                <a href="{release_filename}" style="color: inherit; text-decoration: none;">{html.escape(title)}</a>
                            </h3>
                            <p style="font-size: var(--font-size-sm); color: var(--text-secondary); line-height: 1.6; margin-bottom: var(--space-6);">
                                <span class="lang-content-pl">{html.escape(short_desc)}</span>
                                <span class="lang-content-en" style="display:none;">{html.escape(short_desc_en or short_desc)}</span>
                            </p>
                            <div style="margin-top: auto; display: flex; gap: 10px;">
{actions_html}
                            </div>
                        </div>
                    </div>"""

            target_grid_start = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: var(--space-8);">'

            # Jeśli karta z tym release_filename już istnieje w wydania.html, podmień ją (edycja!)
            # Szukamy bloku karty zawierającego release_filename
            card_pattern = re.compile(
                r'<!--\s*Wydanie Muzyczne:[^\n]*-->\s*<div class="content-card"[^>]*>[\s\S]*?' +
                re.escape(release_filename) +
                r'[\s\S]*?</div>\s*</div>\s*</div>\s*',
                re.IGNORECASE
            )

            if card_pattern.search(wydania_content):
                wydania_content = card_pattern.sub(new_card_html + "\n\n", wydania_content, count=1)
            elif target_grid_start in wydania_content:
                wydania_content = wydania_content.replace(
                    target_grid_start,
                    target_grid_start + "\n" + new_card_html,
                    1
                )

            # Jeśli to wydanie jest również w sekcji wyróżnionej (featured-release-card)
            if f'href="{release_filename}"' in wydania_content and 'featured-release-card' in wydania_content:
                feat_cover_pattern = re.compile(
                    r'(<div class="featured-release-card"[\s\S]*?<a href="' + re.escape(release_filename) + r'"[^>]*>\s*<img src=")[^"]+(")',
                    re.IGNORECASE
                )
                wydania_content = feat_cover_pattern.sub(r'\g<1>' + cover_rel_path + r'\2', wydania_content)

                feat_audio_pattern = re.compile(
                    r'(id="releasePlayBtn"[^>]*data-audio-src=")[^"]+(")',
                    re.IGNORECASE
                )
                wydania_content = feat_audio_pattern.sub(r'\g<1>' + audio_rel_path + r'\2', wydania_content)

            wydania_path.write_text(wydania_content, encoding="utf-8")

        return True, f"Sukces! Wydanie '{title}' zostało pomyślnie zapisane:\n- Plik podstrony: {release_filename}\n- Folder aktywów: hexit/releases/{slug}/\n- Zaktualizowano katalog: wydania.html\n- Zapisano dane edycji: release_data.json"

    except Exception as e:
        return False, f"Wystąpił błąd podczas generowania: {str(e)}"


# ==============================================================================
# INTERFEJS GRAFICZNY (TKINTER GUI)
# ==============================================================================

class ReleaseBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hexit Rely — Release Builder Studio")
        self.root.geometry("940x900")
        self.root.minsize(760, 700)

        # Ciemny motyw w kolorystyce Hexit Rely
        self.bg_dark = "#12100e"
        self.bg_card = "#1c1916"
        self.bg_input = "#25211c"
        self.border_col = "#3d3830"
        self.accent_green = "#4ade9e"
        self.text_primary = "#f5f0eb"
        self.text_muted = "#a89f91"
        self.btn_danger = "#dc2626"

        self.root.configure(bg=self.bg_dark)

        # Pola formularza
        self.fields = {
            "title": tk.StringVar(value=""),
            "slug": tk.StringVar(value=""),
            "artist": tk.StringVar(value="Hexit Rely"),
            "year": tk.StringVar(value="2026"),
            "bpm": tk.StringVar(value="128 BPM"),
            "key": tk.StringVar(value="C Minor"),
            "duration": tk.StringVar(value="3:30"),
            "quality": tk.StringVar(value="48 kHz / 24-bit"),
            "genre": tk.StringVar(value="Elektronika / Wave"),
            # Tagi
            "badge_main": tk.StringVar(value="Nowy Singiel"),
            "badge_stems": tk.StringVar(value="Stems ZIP & Arty"),
            "badge_youtube": tk.StringVar(value="No Copyright Music"),
            # Tłumaczenia EN
            "badge_main_en": tk.StringVar(value="New Single"),
            "badge_youtube_en": tk.StringVar(value="No Copyright Music"),
            # Pliki / Linki
            "audio_file": tk.StringVar(value=""),
            "cover_file": tk.StringVar(value=""),
            "stems_zip_file": tk.StringVar(value=""),
            "pc_wall_file": tk.StringVar(value=""),
            "phone_wall_file": tk.StringVar(value=""),
            # Linki Smartlink
            "link_spotify": tk.StringVar(value="https://open.spotify.com/artist/4hcXADTFvPXtRxVTGYXW4I"),
            "link_youtube": tk.StringVar(value="https://www.youtube.com/channel/UCIpPTE3HsmUSAb-yfNybvSA"),
            "link_apple": tk.StringVar(value=""),
            "link_soundcloud": tk.StringVar(value=""),
            "link_tiktok": tk.StringVar(value="https://www.tiktok.com/@hexit_official"),
        }

        # Czy włączyć Smartlink / Link in Bio
        self.enable_bio_var = tk.BooleanVar(value=True)
        # Czy utwór jest wolny od praw (No Copyright / Content ID Free na YouTube)
        self.youtube_safe_var = tk.BooleanVar(value=True)

        # Dynamiczna lista pojedynczych ścieżek stems
        self.individual_stems = [
            {"name": tk.StringVar(value="1. Drums & Kicks"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="2. Sub Bass & 808"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="3. Lead Synths & Arps"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="4. Ambient Pads & Textures"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="5. Risers, Impacts & FX"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="6. Master Preview MP3"), "file": tk.StringVar(value="")},
        ]

        # Dynamiczna lista grafik, artów i tapet (domyślnie 3 podstawowe)
        self.visual_assets = [
            {
                "title": tk.StringVar(value="Oficjalna Okładka Utworu"),
                "format": tk.StringVar(value="Format 1:1"),
                "desc": tk.StringVar(value="Oryginalny artwork singla w bezstratnej jakości."),
                "file": tk.StringVar(value=""),
            },
            {
                "title": tk.StringVar(value="Tapeta na Pulpit Komputera"),
                "format": tk.StringVar(value="Format 16:9"),
                "desc": tk.StringVar(value="Szerokokątna grafika wysokiej rozdzielczości na monitor."),
                "file": tk.StringVar(value=""),
            },
            {
                "title": tk.StringVar(value="Tapeta na Smartfon (Ekran blokady)"),
                "format": tk.StringVar(value="Format 9:16"),
                "desc": tk.StringVar(value="Dedykowana tapeta pionowa na ekrany telefonów (iOS / Android)."),
                "file": tk.StringVar(value=""),
            },
        ]

        # Stan edycji
        self.current_editing_slug = None
        self.available_releases = []

        self.setup_ui()
        self.refresh_release_selector()

    def setup_ui(self):
        # 1. Górny pasek z nagłówkiem oraz selektorem edycji
        header_frame = tk.Frame(self.root, bg=self.bg_card, padx=20, pady=12, highlightthickness=1, highlightbackground=self.border_col)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        top_row = tk.Frame(header_frame, bg=self.bg_card)
        top_row.pack(fill=tk.X)

        title_lbl = tk.Label(top_row, text="HEXIT RELY — RELEASE BUILDER & EDITOR", font=("Inter", 13, "bold"), fg=self.accent_green, bg=self.bg_card)
        title_lbl.pack(side=tk.LEFT)

        # Selektor istniejacych wydan do edycji
        selector_frame = tk.Frame(top_row, bg=self.bg_card)
        selector_frame.pack(side=tk.RIGHT)

        tk.Label(selector_frame, text="Tryb / Edycja:", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_card).pack(side=tk.LEFT, padx=(0, 6))

        self.release_combo = ttk.Combobox(selector_frame, state="readonly", width=26, font=("Inter", 9))
        self.release_combo.pack(side=tk.LEFT, padx=(0, 6))

        btn_load = tk.Button(
            selector_frame, text="📂 Załaduj", font=("Inter", 8, "bold"),
            bg=self.border_col, fg=self.text_primary, relief=tk.FLAT, padx=10, pady=3,
            cursor="hand2", command=self.on_load_selected_release
        )
        btn_load.pack(side=tk.LEFT, padx=(0, 4))

        btn_new = tk.Button(
            selector_frame, text="+ Nowe", font=("Inter", 8, "bold"),
            bg=self.bg_input, fg=self.accent_green, relief=tk.FLAT, padx=10, pady=3,
            cursor="hand2", command=self.reset_to_new_release
        )
        btn_new.pack(side=tk.LEFT)

        sub_lbl = tk.Label(header_frame, text="Twórz nowe wydania lub ładuj i edytuj istniejące. Zarządzaj stemsami (dodawaj/usuwaj, plik lokalny lub link URL).", font=("Inter", 8), fg=self.text_muted, bg=self.bg_card)
        sub_lbl.pack(anchor=tk.W, pady=(4, 0))

        # 2. Dolny pasek akcji
        bottom_bar = tk.Frame(self.root, bg=self.bg_card, padx=20, pady=12, highlightthickness=1, highlightbackground=self.border_col)
        bottom_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.btn_generate = tk.Button(
            bottom_bar,
            text="🚀 WYGENERUJ WYDANIE I DODAJ DO STRONY",
            font=("Inter", 11, "bold"),
            bg=self.accent_green,
            fg="#12100e",
            activebackground="#22c77a",
            activeforeground="#12100e",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.on_submit
        )
        self.btn_generate.pack(side=tk.RIGHT)

        self.lbl_mode_status = tk.Label(bottom_bar, text="Tryb: Nowe Wydanie", font=("Inter", 9, "bold"), fg=self.text_muted, bg=self.bg_card)
        self.lbl_mode_status.pack(side=tk.LEFT, padx=(0, 16))

        btn_clear = tk.Button(
            bottom_bar,
            text="Wyczyść formularz",
            font=("Inter", 9),
            bg=self.bg_input,
            fg=self.text_muted,
            relief=tk.FLAT,
            padx=12,
            pady=8,
            command=self.clear_fields
        )
        btn_clear.pack(side=tk.LEFT)

        # Stylizacja zakładek Notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.bg_card, foreground=self.text_primary, padding=[14, 8], font=("Inter", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.accent_green)], foreground=[("selected", "#12100e")])

        # Główny kontener z zakładkami
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=16, pady=10)

        self.tab_basic = self.create_scrollable_tab("1. Dane & Opcje")
        self.build_basic_tab(self.tab_basic)

        self.tab_descriptions = self.create_scrollable_tab("2. Opisy Utworu")
        self.build_descriptions_tab(self.tab_descriptions)

        self.tab_audio = self.create_scrollable_tab("3. Pliki & Osobne STEMS")
        self.build_audio_stems_tab(self.tab_audio)

        self.tab_visuals = self.create_scrollable_tab("4. Grafiki & Tapety")
        self.build_visuals_tab(self.tab_visuals)

        self.tab_smartlink = self.create_scrollable_tab("5. Smartlink / Bio Linki")
        self.build_smartlink_tab(self.tab_smartlink)

        self.tab_translations = self.create_scrollable_tab("6. Tłumaczenia (EN)")
        self.build_translations_tab(self.tab_translations)

    def create_scrollable_tab(self, tab_title):
        frame = tk.Frame(self.notebook, bg=self.bg_dark)
        self.notebook.add(frame, text=tab_title)

        canvas = tk.Canvas(frame, bg=self.bg_dark, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_dark, padx=16, pady=16)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return scrollable_frame

    def add_entry_field(self, parent, label_text, var, hint=""):
        f = tk.Frame(parent, bg=self.bg_dark)
        f.pack(fill=tk.X, pady=5)

        lbl = tk.Label(f, text=label_text, font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark)
        lbl.pack(anchor=tk.W, pady=(0, 2))

        if hint:
            h_lbl = tk.Label(f, text=hint, font=("Inter", 8), fg=self.text_muted, bg=self.bg_dark)
            h_lbl.pack(anchor=tk.W, pady=(0, 2))

        ent = tk.Entry(f, textvariable=var, font=("Inter", 10), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        ent.pack(fill=tk.X, ipady=6, ipadx=8)
        return ent

    def add_file_or_url_picker(self, parent, label_text, var, filetypes=[("Wszystkie pliki", "*.*")], hint="Wskaż plik lokalny LUB wklej bezpośredni link URL (np. Google Drive / Dropbox / CDN)"):
        f = tk.Frame(parent, bg=self.bg_dark)
        f.pack(fill=tk.X, pady=5)

        lbl = tk.Label(f, text=label_text, font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark)
        lbl.pack(anchor=tk.W, pady=(0, 2))

        if hint:
            h_lbl = tk.Label(f, text=hint, font=("Inter", 8), fg=self.text_muted, bg=self.bg_dark)
            h_lbl.pack(anchor=tk.W, pady=(0, 2))

        row = tk.Frame(f, bg=self.bg_dark)
        row.pack(fill=tk.X)

        ent = tk.Entry(row, textvariable=var, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, ipadx=8)

        def browse():
            filename = filedialog.askopenfilename(filetypes=filetypes)
            if filename:
                var.set(filename)

        btn = tk.Button(row, text="Plik lokalny...", font=("Inter", 9), bg=self.border_col, fg=self.text_primary, relief=tk.FLAT, padx=12, pady=5, cursor="hand2", command=browse)
        btn.pack(side=tk.RIGHT, padx=(8, 0))

    # --- Budowanie Zakładek ---

    def build_basic_tab(self, parent):
        sec_lbl = tk.Label(parent, text="GŁÓWNE PARAMETRY WYDANIA", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl.pack(anchor=tk.W, pady=(0, 8))

        self.add_entry_field(parent, "Tytuł Utworu / Singla (np. Harmony):", self.fields["title"])
        self.add_entry_field(parent, "Slug URL / Nazwa podstrony (puste = wygeneruje się z tytułu):", self.fields["slug"])
        self.add_entry_field(parent, "Wykonawca / Artysta:", self.fields["artist"])
        self.add_entry_field(parent, "Rok / Data premiery:", self.fields["year"])

        # Grid parametrów technicznych
        grid_f = tk.Frame(parent, bg=self.bg_dark)
        grid_f.pack(fill=tk.X, pady=6)

        for col, (lbl_txt, k) in enumerate([("Tempo (BPM):", "bpm"), ("Tonacja (Key):", "key"), ("Czas trwania:", "duration")]):
            sub_col = tk.Frame(grid_f, bg=self.bg_dark)
            sub_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4 if col > 0 else (0, 4))
            tk.Label(sub_col, text=lbl_txt, font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W)
            tk.Entry(sub_col, textvariable=self.fields[k], font=("Inter", 10), bg=self.bg_input, fg=self.text_primary, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col).pack(fill=tk.X, ipady=6, ipadx=6)

        self.add_entry_field(parent, "Gatunek muzyczny / Styl (np. Elektronika / Orhestra):", self.fields["genre"])
        self.add_entry_field(parent, "Jakość Mastera (np. 48 kHz / 24-bit):", self.fields["quality"])

        sep = tk.Frame(parent, height=1, bg=self.border_col)
        sep.pack(fill=tk.X, pady=14)

        # Opcja Link in Bio
        sec_lbl_bio = tk.Label(parent, text="OPCJA: WIDOK SMARTLINK / LINK IN BIO", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl_bio.pack(anchor=tk.W, pady=(0, 4))

        bio_frame = tk.Frame(parent, bg=self.bg_card, padx=12, pady=10, highlightthickness=1, highlightbackground=self.border_col)
        bio_frame.pack(fill=tk.X, pady=6)

        chk_bio = tk.Checkbutton(
            bio_frame,
            text="Włącz widok 'Smartlink / Link in Bio' dla tego wydania (przełącznik zakładek na stronie i w katalogu)",
            variable=self.enable_bio_var,
            font=("Inter", 9, "bold"),
            fg=self.accent_green,
            bg=self.bg_card,
            selectcolor=self.bg_input,
            activebackground=self.bg_card,
            activeforeground=self.accent_green
        )
        chk_bio.pack(anchor=tk.W)

        bio_desc = tk.Label(
            bio_frame,
            text="Jeśli zaznaczone: strona wydania otrzyma zakładki 'Pełna Strona' oraz 'Widok Smartlink / Bio' do bio na Instagramie/TikToku, a w katalogu wydania pojawi się przycisk 'Smartlink ↗'.\nJeśli odznaczone: strona będzie wyłącznie klasyczną stroną wydania ze stemsami i odtwarzaczem.",
            font=("Inter", 8),
            fg=self.text_muted,
            bg=self.bg_card,
            justify=tk.LEFT
        )
        bio_desc.pack(anchor=tk.W, pady=(4, 0))

        sep2 = tk.Frame(parent, height=1, bg=self.border_col)
        sep2.pack(fill=tk.X, pady=14)

        sec_lbl2 = tk.Label(parent, text="TAGI & BADGE", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl2.pack(anchor=tk.W, pady=(0, 6))

        self.add_entry_field(parent, "Główny Badge 1 (np. Nowy Singiel / Album / EP):", self.fields["badge_main"])
        self.add_entry_field(parent, "Badge 2 (np. Stems ZIP & Arty / Mp3 Files):", self.fields["badge_stems"])

        yt_frame = tk.Frame(parent, bg=self.bg_card, padx=12, pady=10, highlightthickness=1, highlightbackground="#ff3344")
        yt_frame.pack(fill=tk.X, pady=(10, 6))

        chk_yt = tk.Checkbutton(
            yt_frame,
            text="Plakietka YouTube: No Copyright Music / Content ID Free (dozwolone bezpłatnie na YouTube)",
            variable=self.youtube_safe_var,
            font=("Inter", 9, "bold"),
            fg="#ff5555",
            bg=self.bg_card,
            selectcolor=self.bg_input,
            activebackground=self.bg_card,
            activeforeground="#ff6666"
        )
        chk_yt.pack(anchor=tk.W)

        yt_hint = tk.Label(
            yt_frame,
            text="Dodaje elegancką czerwoną plakietkę w stylu YouTube oraz boks informacyjny o braku roszczeń Content ID dla twórców wideo.",
            font=("Inter", 8),
            fg=self.text_muted,
            bg=self.bg_card,
            justify=tk.LEFT
        )
        yt_hint.pack(anchor=tk.W, pady=(2, 6))

        self.add_entry_field(yt_frame, "Tekst plakietki (domyślnie: No Copyright Music):", self.fields["badge_youtube"])

    def build_descriptions_tab(self, parent):
        sec_lbl = tk.Label(parent, text="OPISY I HISTORIA UTWORU", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl.pack(anchor=tk.W, pady=(0, 8))

        tk.Label(parent, text="Krótki opis (do kafelka w katalogu wydań):", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W, pady=(6, 2))
        self.txt_short_desc = tk.Text(parent, height=3, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        self.txt_short_desc.pack(fill=tk.X, pady=(0, 10))
        self.txt_short_desc.insert("1.0", "Mój autorski utwór z przestrzennym basem, głębokimi teksturami syntezatorowymi i organicznym brzmieniem.")

        tk.Label(parent, text="Pełny opis utworu (Akapit 1 na stronie wydania — historia, inspiracje):", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W, pady=(6, 2))
        self.txt_full_desc_1 = tk.Text(parent, height=4, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        self.txt_full_desc_1.pack(fill=tk.X, pady=(0, 10))
        self.txt_full_desc_1.insert("1.0", "Utwór zrodzony z poszukiwań idealnej równowagi między organicznym, przestrzennym ambientem a surowym, pulsującym basem.")

        tk.Label(parent, text="Kulisy produkcji & DAW (Akapit 2 — syntezatory, sprzęt, wtyczki):", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W, pady=(6, 2))
        self.txt_full_desc_2 = tk.Text(parent, height=4, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        self.txt_full_desc_2.pack(fill=tk.X, pady=(0, 10))
        self.txt_full_desc_2.insert("1.0", "Podczas produkcji wykorzystałem hybrydowe łańcuchy syntezy połączone z analogowym ciepłem. Każdy producent może pobrać pojedyncze ścieżki i stworzyć własny remix.")

        tk.Label(parent, text="Nota licencyjna dla twórców (darmowe remiksy, granie live):", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W, pady=(6, 2))
        self.txt_license = tk.Text(parent, height=3, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        self.txt_license.pack(fill=tk.X, pady=(0, 10))
        self.txt_license.insert("1.0", "Licencja Creative Commons (CC BY-NC 4.0): Masz pełne prawo do bezpłatnego pobierania, cięcia sampli, tworzenia remiksów, grania w setach DJ-skich oraz wykorzystywania jako podkład w filmach. Wystarczy podać: Muzyka: Hexit Rely.")

    def build_audio_stems_tab(self, parent):
        sec_lbl = tk.Label(parent, text="PLIKI AUDIO & PACZKA ZIP", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl.pack(anchor=tk.W, pady=(0, 8))

        self.add_file_or_url_picker(
            parent,
            "Główny Plik Odsłuchu Audio (MP3 / WAV do playera):",
            self.fields["audio_file"],
            [("Pliki Audio", "*.mp3 *.wav *.ogg *.flac")],
            "Wskaż lokalny plik audio do skopiowania LUB bezpośredni link do strumienia MP3"
        )

        self.add_file_or_url_picker(
            parent,
            "Kompletna Paczka STEMS (ZIP) — opcjonalne pełne archiwum:",
            self.fields["stems_zip_file"],
            [("Archiwum ZIP", "*.zip *.rar *.7z")],
            "Wskaż lokalne archiwum ZIP LUB wklej link do pobrania (np. Google Drive, Dropbox, MEGA)"
        )

        sep = tk.Frame(parent, height=1, bg=self.border_col)
        sep.pack(fill=tk.X, pady=16)

        sec_lbl2 = tk.Label(parent, text="POJEDYNCZE ŚCIEŻKI STEMS (DODAWANIE / USUWANIE / PLIK LUB LINK)", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl2.pack(anchor=tk.W, pady=(0, 4))

        tk.Label(
            parent,
            text="Wpisz nazwę ścieżki i podaj lokalny plik audio (WAV/MP3) LUB bezpośredni link URL. Możesz dowolnie dodawać i usuwać ścieżki:",
            font=("Inter", 8),
            fg=self.text_muted,
            bg=self.bg_dark
        ).pack(anchor=tk.W, pady=(0, 10))

        # Kontener na dynamiczne wiersze stemsów
        self.stems_container = tk.Frame(parent, bg=self.bg_dark)
        self.stems_container.pack(fill=tk.X)

        self.refresh_stems_ui()

        btn_add_stem = tk.Button(
            parent,
            text="+ Dodaj kolejną ścieżkę STEM",
            font=("Inter", 9, "bold"),
            bg=self.bg_card,
            fg=self.accent_green,
            activebackground=self.border_col,
            activeforeground=self.accent_green,
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.add_new_stem_row
        )
        btn_add_stem.pack(anchor=tk.W, pady=12)

    def refresh_stems_ui(self):
        """Przerysowuje wszystkie wiersze ścieżek STEM z przyciskami usuwania i wyboru pliku/linku."""
        for widget in self.stems_container.winfo_children():
            widget.destroy()

        for idx, stem in enumerate(self.individual_stems):
            self.create_single_stem_widget(self.stems_container, stem, idx)

    def create_single_stem_widget(self, container, stem_dict, idx):
        row = tk.Frame(container, bg=self.bg_card, padx=10, pady=8, highlightthickness=1, highlightbackground=self.border_col)
        row.pack(fill=tk.X, pady=4)

        # Numer i Nazwa ścieżki
        tk.Label(row, text=f"#{idx+1}", font=("Inter", 8, "bold"), fg=self.accent_green, bg=self.bg_card, width=3).pack(side=tk.LEFT)

        tk.Label(row, text="Nazwa:", font=("Inter", 8, "bold"), fg=self.text_muted, bg=self.bg_card).pack(side=tk.LEFT, padx=(4, 2))
        ent_name = tk.Entry(row, textvariable=stem_dict["name"], font=("Inter", 9), width=22, bg=self.bg_input, fg=self.text_primary, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        ent_name.pack(side=tk.LEFT, padx=(0, 10), ipady=4)

        # Plik lokalny LUB Link URL
        tk.Label(row, text="Plik / Link URL:", font=("Inter", 8, "bold"), fg=self.text_muted, bg=self.bg_card).pack(side=tk.LEFT, padx=(0, 2))
        ent_file = tk.Entry(row, textvariable=stem_dict["file"], font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        ent_file.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=4)

        def browse():
            f = filedialog.askopenfilename(filetypes=[("Audio", "*.wav *.mp3 *.ogg *.flac *.zip")])
            if f:
                stem_dict["file"].set(f)

        btn_browse = tk.Button(row, text="Wybierz plik...", font=("Inter", 8), bg=self.border_col, fg=self.text_primary, relief=tk.FLAT, padx=8, pady=3, cursor="hand2", command=browse)
        btn_browse.pack(side=tk.LEFT, padx=(0, 6))

        # Przycisk usuwania tego stema
        def delete_stem():
            if len(self.individual_stems) <= 1:
                # Jeśli to ostatni, czyścimy go zamiast usuwać całkowicie
                stem_dict["name"].set("1. Główny Stem")
                stem_dict["file"].set("")
                self.refresh_stems_ui()
                return
            self.individual_stems.remove(stem_dict)
            self.refresh_stems_ui()

        btn_del = tk.Button(row, text="✕ Usuń", font=("Inter", 8, "bold"), bg="#451a1a", fg="#fca5a5", activebackground="#7f1d1d", relief=tk.FLAT, padx=8, pady=3, cursor="hand2", command=delete_stem)
        btn_del.pack(side=tk.RIGHT)

    def add_new_stem_row(self):
        new_idx = len(self.individual_stems) + 1
        new_stem = {"name": tk.StringVar(value=f"{new_idx}. Nowa ścieżka"), "file": tk.StringVar(value="")}
        self.individual_stems.append(new_stem)
        self.refresh_stems_ui()

    def build_visuals_tab(self, parent):
        sec_lbl = tk.Label(parent, text="GRAFIKI, ARTY I TAPETY (DYNAMICZNA LISTA MATERIAŁÓW)", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl.pack(anchor=tk.W, pady=(0, 4))

        tk.Label(
            parent,
            text="Wskaż pliki graficzne lokalnie lub podaj adresy URL. Możesz dodać dowolną liczbę grafik lub tapet (3 podstawowe są domyślne). Każde pobieranie otworzy się w nowej karcie:",
            font=("Inter", 8),
            fg=self.text_muted,
            bg=self.bg_dark
        ).pack(anchor=tk.W, pady=(0, 10))

        top_bar = tk.Frame(parent, bg=self.bg_dark)
        top_bar.pack(fill=tk.X, pady=(0, 8))

        btn_add = tk.Button(
            top_bar,
            text="+ Dodaj kolejną grafikę / tapetę",
            font=("Inter", 9, "bold"),
            bg="#065f46",
            fg="#a7f3d0",
            activebackground="#047857",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.add_new_visual_row
        )
        btn_add.pack(side=tk.LEFT)

        self.visuals_container = tk.Frame(parent, bg=self.bg_dark)
        self.visuals_container.pack(fill=tk.BOTH, expand=True)

        self.refresh_visuals_ui()

    def refresh_visuals_ui(self):
        """Przerysowuje listę materiałów graficznych i tapet."""
        for widget in self.visuals_container.winfo_children():
            widget.destroy()

        for idx, item in enumerate(self.visual_assets):
            self.create_single_visual_widget(self.visuals_container, item, idx)

    def create_single_visual_widget(self, container, item, idx):
        card = tk.Frame(container, bg=self.bg_card, padx=12, pady=10, highlightthickness=1, highlightbackground=self.border_col)
        card.pack(fill=tk.X, pady=6)

        # Nagłówek karty grafiki z numerem i przyciskiem usuwania
        header = tk.Frame(card, bg=self.bg_card)
        header.pack(fill=tk.X, pady=(0, 6))

        tk.Label(header, text=f"Grafika #{idx+1}", font=("Inter", 9, "bold"), fg=self.accent_green, bg=self.bg_card).pack(side=tk.LEFT)

        def delete_item():
            if len(self.visual_assets) <= 1:
                item["title"].set("Oficjalna Okładka Utworu")
                item["format"].set("Format 1:1")
                item["desc"].set("Oryginalny artwork singla w bezstratnej jakości.")
                item["file"].set("")
                self.refresh_visuals_ui()
                return
            self.visual_assets.remove(item)
            self.refresh_visuals_ui()

        btn_del = tk.Button(header, text="✕ Usuń tę grafikę", font=("Inter", 8, "bold"), bg="#451a1a", fg="#fca5a5", activebackground="#7f1d1d", relief=tk.FLAT, padx=8, pady=2, cursor="hand2", command=delete_item)
        btn_del.pack(side=tk.RIGHT)

        # Tytuł i Format w jednym rzędzie
        row1 = tk.Frame(card, bg=self.bg_card)
        row1.pack(fill=tk.X, pady=2)

        f_title = tk.Frame(row1, bg=self.bg_card)
        f_title.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        tk.Label(f_title, text="Nazwa / Tytuł (np. Tapeta na Pulpit):", font=("Inter", 8, "bold"), fg=self.text_primary, bg=self.bg_card).pack(anchor=tk.W)
        tk.Entry(f_title, textvariable=item["title"], font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col).pack(fill=tk.X, ipady=4, pady=2)

        f_fmt = tk.Frame(row1, bg=self.bg_card, width=150)
        f_fmt.pack(side=tk.RIGHT, fill=tk.X, padx=(6, 0))
        tk.Label(f_fmt, text="Format (np. Format 16:9):", font=("Inter", 8, "bold"), fg=self.text_primary, bg=self.bg_card).pack(anchor=tk.W)
        tk.Entry(f_fmt, textvariable=item["format"], font=("Inter", 9), width=18, bg=self.bg_input, fg=self.text_primary, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col).pack(fill=tk.X, ipady=4, pady=2)

        # Opis
        row2 = tk.Frame(card, bg=self.bg_card)
        row2.pack(fill=tk.X, pady=2)
        tk.Label(row2, text="Krótki opis grafiki:", font=("Inter", 8, "bold"), fg=self.text_primary, bg=self.bg_card).pack(anchor=tk.W)
        tk.Entry(row2, textvariable=item["desc"], font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col).pack(fill=tk.X, ipady=4, pady=2)

        # Plik / URL z przeglądaniem
        row3 = tk.Frame(card, bg=self.bg_card)
        row3.pack(fill=tk.X, pady=(2, 0))
        tk.Label(row3, text="Ścieżka do pliku lokalnego LUB link URL do grafiki:", font=("Inter", 8, "bold"), fg=self.text_primary, bg=self.bg_card).pack(anchor=tk.W)

        f_file = tk.Frame(row3, bg=self.bg_card)
        f_file.pack(fill=tk.X, pady=2)
        ent_f = tk.Entry(f_file, textvariable=item["file"], font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        ent_f.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=4)

        def browse():
            f = filedialog.askopenfilename(filetypes=[("Grafika", "*.jpg *.jpeg *.png *.webp *.avif *.gif")])
            if f:
                item["file"].set(f)

        btn_browse = tk.Button(f_file, text="Wybierz plik...", font=("Inter", 8), bg=self.border_col, fg=self.text_primary, relief=tk.FLAT, padx=10, pady=3, cursor="hand2", command=browse)
        btn_browse.pack(side=tk.RIGHT)

    def add_new_visual_row(self):
        new_idx = len(self.visual_assets) + 1
        new_item = {
            "title": tk.StringVar(value=f"Dodatkowa Tapeta {new_idx}"),
            "format": tk.StringVar(value="Format 16:9"),
            "desc": tk.StringVar(value="Dodatkowa grafika wysokiej rozdzielczości do pobrania."),
            "file": tk.StringVar(value=""),
        }
        self.visual_assets.append(new_item)
        self.refresh_visuals_ui()

    def build_smartlink_tab(self, parent):
        sec_lbl = tk.Label(parent, text="LINKI DO WERSJI SMARTLINK / BIO (STREAMING)", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl.pack(anchor=tk.W, pady=(0, 4))

        tk.Label(parent, text="Adresy URL do poszczególnych platform streamingowych wyświetlane w widoku Bio:", font=("Inter", 8), fg=self.text_muted, bg=self.bg_dark).pack(anchor=tk.W, pady=(0, 12))

        self.add_entry_field(parent, "Link Spotify:", self.fields["link_spotify"])
        self.add_entry_field(parent, "Link YouTube / YouTube Music:", self.fields["link_youtube"])
        self.add_entry_field(parent, "Link Apple Music:", self.fields["link_apple"])
        self.add_entry_field(parent, "Link SoundCloud:", self.fields["link_soundcloud"])
        self.add_entry_field(parent, "Link TikTok Audio:", self.fields["link_tiktok"])

    def build_translations_tab(self, parent):
        sec_lbl = tk.Label(parent, text="ANGIELSKIE TŁUMACZENIA WYDANIA (SYSTEM DWUJĘZYCZNY)", font=("Inter", 11, "bold"), fg=self.accent_green, bg=self.bg_dark)
        sec_lbl.pack(anchor=tk.W, pady=(0, 4))

        tk.Label(parent, text="Uzupełnij poniższe pola w języku angielskim. Strona automatycznie zaoferuje przełącznik PL / EN dla użytkowników.", font=("Inter", 8), fg=self.text_muted, bg=self.bg_dark).pack(anchor=tk.W, pady=(0, 10))

        self.add_entry_field(parent, "Główny Badge EN (np. New Single / Album / EP):", self.fields["badge_main_en"])
        self.add_entry_field(parent, "Plakietka YouTube EN (np. No Copyright Music):", self.fields["badge_youtube_en"])

        tk.Label(parent, text="Krótki opis EN (do kafelka w katalogu wydań):", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W, pady=(8, 2))
        self.txt_short_desc_en = tk.Text(parent, height=3, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        self.txt_short_desc_en.pack(fill=tk.X, pady=(0, 10))
        self.txt_short_desc_en.insert("1.0", "My original production featuring immersive basslines, deep synthesizer textures, and organic atmosphere.")

        tk.Label(parent, text="Pełny opis utworu EN (Akapit 1 — story & inspirations):", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W, pady=(6, 2))
        self.txt_full_desc_1_en = tk.Text(parent, height=4, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        self.txt_full_desc_1_en.pack(fill=tk.X, pady=(0, 10))
        self.txt_full_desc_1_en.insert("1.0", "A track born out of seeking balance between organic ambient spaces and raw, pulsing sub bass.")

        tk.Label(parent, text="Kulisy produkcji EN (Akapit 2 — DAW, gear & plugins):", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W, pady=(6, 2))
        self.txt_full_desc_2_en = tk.Text(parent, height=4, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        self.txt_full_desc_2_en.pack(fill=tk.X, pady=(0, 10))
        self.txt_full_desc_2_en.insert("1.0", "Produced with hybrid synthesis and analogue warmth. Creators can download multitrack stems below for remixes and video production.")

        tk.Label(parent, text="Nota licencyjna EN (Creative Commons notice):", font=("Inter", 9, "bold"), fg=self.text_primary, bg=self.bg_dark).pack(anchor=tk.W, pady=(6, 2))
        self.txt_license_en = tk.Text(parent, height=3, font=("Inter", 9), bg=self.bg_input, fg=self.text_primary, insertbackground=self.accent_green, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.border_col)
        self.txt_license_en.pack(fill=tk.X, pady=(0, 10))
        self.txt_license_en.insert("1.0", "Creative Commons License (CC BY-NC 4.0): You have full permission to freely download, sample, remix, perform in DJ sets, and use as background music in videos. Just credit: Music: Hexit Rely.")

    # --- Zarządzanie Stanem i Edycją ---

    def refresh_release_selector(self):
        """Odświeża listę wydań w ComboBox."""
        self.available_releases = get_available_releases()
        values = ["[+] -- Nowe Wydanie --"]
        for r in self.available_releases:
            values.append(f"{r['title']} ({r['slug']})")
        self.release_combo["values"] = values
        self.release_combo.current(0)

    def on_load_selected_release(self):
        sel_idx = self.release_combo.current()
        if sel_idx <= 0:
            self.reset_to_new_release()
            return

        rel_info = self.available_releases[sel_idx - 1]
        slug = rel_info["slug"]
        self.load_release_data(slug, rel_info)

    def load_release_data(self, slug: str, rel_info: dict):
        """Wczytuje dane wybranego wydania do formularza w celu edycji."""
        data_file = PROJECT_ROOT / "hexit" / "releases" / slug / "release_data.json"
        data = None

        if data_file.is_file():
            try:
                data = json.loads(data_file.read_text(encoding="utf-8"))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się odczytać pliku release_data.json: {e}")
                return

        if not data:
            messagebox.showwarning("Informacja", f"Wydanie '{slug}' nie posiadało pliku release_data.json. Wczytuję podstawowy identyfikator.")
            data = {"title": slug.capitalize(), "slug": slug}

        self.current_editing_slug = slug

        # Wypełnianie pól tekstowych
        for k, var in self.fields.items():
            if k in data:
                var.set(str(data[k]))

        # Flaga enable_bio & youtube_safe
        self.enable_bio_var.set(data.get("enable_bio", True))
        self.youtube_safe_var.set(data.get("youtube_safe", True))
        self.fields["badge_youtube"].set(data.get("badge_youtube", "No Copyright Music"))

        # Wypełnianie opisów
        self.txt_short_desc.delete("1.0", tk.END)
        self.txt_short_desc.insert("1.0", data.get("short_desc", ""))

        self.txt_full_desc_1.delete("1.0", tk.END)
        self.txt_full_desc_1.insert("1.0", data.get("full_desc_1", ""))

        self.txt_full_desc_2.delete("1.0", tk.END)
        self.txt_full_desc_2.insert("1.0", data.get("full_desc_2", ""))

        self.txt_license.delete("1.0", tk.END)
        self.txt_license.insert("1.0", data.get("license_notice", ""))

        # Wczytanie tłumaczeń EN
        translations_en = data.get("translations_en", {})
        self.fields["badge_main_en"].set(translations_en.get("badge_main", "New Single"))
        self.fields["badge_youtube_en"].set(translations_en.get("badge_youtube", "No Copyright Music"))

        if hasattr(self, 'txt_short_desc_en') and self.txt_short_desc_en:
            self.txt_short_desc_en.delete("1.0", tk.END)
            self.txt_short_desc_en.insert("1.0", translations_en.get("short_desc", ""))

        if hasattr(self, 'txt_full_desc_1_en') and self.txt_full_desc_1_en:
            self.txt_full_desc_1_en.delete("1.0", tk.END)
            self.txt_full_desc_1_en.insert("1.0", translations_en.get("full_desc_1", ""))

        if hasattr(self, 'txt_full_desc_2_en') and self.txt_full_desc_2_en:
            self.txt_full_desc_2_en.delete("1.0", tk.END)
            self.txt_full_desc_2_en.insert("1.0", translations_en.get("full_desc_2", ""))

        if hasattr(self, 'txt_license_en') and self.txt_license_en:
            self.txt_license_en.delete("1.0", tk.END)
            self.txt_license_en.insert("1.0", translations_en.get("license_notice", ""))

        # Wypełnianie listy stemsów
        stems = data.get("stems_individual", [])
        self.individual_stems = []
        if stems:
            for s in stems:
                self.individual_stems.append({
                    "name": tk.StringVar(value=s.get("name", "")),
                    "file": tk.StringVar(value=s.get("file", ""))
                })
        else:
            self.individual_stems = [
                {"name": tk.StringVar(value="1. Główny Stem"), "file": tk.StringVar(value="")}
            ]
        self.refresh_stems_ui()

        # Wypełnianie listy grafik i tapet
        visuals = data.get("visual_assets", [])
        self.visual_assets = []
        if visuals:
            for v in visuals:
                self.visual_assets.append({
                    "title": tk.StringVar(value=v.get("title", "")),
                    "format": tk.StringVar(value=v.get("format", "")),
                    "desc": tk.StringVar(value=v.get("desc", "")),
                    "file": tk.StringVar(value=v.get("file", ""))
                })
        else:
            cov = data.get("cover_file", "")
            pc = data.get("pc_wall_file", "")
            ph = data.get("phone_wall_file", "")
            self.visual_assets = [
                {"title": tk.StringVar(value="Oficjalna Okładka Utworu"), "format": tk.StringVar(value="Format 1:1"), "desc": tk.StringVar(value="Oryginalny artwork singla w bezstratnej jakości."), "file": tk.StringVar(value=cov)},
                {"title": tk.StringVar(value="Tapeta na Pulpit Komputera"), "format": tk.StringVar(value="Format 16:9"), "desc": tk.StringVar(value="Szerokokątna grafika wysokiej rozdzielczości na monitor."), "file": tk.StringVar(value=pc)},
                {"title": tk.StringVar(value="Tapeta na Smartfon (Ekran blokady)"), "format": tk.StringVar(value="Format 9:16"), "desc": tk.StringVar(value="Dedykowana tapeta pionowa na ekrany telefonów (iOS / Android)."), "file": tk.StringVar(value=ph)},
            ]
        self.refresh_visuals_ui()

        # Zmiana etykiet na tryb edycji
        self.lbl_mode_status.config(text=f"Tryb: EDYCJA ({slug})", fg=self.accent_green)
        self.btn_generate.config(text=f"💾 ZAPISZ ZMIANY W WYDANIU ({slug.upper()})")
        messagebox.showinfo("Załadowano Wydanie", f"Załadowano dane wydania '{data.get('title', slug)}'. Możesz teraz modyfikować pola, stemsy i kliknąć 'Zapisz zmiany'.")

    def reset_to_new_release(self):
        """Przełącza aplikację w tryb tworzenia nowego wydania."""
        self.current_editing_slug = None
        self.clear_fields()
        self.lbl_mode_status.config(text="Tryb: Nowe Wydanie", fg=self.text_muted)
        self.btn_generate.config(text="🚀 WYGENERUJ WYDANIE I DODAJ DO STRONY")
        self.release_combo.current(0)

    def clear_fields(self):
        for k in ["title", "slug", "audio_file", "cover_file", "stems_zip_file", "pc_wall_file", "phone_wall_file"]:
            self.fields[k].set("")
        self.enable_bio_var.set(True)
        self.youtube_safe_var.set(True)
        self.fields["badge_youtube"].set("No Copyright Music")
        self.fields["badge_main_en"].set("New Single")
        self.fields["badge_youtube_en"].set("No Copyright Music")
        if hasattr(self, 'txt_short_desc_en') and self.txt_short_desc_en:
            self.txt_short_desc_en.delete("1.0", tk.END)
        if hasattr(self, 'txt_full_desc_1_en') and self.txt_full_desc_1_en:
            self.txt_full_desc_1_en.delete("1.0", tk.END)
        if hasattr(self, 'txt_full_desc_2_en') and self.txt_full_desc_2_en:
            self.txt_full_desc_2_en.delete("1.0", tk.END)
        if hasattr(self, 'txt_license_en') and self.txt_license_en:
            self.txt_license_en.delete("1.0", tk.END)

        self.individual_stems = [
            {"name": tk.StringVar(value="1. Drums & Kicks"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="2. Sub Bass & 808"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="3. Lead Synths & Arps"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="4. Ambient Pads & Textures"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="5. Risers, Impacts & FX"), "file": tk.StringVar(value="")},
            {"name": tk.StringVar(value="6. Master Preview MP3"), "file": tk.StringVar(value="")},
        ]
        self.refresh_stems_ui()
        self.visual_assets = [
            {"title": tk.StringVar(value="Oficjalna Okładka Utworu"), "format": tk.StringVar(value="Format 1:1"), "desc": tk.StringVar(value="Oryginalny artwork singla w bezstratnej jakości."), "file": tk.StringVar(value="")},
            {"title": tk.StringVar(value="Tapeta na Pulpit Komputera"), "format": tk.StringVar(value="Format 16:9"), "desc": tk.StringVar(value="Szerokokątna grafika wysokiej rozdzielczości na monitor."), "file": tk.StringVar(value="")},
            {"title": tk.StringVar(value="Tapeta na Smartfon (Ekran blokady)"), "format": tk.StringVar(value="Format 9:16"), "desc": tk.StringVar(value="Dedykowana tapeta pionowa na ekrany telefonów (iOS / Android)."), "file": tk.StringVar(value="")},
        ]
        self.refresh_visuals_ui()

    def on_submit(self):
        data = {k: v.get() for k, v in self.fields.items()}
        data["enable_bio"] = self.enable_bio_var.get()
        data["youtube_safe"] = self.youtube_safe_var.get()
        data["badge_youtube"] = self.fields["badge_youtube"].get().strip() or "No Copyright Music"
        data["short_desc"] = self.txt_short_desc.get("1.0", tk.END).strip()
        data["full_desc_1"] = self.txt_full_desc_1.get("1.0", tk.END).strip()
        data["full_desc_2"] = self.txt_full_desc_2.get("1.0", tk.END).strip()
        data["license_notice"] = self.txt_license.get("1.0", tk.END).strip()

        # Zebranie tłumaczeń EN
        translations_en = {
            "badge_main": self.fields["badge_main_en"].get().strip() or "New Single",
            "badge_youtube": self.fields["badge_youtube_en"].get().strip() or "No Copyright Music",
            "short_desc": self.txt_short_desc_en.get("1.0", tk.END).strip() if hasattr(self, 'txt_short_desc_en') and self.txt_short_desc_en else "",
            "full_desc_1": self.txt_full_desc_1_en.get("1.0", tk.END).strip() if hasattr(self, 'txt_full_desc_1_en') and self.txt_full_desc_1_en else "",
            "full_desc_2": self.txt_full_desc_2_en.get("1.0", tk.END).strip() if hasattr(self, 'txt_full_desc_2_en') and self.txt_full_desc_2_en else "",
            "license_notice": self.txt_license_en.get("1.0", tk.END).strip() if hasattr(self, 'txt_license_en') and self.txt_license_en else "",
        }
        data["translations_en"] = translations_en

        # Jeśli byliśmy w trybie edycji i użytkownik nie zmienił sluga
        if self.current_editing_slug and not data["slug"]:
            data["slug"] = self.current_editing_slug

        data["stems_individual"] = [
            {"name": s["name"].get().strip(), "file": s["file"].get().strip()}
            for s in self.individual_stems
            if s["name"].get().strip()
        ]

        data["visual_assets"] = [
            {
                "title": v["title"].get().strip(),
                "format": v["format"].get().strip() or "Grafika",
                "desc": v["desc"].get().strip(),
                "file": v["file"].get().strip(),
            }
            for v in self.visual_assets
            if v["title"].get().strip() or v["file"].get().strip()
        ]
        if self.visual_assets:
            if len(self.visual_assets) > 0 and self.visual_assets[0]["file"].get().strip():
                data["cover_file"] = self.visual_assets[0]["file"].get().strip()
            if len(self.visual_assets) > 1 and self.visual_assets[1]["file"].get().strip():
                data["pc_wall_file"] = self.visual_assets[1]["file"].get().strip()
            if len(self.visual_assets) > 2 and self.visual_assets[2]["file"].get().strip():
                data["phone_wall_file"] = self.visual_assets[2]["file"].get().strip()

        success, msg = generate_release(data)
        if success:
            self.refresh_release_selector()
            messagebox.showinfo("Sukces!", msg)
        else:
            messagebox.showerror("Błąd", msg)


# ==============================================================================
# TRYB CLI (DLA LINII POLECEŃ LUB AUTOMATYZACJI)
# ==============================================================================

def run_cli_demo():
    print("=== Hexit Rely Release Builder ===")
    releases = get_available_releases()
    print(f"Dostępne wydania ({len(releases)}):")
    for r in releases:
        print(f"- {r['title']} ({r['slug']})")

    title = input("\nPodaj tytuł utworu: ").strip() or "Nowy Utwór"
    data = {
        "title": title,
        "artist": "Hexit Rely",
        "bpm": "128 BPM",
        "key": "C Minor",
        "genre": "Elektronika",
        "enable_bio": True
    }
    success, msg = generate_release(data)
    print(msg)


def main():
    if "--cli" in sys.argv or not HAS_TKINTER:
        run_cli_demo()
    else:
        root = tk.Tk()
        app = ReleaseBuilderApp(root)
        root.mainloop()


if __name__ == "__main__":
    main()
