document.getElementById('download-form').addEventListener('submit', function() {
    var button = document.querySelector('.submit-button');
    button.textContent = 'Downloading...';
    button.disabled = true;
    button.style.backgroundColor = '#6c757d';
});
