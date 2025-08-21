// Theme Management System
class ThemeManager {
	constructor() {
		this.theme = this.getStoredTheme() || this.getPreferredTheme();
		this.init();
	}

	// Get theme from localStorage
	getStoredTheme() {
		return localStorage.getItem('theme');
	}

	// Get system preferred theme
	getPreferredTheme() {
		if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
			return 'dark';
		}
		return 'light';
	}

	// Set theme
	setTheme(theme) {
		this.theme = theme;
		document.documentElement.setAttribute('data-theme', theme);
		localStorage.setItem('theme', theme);
		
		// Update theme toggle button state
		this.updateToggleButton();
		
		// Dispatch custom event for other scripts
		window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
	}

	// Toggle between light and dark
	toggleTheme() {
		const newTheme = this.theme === 'light' ? 'dark' : 'light';
		this.setTheme(newTheme);
	}

	// Update toggle button appearance
	updateToggleButton() {
		const toggle = document.getElementById('themeToggle');
		if (toggle) {
			const sunIcon = toggle.querySelector('.icon.sun');
			const moonIcon = toggle.querySelector('.icon.moon');
			
			if (this.theme === 'dark') {
				sunIcon.style.opacity = '0';
				moonIcon.style.opacity = '1';
			} else {
				sunIcon.style.opacity = '1';
				moonIcon.style.opacity = '0';
			}
		}
	}

	// Initialize theme system
	init() {
		// Set initial theme
		this.setTheme(this.theme);
		
		// Add event listener to toggle button
		const toggle = document.getElementById('themeToggle');
		if (toggle) {
			toggle.addEventListener('click', () => {
				this.toggleTheme();
			});
		}

		// Listen for system theme changes
		if (window.matchMedia) {
			window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
				if (!this.getStoredTheme()) {
					this.setTheme(e.matches ? 'dark' : 'light');
				}
			});
		}

		// Add smooth transitions to all elements
		this.addThemeTransitions();
	}

	// Add smooth transitions for theme changes
	addThemeTransitions() {
		const style = document.createElement('style');
		style.textContent = `
			* {
				transition: background-color 0.3s ease, 
							color 0.3s ease, 
							border-color 0.3s ease, 
							box-shadow 0.3s ease !important;
			}
		`;
		document.head.appendChild(style);
	}

	// Get current theme
	getCurrentTheme() {
		return this.theme;
	}

	// Check if dark mode is active
	isDarkMode() {
		return this.theme === 'dark';
	}

	// Check if light mode is active
	isLightMode() {
		return this.theme === 'light';
	}
}

// Initialize theme manager when DOM is loaded
let themeManager;

document.addEventListener('DOMContentLoaded', () => {
	themeManager = new ThemeManager();
});

// Export for use in other scripts
window.ThemeManager = ThemeManager;
window.themeManager = themeManager;

// Utility functions for other scripts
window.getCurrentTheme = () => themeManager?.getCurrentTheme();
window.isDarkMode = () => themeManager?.isDarkMode();
window.isLightMode = () => themeManager?.isLightMode();
window.toggleTheme = () => themeManager?.toggleTheme();
