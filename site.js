/**
 * Martian Cylinder Photogrammetry - Public Presentation Website
 * Interactions: Lightbox viewer, BibTeX copy with fallback, smooth navigation
 */

function initSite() {
  // 1. BibTeX Copy to Clipboard (with fallback for file:/// and non-HTTPS origins)
  const copyBtn = document.getElementById('btnCopyBibtex');
  const bibtexCode = document.getElementById('bibtexCode');
  const copyFeedback = document.getElementById('copyFeedback');

  if (copyBtn && bibtexCode) {
    copyBtn.addEventListener('click', () => {
      const textToCopy = bibtexCode.innerText.trim();
      let copySuccess = false;

      function showCopiedFeedback() {
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = `
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <span style="color: #10b981; font-weight: 600;">Copied!</span>
        `;
        if (copyFeedback) copyFeedback.style.display = 'inline';
        setTimeout(() => {
          copyBtn.innerHTML = originalText;
          if (copyFeedback) copyFeedback.style.display = 'none';
        }, 2200);
      }

      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          showCopiedFeedback();
        }).catch(() => {
          fallbackCopy();
        });
      } else {
        fallbackCopy();
      }

      function fallbackCopy() {
        try {
          const textarea = document.createElement('textarea');
          textarea.value = textToCopy;
          textarea.style.position = 'fixed';
          textarea.style.opacity = '0';
          textarea.style.pointerEvents = 'none';
          document.body.appendChild(textarea);
          textarea.select();
          const successful = document.execCommand('copy');
          document.body.removeChild(textarea);
          if (successful) {
            showCopiedFeedback();
          }
        } catch (err) {
          console.error('Fallback clipboard copy failed:', err);
        }
      }
    });
  }

  // 2. Lightbox Modal
  const modalOverlay = document.getElementById('imageModal');
  const modalImg = document.getElementById('modalImg');
  const modalCaption = document.getElementById('modalCaption');
  const modalClose = document.getElementById('modalClose');

  function openModal(src, caption) {
    if (!modalOverlay || !modalImg) return;
    modalImg.src = src;
    if (modalCaption) modalCaption.textContent = caption || '';
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    if (!modalOverlay) return;
    modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  // Bind to evidence cards
  const evidenceMediaList = document.querySelectorAll('.evidence-media');
  evidenceMediaList.forEach((media) => {
    media.addEventListener('click', () => {
      const img = media.querySelector('img');
      const caption = media.getAttribute('data-caption') || (img ? img.alt : '');
      if (img) {
        openModal(img.src, caption);
      }
    });
  });

  if (modalClose) {
    modalClose.addEventListener('click', closeModal);
  }

  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        closeModal();
      }
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay && modalOverlay.classList.contains('active')) {
      closeModal();
    }
  });

  // 3. Navigation link active state tracking on scroll
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  function highlightNavOnScroll() {
    const scrollY = window.pageYOffset;
    sections.forEach((section) => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop - 100;
      const sectionId = section.getAttribute('id');

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLinks.forEach((link) => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', highlightNavOnScroll, { passive: true });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initSite);
} else {
  initSite();
}
