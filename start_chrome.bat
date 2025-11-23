@echo off
echo Starting Chrome in Debug Mode for OmniFetch...
echo.
echo This will open a new Chrome instance with debugging enabled.
echo Use this browser to login to websites you want to scrape.
echo.
echo The scraper will connect to this browser automatically.
echo.

"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug_profile" --disable-web-security --disable-features=VizDisplayCompositor

echo.
echo Chrome has been closed.
echo You can now close this window.
pause