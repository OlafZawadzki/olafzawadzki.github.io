document.addEventListener("DOMContentLoaded", function() {
    // Cookie notice functionality
    var acceptButton = document.getElementById('acceptButton');
    var privacyNotice = document.getElementById('privacyNotice');

    if (acceptButton && privacyNotice) {
        // Check if user has already accepted cookies
        if (localStorage.getItem('cookiesAccepted') === 'true') {
            privacyNotice.classList.add('hidden');
        }

        acceptButton.addEventListener('click', function() {
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
        mailtoLink.addEventListener('click', function(e) {
            // Don't prevent default for mailto links
            console.log('Mailto link clicked:', this.href);
        });
    });

    // Add scroll effect to header
    const header = document.querySelector('.modern-header');
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                header.style.background = 'rgba(17, 24, 39, 0.98)';
                header.style.backdropFilter = 'blur(20px)';
            } else {
                header.style.background = 'rgba(17, 24, 39, 0.95)';
                header.style.backdropFilter = 'blur(10px)';
            }
        });
    }

    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
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
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add click tracking for portfolio items
    document.querySelectorAll('.work-item, .project-card').forEach(item => {
        item.addEventListener('click', function() {
            // Track portfolio item clicks
            console.log('Portfolio item clicked:', this.querySelector('h3')?.textContent);
        });
    });

    // Copy email button on contact page
    const copyEmailBtn = document.getElementById('copyEmailBtn');
    if (copyEmailBtn) {
        copyEmailBtn.addEventListener('click', async function() {
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
document.addEventListener('DOMContentLoaded', function() {
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxTitle = document.getElementById('lightbox-title');
    const lightboxClose = document.getElementById('lightbox-close');

    // Add click handlers to work item images
    const workItems = document.querySelectorAll('.work-item img');
    
    workItems.forEach(img => {
        img.addEventListener('click', function(e) {
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
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
    }
    
    // Close with Escape key
    document.addEventListener('keydown', function(e) {
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







emailjs.init("KhhpDMoVBpGtqgSjM");

const sendEmail = async (event) => {
  event.preventDefault();

  const form = event.target;

  try {
    const response = await emailjs.sendForm(
      "service_kf463es",
      "template_q83n3iv",
      form,

    );
    console.log("Email sent successfully!", response);
    document.getElementById("contact-form").reset();
  } catch (error) {
    console.error("Failed to send email:", error);
  }
};

document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("contact-form")
    .addEventListener("submit", sendEmail);
    

})



  
