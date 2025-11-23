# 🚀 Setup Guide OmniFetch Enhanced Scraper

## Langkah 1: Install Python Dependencies

```bash
pip install DrissionPage pandas loguru
```

## Langkah 2: Install Browser Extension

### Chrome:
1. Buka Chrome dan ketik `chrome://extensions/` di address bar
2. Enable "Developer mode" (toggle di kanan atas)
3. Klik "Load unpacked"
4. Pilih folder `extension` dari project ini

### Firefox:
1. Buka `about:debugging`
2. Klik "This Firefox"
3. Klik "Load Temporary Add-on"
4. Pilih file `manifest.json` dari folder extension

## Langkah 3: Start Chrome dengan Remote Debugging

Buka command prompt dan jalankan:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
```

## Langkah 4: Jalankan Enhanced Scraper

```bash
python enhanced_scraper.py
```

## Cara Pakai:

1. **Buka website target** di Chrome yang sudah di-debug
2. **Aktifkan extension** (klik icon extension, pastikan "Active")
3. **Hover ke elemen** - akan muncul tooltip dengan selector
4. **Klik elemen** - selector otomatis ter-copy dan dikirim ke scraper
5. **Monitor terminal** - lihat hasil scraping real-time

## Keyboard Shortcuts:
- `Ctrl+Shift+S`: Toggle extension on/off

Selamat scraping! 🎯