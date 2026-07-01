document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.bibtex-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const bibkey = link.getAttribute('href').split('#')[1];
      fetchBibtexEntry(bibkey, link.href);
    });
  });

  function fetchBibtexEntry(bibkey, fileUrl) {
    const bibFileUrl = fileUrl.split('#')[0];

    fetch(bibFileUrl)
      .then(response => response.text())
      .then(bibtexContent => {
        const entry = extractBibtexEntry(bibtexContent, bibkey);
        showBibtexModal(entry, bibkey);
      })
      .catch(error => {
        console.error('Error fetching BibTeX:', error);
        showBibtexModal('Error loading BibTeX entry.', bibkey);
      });
  }

  function extractBibtexEntry(bibtexContent, bibkey) {
    const escapedKey = bibkey.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(@[a-zA-Z]+\\{[^}]*${escapedKey}[^}]*\\{[^}]*\\}.*?)\\n\\n(?=@|$)`, 's');
    const match = bibtexContent.match(regex);

    if (match) {
      let entry = match[1].trim();
      entry = entry.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      return entry;
    }

    const lines = bibtexContent.split('\n');
    let entryLines = [];
    let inEntry = false;

    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes('{' + bibkey + ',')) {
        inEntry = true;
      }
      if (inEntry) {
        entryLines.push(lines[i]);
        if (lines[i].trim() === '}') {
          break;
        }
      }
    }

    if (entryLines.length > 0) {
      return entryLines.join('\n');
    }

    return 'Entry not found';
  }

  function showBibtexModal(content, bibkey) {
    const existingModal = document.getElementById('bibtex-modal');
    if (existingModal) {
      existingModal.remove();
    }

    const modal = document.createElement('div');
    modal.id = 'bibtex-modal';
    modal.className = 'bibtex-modal';

    const modalContent = document.createElement('div');
    modalContent.className = 'bibtex-modal-content';

    const modalHeader = document.createElement('div');
    modalHeader.className = 'bibtex-modal-header';

    const title = document.createElement('h3');
    title.className = 'bibtex-modal-title';
    title.textContent = `BibTeX: ${bibkey}`;

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'bibtex-modal-close';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.textContent = '\u00d7';

    modalHeader.appendChild(title);
    modalHeader.appendChild(closeBtn);

    const modalBody = document.createElement('div');
    modalBody.className = 'bibtex-modal-body';
    modalBody.id = 'bibtex-content';
    modalBody.textContent = content;

    const copyButton = document.createElement('button');
    copyButton.className = 'bibtex-modal-copy';
    copyButton.textContent = 'Copy to Clipboard';
    copyButton.addEventListener('click', copyBibtexToClipboard);

    modalContent.appendChild(modalHeader);
    modalContent.appendChild(modalBody);
    modalContent.appendChild(copyButton);

    modal.appendChild(modalContent);

    document.body.appendChild(modal);
    modal.style.display = 'block';

    closeBtn.onclick = () => modal.style.display = 'none';

    window.onclick = (event) => {
      if (event.target === modal) {
        modal.style.display = 'none';
      }
    };

    window.bibtexContent = content;
  }
});

function copyBibtexToClipboard() {
  const content = document.getElementById('bibtex-content').textContent;
  navigator.clipboard.writeText(content).then(() => {
    const button = document.querySelector('.bibtex-modal-copy');
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    setTimeout(() => {
      button.textContent = originalText;
    }, 2000);
  });
}
