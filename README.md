# 🎯 OmniFetch Enhanced Scraper

Scraper profesional dengan **browser extension untuk hover-to-select selector**. Cukup arahkan cursor ke elemen web, dan dapatkan CSS selector secara otomatis!

## ✨ Fitur Utama

### 🌐 Browser Extension
- **Hover Highlight**: Elemen di-highlight saat cursor diarahkan
- **Auto Selector Generation**: Generate CSS selector, XPath, dan full path otomatis
- **Click to Copy**: Klik elemen untuk langsung copy selector
- **Smart Detection**: Prioritaskan ID → class → nth-child
- **Real-time Tooltip**: Informasi selector langsung di browser

### 🚀 Enhanced Scraper
- **API Integration**: Menerima selector langsung dari extension
- **Visual Highlighting**: Elemen di-highlight saat dicek
- **Multiple Export**: CSV, Excel, JSON
- **Real-time Processing**: Proses selector dari extension
- **Data Storage**: Simpan hasil untuk export batch

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install DrissionPage pandas loguru
```

### 2. Install Browser Extension

**Chrome:**
1. Buka `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Pilih folder `extension`

### 3. Start Chrome Debugging
```bash
chrome.exe --remote-debugging-port=9222
```

### 4. Run Enhanced Scraper
```bash
python enhanced_scraper.py
```

## 🎮 Cara Penggunaan

### Mode Extension (Recommended)
1. **Start enhanced scraper**
2. **Buka website target** di Chrome
3. **Aktifkan extension** (icon extension → Active)
4. **Hover ke elemen** → muncul tooltip selector
5. **Klik elemen** → selector otomatis dikirim ke scraper
6. **Monitor terminal** → lihat hasil real-time

### Menu Scraper
```bash
check      - Test selector manual
scrape     - Scrape dengan selector manual
extension  - Lihat data dari extension
export     - Export data dari extension
exit       - Keluar
```

## ⌨️ Shortcuts

- **`Ctrl+Shift+S`** - Toggle extension on/off
- **Click element** - Copy selector & send to scraper

## 📁 Project Structure

```
OmniFetch/
├── extension/              # Browser extension
│   ├── manifest.json      # Extension config
│   ├── content.js         # Main functionality
│   ├── popup.html/js      # Extension UI
│   └── styles.css         # Styling
├── enhanced_scraper.py    # Main scraper dengan API
├── start_chrome.bat       # Chrome debugging shortcut
└── setup_guide.md         # Detailed setup guide
```

## 🎯 Extension Features

### Selector Types Generated:
- **CSS ID**: `#element-id` (prioritas utama)
- **CSS Class**: `.class-name`
- **CSS Nth-child**: `div:nth-child(2)`
- **CSS Full Path**: `div.container > ul > li`
- **XPath**: `//div[@class='content']/p[1]`

### Visual Feedback:
- **Red outline highlight** saat hover
- **Tooltip info** dengan selector terbaik
- **Copy confirmation** notification
- **Element info** (tag, ID, class, text preview)

## 📊 Export Options

- **CSV**: Comma-separated values
- **Excel**: .xlsx dengan formatting
- **JSON**: Structured JSON data
- **Auto timestamp**: `scrape_20241123_143022.csv`

## 🔧 Troubleshooting

### Extension tidak muncul?
- Enable Developer mode di `chrome://extensions/`
- Refresh halaman setelah install

### Scraper tidak connect?
- Pastikan Chrome jalan di port 9222
- Check API server di localhost:8888

### Selector tidak bekerja?
- Coba alternative selector (XPath vs CSS)
- Tunggu jika loading lambat

**Full setup guide**: Lihat `setup_guide.md` untuk instruksi detail!

---

Made with ❤️ using DrissionPage + Pure JavaScript# OmniFetch
