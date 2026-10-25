document.addEventListener("DOMContentLoaded", function () {
  // Cookie notice functionality
  var acceptButton = document.getElementById('acceptButton');
  var privacyNotice = document.getElementById('privacyNotice');

  if (acceptButton && privacyNotice) {
    // Check if user has already accepted cookies
    if (localStorage.getItem('cookiesAccepted') === 'true') {
      privacyNotice.classList.add('hidden');
    }

    acceptButton.addEventListener('click', function () {
      privacyNotice.classList.add('hidden');
      localStorage.setItem('cookiesAccepted', 'true');
    });
  }

  // Smooth scrolling for anchor links (but not mailto links)
  document.querySelectorAll('a[href^="#"]:not([href^="mailto:"])').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Ensure mailto links work properly
  document.querySelectorAll('a[href^="mailto:"]').forEach(mailtoLink => {
    mailtoLink.addEventListener('click', function (e) {
      // Don't prevent default for mailto links
      console.log('Mailto link clicked:', this.href);
    });
  });

  // Add scroll effect to header
  const header = document.querySelector('.modern-header');
  if (header) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 100) {
        header.style.background = 'rgba(18, 16, 14, 0.98)';
        header.style.backdropFilter = 'blur(20px)';
      } else {
        header.style.background = 'rgba(18, 16, 14, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
      }
    });
  }

  // Add fade-in animation to elements
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in-up');
      }
    });
  }, observerOptions);

  // Observe all sections for animation
  document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
  });

  // Add hover effects to project cards
  document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mouseenter', function () {
      this.style.transform = 'translateY(-8px) scale(1.02)';
    });

    card.addEventListener('mouseleave', function () {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });

  // Add click tracking for portfolio items
  document.querySelectorAll('.work-item, .project-card').forEach(item => {
    item.addEventListener('click', function () {
      // Track portfolio item clicks
      console.log('Portfolio item clicked:', this.querySelector('h3')?.textContent);
    });
  });

  // Copy email button on contact page
  const copyEmailBtn = document.getElementById('copyEmailBtn');
  if (copyEmailBtn) {
    copyEmailBtn.addEventListener('click', async function () {
      const email = this.getAttribute('data-email');
      try {
        await navigator.clipboard.writeText(email);
        this.textContent = 'Copied!';
        setTimeout(() => {
          this.textContent = 'Copy Email';
        }, 1500);
      } catch (e) {
        // Fallback: create a temporary input
        const temp = document.createElement('input');
        temp.value = email;
        document.body.appendChild(temp);
        temp.select();
        document.execCommand('copy');
        document.body.removeChild(temp);
        this.textContent = 'Copied!';
        setTimeout(() => {
          this.textContent = 'Copy Email';
        }, 1500);
      }
    });
  }
});
// function createLeaf() {
// const leaf = document.createElement('div');
//leaf.classList.add('leaf');

// Ustaw losową pozycję startową z góry

//leaf.style.left = Math.random() * window.innerWidth - 50 + 'px';
//leaf.style.top = '-50px'; // Ustawiamy liść, aby zaczynał nad ekranem
//leaf.style.maxWidth = Window.innerWidth
//leaf.style.animationDuration = (Math.random() * 8 + 15) + 's'; // Czas spadania (3-8s)
//leaf.style.animationName = 'fall';



//document.body.appendChild(leaf);

// Usuń liść po zakończeniu animacji
//leaf.addEventListener('animationend', () => {
//  leaf.remove();
//});
//}

// Twórz liście co 500ms
//setInterval(createLeaf, 300);










document.addEventListener('DOMContentLoaded', () => {
  console.log('Blog załadowany!');
});

// Lightbox functionality
document.addEventListener('DOMContentLoaded', function () {
  const lightbox = document.getElementById('lightbox');
  const lightboxImage = document.getElementById('lightbox-image');
  const lightboxTitle = document.getElementById('lightbox-title');
  const lightboxClose = document.getElementById('lightbox-close');

  // Add click handlers to work item images
  const workItems = document.querySelectorAll('.work-item img');

  workItems.forEach(img => {
    img.addEventListener('click', function (e) {
      e.stopPropagation();
      const src = this.src;
      const alt = this.alt;
      const title = this.closest('.work-item').querySelector('h3').textContent;

      lightboxImage.src = src;
      lightboxImage.alt = alt;
      lightboxTitle.textContent = title;
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  // Close lightbox
  if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
  }

  if (lightbox) {
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });
  }

  // Close with Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lightbox && lightbox.classList.contains('active')) {
      closeLightbox();
    }
  });

  function closeLightbox() {
    if (lightbox) {
      lightbox.classList.remove('active');
      document.body.style.overflow = 'auto';
    }
  }
});







// Safely initialize EmailJS if present
if (typeof emailjs !== 'undefined') {
  try {
    emailjs.init("KhhpDMoVBpGtqgSjM");
  } catch (e) {
    console.warn("EmailJS init warning:", e);
  }
}

const sendEmail = async (event) => {
  event.preventDefault();
  const form = event.target;
  const statusMsg = document.getElementById("status-message");

  if (statusMsg) {
    statusMsg.textContent = "Wysyłanie wiadomości...";
    statusMsg.style.color = "#9ca3af";
  }

  if (typeof emailjs === 'undefined') {
    if (statusMsg) {
      statusMsg.textContent = "Dziękuję! Formularz został przesłany (tryb demonstracyjny).";
      statusMsg.style.color = "#10b981";
    }
    form.reset();
    return;
  }

  try {
    const response = await emailjs.sendForm(
      "service_kf463es",
      "template_q83n3iv",
      form
    );
    console.log("Email sent successfully!", response);
    if (statusMsg) {
      statusMsg.textContent = "Wiadomość wysłana pomyślnie! Odpowiem najszybciej jak to możliwe.";
      statusMsg.style.color = "#10b981";
    }
    form.reset();
  } catch (error) {
    console.error("Failed to send email:", error);
    if (statusMsg) {
      statusMsg.textContent = "Nie udało się wysłać wiadomości przez formularz. Napisz bezpośrednio na maila lub Discord!";
      statusMsg.style.color = "#ef4444";
    }
  }
};

/* ==========================================================================
   HEXIT RELY - ARCHITEKTURA LIVE STATUS STREAMU
   ==========================================================================
   Uwagi techniczne dotyczące YouTube Data API v3 na stronach statycznych (GitHub Pages):
   1. Bezpośrednie odpytywanie YouTube Data API v3 z frontendu ujawniałoby prywatny klucz API w kodzie źródłowym.
   2. YouTube Data API v3 ma restrykcyjny dzienny limit 10 000 jednostek. Zapytanie `search.list` z `eventType=live`
      zużywa aż 100 jednostek na jedno wywołanie, co oznacza wyczerpanie dziennego limitu już po 100 wizytach na stronie!
   3. Rozwiązanie:
      - System obsługuje inteligentne cache'owanie w localStorage (TTL 10 minut).
      - Jeśli podasz URL własnego mikro-proxy (np. bezpłatnego Cloudflare Workera czy Netlify Functions),
        system go automatycznie odpyta.
      - Domyślny fallback: responsywny embed YouTube z kanału w trybie live (`live_stream?channel=...`)
        oraz czytelne badge'e "LIVE" / "OFFLINE" zintegrowane z harmonogramem streamów.
   ========================================================================== */
const HexitLiveSystem = {
  // YouTube Channel ID Olafa / Hexit Rely
  channelId: "UCIpPTE3HsmUSAb-yfNybvSA",

  // Opcjonalny URL zewnętrznej funkcji serverless zwracającej JSON: { isLive: boolean, title: string, videoId: string }
  apiEndpoint: null,

  // Domyślny stan (można zmienić na true podczas streamu lub gdy API wykryje live)
  isLive: false,

  init: function () {
    this.checkStatus();
    this.updateUI();
    this.bindEvents();
  },

  checkStatus: function () {
    // 1. Sprawdź cache w localStorage
    const cached = localStorage.getItem("hexit_live_status");
    const cacheTime = localStorage.getItem("hexit_live_status_time");
    const now = Date.now();

    if (cached !== null && cacheTime && (now - parseInt(cacheTime, 10)) < 10 * 60 * 1000) {
      this.isLive = cached === "true";
      this.updateUI();
      return;
    }

    // 2. Jeśli zdefiniowano endpoint serverless, odpytaj go
    if (this.apiEndpoint) {
      fetch(this.apiEndpoint)
        .then(res => res.json())
        .then(data => {
          this.isLive = Boolean(data.isLive);
          localStorage.setItem("hexit_live_status", this.isLive);
          localStorage.setItem("hexit_live_status_time", Date.now());
          this.updateUI();
        })
        .catch(err => {
          console.warn("Błąd odpytywania statusu live:", err);
          this.fallbackStatus();
        });
    } else {
      this.fallbackStatus();
    }
  },

  fallbackStatus: function () {
    // Sprawdzamy dzień tygodnia i godziny streamów (np. wtorki i czwartki od 18:00 do 22:00 czasu PL)
    const now = new Date();
    const day = now.getDay(); // 0=nd, 2=wt, 4=czw, 6=sob
    const hour = now.getHours();

    // Logika orientacyjna - jeśli jesteśmy w oknie streamowym, ustawiamy sugerowany live
    const isScheduleWindow = (day === 2 || day === 4) && (hour >= 18 && hour < 22);

    // Zapisujemy domyślny status
    this.isLive = isScheduleWindow;
    this.updateUI();
  },

  updateUI: function () {
    const navBadge = document.getElementById("navLiveBadge");
    const heroBadge = document.getElementById("heroLiveBadge");
    const streamStatusText = document.getElementById("streamStatusIndicator");

    if (this.isLive) {
      if (navBadge) {
        navBadge.className = "badge-live is-live";
        navBadge.innerHTML = '<span class="live-pulse-dot"></span> LIVE TERAZ';
      }
      if (heroBadge) {
        heroBadge.className = "badge-live is-live";
        heroBadge.innerHTML = '<span class="live-pulse-dot"></span> 🔴 Nadaję na żywo! Zobacz stream &rarr;';
      }
      if (streamStatusText) {
        streamStatusText.innerHTML = '<span class="live-pulse-dot" style="background:#ef4444"></span> <strong>NA ŻYWO</strong>: Trwa transmisja!';
      }
    } else {
      if (navBadge) {
        navBadge.className = "badge-live is-offline";
        navBadge.innerHTML = '<span class="live-pulse-dot"></span> OFFLINE';
      }
      if (heroBadge) {
        heroBadge.className = "badge-live is-offline";
        heroBadge.innerHTML = '<span class="live-pulse-dot"></span> Stream offline • Zobacz kanał &rarr;';
      }
      if (streamStatusText) {
        streamStatusText.innerHTML = '<span class="live-pulse-dot" style="background:#9ca3af"></span> Stream jest obecnie offline. Zobacz ostatnie materiały poniżej.';
      }
    }
  },

  bindEvents: function () {
    // Opcjonalne ręczne przełączanie w trybie testowym za pomocą potrójnego kliknięcia w stopkę
    const footerLogo = document.querySelector(".footer-logo");
    if (footerLogo) {
      let clickCount = 0;
      footerLogo.addEventListener("click", () => {
        clickCount++;
        if (clickCount === 3) {
          this.isLive = !this.isLive;
          localStorage.setItem("hexit_live_status", this.isLive);
          localStorage.setItem("hexit_live_status_time", Date.now());
          this.updateUI();
          alert(`Tryb demonstracyjny: Status live ustawiony na ${this.isLive ? 'LIVE' : 'OFFLINE'}`);
          clickCount = 0;
        }
      });
    }
  }
};

/* ==========================================================================
   GŁÓWNA INICJALIZACJA STRONY
   ========================================================================== */
document.addEventListener("DOMContentLoaded", () => {
  // 1. Inicjalizacja Live Status
  HexitLiveSystem.init();

  // 2. Formularz kontaktowy
  const contactForm = document.getElementById("contact-form");
  if (contactForm) {
    contactForm.addEventListener("submit", sendEmail);
  }

  // 3. Mobilne Menu Hamburger
  const navToggle = document.getElementById("navToggle");
  const navMenu = document.getElementById("navMenu");
  const navOverlay = document.getElementById("navOverlay");

  if (navToggle && navMenu) {
    const toggleMenu = () => {
      const isOpen = navMenu.classList.contains("is-open");
      navToggle.classList.toggle("is-active", !isOpen);
      navMenu.classList.toggle("is-open", !isOpen);
      if (navOverlay) {
        navOverlay.classList.toggle("is-active", !isOpen);
      }
      document.body.style.overflow = !isOpen ? "hidden" : "";
    };

    navToggle.addEventListener("click", toggleMenu);

    if (navOverlay) {
      navOverlay.addEventListener("click", toggleMenu);
    }

    // Zamknięcie menu po kliknięciu linku
    navMenu.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        if (navMenu.classList.contains("is-open")) {
          toggleMenu();
        }
      });
    });

    // Zamknięcie klawiszem ESC
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navMenu.classList.contains("is-open")) {
        toggleMenu();
      }
    });
  }

  // 4. Filtrowanie postów na blogu
  const filterPills = document.querySelectorAll(".filter-pill");
  const blogCards = document.querySelectorAll(".blog-card-modern");

  if (filterPills.length > 0 && blogCards.length > 0) {
    filterPills.forEach(pill => {
      pill.addEventListener("click", function () {
        filterPills.forEach(p => p.classList.remove("active"));
        this.classList.add("active");

        const category = this.getAttribute("data-category");

        blogCards.forEach(card => {
          const cardCategory = card.getAttribute("data-category");
          if (category === "all" || cardCategory === category) {
            card.style.display = "flex";
            card.style.animation = "fadeInUp 0.35s ease forwards";
          } else {
            card.style.display = "none";
          }
        });
      });
    });
  }

  // 5. Powiadomienia o dropach w sklepie
  const notifyForms = document.querySelectorAll(".drop-notify-form");
  notifyForms.forEach(form => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const emailInput = form.querySelector("input[type='email']");
      const button = form.querySelector("button");
      if (emailInput && button) {
        const originalText = button.textContent;
        button.textContent = "Zapisano! Dziękuję.";
        button.disabled = true;
        button.style.backgroundColor = "#10b981";
        emailInput.value = "";
        setTimeout(() => {
          button.textContent = originalText;
          button.disabled = false;
          button.style.backgroundColor = "";
        }, 3000);
      }
    });
  });

  // 6. Podświetlanie aktywnej pozycji w menu w zależności od aktualnego pliku
  const currentPath = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-menu a").forEach(link => {
    const href = link.getAttribute("href");
    if (href && (href === currentPath || (currentPath === "" && href === "index.html"))) {
      link.classList.add("active");
    }
  });

  // 7. Lightbox dla galerii
  const lightbox = document.getElementById('lightbox');
  const lightboxImage = document.getElementById('lightbox-image');
  const lightboxTitle = document.getElementById('lightbox-title');
  const lightboxClose = document.getElementById('lightbox-close');

  if (lightbox && lightboxImage && lightboxTitle) {
    document.querySelectorAll('.work-item img, .gallery-item img').forEach(img => {
      img.addEventListener('click', function (e) {
        e.stopPropagation();
        lightboxImage.src = this.src;
        lightboxImage.alt = this.alt;
        lightboxTitle.textContent = this.alt || 'Powiększenie';
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    const closeLightbox = () => {
      lightbox.classList.remove('active');
      document.body.style.overflow = 'auto';
    };

    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox();
      }
    });
  }

  // 8. Interaktywne Laboratorium Kodu / Showcase Tabs (Home Hero)
  const labTabs = document.querySelectorAll('.code-lab-tab');
  const labPanels = document.querySelectorAll('.code-lab-panel');

  if (labTabs.length > 0 && labPanels.length > 0) {
    labTabs.forEach(tab => {
      tab.addEventListener('click', function () {
        const targetId = this.getAttribute('data-target');

        labTabs.forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        labPanels.forEach(p => p.classList.remove('active'));

        this.classList.add('active');
        this.setAttribute('aria-selected', 'true');
        const targetPanel = document.getElementById(targetId);
        if (targetPanel) {
          targetPanel.classList.add('active');
        }
      });
    });
  }

  // 9. Dedykowany, nowoczesny Ambient Player w rogu (Corner Dock)
  initAmbientPlayer();

  // 10. Dźwięki interfejsu (UI click) na przyciskach i menu
  initUiSound();
});

// UI Click Sound Player (pulowa obsługa szybkich kliknięć)
function initUiSound() {
  const clickAudioPath = "Sounds/ui click.mp3";
  const pool = [];
  const POOL_SIZE = 4;

  for (let i = 0; i < POOL_SIZE; i++) {
    const a = new Audio(clickAudioPath);
    a.volume = 0.35; // zbalansowana głośność kliku
    pool.push(a);
  }

  let poolIndex = 0;
  const playClickSound = () => {
    try {
      const sound = pool[poolIndex];
      sound.currentTime = 0;
      sound.play().catch(() => {});
      poolIndex = (poolIndex + 1) % POOL_SIZE;
    } catch (e) {
      // Ignoruj błędy polityki autoplay
    }
  };

  // Podepnij pod menu, przyciski i linki nawigacyjne (w tym elementy strony /bio)
  const interactiveSelectors = [
    ".nav-menu a",
    ".nav-dropdown-toggle",
    ".nav-dropdown-menu a",
    ".btn",
    "button",
    ".ambient-corner-dock",
    ".social-link",
    ".hub-btn",
    ".nav-toggle",
    ".bio-link-item",
    ".bio-social-btn",
    ".bio-avatar"
  ].join(",");

  document.querySelectorAll(interactiveSelectors).forEach(el => {
    // pointerdown daje natychmiastową reakcję dźwiękową zanim przeglądarka zacznie nawigację
    el.addEventListener("pointerdown", () => {
      playClickSound();
    });
  });
}

function initAmbientPlayer() {
  const dock = document.getElementById("ambientCornerDock");
  const audio = document.getElementById("ambientAudio");
  if (!dock || !audio) return;

  const icon = dock.querySelector(".ambient-icon");
  const status = dock.querySelector(".ambient-status");

  // Ikony wektorowe (symbole) dla Ambientu
  const symbolMuted = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line></svg>`;
  const symbolPlaying = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>`;

  let fadeInterval = null;
  // Głośność ambientu w tle obniżona o 15% (do poziomu 0.15 / 15%)
  const defaultAmbientVolume = 0.15;
  const targetMaxVolume = () => parseFloat(sessionStorage.getItem("hexit_ambient_volume") || defaultAmbientVolume.toString());
  const fadeStepTime = 40; // ms
  const fadeDuration = 800; // płynne wejście

  // Ciągły zapis pozycji odtwarzania do sessionStorage
  audio.addEventListener("timeupdate", () => {
    if (!audio.paused && audio.currentTime > 0) {
      sessionStorage.setItem("hexit_ambient_time", audio.currentTime.toString());
    }
  });

  window.addEventListener("beforeunload", () => {
    if (!audio.paused) {
      sessionStorage.setItem("hexit_ambient_time", audio.currentTime.toString());
    }
  });

  const clearFade = () => {
    if (fadeInterval) {
      clearInterval(fadeInterval);
      fadeInterval = null;
    }
  };

  const fadeIn = async (isTransition = false) => {
    clearFade();

    // Przywróć dokładną sekundę utworu
    const savedTime = parseFloat(sessionStorage.getItem("hexit_ambient_time") || "0");
    if (savedTime && !isNaN(savedTime) && isFinite(savedTime)) {
      audio.currentTime = savedTime;
    }

    const currentTarget = targetMaxVolume();
    const volumeStep = currentTarget / (fadeDuration / fadeStepTime);

    if (isTransition) {
      audio.volume = currentTarget;
    } else {
      audio.volume = 0;
    }

    try {
      await audio.play();
      updateUI(true);
      sessionStorage.setItem("hexit_ambient_playing", "true");

      if (!isTransition) {
        fadeInterval = setInterval(() => {
          if (audio.volume + volumeStep < currentTarget) {
            audio.volume = Math.min(currentTarget, audio.volume + volumeStep);
          } else {
            audio.volume = currentTarget;
            clearFade();
          }
        }, fadeStepTime);
      }
    } catch (err) {
      console.warn("Autoplay / audio policy on navigation:", err);
      updateUI(false);

      const resumeOnFirstTouch = () => {
        fadeIn(true);
        window.removeEventListener("pointerdown", resumeOnFirstTouch);
        window.removeEventListener("keydown", resumeOnFirstTouch);
      };
      window.addEventListener("pointerdown", resumeOnFirstTouch, { once: true });
      window.addEventListener("keydown", resumeOnFirstTouch, { once: true });
    }
  };

  const fadeOut = () => {
    clearFade();
    sessionStorage.setItem("hexit_ambient_playing", "false");
    updateUI(false);

    const currentTarget = targetMaxVolume();
    const volumeStep = currentTarget / (fadeDuration / fadeStepTime);

    fadeInterval = setInterval(() => {
      if (audio.volume - volumeStep > 0.02) {
        audio.volume = Math.max(0, audio.volume - volumeStep);
      } else {
        audio.volume = 0;
        audio.pause();
        clearFade();
      }
    }, fadeStepTime);
  };

  const updateUI = (playing) => {
    if (playing) {
      dock.classList.add("is-playing");
      dock.setAttribute("aria-label", "Wycisz ambient w tle");
      if (icon) icon.innerHTML = symbolPlaying;
      if (status) status.textContent = "Odtwarzanie (Harmony)";
    } else {
      dock.classList.remove("is-playing");
      dock.setAttribute("aria-label", "Włącz ambient w tle");
      if (icon) icon.innerHTML = symbolMuted;
      if (status) status.textContent = "Kliknij, aby włączyć";
    }
  };

  // Obsługa suwaka głośności na hover
  const volSlider = dock.querySelector(".ambient-vol-slider");
  let userVolume = parseFloat(sessionStorage.getItem("hexit_ambient_volume") || defaultAmbientVolume.toString());

  if (volSlider) {
    volSlider.value = Math.round(userVolume * 100);
    volSlider.addEventListener("input", (e) => {
      userVolume = parseFloat(e.target.value) / 100;
      audio.volume = userVolume;
      sessionStorage.setItem("hexit_ambient_volume", userVolume.toString());
    });
    // Zabezpieczenie: kliknięcie w suwak nie przełącza stanu odtwarzania doku
    volSlider.addEventListener("click", (e) => e.stopPropagation());
    volSlider.addEventListener("pointerdown", (e) => e.stopPropagation());
  }

  dock.addEventListener("click", (e) => {
    if (e.target.closest(".ambient-vol-wrap")) return;
    if (audio.paused || dock.classList.contains("is-playing") === false) {
      fadeIn(false);
    } else {
      fadeOut();
    }
  });

  // Czy ambient był włączony w tej sesji przeglądania?
  const isPlayingSession = sessionStorage.getItem("hexit_ambient_playing") === "true";
  if (isPlayingSession) {
    fadeIn(true);
  }
}

// Inicjalizacja szybkiego odtwarzacza w kafelkach wydań (np. na stronie głównej)
document.addEventListener("DOMContentLoaded", function () {
  const releaseBtn = document.getElementById("releasePlayBtn");
  if (!releaseBtn) return;

  const playIcon = document.getElementById("releasePlayIcon");
  const trackBar = document.getElementById("releaseTrackBar");
  const trackFill = document.getElementById("releaseTrackFill");
  const currentTimeEl = document.getElementById("releaseCurrentTime");
  const totalDurationEl = document.getElementById("releaseTotalDuration");
  const audioSrc = releaseBtn.getAttribute("data-audio-src") || "Sounds/Harmony.mp3";

  let releaseAudio = document.getElementById("globalReleaseAudio");
  if (!releaseAudio) {
    releaseAudio = new Audio(audioSrc);
    releaseAudio.id = "globalReleaseAudio";
    releaseAudio.preload = "metadata";
  }

  const playSvg = '<path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/>';
  const pauseSvg = '<path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/>';

  const formatSecs = (sec) => {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  releaseBtn.addEventListener("click", function () {
    if (releaseAudio.paused) {
      releaseAudio.play().then(() => {
        if (playIcon) playIcon.innerHTML = pauseSvg;
      }).catch(err => console.log("Audio play error:", err));
    } else {
      releaseAudio.pause();
      if (playIcon) playIcon.innerHTML = playSvg;
    }
  });

  releaseAudio.addEventListener("timeupdate", function () {
    if (releaseAudio.duration) {
      const pct = (releaseAudio.currentTime / releaseAudio.duration) * 100;
      if (trackFill) trackFill.style.width = pct + "%";
      if (currentTimeEl) currentTimeEl.textContent = formatSecs(releaseAudio.currentTime);
      if (totalDurationEl) totalDurationEl.textContent = formatSecs(releaseAudio.duration);
    }
  });

  releaseAudio.addEventListener("ended", function () {
    if (playIcon) playIcon.innerHTML = playSvg;
    if (trackFill) trackFill.style.width = "0%";
    if (currentTimeEl) currentTimeEl.textContent = "0:00";
  });

  if (trackBar) {
    trackBar.addEventListener("click", function (e) {
      if (releaseAudio.duration) {
        const rect = trackBar.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        releaseAudio.currentTime = pos * releaseAudio.duration;
      }
    });
  }
});

// ==========================================
// SYSTEM TŁUMACZEŃ (PL / EN I18N SYSTEM)
// ==========================================
(function initI18n() {
  const UI_DICT = {
    pl: {
      nav_start: "Start",
      nav_about: "O mnie",
      nav_releases: "Wydania",
      nav_projects: "Projekty",
      nav_contact: "Kontakt",
      nav_gamedev: "Game Dev",
      nav_music: "Muzyka",
      all_releases_breadcrumb: "← Wszystkie Wydania & STEMS",
      stems_package_title: "Pobierz STEMS (Do Remiksów)",
      stems_package_desc: "Pobierz kompletną paczkę wielościeżkową lub pobieraj pojedyncze ścieżki osobno poniżej:",
      download_zip: "Pobierz Paczkę STEMS (.ZIP)",
      download_single_title: "Pobierz pojedyncze ścieżki osobno (WAV / MP3):",
      visuals_title: "Oficjalne Arty i Tapety do Pobrania",
      visuals_desc: "Pobierz oficjalne materiały wizualne w pełnej rozdzielczości: okładkę albumu, tapetę na komputer oraz grafikę pionową na ekran blokady smartfona.",
      btn_zoom: "Powiększ",
      btn_download: "Pobierz ↓",
      btn_download_arrow: "Pobierz &darr;",
      meta_bpm: "Tempo",
      meta_key: "Tonacja",
      meta_duration: "Długość",
      meta_quality: "Jakość Mastera",
      meta_genre: "Gatunek",
      meta_producer: "Producent",
      meta_stems_fmt: "Format STEMS",
      meta_heading: "Metadane Studyjne",
      listen_full: "Pełny Odsłuch Audio",
      listen_sub: "Plik preview w wysokiej jakości",
      about_track_heading: "O utworze & Procesie Produkcji",
      tab_full_page: "Pełna Strona Wydania & STEMS",
      tab_smartlink: "Widok Smartlink / Bio",
      yt_box_title: "Content ID Free • Muzyka bez roszczeń (Tylko na YouTube)",
      yt_box_desc: "Utwór jest w 100% bezpieczny od roszczeń praw autorskich dla twórców wideo — możesz bez obaw używać go jako darmowy podkład w swoich materiałach na platformie YouTube (wystarczy podać w opisie autora).",
      catalog_eyebrow: "Katalog Wydawniczy",
      catalog_title: "Wszystkie Wydania & Ścieżki",
      catalog_desc: "Kliknij w okładkę dowolnego projektu, aby sprawdzić szczegóły, odsłuch i materiały.",
      btn_release_page: "Strona Wydania →",
      btn_smartlink_view: "Widok Smartlink / Bio ↗"
    },
    en: {
      nav_start: "Home",
      nav_about: "About",
      nav_releases: "Releases",
      nav_projects: "Projects",
      nav_contact: "Contact",
      nav_gamedev: "Game Dev",
      nav_music: "Music",
      all_releases_breadcrumb: "← All Releases & STEMS",
      stems_package_title: "Download STEMS (For Remixes)",
      stems_package_desc: "Download complete multitrack package or grab individual stems separately below:",
      download_zip: "Download STEMS Pack (.ZIP)",
      download_single_title: "Download individual audio stems (WAV / MP3):",
      visuals_title: "Official Artworks & Wallpapers to Download",
      visuals_desc: "Download official high-resolution visuals: album cover, desktop wallpaper, and smartphone lockscreen artwork.",
      btn_zoom: "Zoom",
      btn_download: "Download ↓",
      btn_download_arrow: "Download &darr;",
      meta_bpm: "Tempo",
      meta_key: "Key",
      meta_duration: "Duration",
      meta_quality: "Master Quality",
      meta_genre: "Genre",
      meta_producer: "Producer",
      meta_stems_fmt: "STEMS Format",
      meta_heading: "Studio Metadata",
      listen_full: "Full Audio Preview",
      listen_sub: "High quality preview file",
      about_track_heading: "About Track & Production Process",
      tab_full_page: "Full Release Page & STEMS",
      tab_smartlink: "Smartlink / Bio View",
      yt_box_title: "Content ID Free • Claim-Free Music (YouTube Only)",
      yt_box_desc: "This track is 100% safe from copyright claims for video creators — feel free to use it as background music in your YouTube videos (credit required in description).",
      catalog_eyebrow: "Release Catalog",
      catalog_title: "All Releases & Stems",
      catalog_desc: "Click any project cover to check details, stream audio, and download creator assets.",
      btn_release_page: "Release Page →",
      btn_smartlink_view: "Smartlink / Bio View ↗"
    }
  };

  function applyLanguage(lang) {
    document.documentElement.lang = lang;
    try {
      localStorage.setItem('hexit_lang', lang);
    } catch (e) {}

    // Update active state on language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
      const bLang = btn.getAttribute('data-lang') || btn.getAttribute('data-lang-target');
      const isActive = (bLang === lang);
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });

    // Toggle language content blocks
    document.querySelectorAll('.lang-content-pl').forEach(el => {
      el.style.display = lang === 'pl' ? '' : 'none';
    });
    document.querySelectorAll('.lang-content-en').forEach(el => {
      el.style.display = lang === 'en' ? '' : 'none';
    });

    // Toggle inline elements with data-pl and data-en
    document.querySelectorAll('[data-pl][data-en]').forEach(el => {
      const val = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-pl');
      if (val !== null) {
        if (el.children.length === 0) {
          el.textContent = val;
        } else {
          el.innerHTML = val;
        }
      }
    });

    // Dictionary lookup elements [data-i18n]
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (UI_DICT[lang] && UI_DICT[lang][key]) {
        el.textContent = UI_DICT[lang][key];
      }
    });

    // Standard Navigation menu links translation
    const navStart = document.querySelector('.nav-menu a[href="index.html"]');
    if (navStart && !navStart.hasAttribute('data-i18n')) {
      navStart.textContent = lang === 'en' ? "Home" : "Start";
    }
    const navAbout = document.querySelector('.nav-menu a[href="about.html"]');
    if (navAbout && !navAbout.hasAttribute('data-i18n')) {
      navAbout.textContent = lang === 'en' ? "About" : "O mnie";
    }
    const navWydania = document.querySelector('.nav-menu a[href="wydania.html"]');
    if (navWydania && !navWydania.hasAttribute('data-i18n')) {
      navWydania.textContent = lang === 'en' ? "Releases" : "Wydania";
    }
    const navProjects = document.querySelector('.nav-menu a[href="index.html#projekty"]');
    if (navProjects && !navProjects.hasAttribute('data-i18n')) {
      navProjects.textContent = lang === 'en' ? "Projects" : "Projekty";
    }
    const navContact = document.querySelector('.nav-menu a[href="index.html#kontakt"], .nav-menu a[href="kontakt.html"]');
    if (navContact && !navContact.hasAttribute('data-i18n')) {
      navContact.textContent = lang === 'en' ? "Contact" : "Kontakt";
    }

    // Comprehensive translations for index.html
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
      const cTag = heroSection.querySelector('.creator-tag');
      if (cTag) cTag.textContent = lang === 'en' ? "Music Producer & Sound Designer" : "Producent Muzyczny & Sound Designer";

      const nTag = heroSection.querySelector('.now-tag');
      if (nTag) nTag.textContent = lang === 'en' ? "NOX & Samplix Projects" : "Projekty NOX & Samplix";

      const hTitle = heroSection.querySelector('.hero-title');
      if (hTitle) hTitle.textContent = lang === 'en' ? "Music Production, Sound Design & Audio Engineering." : "Produkcja Muzyczna, Sound Design & Autorskie Projekty Audio.";

      const hSub = heroSection.querySelector('.hero-subtitle');
      if (hSub) {
        hSub.innerHTML = lang === 'en'
          ? "Hi! My name is Olaf \"Hexit Rely\" Zawadzki. My world revolves around original music production, composition, hybrid sound design (NOX projects), creating Samplix audio tools, gaming, and late-night streams on <em>Its Hexit IRL</em>."
          : "Cześć! Nazywam się Olaf \"Hexit Rely\" Zawadzki. Mój świat to autorska produkcja muzyczna, kompozycja, hybrydowy sound design (projekty NOX), tworzenie narzędzi audio Samplix oraz gaming i nocne streamy na kanale <em>Its Hexit IRL</em>.";
      }

      const btnWydania = heroSection.querySelector('.hero-buttons a[href="wydania.html"]');
      if (btnWydania) {
        btnWydania.innerHTML = lang === 'en'
          ? '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M9 13c0 1.105-1.12 2-2.5 2S4 14.105 4 13s1.12-2 2.5-2 2.5.895 2.5 2z"/><path fill-rule="evenodd" d="M9 3v10H8V3h1z"/><path d="M8 2.82a1 1 0 0 1 .804-.98l3-.6A1 1 0 0 1 13 2.22V4L8 5V2.82z"/></svg> Releases &amp; STEMS &rarr;'
          : '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M9 13c0 1.105-1.12 2-2.5 2S4 14.105 4 13s1.12-2 2.5-2 2.5.895 2.5 2z"/><path fill-rule="evenodd" d="M9 3v10H8V3h1z"/><path d="M8 2.82a1 1 0 0 1 .804-.98l3-.6A1 1 0 0 1 13 2.22V4L8 5V2.82z"/></svg> Wydania &amp; STEMS &rarr;';
      }

      const btnLab = heroSection.querySelector('.hero-buttons a[href="#laboratorium"]');
      if (btnLab) btnLab.textContent = lang === 'en' ? "Explore Craft & Projects" : "Poznaj warsztat & projekty";

      const hubLbl = heroSection.querySelector('.hub-label');
      if (hubLbl) hubLbl.innerHTML = lang === 'en' ? "Stay up to date &bull; My platforms:" : "Bądź na bieżąco &bull; Moje platformy:";
    }

    // About Section (Cześć, tu Olaf)
    const aboutSec = document.querySelector('#o-mnie, .about-story-section');
    if (aboutSec) {
      const eyebrow = aboutSec.querySelector('.section-eyebrow');
      if (eyebrow) eyebrow.textContent = lang === 'en' ? "My Journey & Philosophy" : "Moja droga i filozofia";

      const title = aboutSec.querySelector('.hero-title, h2');
      if (title) title.textContent = lang === 'en' ? "Hi, I'm Olaf." : "Cześć, tu Olaf.";

      const p = aboutSec.querySelector('.about-story-text p');
      if (p) {
        p.innerHTML = lang === 'en'
          ? "Online, I go by <strong>HEXIT RELY</strong>. For over 7 years I have explored sound, sharing my passion for sound design and music production live on stream."
          : "W sieci funkcjonuję jako <strong>HEXIT RELY</strong>. Od ponad 7 lat zgłębiam dźwięk, a swoją pasją do sound designu i tworzenia muzyki dzielę się na żywo podczas streamów.";
      }

      const btn = aboutSec.querySelector('.about-story-text a.btn');
      if (btn) btn.innerHTML = lang === 'en' ? "Learn more about me &rarr;" : "Poznaj mnie bliżej &rarr;";

      const pill = aboutSec.querySelector('.hero-status-pill span');
      if (pill) pill.textContent = lang === 'en' ? "Music • Streaming • Gaming" : "Muzyka • Streaming • Gaming";
    }

    // Three Pillars of Craft
    const pillarsWrap = document.querySelector('.about-story-section .now-cards-grid');
    if (pillarsWrap) {
      const headerWrap = pillarsWrap.previousElementSibling;
      if (headerWrap) {
        const eb = headerWrap.querySelector('.section-eyebrow');
        if (eb) eb.textContent = lang === 'en' ? "Pillars of HEXIT RELY" : "Filary HEXIT RELY";
        const st = headerWrap.querySelector('.section-title, h3');
        if (st) st.textContent = lang === 'en' ? "Three Passions, One Cohesive Ecosystem" : "Trzy pasje, jeden spójny organizm";
        const sd = headerWrap.querySelector('.section-desc');
        if (sd) sd.textContent = lang === 'en'
          ? "I don't believe in confining myself to a single box. My world is driven by the synergy between digital audio, transparent community connection, and physical craft."
          : "Nie wierzę w zamykanie się w jednej szufladce. Mój świat napędza synergia między cyfrowym audio, transparentnym kontaktem i pracą fizyczną.";
      }

      const cards = pillarsWrap.querySelectorAll('.now-card');
      if (cards.length >= 3) {
        const c1_h = cards[0].querySelector('h4');
        if (c1_h) c1_h.textContent = lang === 'en' ? "1. Music & Experimentation" : "1. Muzyka & Eksperyment";
        const c1_p = cards[0].querySelector('p');
        if (c1_p) c1_p.textContent = lang === 'en'
          ? "My sound blends dark electronics, glitch textures, organic instruments, and cinematic sound design. I release original music and score indie games."
          : "Moje brzmienie to połączenie mrocznej elektroniki, glitchowych tekstur, organicznych instrumentów i filmowego sound designu. Tworzę autorskie wydawnictwa oraz udźwiękowienie do gier niezależnych.";
        const c1_a = cards[0].querySelector('.now-card-link');
        if (c1_a) c1_a.textContent = lang === 'en' ? "View Music Portfolio ↗" : "Zobacz muzyczne portfolio ↗";

        const c2_h = cards[1].querySelector('h4');
        if (c2_h) c2_h.textContent = lang === 'en' ? "2. Streaming & Transparency" : "2. Streaming & Transparentność";
        const c2_p = cards[1].querySelector('p');
        if (c2_p) c2_p.textContent = lang === 'en'
          ? "I stream because I value authenticity. On the main channel we produce music and edit video, while on the second channel we host longer sessions (Minecraft, chill evenings, discussions). Building a mature community."
          : "Streamuję, bo cenię autentyczność. Na kanale głównym tworzymy muzykę i montujemy filmy, a na drugim odpalamy dłuższe sesje (Minecraft, chillowe wieczory, dyskusje). Budujemy zgraną, dojrzałą społeczność.";
        const c2_a = cards[1].querySelector('.now-card-link');
        if (c2_a) c2_a.innerHTML = lang === 'en' ? "Join the Stream &rarr;" : "Wpadnij na stream &rarr;";

        const c3_h = cards[2].querySelector('h4');
        if (c3_h) c3_h.textContent = lang === 'en' ? "3. DIY & Creativity" : "3. DIY & Kreatywnosć";
        const c3_p = cards[2].querySelector('p');
        if (c3_p) c3_p.textContent = lang === 'en'
          ? "Creativity cannot be boxed in. Thanks to it, I sip coffee over FL Studio in the morning, code this site in the afternoon, stream in the evening, and deploy a new local network service at night just because."
          : "kreatywnosć to coś czego nie da się szufladkować. Dzięki niej z rana pije kawe przy fl studio popołudniem piszę tą stronę a wieczorem strimuje aby w nocy stwierdzić że pora dodac nową usługę w sieci lokalnej bo czemu by nie.";
        const c3_a = cards[2].querySelector('.now-card-link');
        if (c3_a) c3_a.innerHTML = lang === 'en' ? "Behind the scenes & process logs &rarr;" : "Kulisy & wpisy z procesu &rarr;";
      }
    }

    // Lab Section (#laboratorium)
    const labSec = document.querySelector('#laboratorium');
    if (labSec) {
      const eb = labSec.querySelector('.section-eyebrow');
      if (eb) eb.textContent = lang === 'en' ? "My Craft & Pillars" : "Mój Warsztat & Filary";
      const st = labSec.querySelector('.section-title');
      if (st) st.textContent = lang === 'en' ? "Music, Software & Gaming" : "Muzyka, Software & Gaming";
      const sd = labSec.querySelector('.section-desc');
      if (sd) sd.textContent = lang === 'en'
        ? "Three domains where I connect audio engineering with a passion for gaming and tool creation. Toggle tabs to explore my workflow:"
        : "Trzy obszary, w których łączę inżynierię dźwięku z pasją do gamingu i tworzenia narzędzi. Przełączaj zakładki, by poznać mój proces:";

      const tabs = labSec.querySelectorAll('.code-lab-tab');
      if (tabs.length >= 3) {
        tabs[0].textContent = lang === 'en' ? "Music Production" : "Produkcja Muzyczna";
        tabs[1].textContent = lang === 'en' ? "Audio Software" : "Oprogramowanie Audio";
        tabs[2].textContent = lang === 'en' ? "Minecraft & Streaming" : "Minecraft & Streaming";
      }

      // Panel 1: Piano roll
      const p1 = document.querySelector('#lab-pianoroll');
      if (p1) {
        const p1_eb = p1.querySelector('.section-eyebrow');
        if (p1_eb) p1_eb.textContent = lang === 'en' ? "Composition & Sound Design" : "Kompozycja & Sound Design";
        const p1_h = p1.querySelector('h3');
        if (p1_h) p1_h.textContent = lang === 'en' ? "Piano Roll — How I Craft My Sound" : "Piano Roll — jak buduję brzmienie";
        const p1_ps = p1.querySelectorAll('.pianoroll-text p');
        if (p1_ps.length >= 2) {
          p1_ps[0].textContent = lang === 'en'
            ? "Every track and sound design project begins in the sequencer grid. Precise semitone arrangement, velocity control, and hybrid synthesis form the core of my music releases and sample libraries."
            : "Każdy utwór i sound design zaczyna się w siatce sekwencera. Precyzyjne układanie półtonów, kontrola dynamiki (velocity) i synteza hybrydowa to fundament moich produkcji muzycznych oraz bibliotek sampli.";
          p1_ps[1].textContent = lang === 'en'
            ? "I work primarily in Ableton Live Suite and FL Studio, combining digital processing with analogue MIDI hardware and custom FX chains."
            : "Pracuję głównie w Ableton Live Suite oraz FL Studio, łącząc cyfrowe przetwarzanie z analogowymi kontrolerami MIDI i autorskimi łańcuchami efektów FX.";
        }
        const p1_tags = p1.querySelectorAll('.pianoroll-text .now-tag');
        if (p1_tags.length >= 4) {
          p1_tags[0].textContent = lang === 'en' ? "Composition" : "Kompozycja";
          p1_tags[1].textContent = lang === 'en' ? "Sound Synthesis" : "Synteza Dźwięku";
          p1_tags[2].textContent = "Ableton Live & FL Studio";
          p1_tags[3].textContent = "Sound Design NOX";
        }
        const p1_a1 = p1.querySelector('a.btn-primary');
        if (p1_a1) p1_a1.textContent = lang === 'en' ? "Listen on Spotify ↗" : "Posłuchaj na Spotify ↗";
        const p1_a2 = p1.querySelector('a.btn-secondary');
        if (p1_a2) p1_a2.textContent = lang === 'en' ? "NOX Music Portfolio ↗" : "Portfolio Muzyczne NOX ↗";
      }

      // Panel 2: Code 3D / Samplix
      const p2 = document.querySelector('#lab-code3d');
      if (p2) {
        const p2_eb = p2.querySelector('.section-eyebrow');
        if (p2_eb) p2_eb.textContent = "Software & DSP";
        const p2_h = p2.querySelector('h3');
        if (p2_h) p2_h.textContent = lang === 'en' ? "Samplix Engine — Audio Analysis & Algorithms" : "Silnik Samplix — analiza audio i algorytmy";
        const p2_ps = p2.querySelectorAll('.code3d-text p');
        if (p2_ps.length >= 2) {
          p2_ps[0].textContent = lang === 'en'
            ? "Samplix is my proprietary software tool designed for producers wrestling with hundreds of gigabytes of one-shots and loops."
            : "Samplix to moje autorskie narzędzie programistyczne, zaprojektowane dla producentów borykających się z setkami gigabajtów one-shotów i pętli.";
          p2_ps[1].textContent = lang === 'en'
            ? "The built-in audio engine instantly detects key (chroma CQT), estimates BPM, and indexes samples in a fraction of a second, enabling drag-and-drop straight into your DAW."
            : "Wbudowany silnik analizy audio natychmiast wykrywa tonację (chroma CQT), estymuje tempo BPM i indeksuje próbki w ułamku sekundy, umożliwiając błyskawiczne przeciąganie plików bezpośrednio do DAW.";
        }
        const p2_tags = p2.querySelectorAll('.code3d-text .now-tag');
        if (p2_tags.length >= 3) {
          p2_tags[0].textContent = "Python Audio DSP";
          p2_tags[1].textContent = lang === 'en' ? "Key & BPM Detection" : "Detekcja Tonacji & BPM";
          p2_tags[2].textContent = lang === 'en' ? "Samplix Ecosystem" : "Ekosystem Samplix";
        }
      }

      // Panel 3: Minecraft & Gaming
      const p3 = document.querySelector('#lab-pixelart');
      if (p3) {
        const p3_eb = p3.querySelector('.section-eyebrow');
        if (p3_eb) p3_eb.textContent = "Gaming, Dev & Streaming";
        const p3_h = p3.querySelector('h3');
        if (p3_h) p3_h.textContent = lang === 'en' ? "Minecraft Survival, Plugins & Community" : "Minecraft Survival, Pluginy & Społeczność";
        const p3_ps = p3.querySelectorAll('.pixelart-text p');
        if (p3_ps.length >= 2) {
          p3_ps[0].innerHTML = lang === 'en'
            ? "The <strong>Its Hexit IRL</strong> YouTube channel features multi-hour Minecraft survival sessions as VOD archives from live broadcasts. It's not just gaming — it's coding: I develop custom plugins and server scripts, develop gameplay mechanics, optimize server performance, and enjoy survival gameplay."
            : "Na kanale <strong>Its Hexit IRL</strong> (YouTube) znajdują się wielogodzinne sesje survivalu w Minecraft w formie zapisów VOD z transmisji na żywo. To nie tylko granie — to także kodowanie: tworzę autorskie pluginy i skrypty serwerowe, rozwijam niestandardowe mechaniki rozgrywki oraz optymalizuję świat serwera, czy poprostu chill na survivalu co także jest potrzebne.";
          p3_ps[1].textContent = lang === 'en'
            ? "Together with the community, we build bases, automate systems, and spend time in an authentic, mature atmosphere during late-night streams."
            : "Wspólnie ze społecznością budujemy bazy, automatyzacje i spędzamy czas w bezpretensjonalnej, dojrzałej atmosferze podczas nocnych streamów.";
        }
        const p3_tags = p3.querySelectorAll('.pixelart-text .now-tag');
        if (p3_tags.length >= 3) {
          p3_tags[0].textContent = lang === 'en' ? "Survival & Community" : "Survival & Społeczność";
          p3_tags[1].textContent = lang === 'en' ? "Plugins & Scripts" : "Pluginy & Skrypty";
          p3_tags[2].textContent = lang === 'en' ? "VOD Archives" : "Zapisy VOD";
        }
        const p3_a = p3.querySelector('.pixelart-text a.btn');
        if (p3_a) p3_a.textContent = lang === 'en' ? "Watch on YouTube: Its Hexit IRL (@HexitIrl) ↗" : "Oglądaj na YouTube: Its Hexit IRL (@HexitIrl) ↗";
      }
    }

    // Projects Ecosystem Section (#projekty)
    const projSec = document.querySelector('#projekty');
    if (projSec) {
      const eb = projSec.querySelector('.section-eyebrow');
      if (eb) eb.textContent = lang === 'en' ? "Project Ecosystem" : "Ekosystem projektów";
      const st = projSec.querySelector('.section-title');
      if (st) st.textContent = lang === 'en' ? "Tools & Studio" : "Narzędzia i Studio";
      const sd = projSec.querySelector('.section-desc');
      if (sd) sd.textContent = lang === 'en'
        ? "I develop original software for music producers and handle audio production from recording to mix, mastering, and complete sound design from scratch."
        : "Tworzę autorskie oprogramowanie dla producentów oraz sam zajmuję się twórczością od realizacji nagran przez mix mastering czy czystą produkcję od zera.";

      // Samplix Card
      const samplixCard = projSec.querySelector('.samplix-card');
      if (samplixCard) {
        const badge = samplixCard.querySelector('.ecosystem-badge');
        if (badge) badge.textContent = lang === 'en' ? "Software from 'Lix' Series" : "Oprogramowanie z serii \"Lix\"";
        const ps = samplixCard.querySelectorAll('p');
        if (ps.length >= 2) {
          ps[0].textContent = lang === 'en'
            ? "Got gigabytes of samples and wasting hours looking for the right one-shot? Samplix is my proprietary software tool, designed by a producer for producers — to organize your audio library and speed up your DAW workflow without taking your hands off the keyboard."
            : "Masz gigabajty sampli i tracisz godziny na szukanie odpowiedniego one-shota? Samplix to moje autorskie narzędzie software'owe, zaprojektowane przez producenta dla producentów — żeby ogarnąć bibliotekę audio i przyspieszyć pracę w DAW bez odrywania rąk od klawiatury.";
          ps[1].textContent = lang === 'en'
            ? "Samplix is part of a larger 'Lix' tool series — I build them independently, step by step, solving real friction points in daily production."
            : "Samplix to część większej serii narzędzi \"Lix\" — buduję je samodzielnie, krok po kroku, rozwiązując problemy, które sam napotykam przy codziennej produkcji.";
        }
        const feats = samplixCard.querySelectorAll('.samplix-features-list li');
        if (feats.length >= 6) {
          feats[0].textContent = lang === 'en' ? "Instant folder indexing" : "Błyskawiczne indeksowanie folderów";
          feats[1].textContent = lang === 'en' ? "Smart sample tagging" : "Inteligentne tagowanie próbek";
          feats[2].textContent = lang === 'en' ? "Drag & drop straight into DAW" : "Przeciąganie bezpośrednio do DAW";
          feats[3].textContent = lang === 'en' ? "Lightweight, minimal UI" : "Lekki i minimalistyczny interfejs";
          feats[4].textContent = lang === 'en' ? "Built-in waveform preview" : "Wbudowany podgląd fal audio";
          feats[5].textContent = lang === 'en' ? "Full integration with NOX sample packs" : "Pełna integracja z sample packami NOX";
        }
        const btn = samplixCard.querySelector('a.btn');
        if (btn) btn.textContent = lang === 'en' ? "Go to Samplix ↗" : "Przejdź do Samplix ↗";
      }

      // 4NOX WAV Card
      const noxCard = projSec.querySelector('.nox-service-card');
      if (noxCard) {
        const pill = noxCard.querySelector('.service-notice-pill');
        if (pill) pill.textContent = lang === 'en' ? "Studio & Production Brand" : "Marka Studyjna & Produkcyjna";
        const ps = noxCard.querySelectorAll('p');
        if (ps.length >= 2) {
          ps[0].textContent = lang === 'en'
            ? "If you are looking for professional commercial services — custom music, sound design for games and media, mixing, mastering, audio restoration, or dedicated sound libraries — my full NOX studio profile (4noxwav) is hosted at a dedicated address."
            : "Jeśli szukasz profesjonalnych usług komercyjnych — autorskiej muzyki, sound designu do gier i mediów, miksu, masteringu, czyszczenia nagrań czy dedykowanych bibliotek brzmień — cały mój profil studyjny NOX (4noxwav) znajduje się pod osobnym adresem.";
          ps[1].textContent = lang === 'en'
            ? "hexitrely.pl is my personal artist and streaming space. Rates, service packages, and dedicated commercial inquiries are available on 4noxwav.com and my external portfolio."
            : "hexitrely.pl to moja przestrzeń autorska i streamingowa. Cenniki, pakiety i dedykowane zlecenia komercyjne NOX znajdziesz bezpośrednio na 4noxwav.com oraz w portfolio zewnętrznym.";
        }
        const btns = noxCard.querySelectorAll('a.btn');
        if (btns.length >= 2) {
          btns[0].textContent = lang === 'en' ? "NOX Studio at 4noxwav.com ↗" : "Studio NOX na 4noxwav.com ↗";
          btns[1].textContent = lang === 'en' ? "Portfolio NOX ↗" : "Portfolio NOX ↗";
        }
      }
    }

    // Contact Section (#kontakt)
    const contactSec = document.querySelector('#kontakt');
    if (contactSec) {
      const eb = contactSec.querySelector('.section-eyebrow');
      if (eb) eb.textContent = lang === 'en' ? "Let's Talk" : "Porozmawiajmy";
      const st = contactSec.querySelector('.section-title');
      if (st) st.textContent = lang === 'en' ? "Get in Touch" : "Skontaktuj się ze mną";
      const sd = contactSec.querySelector('.section-desc');
      if (sd) sd.textContent = lang === 'en'
        ? "Have a question about music, Samplix, streaming, or collaboration?"
        : "Masz pytanie o muzykę, Samplix, streaming lub propozycję współpracy?";

      const leftCardH3 = contactSec.querySelector('.content-card h3');
      if (leftCardH3) leftCardH3.textContent = lang === 'en' ? "Direct Email Address:" : "Bezpośredni adres e-mail:";
      const leftCardP = contactSec.querySelector('.content-card p');
      if (leftCardP) leftCardP.textContent = lang === 'en' ? "The fastest way to reach out for project and business inquiries:" : "Najszybsza forma kontaktu w sprawach projektowych i biznesowych:";

      const findH4 = contactSec.querySelector('.info-pill-box h4');
      if (findH4) findH4.textContent = lang === 'en' ? "Where else can you find me?" : "Gdzie jeszcze mnie znajdziesz?";

      const formH3 = contactSec.querySelector('form h3, .content-card:nth-of-type(2) h3');
      if (formH3) formH3.textContent = lang === 'en' ? "Send a Quick Message" : "Wyślij szybką wiadomość";

      const labels = contactSec.querySelectorAll('form label');
      if (labels.length >= 3) {
        labels[0].textContent = lang === 'en' ? "Your Name / Handle:" : "Twoje imię / Nick:";
        labels[1].textContent = lang === 'en' ? "Your Email:" : "Twój e-mail:";
        labels[2].textContent = lang === 'en' ? "Message:" : "Wiadomość:";
      }
      const submitBtn = contactSec.querySelector('form button[type="submit"]');
      if (submitBtn) submitBtn.innerHTML = lang === 'en' ? "Send Message &rarr;" : "Wyślij wiadomość &rarr;";
    }

    // Modern Footer translations
    const footer = document.querySelector('.modern-footer');
    if (footer) {
      const fDesc = footer.querySelector('.footer-desc');
      if (fDesc) fDesc.textContent = lang === 'en'
        ? "Official creative space of Olaf \"Hexit Rely\" Zawadzki. Sound, visuals, code, and transparent creative process without pretension."
        : "Oficjalna autorska przestrzeń Olafa \"Hexit Rely\" Zawadzkiego. Dźwięk, obraz, kod i transparentny proces twórczy bez zbędnego zadęcia.";

      const fCols = footer.querySelectorAll('.footer-col h4');
      if (fCols.length >= 3) {
        fCols[0].textContent = lang === 'en' ? "Navigation" : "Nawigacja";
        fCols[1].textContent = lang === 'en' ? "Projects & External" : "Projekty & Zewnętrzne";
        fCols[2].textContent = lang === 'en' ? "Contact" : "Kontakt";
      }

      const fLinks = footer.querySelectorAll('.footer-col:first-of-type ul a');
      if (fLinks.length >= 6) {
        fLinks[0].textContent = lang === 'en' ? "Home" : "Start";
        fLinks[1].textContent = lang === 'en' ? "About & Setup" : "O mnie & Setup";
        fLinks[2].textContent = lang === 'en' ? "Releases & STEMS" : "Wydania & STEMS";
        fLinks[3].textContent = lang === 'en' ? "Samplix Ecosystem" : "Ekosystem Samplix";
        fLinks[4].textContent = "Blog";
        fLinks[5].textContent = lang === 'en' ? "Shop (Soon)" : "Sklep (Wkrótce)";
      }

      const fBottomP = footer.querySelector('.footer-bottom p');
      if (fBottomP) {
        fBottomP.innerHTML = lang === 'en'
          ? '&copy; 2024 &ndash; 2026 Olaf "Hexit Rely" Zawadzki. All rights reserved.'
          : '&copy; 2024 &ndash; 2026 Olaf "Hexit Rely" Zawadzki. Wszelkie prawa zastrzeżone.';
      }

      const fBottomLinks = footer.querySelectorAll('.footer-bottom-links a');
      if (fBottomLinks.length >= 3) {
        fBottomLinks[0].textContent = lang === 'en' ? "Releases & STEMS" : "Wydania & STEMS";
        fBottomLinks[1].textContent = lang === 'en' ? "Privacy Policy" : "Polityka Prywatności";
        fBottomLinks[2].textContent = lang === 'en' ? "Contact" : "Kontakt";
      }
    }

    // Ambient Dock Bar
    const ambientDock = document.querySelector('#ambientCornerDock');
    if (ambientDock) {
      const aTitle = ambientDock.querySelector('.ambient-title');
      if (aTitle) {
        const eqHtml = '<div class="ambient-eq" aria-hidden="true"><span></span><span></span><span></span><span></span></div>';
        aTitle.innerHTML = (lang === 'en' ? "Studio Ambient " : "Ambient Studyjny ") + eqHtml;
      }
      const aStatus = ambientDock.querySelector('.ambient-status');
      if (aStatus && aStatus.textContent.includes('Kliknij')) {
        aStatus.textContent = lang === 'en' ? "Click to play" : "Kliknij, aby włączyć";
      }
    }
  }

  // Attach global listener for language buttons and init
  document.addEventListener('DOMContentLoaded', function () {
    let savedLang = 'pl';
    try {
      savedLang = localStorage.getItem('hexit_lang') || 'pl';
    } catch (e) {}

    // Add click listeners to switcher buttons
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('.lang-btn');
      if (btn) {
        e.preventDefault();
        const targetLang = btn.getAttribute('data-lang') || btn.getAttribute('data-lang-target');
        if (targetLang) {
          applyLanguage(targetLang);
        }
      }
    });

    applyLanguage(savedLang);
  });

  window.hexitSetLang = applyLanguage;
})();




