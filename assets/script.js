// Force dropdown styling with JavaScript when dropdown opens
function styleDropdowns() {
    setTimeout(function() {
        // Target all dropdown menus
        const listboxes = document.querySelectorAll('[role="listbox"]');
        listboxes.forEach(function(listbox) {
            listbox.style.setProperty('background', '#0F1535', 'important');
            listbox.style.setProperty('border', '1px solid rgba(0, 212, 255, 0.4)', 'important');
            listbox.style.setProperty('border-radius', '12px', 'important');
            listbox.style.setProperty('padding', '8px', 'important');
        });

        // Target all options
        const options = document.querySelectorAll('[role="option"]');
        options.forEach(function(option) {
            const isSelected = option.getAttribute('aria-selected') === 'true';

            option.style.setProperty('background', isSelected ? 'rgba(0, 212, 255, 0.2)' : 'transparent', 'important');
            option.style.setProperty('color', isSelected ? '#00D4FF' : '#E8EEFF', 'important');
            option.style.setProperty('padding', '14px 18px', 'important');
            option.style.setProperty('margin', '3px 0', 'important');
            option.style.setProperty('border-radius', '10px', 'important');
            option.style.setProperty('font-size', '15px', 'important');
            option.style.setProperty('border', isSelected ? '1px solid rgba(0, 212, 255, 0.5)' : '1px solid transparent', 'important');
        });
    }, 50);
}

// Run when DOM changes (dropdown opens)
const observer = new MutationObserver(styleDropdowns);
observer.observe(document.body, { childList: true, subtree: true });