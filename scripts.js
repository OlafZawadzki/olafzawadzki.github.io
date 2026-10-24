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




