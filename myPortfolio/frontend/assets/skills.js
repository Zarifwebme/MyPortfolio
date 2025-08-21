async function fetchJSON(url) {
	const res = await fetch(url);
	if (!res.ok) throw new Error(`Request failed: ${res.status}`);
	return res.json();
}

function getSkillLevelText(level) {
	if (level >= 90) return 'Expert';
	if (level >= 75) return 'Advanced';
	if (level >= 60) return 'Intermediate';
	if (level >= 40) return 'Beginner';
	return 'Learning';
}

function getSkillLevelColor(level) {
	if (level >= 90) return 'success';
	if (level >= 75) return 'primary';
	if (level >= 60) return 'info';
	if (level >= 40) return 'warning';
	return 'secondary';
}

async function loadSkills() {
	const container = document.getElementById('skillsContainer');
	if (!container) return;
	
	try {
		const skills = await fetchJSON('/api/skills');
		
		if (skills.length === 0) {
			container.innerHTML = `
				<div class="col-12 text-center">
					<div class="alert alert-info">
						<i class="bi bi-info-circle"></i>
						No skills found. Add some skills through the admin panel.
					</div>
				</div>
			`;
			return;
		}
		
		// Group skills by level for better organization
		const expertSkills = skills.filter(s => s.level >= 90);
		const advancedSkills = skills.filter(s => s.level >= 75 && s.level < 90);
		const intermediateSkills = skills.filter(s => s.level >= 60 && s.level < 75);
		const beginnerSkills = skills.filter(s => s.level < 60);
		
		container.innerHTML = `
			${expertSkills.length > 0 ? `
				<div class="col-12 mb-4">
					<h3 class="text-success mb-3">
						<i class="bi bi-star-fill me-2"></i>
						Expert Level
					</h3>
					<div class="row g-4">
						${expertSkills.map(skill => renderSkillCard(skill)).join('')}
					</div>
				</div>
			` : ''}
			
			${advancedSkills.length > 0 ? `
				<div class="col-12 mb-4">
					<h3 class="text-primary mb-3">
						<i class="bi bi-star me-2"></i>
						Advanced Level
					</h3>
					<div class="row g-4">
						${advancedSkills.map(skill => renderSkillCard(skill)).join('')}
					</div>
				</div>
			` : ''}
			
			${intermediateSkills.length > 0 ? `
				<div class="col-12 mb-4">
					<h3 class="text-info mb-3">
						<i class="bi bi-star-half me-2"></i>
						Intermediate Level
					</h3>
					<div class="row g-4">
						${intermediateSkills.map(skill => renderSkillCard(skill)).join('')}
					</div>
				</div>
			` : ''}
			
			${beginnerSkills.length > 0 ? `
				<div class="col-12 mb-4">
					<h3 class="text-warning mb-3">
						<i class="bi bi-star me-2"></i>
						Learning
					</h3>
					<div class="row g-4">
						${beginnerSkills.map(skill => renderSkillCard(skill)).join('')}
					</div>
				</div>
			` : ''}
		`;
		
		// Animate progress bars after rendering
		setTimeout(() => {
			animateProgressBars();
		}, 100);
		
	} catch (error) {
		console.error('Error loading skills:', error);
		container.innerHTML = `
			<div class="col-12 text-center">
				<div class="alert alert-danger">
					<i class="bi bi-exclamation-triangle"></i>
					Failed to load skills. Please try again later.
				</div>
			</div>
		`;
	}
}

function renderSkillCard(skill) {
	const levelColor = getSkillLevelColor(skill.level);
	const levelText = getSkillLevelText(skill.level);
	
	return `
		<div class="col-lg-4 col-md-4 animate-fade-in-up">
			<div class="card h-100 hover-lift">
				<div class="card-body">
					<div class="skill-item">
						<div class="skill-header">
							<span class="skill-name">${skill.name}</span>
							<span class="skill-level badge bg-${levelColor}">${levelText}</span>
						</div>
						<div class="progress">
							<div class="progress-bar bg-${levelColor}" 
								 role="progressbar" 
								 style="width: 0%" 
								 data-width="${skill.level}"
								 aria-valuenow="${skill.level}" 
								 aria-valuemin="0" 
								 aria-valuemax="100">
							</div>
						</div>
						<div class="text-end mt-2">
							<small class="text-muted">${skill.level}%</small>
						</div>
					</div>
				</div>
			</div>
		</div>
	`;
}

function animateProgressBars() {
	const progressBars = document.querySelectorAll('.progress-bar[data-width]');
	
	progressBars.forEach(bar => {
		const targetWidth = bar.getAttribute('data-width');
		setTimeout(() => {
			bar.style.width = targetWidth + '%';
		}, Math.random() * 500); // Stagger animation
	});
}

// Initialize when DOM is loaded
window.addEventListener('DOMContentLoaded', () => {
	loadSkills();
	
	// Setup animations
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
});
