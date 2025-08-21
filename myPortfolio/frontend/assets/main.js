async function fetchJSON(url, options) {
	const res = await fetch(url, options);
	if (!res.ok) throw new Error(`Request failed: ${res.status}`);
	return res.json();
}

function renderTechBadges(tech) {
	if (!tech) return '';
	return tech.split(',').map(t => t.trim()).filter(Boolean).map(t => 
		`<span class="tech-badge">${t}</span>`
	).join('');
}

async function loadLatestProjects() {
	const container = document.getElementById('projectsContainer');
	if (!container) return;
	
	try {
		const projects = await fetchJSON('/api/projects');
		container.innerHTML = projects.slice(0, 6).map(p => `
			<div class="col-lg-4 col-md-6 animate-fade-in-up">
				<div class="card project-card h-100 hover-lift">
					${p.image_url ? `<img src="${p.image_url}" alt="${p.title}" class="card-img-top" style="object-fit: cover; height: 180px;">` : ''}
					<div class="card-body d-flex flex-column">
						<h5 class="card-title">${p.title}</h5>
						<p class="card-text">${p.description.substring(0, 120)}${p.description.length > 120 ? '...' : ''}</p>
						<div class="project-tech">${renderTechBadges(p.tech_stack)}</div>
						<div class="project-links mt-auto">
							${p.github_link ? `<a class="btn btn-sm btn-outline-primary" href="${p.github_link}" target="_blank"><i class="bi bi-github"></i> Code</a>` : ''}
							${p.demo_link ? `<a class="btn btn-sm btn-accent" href="${p.demo_link}" target="_blank"><i class="bi bi-box-arrow-up-right"></i> Demo</a>` : ''}
						</div>
					</div>
				</div>
			</div>
		`).join('');
	} catch (e) {
		container.innerHTML = `
			<div class="col-12 text-center">
				<div class="alert alert-warning">
					<i class="bi bi-exclamation-triangle"></i>
					No projects found. Add some projects through the admin panel.
				</div>
			</div>
		`;
	}
}

async function loadRepos() {
	const container = document.getElementById('reposContainer');
	if (!container) {
		console.error('reposContainer not found');
		return;
	}
	
	// Show loading state
	container.innerHTML = `
		<div class="col-12 text-center">
			<div class="spinner-border text-primary" role="status">
				<span class="visually-hidden">Loading...</span>
			</div>
			<p class="mt-3 text-muted">Fetching GitHub repositories...</p>
		</div>
	`;
	
	try {
		console.log('Fetching GitHub repos from /api/github/repos...');
		const response = await fetch('/api/github/repos');
		
		if (!response.ok) {
			const errorData = await response.json();
			throw new Error(`HTTP ${response.status}: ${errorData.error || 'Unknown error'}`);
		}
		
		const repos = await response.json();
		console.log('GitHub repos received:', repos);
		
		if (!repos || repos.length === 0) {
			container.innerHTML = `
				<div class="col-12 text-center">
					<div class="alert alert-info">
						<i class="bi bi-info-circle"></i>
						No public repositories found. Check your GitHub username in the environment variables.
					</div>
				</div>
			`;
			return;
		}
		
		// Render repositories
		container.innerHTML = repos.map((r, index) => `
			<div class="col-lg-4 col-md-6 animate-fade-in-up" style="animation-delay: ${index * 0.1}s">
				<div class="card h-100 hover-lift">
					<div class="card-body d-flex flex-column">
						<div class="d-flex align-items-center mb-2">
							<i class="bi bi-github text-primary fs-4 me-2"></i>
							<h5 class="card-title mb-0">${r.name}</h5>
						</div>
						<p class="card-text flex-grow-1">${r.description || 'No description available'}</p>
						
						<div class="mt-3">
							<div class="d-flex flex-wrap gap-2 mb-3">
								${r.language ? `<span class="badge bg-secondary">${r.language}</span>` : ''}
								${r.fork ? `<span class="badge bg-info">Fork</span>` : ''}
								${r.archived ? `<span class="badge bg-warning">Archived</span>` : ''}
							</div>
							
							<div class="d-flex justify-content-between align-items-center">
								<div class="d-flex gap-2">
									<span class="badge bg-warning text-dark" title="Stars">
										<i class="bi bi-star-fill me-1"></i>
										${r.stargazers_count || 0}
									</span>
									<span class="badge bg-info text-dark" title="Forks">
										<i class="bi bi-git-branch me-1"></i>
										${r.forks_count || 0}
									</span>
									<span class="badge bg-success text-dark" title="Watchers">
										<i class="bi bi-eye me-1"></i>
										${r.watchers_count || 0}
									</span>
								</div>
								<a class="btn btn-sm btn-primary" href="${r.html_url}" target="_blank" rel="noopener">
									<i class="bi bi-box-arrow-up-right"></i>
									View
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		`).join('');
		
		// Re-run animations for new content
		setupAnimations();
		
	} catch (error) {
		console.error('Error loading GitHub repos:', error);
		
		let errorMessage = error.message;
		if (error.message.includes('Failed to fetch')) {
			errorMessage = 'Network error. Please check your internet connection and try again.';
		} else if (error.message.includes('username not configured')) {
			errorMessage = 'GitHub username not configured. Please set GITHUB_USERNAME in your environment variables.';
		} else if (error.message.includes('not found')) {
			errorMessage = 'GitHub user not found. Please check your username.';
		} else if (error.message.includes('rate limit')) {
			errorMessage = 'GitHub API rate limit exceeded. Please try again later.';
		}
		
		container.innerHTML = `
			<div class="col-12 text-center">
				<div class="alert alert-danger">
					<i class="bi bi-exclamation-triangle"></i>
					<strong>Failed to load GitHub repositories</strong><br>
					<small class="text-muted">${errorMessage}</small>
					<div class="mt-3">
						<button class="btn btn-outline-primary btn-sm" onclick="loadRepos()">
							<i class="bi bi-arrow-clockwise"></i>
							Try Again
						</button>
					</div>
				</div>
			</div>
		`;
	}
}

// Enhanced GitHub repos button functionality
function setupGitHubButton() {
	const btn = document.getElementById('fetchReposBtn');
	if (!btn) {
		console.error('fetchReposBtn not found');
		return;
	}
	
	// Remove any existing event listeners
	btn.replaceWith(btn.cloneNode(true));
	const newBtn = document.getElementById('fetchReposBtn');
	
	newBtn.addEventListener('click', async (e) => {
		e.preventDefault();
		
		// Update button state
		const originalContent = newBtn.innerHTML;
		newBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
		newBtn.disabled = true;
		
		try {
			await loadRepos();
			
			// Scroll to repos section
			const reposSection = document.getElementById('github');
			if (reposSection) {
				reposSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
			}
			
		} catch (error) {
			console.error('Error in GitHub button click:', error);
		} finally {
			// Restore button state
			newBtn.innerHTML = originalContent;
			newBtn.disabled = false;
		}
	});
	
	console.log('GitHub button setup complete');
}

// Intersection Observer for animations
function setupAnimations() {
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
	
	// Observe all elements with animation classes
	document.querySelectorAll('.animate-fade-in-up').forEach(el => {
		el.style.opacity = '0';
		el.style.transform = 'translateY(30px)';
		el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
		observer.observe(el);
	});
}

// Handle theme changes
function handleThemeChange() {
	// Re-render any dynamic content that might need theme updates
	setupAnimations();
	
	// Update any theme-specific elements
	updateThemeSpecificElements();
}

// Update theme-specific elements
function updateThemeSpecificElements() {
	// Update any elements that need theme-specific styling
	const theme = window.getCurrentTheme();
	
	// Example: Update placeholder images based on theme
	const placeholders = document.querySelectorAll('img[src*="placeholder"]');
	placeholders.forEach(img => {
		if (img.src.includes('placeholder')) {
			const isDark = theme === 'dark';
			const bgColor = isDark ? '1E293B' : '1E40AF';
			const textColor = isDark ? 'F1F5F9' : 'FFFFFF';
			img.src = img.src.replace(/\/[^\/]+\/FFFFFF/, `/${bgColor}/${textColor}`);
		}
	});
}

// Update placeholder text when language changes
function updatePlaceholderText() {
	if (window.currentLanguage && window.languages) {
		const lang = window.languages[window.currentLanguage];
		if (lang && lang.contact && lang.contact.form) {
			const messageTextarea = document.getElementById('message');
			if (messageTextarea) {
				messageTextarea.placeholder = lang.contact.form.messagePlaceholder;
			}
		}
	}
}

// Initialize when DOM is loaded
window.addEventListener('DOMContentLoaded', () => {
	loadLatestProjects();
	setupAnimations();
	setupGitHubButton();
	
	// Add loading state to other buttons (excluding GitHub button)
	setupButtonLoadingStates();
	
	// Listen for theme changes
	window.addEventListener('themeChanged', handleThemeChange);
	
	// Update placeholder text after language initialization
	setTimeout(updatePlaceholderText, 100);
});

// Setup loading states for buttons
function setupButtonLoadingStates() {
	document.querySelectorAll('.btn').forEach(btn => {
		// Skip the GitHub button as it has its own loading state
		if (btn.id === 'fetchReposBtn') return;
		// Skip language dropdown toggle and any dropdown toggle buttons
		if (btn.id === 'languageDropdown' || btn.classList.contains('dropdown-toggle') || btn.getAttribute('data-bs-toggle') === 'dropdown') return;
		
		btn.addEventListener('click', function() {
			// Only add loading state for buttons that don't have href or form submission
			if (this.type === 'submit' || this.hasAttribute('href')) return;
			
			const originalText = this.innerHTML;
			this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
			this.disabled = true;
			
			// Re-enable after a delay
			setTimeout(() => {
				this.innerHTML = originalText;
				this.disabled = false;
			}, 2000);
		});
	});
}

// Smooth scroll to top functionality
window.addEventListener('scroll', () => {
	const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
	
	// Show/hide scroll to top button
			if (scrollTop > 300) {
			if (!document.getElementById('scrollToTop')) {
				const scrollBtn = document.createElement('button');
				scrollBtn.id = 'scrollToTop';
				scrollBtn.className = 'btn btn-primary position-fixed';
				scrollBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 50%; width: 50px; height: 50px; padding: 0; display: flex; align-items: center; justify-content: center;';
				scrollBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
				scrollBtn.addEventListener('click', () => {
					window.scrollTo({ top: 0, behavior: 'smooth' });
				});
				document.body.appendChild(scrollBtn);
			}
		} else {
		const scrollBtn = document.getElementById('scrollToTop');
		if (scrollBtn) scrollBtn.remove();
	}
});
