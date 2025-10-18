/**
 * Custom JavaScript for Tom Gair Portfolio
 * Handles dark mode, animations, and interactive features
 */

// Dark Mode Management
class ThemeManager {
    constructor() {
        this.themeToggleBtn = document.getElementById('theme-toggle');
        this.themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
        this.themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
        
        this.init();
    }

    init() {
        // Set initial theme based on localStorage or system preference
        this.setInitialTheme();
        
        // Add event listener to toggle button
        if (this.themeToggleBtn) {
            this.themeToggleBtn.addEventListener('click', () => this.toggleTheme());
        }
    }

    setInitialTheme() {
        const savedTheme = localStorage.getItem('color-theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
            this.enableDarkMode();
        } else {
            this.enableLightMode();
        }
    }

    enableDarkMode() {
        document.documentElement.classList.add('dark');
        if (this.themeToggleLightIcon) this.themeToggleLightIcon.classList.remove('hidden');
        if (this.themeToggleDarkIcon) this.themeToggleDarkIcon.classList.add('hidden');
    }

    enableLightMode() {
        document.documentElement.classList.remove('dark');
        if (this.themeToggleDarkIcon) this.themeToggleDarkIcon.classList.remove('hidden');
        if (this.themeToggleLightIcon) this.themeToggleLightIcon.classList.add('hidden');
    }

    toggleTheme() {
        const isDark = document.documentElement.classList.contains('dark');
        
        if (isDark) {
            this.enableLightMode();
            localStorage.setItem('color-theme', 'light');
        } else {
            this.enableDarkMode();
            localStorage.setItem('color-theme', 'dark');
        }
    }
}

// Admin Dashboard Form Management
class AdminFormManager {
    constructor() {
        this.init();
    }

    init() {
        // Blog form toggle
        window.toggleCreateBlogForm = () => this.toggleForm('create-blog-form', 'title');
        
        // Project form toggle
        window.toggleCreateProjectForm = () => this.toggleForm('create-project-form', 'project-title');
        
        // Slug auto-generation
        this.setupSlugGeneration();
    }

    toggleForm(formId, focusFieldId) {
        const form = document.getElementById(formId);
        if (!form) return;
        
        form.classList.toggle('hidden');
        
        // Auto-focus field when opening
        if (!form.classList.contains('hidden')) {
            const focusField = document.getElementById(focusFieldId);
            if (focusField) {
                setTimeout(() => focusField.focus(), 100);
            }
        }
    }

    setupSlugGeneration() {
        // Blog post slug generation
        const blogTitleField = document.getElementById('title');
        const blogSlugField = document.getElementById('slug');
        
        if (blogTitleField && blogSlugField) {
            blogTitleField.addEventListener('input', (e) => {
                this.updateSlugPreview(e.target.value, blogSlugField);
            });
        }

        // Project slug generation
        const projectTitleField = document.getElementById('project-title');
        const projectSlugField = document.getElementById('project-slug');
        
        if (projectTitleField && projectSlugField) {
            projectTitleField.addEventListener('input', (e) => {
                this.updateSlugPreview(e.target.value, projectSlugField);
            });
        }
    }

    updateSlugPreview(title, slugField) {
        if (!slugField.value) {
            const slug = this.generateSlug(title);
            slugField.placeholder = slug || 'auto-generated from title';
        }
    }

    generateSlug(text) {
        return text
            .toLowerCase()
            .replace(/[^a-z0-9\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-')
            .trim();
    }
}

// Animation and Interaction Management
class AnimationManager {
    constructor() {
        this.init();
    }

    init() {
        // Add intersection observer for scroll animations
        this.setupScrollAnimations();
        
        // Add hover sound effects (optional)
        this.setupHoverEffects();
    }

    setupScrollAnimations() {
        // Only run if user hasn't requested reduced motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observe elements that should animate on scroll
        document.querySelectorAll('.scroll-animate').forEach(el => {
            observer.observe(el);
        });
    }

    setupHoverEffects() {
        // Add subtle hover effects to interactive elements
        document.querySelectorAll('.hover-lift, .hover-scale').forEach(element => {
            element.addEventListener('mouseenter', () => {
                if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    element.style.willChange = 'transform';
                }
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.willChange = 'auto';
            });
        });
    }
}

// Contact Form Management
class ContactFormManager {
    constructor() {
        this.init();
    }

    init() {
        // Handle HTMX events for contact form
        this.setupHTMXEvents();
    }

    setupHTMXEvents() {
        document.body.addEventListener('htmx:afterRequest', (event) => {
            if (event.detail.xhr.status === 200 && event.detail.target.id === 'form-response') {
                this.showSuccessMessage(event.detail.target);
                this.resetContactForm(event.detail.target);
            }
        });

        document.body.addEventListener('htmx:responseError', (event) => {
            this.showErrorMessage(event.detail.target);
        });
    }

    showSuccessMessage(target) {
        target.innerHTML = `
            <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-md p-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-green-800 dark:text-green-200">Message sent successfully!</h3>
                        <p class="mt-1 text-sm text-green-700 dark:text-green-300">Thanks for reaching out. I'll get back to you soon.</p>
                    </div>
                </div>
            </div>
        `;
    }

    showErrorMessage(target) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded mt-4';
        errorDiv.textContent = 'There was an error sending your message. Please try again.';
        
        if (target) {
            target.appendChild(errorDiv);
            setTimeout(() => errorDiv.remove(), 5000);
        }
    }

    resetContactForm(target) {
        const form = target.closest('section')?.querySelector('form');
        if (form) {
            setTimeout(() => form.reset(), 1000);
        }
    }
}

// Utility Functions
class Utils {
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    static throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all managers
    new ThemeManager();
    new AdminFormManager();
    new AnimationManager();
    new ContactFormManager();

    // Add any additional initialization here
    console.log('🚀 Tom Gair Portfolio - Initialized successfully');
});

// Export for potential use in other scripts
window.PortfolioApp = {
    ThemeManager,
    AdminFormManager,
    AnimationManager,
    ContactFormManager,
    Utils
};