document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleBtn');
    const resetBtn = document.getElementById('resetBtn');
    const statusDiv = document.getElementById('status');

    toggleBtn.addEventListener('click', function() {
        // Kirim pesan ke content script untuk toggle
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'toggle'
            });
        });

        // Update UI
        if (statusDiv.classList.contains('active')) {
            statusDiv.classList.remove('active');
            statusDiv.classList.add('paused');
            statusDiv.innerHTML = '<strong>⏸️ Paused</strong> - Click to resume';
            toggleBtn.textContent = 'Resume';
        } else {
            statusDiv.classList.remove('paused');
            statusDiv.classList.add('active');
            statusDiv.innerHTML = '<strong>✅ Active</strong> - Hover over elements';
            toggleBtn.textContent = 'Pause';
        }
    });

    resetBtn.addEventListener('click', function() {
        // Refresh halaman untuk reset helper
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.reload(tabs[0].id);
        });
    });
});