// --- Mode switching (Farbe / Typ) ---
function switchMode(mode) {
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });
    document.getElementById('color-filters').classList.toggle('hidden', mode !== 'color');
    document.getElementById('type-filters').classList.toggle('hidden', mode !== 'type');

    // Clear active filter highlight
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active-filter'));

    // Reset grid
    document.getElementById('pokemon-grid').innerHTML = '<p class="hint">Wähle eine Farbe oder einen Typ!</p>';
}

// --- Active filter highlight ---
function setActive(btn) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active-filter'));
    btn.classList.add('active-filter');
}

// --- Detail overlay ---
function showDetail() {
    document.getElementById('detail-overlay').classList.remove('hidden');
}

let currentAudio = null;

function closeDetail(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('detail-overlay').classList.add('hidden');
    stopAudio();
}

// Close with no-arg version (for X button)
document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('detail-overlay');
    if (overlay) {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.add('hidden');
                stopAudio();
            }
        });
    }
});

// --- Audio playback (pre-generated Edge TTS files) ---
function speakName(pokemonId) {
    stopAudio();
    currentAudio = new Audio(`/static/audio/${pokemonId}.mp3`);
    currentAudio.play().catch(() => {});
}

function speakSize(pokemonId) {
    stopAudio();
    currentAudio = new Audio(`/static/audio/size_${pokemonId}.mp3`);
    currentAudio.play().catch(() => {});
}

function stopAudio() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
}

// --- Long-press on logo to open settings (3 seconds) ---
let longPressTimer = null;

document.addEventListener('DOMContentLoaded', () => {
    const logo = document.getElementById('app-logo');
    if (!logo) return;

    const startPress = (e) => {
        e.preventDefault();
        longPressTimer = setTimeout(() => {
            window.location.href = '/settings';
        }, 3000);
    };

    const cancelPress = () => {
        if (longPressTimer) {
            clearTimeout(longPressTimer);
            longPressTimer = null;
        }
    };

    // Touch events
    logo.addEventListener('touchstart', startPress, { passive: false });
    logo.addEventListener('touchend', cancelPress);
    logo.addEventListener('touchcancel', cancelPress);
    logo.addEventListener('touchmove', cancelPress);

    // Mouse events (for desktop testing)
    logo.addEventListener('mousedown', startPress);
    logo.addEventListener('mouseup', cancelPress);
    logo.addEventListener('mouseleave', cancelPress);
});
