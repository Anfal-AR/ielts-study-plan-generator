// Enhanced IELTS Study Plan Generator JavaScript
// File: static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    initializeFormHandling();
    initializeLanguageSwitcher();
    initializeAnimations();
}

// Form Handling
function initializeFormHandling() {
    const form = document.getElementById('studyPlanForm');
    const generateBtn = document.querySelector('.generate-btn');
    
    if (!form || !generateBtn) return;
    
    form.addEventListener('submit', handleFormSubmit);
    
    // Real-time form validation
    const selects = form.querySelectorAll('select[required]');
    selects.forEach(select => {
        select.addEventListener('change', validateForm);
    });
    
    validateForm();
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const generateBtn = form.querySelector('.generate-btn');
    
    setLoadingState(generateBtn, true);
    
    // Submit form normally for now
    setTimeout(() => {
        form.submit();
    }, 500);
}

function setLoadingState(button, loading) {
    if (loading) {
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        button.disabled = true;
        button.style.background = '#94a3b8';
    } else {
        button.innerHTML = '<i class="fas fa-magic"></i> Generate My Study Plan';
        button.disabled = false;
        button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    }
}

function validateForm() {
    const form = document.getElementById('studyPlanForm');
    if (!form) return;
    
    const generateBtn = form.querySelector('.generate-btn');
    const requiredFields = form.querySelectorAll('select[required]');
    
    let allValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value) {
            allValid = false;
        }
        
        // Visual feedback
        if (field.value) {
            field.style.borderColor = '#10b981';
        } else {
            field.style.borderColor = '#e2e8f0';
        }
    });
    
    generateBtn.disabled = !allValid;
    generateBtn.style.opacity = allValid ? '1' : '0.6';
}

// Language Switching
function initializeLanguageSwitcher() {
    const languageSelect = document.getElementById('language');
    
    if (!languageSelect) return;
    
    languageSelect.addEventListener('change', function() {
        const selectedLanguage = this.value;
        switchLanguage(selectedLanguage);
    });
}

function switchLanguage(lang) {
    const url = new URL(window.location);
    url.searchParams.set('lang', lang);
    
    document.body.style.opacity = '0.8';
    
    setTimeout(() => {
        window.location.href = url.toString();
    }, 200);
}

// Animations
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for scroll animations
    const animatedElements = document.querySelectorAll('.resource-category, .form-group');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Hover effects for resource cards
    const resourceCards = document.querySelectorAll('.resource-category');
    resourceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Utility Functions
function showMessage(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    if (type === 'success') {
        toast.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        toast.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    } else if (type === 'error') {
        toast.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
        toast.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    } else {
        toast.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
        toast.innerHTML = `<i class="fas fa-info-circle"></i> ${message}`;
    }
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);