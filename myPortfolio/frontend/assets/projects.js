let allProjects = [];
let currentFilter = 'all';
let displayedCount = 6;

async function fetchJSON(url) {
	const res = await fetch(url);
	if (!res.ok) throw new Error(`Request failed: ${res.status}`);
	return res.json();
}

function renderTechBadges(tech) {
	if (!tech) return '';
	return tech.split(',').map(t => t.trim()).filter(Boolean).map(t => 
		`<span class="tech-badge">${t}</span>`
	).join('');
}

function formatDate(dateString) {
	const date = new Date(dateString);
	return date.toLocaleDateString('en-US', { 
		year: 'numeric', 
		month: 'long', 
		day: 'numeric' 
	});
}

function renderProjectCard(project) {
	return `
		<div class="col-lg-4 col-md-6 animate-fade-in-up">
			<div class="card project-card h-100 hover-lift">
				<div class="card-body d-flex flex-column">
					<div class="d-flex justify-content-between align-items-start mb-2">
						<h5 class="card-title">${project.title}</h5>
						<small class="text-muted">${formatDate(project.created_at)}</small>
					</div>
					<p class="card-text">${project.description}</p>
					<div class="project-tech mb-3">${renderTechBadges(project.tech_stack)}</div>
					<div class="project-links mt-auto">
						${project.github_link ? `
							<a class="btn btn-sm btn-outline-primary" href="${project.github_link}" target="_blank">
								<i class="bi bi-github"></i> Code
							</a>
						` : ''}
						${project.demo_link ? `
							<a class="btn btn-sm btn-accent" href="${project.demo_link}" target="_blank">
								<i class="bi bi-box-arrow-up-right"></i> Demo
							</a>
						` : ''}
					</div>
				</div>
			</div>
		</div>
	`;
}

function filterProjects() {
	const filteredProjects = currentFilter === 'all' 
		? allProjects 
		: allProjects.filter(project => {
			const tech = project.tech_stack?.toLowerCase() || '';
			switch (currentFilter) {
				case 'web':
					return tech.includes('html') || tech.includes('css') || tech.includes('javascript') || 
						   tech.includes('react') || tech.includes('vue') || tech.includes('angular');
				case 'api':
					return tech.includes('python') || tech.includes('flask') || tech.includes('django') || 
						   tech.includes('node') || tech.includes('express') || tech.includes('fastapi');
				case 'mobile':
					return tech.includes('react native') || tech.includes('flutter') || tech.includes('ionic') || 
						   tech.includes('mobile') || tech.includes('pwa');
				default:
					return true;
			}
		});
	
	return filteredProjects;
}

function displayProjects() {
	const container = document.getElementById('projectsContainer');
	const filteredProjects = filterProjects();
	const projectsToShow = filteredProjects.slice(0, displayedCount);
	
	if (projectsToShow.length === 0) {
		container.innerHTML = `
			<div class="col-12 text-center">
				<div class="alert alert-info">
					<i class="bi bi-info-circle"></i>
					No projects found for the selected filter. Try a different category or add some projects through the admin panel.
				</div>
			</div>
		`;
		return;
	}
	
	container.innerHTML = projectsToShow.map(renderProjectCard).join('');
	
	// Show/hide load more button
	const loadMoreBtn = document.getElementById('loadMoreBtn');
	if (filteredProjects.length > displayedCount) {
		loadMoreBtn.style.display = 'inline-block';
	} else {
		loadMoreBtn.style.display = 'none';
	}
	
	// Reset displayed count when filtering
	if (currentFilter !== 'all') {
		displayedCount = 6;
	}
}

async function loadProjects() {
	const container = document.getElementById('projectsContainer');
	
	try {
		allProjects = await fetchJSON('/api/projects');
		
		if (allProjects.length === 0) {
			container.innerHTML = `
				<div class="col-12 text-center">
					<div class="alert alert-warning">
						<i class="bi bi-exclamation-triangle"></i>
						No projects found. Add some projects through the admin panel to get started.
					</div>
				</div>
			`;
			return;
		}
		
		displayProjects();
		
	} catch (error) {
		console.error('Error loading projects:', error);
		container.innerHTML = `
			<div class="col-12 text-center">
				<div class="alert alert-danger">
					<i class="bi bi-exclamation-triangle"></i>
					Failed to load projects. Please try again later.
				</div>
			</div>
		`;
	}
}

function setupFilterButtons() {
	const filterButtons = document.querySelectorAll('[data-filter]');
	
	filterButtons.forEach(button => {
		button.addEventListener('click', () => {
			// Remove active class from all buttons
			filterButtons.forEach(btn => btn.classList.remove('active'));
			
			// Add active class to clicked button
			button.classList.add('active');
			
			// Update filter and display
			currentFilter = button.getAttribute('data-filter');
			displayedCount = 6;
			displayProjects();
		});
	});
}

function setupLoadMore() {
	const loadMoreBtn = document.getElementById('loadMoreBtn');
	if (loadMoreBtn) {
		loadMoreBtn.addEventListener('click', () => {
			displayedCount += 6;
			displayProjects();
		});
	}
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

// Initialize when DOM is loaded
window.addEventListener('DOMContentLoaded', () => {
	loadProjects();
	setupFilterButtons();
	setupLoadMore();
	setupAnimations();
});
