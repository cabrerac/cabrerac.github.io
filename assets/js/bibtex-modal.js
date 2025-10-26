document.addEventListener("DOMContentLoaded", () => {
  const style = document.createElement("style");
  style.textContent = `
    .bibtex-modal {
      display: none;
      position: fixed;
      z-index: 10000;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0,0,0,0.4);
    }

    .bibtex-modal-content {
      background-color: #fefefe;
      margin: 5% auto;
      padding: 20px;
      border: 1px solid #888;
      width: 80%;
      max-width: 800px;
      border-radius: 5px;
    }

    .bibtex-modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
    }

    .bibtex-modal-close {
      color: #aaa;
      font-size: 28px;
      font-weight: bold;
      cursor: pointer;
    }

    .bibtex-modal-close:hover,
    .bibtex-modal-close:focus {
      color: black;
    }

    .bibtex-modal-body {
      background-color: #f5f5f5;
      padding: 15px;
      border-radius: 3px;
      font-family: monospace;
      white-space: pre-wrap;
      overflow-x: auto;
      max-height: 60vh;
      overflow-y: auto;
    }

    .bibtex-modal-copy {
      margin-top: 10px;
      padding: 8px 15px;
      background-color: var(--link-color);
      color: white;
      border: none;
      border-radius: 3px;
      cursor: pointer;
    }

    .bibtex-modal-copy:hover {
      background-color: #0056b3;
    }
  `;
  document.head.appendChild(style);

  // Add click handlers to bibtex links
  document.querySelectorAll('.bibtex-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const bibkey = link.getAttribute('href').split('#')[1];
      fetchBibtexEntry(bibkey, link.href);
    });
  });

  function fetchBibtexEntry(bibkey, fileUrl) {
    // Extract just the bib file URL without the hash
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
    // Escape special regex characters in bibkey (like dots in DOIs)
    const escapedKey = bibkey.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    // Match the full BibTeX entry including the type (article, inproceedings, etc.)
    // This handles keys that appear after @type{
    const regex = new RegExp(`(@[a-zA-Z]+\\{[^}]*${escapedKey}[^}]*\\{[^}]*\\}.*?)\\n\\n(?=@|$)`, 's');
    const match = bibtexContent.match(regex);

    if (match) {
      let entry = match[1].trim();
      // Clean up the entry to ensure proper formatting
      entry = entry.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      return entry;
    }

    // Fallback: try to find the entry more flexibly
    const lines = bibtexContent.split('\n');
    let entryLines = [];
    let inEntry = false;

    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes('{' + bibkey + ',')) {
        inEntry = true;
      }
      if (inEntry) {
        entryLines.push(lines[i]);
        // Entry ends when we hit a line with just } or empty line followed by @
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
    // Remove existing modal if any
    const existingModal = document.getElementById('bibtex-modal');
    if (existingModal) {
      existingModal.remove();
    }

    const modal = document.createElement('div');
    modal.id = 'bibtex-modal';
    modal.className = 'bibtex-modal';
    modal.innerHTML = `
      <div class="bibtex-modal-content">
        <div class="bibtex-modal-header">
          <h3>BibTeX Entry: ${bibkey}</h3>
          <span class="bibtex-modal-close">&times;</span>
        </div>
        <div class="bibtex-modal-body" id="bibtex-content">${content}</div>
        <button class="bibtex-modal-copy" onclick="copyBibtexToClipboard()">Copy to Clipboard</button>
      </div>
    `;

    document.body.appendChild(modal);
    modal.style.display = 'block';

    // Close modal handlers
    const closeBtn = modal.querySelector('.bibtex-modal-close');
    closeBtn.onclick = () => modal.style.display = 'none';

    window.onclick = (event) => {
      if (event.target === modal) {
        modal.style.display = 'none';
      }
    };

    // Store content for copying
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
