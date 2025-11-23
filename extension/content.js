class OmniFetchSelectorHelper {
  constructor() {
    this.isActive = true;
    this.tooltip = null;
    this.statusIndicator = null;
    this.currentTarget = null;
    this.clipboardBuffer = '';

    this.init();
  }

  init() {
    // Membuat tooltip
    this.createTooltip();

    // Membuat status indicator
    this.createStatusIndicator();

    // Event listeners
    this.addEventListeners();

    console.log('🎯 OmniFetch Selector Helper activated!');
  }

  createTooltip() {
    this.tooltip = document.createElement('div');
    this.tooltip.className = 'omnifetch-tooltip';
    document.body.appendChild(this.tooltip);
  }

  createStatusIndicator() {
    this.statusIndicator = document.createElement('div');
    this.statusIndicator.className = 'omnifetch-status';
    this.statusIndicator.textContent = '🎯 Selector Helper Active';
    this.statusIndicator.classList.add('active');
    document.body.appendChild(this.statusIndicator);
  }

  addEventListeners() {
    // Mouse over event
    document.addEventListener('mouseover', this.handleMouseOver.bind(this));

    // Mouse move event untuk update posisi tooltip
    document.addEventListener('mousemove', this.handleMouseMove.bind(this));

    // Mouse out event
    document.addEventListener('mouseout', this.handleMouseOut.bind(this));

    // Click event untuk copy selector
    document.addEventListener('click', this.handleClick.bind(this));

    // Keyboard shortcut untuk toggle (Ctrl+Shift+S)
    document.addEventListener('keydown', this.handleKeyDown.bind(this));
  }

  handleMouseOver(event) {
    if (!this.isActive) return;

    const element = event.target;
    if (element === this.tooltip || element.classList.contains('omnifetch-tooltip')) return;

    this.currentTarget = element;

    // Highlight elemen
    element.classList.add('omnifetch-highlight');

    // Generate selector info
    const selectorInfo = this.generateSelectorInfo(element);

    // Update tooltip content
    this.updateTooltip(selectorInfo);

    // Show tooltip
    this.showTooltip(event.pageX, event.pageY);
  }

  handleMouseMove(event) {
    if (!this.isActive || !this.tooltip.classList.contains('show')) return;

    // Update posisi tooltip mengikuti cursor
    this.updateTooltipPosition(event.pageX, event.pageY);
  }

  handleMouseOut(event) {
    if (!this.isActive) return;

    const element = event.target;
    if (element === this.currentTarget) {
      // Remove highlight
      element.classList.remove('omnifetch-highlight');

      // Hide tooltip
      this.hideTooltip();

      this.currentTarget = null;
    }
  }

  handleClick(event) {
    if (!this.isActive || event.ctrlKey || event.shiftKey) return;

    // Copy selector ke clipboard
    if (this.currentTarget && this.clipboardBuffer) {
      this.copyToClipboard(this.clipboardBuffer);
      this.showCopyNotification();
      event.preventDefault();
    }
  }

  handleKeyDown(event) {
    // Ctrl+Shift+S untuk toggle helper
    if (event.ctrlKey && event.shiftKey && event.key === 'S') {
      this.toggle();
      event.preventDefault();
    }
  }

  generateSelectorInfo(element) {
    const selectors = this.generateMultipleSelectors(element);
    const elementInfo = this.getElementInfo(element);

    // Pilih selector terbaik untuk dicopy
    this.clipboardBuffer = selectors.css.id || selectors.css.class || selectors.css.tag;

    return {
      element: elementInfo,
      selectors: selectors
    };
  }

  generateMultipleSelectors(element) {
    return {
      css: {
        id: this.generateIdSelector(element),
        class: this.generateClassSelector(element),
        tag: this.generateTagSelector(element),
        nth: this.generateNthSelector(element),
        full: this.generateFullCSSPath(element)
      },
      xpath: {
        full: this.generateXPath(element),
        text: this.generateXPathByText(element),
        attribute: this.generateXPathByAttribute(element)
      }
    };
  }

  generateIdSelector(element) {
    if (element.id) {
      return `#${element.id}`;
    }
    return null;
  }

  generateClassSelector(element) {
    if (element.className && typeof element.className === 'string') {
      const classes = element.className.trim().split(/\s+/);
      if (classes.length > 0) {
        return '.' + classes.join('.');
      }
    }
    return null;
  }

  generateTagSelector(element) {
    return element.tagName.toLowerCase();
  }

  generateNthSelector(element) {
    const parent = element.parentNode;
    if (!parent) return element.tagName.toLowerCase();

    const siblings = Array.from(parent.children);
    const index = siblings.indexOf(element) + 1;

    return `${element.tagName.toLowerCase()}:nth-child(${index})`;
  }

  generateFullCSSPath(element) {
    const path = [];
    let current = element;

    while (current && current.nodeType === Node.ELEMENT_NODE) {
      let selector = current.tagName.toLowerCase();

      // Tambahkan ID jika ada
      if (current.id) {
        selector += `#${current.id}`;
      }
      // Tambahkan class jika ada
      else if (current.className) {
        const classes = current.className.trim().split(/\s+/).slice(0, 2); // Max 2 classes
        selector += '.' + classes.join('.');
      }
      // Tambahkan nth-child jika perlu
      else {
        const parent = current.parentNode;
        if (parent) {
          const siblings = Array.from(parent.children).filter(el => el.tagName === current.tagName);
          if (siblings.length > 1) {
            const index = siblings.indexOf(current) + 1;
            selector += `:nth-of-type(${index})`;
          }
        }
      }

      path.unshift(selector);
      current = current.parentNode;

      // Batasi depth
      if (path.length > 5) break;
    }

    return path.join(' > ');
  }

  generateXPath(element) {
    if (element.id) {
      return `//*[@id="${element.id}"]`;
    }

    const path = [];
    let current = element;

    while (current && current.nodeType === Node.ELEMENT_NODE) {
      let index = 0;
      const siblings = current.parentNode ? current.parentNode.children : [];

      for (let i = 0; i < siblings.length; i++) {
        if (siblings[i] === current) {
          index = i + 1;
          break;
        }
      }

      path.unshift(`${current.tagName.toLowerCase()}[${index}]`);
      current = current.parentNode;

      if (path.length > 5) break;
    }

    return '/' + path.join('/');
  }

  generateXPathByText(element) {
    const text = element.textContent.trim();
    if (text) {
      return `//*[text()="${text.substring(0, 50)}${text.length > 50 ? '...' : ''}"]`;
    }
    return null;
  }

  generateXPathByAttribute(element) {
    // Cari atribut unik
    for (let attr of element.attributes) {
      if (attr.name !== 'class' && attr.name !== 'style' && attr.value) {
        return `//*[@${attr.name}="${attr.value}"]`;
      }
    }
    return null;
  }

  getElementInfo(element) {
    return {
      tag: element.tagName.toLowerCase(),
      id: element.id || null,
      class: element.className || null,
      text: element.textContent ? element.textContent.trim().substring(0, 50) : '',
      attributes: Array.from(element.attributes).map(attr => ({
        name: attr.name,
        value: attr.value
      }))
    };
  }

  updateTooltip(selectorInfo) {
    const bestSelector = selectorInfo.selectors.css.id ||
                        selectorInfo.selectors.css.class ||
                        selectorInfo.selectors.css.tag;

    let html = `
      <div style="margin-bottom: 5px; font-size: 14px;">
        📍 <strong>${selectorInfo.element.tag}</strong>
        ${selectorInfo.element.id ? `#${selectorInfo.element.id}` : ''}
        ${selectorInfo.element.class ? `.${selectorInfo.element.className.split(' ')[0]}` : ''}
      </div>

      <div style="margin-bottom: 5px; opacity: 0.9; font-size: 11px;">
        💡 <strong>Best CSS:</strong> ${bestSelector}
      </div>

      <div style="margin-bottom: 8px; opacity: 0.8; font-size: 10px;">
        📋 Click to copy • Ctrl+Shift+S to toggle
      </div>
    `;

    this.tooltip.innerHTML = html;
  }

  showTooltip(x, y) {
    this.tooltip.classList.add('show');
    this.updateTooltipPosition(x, y);
  }

  updateTooltipPosition(x, y) {
    // Offset tooltip agar tidak mengganggu hover
    const offsetX = 15;
    const offsetY = 15;

    // Cek batas viewport
    const tooltipRect = this.tooltip.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    let finalX = x + offsetX;
    let finalY = y + offsetY;

    // Adjust if tooltip goes outside viewport
    if (finalX + tooltipRect.width > viewportWidth) {
      finalX = x - tooltipRect.width - offsetX;
    }

    if (finalY + tooltipRect.height > viewportHeight) {
      finalY = y - tooltipRect.height - offsetY;
    }

    this.tooltip.style.left = `${finalX}px`;
    this.tooltip.style.top = `${finalY}px`;
  }

  hideTooltip() {
    this.tooltip.classList.remove('show');
  }

  copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
      console.log('✅ Selector copied to clipboard:', text);
    }).catch(err => {
      console.error('❌ Failed to copy:', err);
    });
  }

  showCopyNotification() {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 50px;
      right: 10px;
      background: #4CAF50;
      color: white;
      padding: 10px 15px;
      border-radius: 5px;
      font-family: monospace;
      z-index: 10001;
      animation: slideIn 0.3s ease;
    `;
    notification.textContent = '✅ Selector copied!';

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 2000);
  }

  toggle() {
    this.isActive = !this.isActive;

    if (this.isActive) {
      this.statusIndicator.classList.add('active');
      this.statusIndicator.style.color = '#4CAF50';
      this.statusIndicator.textContent = '🎯 Selector Helper Active';
    } else {
      this.statusIndicator.style.color = '#ff4757';
      this.statusIndicator.textContent = '⏸️ Selector Helper Paused';
      this.hideTooltip();

      // Remove all highlights
      document.querySelectorAll('.omnifetch-highlight').forEach(el => {
        el.classList.remove('omnifetch-highlight');
      });
    }
  }
}

// Inisialisasi helper
const helper = new OmniFetchSelectorHelper();