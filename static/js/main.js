// Daily News Flow - Professional JavaScript Enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the news flow application
    const newsFlowApp = new NewsFlowApp();
});

class NewsFlowApp {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.setupMarketUpdates();
        this.setupAnimations();
    }

    init() {
        // Initialize app components
        this.setupLazyLoading();
        this.setupBackToTop();
        this.setupScrollEffects();
        this.setupFormEnhancements();
    }

    setupEventListeners() {
        // Navigation enhancements
        this.setupNavigation();
        
        // Search functionality
        this.setupSearch();
        
        // Filter functionality
        this.setupFilters();
        
        // Article interactions
        this.setupArticleInteractions();
    }

    // Enhanced Back to Top Button
    setupBackToTop() {
        const backToTopButton = document.getElementById('backToTop') || this.createBackToTopButton();
        
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                if (window.pageYOffset > 400) {
                    backToTopButton.classList.add('show');
                } else {
                    backToTopButton.classList.remove('show');
                }
            }, 10);
        });
        
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    createBackToTopButton() {
        const button = document.createElement('button');
        button.id = 'backToTop';
        button.className = 'btn-back-to-top';
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.setAttribute('aria-label', 'Back to top');
        document.body.appendChild(button);
        return button;
    }

    // Professional Loading States
    showLoading(target = null) {
        if (target) {
            target.classList.add('loading');
            target.style.pointerEvents = 'none';
        } else {
            const overlay = document.getElementById('loadingOverlay') || this.createLoadingOverlay();
            overlay.style.display = 'flex';
        }
    }

    hideLoading(target = null) {
        if (target) {
            target.classList.remove('loading');
            target.style.pointerEvents = 'auto';
        } else {
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                overlay.style.display = 'none';
            }
        }
    }

    createLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="d-flex flex-column align-items-center">
                <div class="loading-spinner mb-3"></div>
                <p class="text-muted">Loading...</p>
            </div>
        `;
        document.body.appendChild(overlay);
        return overlay;
    }

    // Enhanced Lazy Loading
    setupLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        imageObserver.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.1
            });
            
            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback for older browsers
            images.forEach(img => this.loadImage(img));
        }
    }

    loadImage(img) {
        img.style.opacity = '0';
        img.src = img.dataset.src;
        img.onload = () => {
            img.style.transition = 'opacity 0.3s ease';
            img.style.opacity = '1';
            img.classList.remove('lazy');
        };
        img.onerror = () => {
            img.src = '/static/images/placeholder.jpg'; // Fallback image
        };
    }

    // Market Data Updates
    setupMarketUpdates() {
        this.updateMarketData();
        
        // Update market data every 30 seconds
        setInterval(() => {
            this.updateMarketData();
        }, 30000);
        
        // Add real-time indicators
        this.addUpdateIndicators();
    }

    updateMarketData() {
        const marketItems = document.querySelectorAll('.market-change');
        
        marketItems.forEach(item => {
            // Add loading animation
            item.style.opacity = '0.6';
            
            setTimeout(() => {
                // Simulate price change
                const isPositive = Math.random() > 0.5;
                const change = (Math.random() * 2).toFixed(2);
                
                // Update the display
                item.style.opacity = '1';
                
                // Add flash effect for changes
                item.style.background = isPositive ? 
                    'rgba(22, 163, 74, 0.2)' : 
                    'rgba(220, 38, 38, 0.2)';
                
                setTimeout(() => {
                    item.style.background = '';
                }, 1000);
                
            }, Math.random() * 1000);
        });
    }

    addUpdateIndicators() {
        const marketWidgets = document.querySelectorAll('.sidebar-widget');
        
        marketWidgets.forEach(widget => {
            if (widget.querySelector('.market-table')) {
                const indicator = document.createElement('div');
                indicator.className = 'update-indicator';
                indicator.setAttribute('title', 'Live data');
                widget.style.position = 'relative';
                widget.appendChild(indicator);
            }
        });
    }

    // Navigation Enhancements
    setupNavigation() {
        const navbar = document.querySelector('.navbar');
        let lastScrollTop = 0;
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // Scrolling down - hide navbar
                navbar.style.transform = 'translateY(-100%)';
            } else {
                // Scrolling up - show navbar
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop;
        });
    }

    // Enhanced Search Functionality
    setupSearch() {
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            let searchTimeout;
            
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                const query = e.target.value.trim();
                
                if (query.length > 2) {
                    searchTimeout = setTimeout(() => {
                        this.performLiveSearch(query);
                    }, 300);
                }
            });
        }
    }

    performLiveSearch(query) {
        // Implement live search functionality
        console.log('Performing live search for:', query);
        // This can be enhanced with AJAX calls to search endpoint
    }

    // Scroll Effects and Animations
    setupScrollEffects() {
        // Fade in animations for cards
        this.setupScrollAnimations();
    }

    setupScrollAnimations() {
        const animatedElements = document.querySelectorAll('.news-card, .sidebar-widget');
        
        if ('IntersectionObserver' in window) {
            const animationObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '0';
                        entry.target.style.transform = 'translateY(20px)';
                        entry.target.style.transition = 'all 0.6s ease';
                        
                        setTimeout(() => {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                        }, 100);
                        
                        animationObserver.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            });
            
            animatedElements.forEach(el => animationObserver.observe(el));
        }
    }

    // Form Enhancements
    setupFormEnhancements() {
        // Newsletter subscription
        const newsletterForm = document.querySelector('.newsletter-form');
        if (newsletterForm) {
            newsletterForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleNewsletterSubmission(newsletterForm);
            });
        }
        
        // Auto-dismiss alerts
        this.setupAlerts();
    }

    handleNewsletterSubmission(form) {
        const email = form.querySelector('input[type="email"]').value;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (email) {
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Subscribing...';
            submitBtn.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Subscribed!';
                submitBtn.classList.remove('btn-primary');
                submitBtn.classList.add('btn-success');
                
                this.showNotification('Thank you for subscribing to our newsletter!', 'success');
                form.querySelector('input[type="email"]').value = '';
                
                // Reset button after 3 seconds
                setTimeout(() => {
                    submitBtn.innerHTML = 'Subscribe';
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('btn-success');
                    submitBtn.classList.add('btn-primary');
                }, 3000);
            }, 1500);
        }
    }

    setupAlerts() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (!alert.querySelector('.btn-close')) {
                setTimeout(() => {
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateY(-20px)';
                    setTimeout(() => {
                        alert.remove();
                    }, 300);
                }, 5000);
            }
        });
    }

    // Filter Functionality
    setupFilters() {
        const filterButtons = document.querySelectorAll('[data-filter]');
        if (filterButtons.length > 0) {
            filterButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.handleFilter(button);
                });
            });
        }
    }

    handleFilter(button) {
        const filter = button.dataset.filter;
        const articles = document.querySelectorAll('.news-card');
        
        // Update active button
        document.querySelectorAll('[data-filter]').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');
        
        // Filter articles
        articles.forEach(article => {
            if (filter === 'all' || article.dataset.category === filter) {
                article.style.display = 'block';
                article.style.opacity = '0';
                setTimeout(() => {
                    article.style.opacity = '1';
                }, 100);
            } else {
                article.style.opacity = '0';
                setTimeout(() => {
                    article.style.display = 'none';
                }, 300);
            }
        });
    }

    // Article Interactions
    setupArticleInteractions() {
        // Share functionality
        this.setupShareButtons();
        
        // Article bookmarking
        this.setupBookmarking();
    }

    setupShareButtons() {
        const shareButtons = document.querySelectorAll('[data-share]');
        shareButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.shareArticle(button.dataset.share);
            });
        });
    }

    shareArticle(platform) {
        const url = encodeURIComponent(window.location.href);
        const title = encodeURIComponent(document.title);
        
        let shareUrl = '';
        
        switch (platform) {
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                break;
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
                break;
            case 'email':
                shareUrl = `mailto:?subject=${title}&body=${url}`;
                break;
        }
        
        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    }

    setupBookmarking() {
        const bookmarkButtons = document.querySelectorAll('[data-bookmark]');
        bookmarkButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleBookmark(button);
            });
        });
    }

    toggleBookmark(button) {
        const articleId = button.dataset.bookmark;
        const isBookmarked = button.classList.contains('bookmarked');
        
        if (isBookmarked) {
            button.classList.remove('bookmarked');
            button.innerHTML = '<i class="far fa-bookmark"></i>';
            this.showNotification('Bookmark removed', 'info');
        } else {
            button.classList.add('bookmarked');
            button.innerHTML = '<i class="fas fa-bookmark"></i>';
            this.showNotification('Article bookmarked', 'success');
        }
        
        // Store in localStorage
        const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]');
        if (isBookmarked) {
            const index = bookmarks.indexOf(articleId);
            if (index > -1) bookmarks.splice(index, 1);
        } else {
            bookmarks.push(articleId);
        }
        localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
    }

    // Notification System
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification-toast`;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${this.getNotificationIcon(type)} me-2"></i>
                ${message}
            </div>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Hide notification
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 4000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // Additional Animations
    setupAnimations() {
        // Add hover effects to market widgets
        document.querySelectorAll('.sidebar-widget').forEach(widget => {
            widget.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px)';
            });
            
            widget.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
        
        // Add click effects to buttons
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('mousedown', function() {
                this.style.transform = 'scale(0.98)';
            });
            
            button.addEventListener('mouseup', function() {
                this.style.transform = 'scale(1)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }
}

// Initialize tooltips and other Bootstrap components
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
        
        // Initialize popovers
        const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
        popovers.forEach(popover => {
            new bootstrap.Popover(popover);
        });
    }
});
