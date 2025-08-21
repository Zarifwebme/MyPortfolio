let allBlogs = [];
let allCategories = [];
let currentCategory = 'all';
let displayedCount = 6;

async function fetchJSON(url) {
	const res = await fetch(url);
	if (!res.ok) throw new Error(`Request failed: ${res.status}`);
	return res.json();
}

function formatDate(dateString) {
	const date = new Date(dateString);
	return date.toLocaleDateString('en-US', { 
		year: 'numeric', 
		month: 'long', 
		day: 'numeric' 
	});
}

function truncateText(text, maxLength = 150) {
	if (text.length <= maxLength) return text;
	return text.substring(0, maxLength).trim() + '...';
}

function setCategoryFilter(name) {
	const btn = Array.from(document.querySelectorAll('#categoryFilters button')).find(b => b.dataset.category === name);
	if (btn) btn.click();
}

function renderBlogCard(blog) {
	const category = allCategories.find(c => c.id === blog.category_id);
	const categoryName = category ? category.name : 'Uncategorized';
	
	return `
		<div class="col-lg-6 col-md-6 animate-fade-in-up">
			<div class="card blog-card h-100 hover-lift">
				<div class="card-body d-flex flex-column">
					<div class="d-flex justify-content-between align-items-center mb-2">
						<span class="blog-category">${categoryName}</span>
						<small class="text-muted">
							<i class="bi bi-calendar3 me-1"></i>
							${formatDate(blog.created_at)}
						</small>
					</div>
					<h5 class="card-title mb-2">${blog.title}</h5>
					<p class="card-text">${truncateText(blog.content)}</p>
					<div class="mt-auto d-flex justify-content-between align-items-center">
						<a href="/blog_detail.html?id=${blog.id}" class="btn btn-primary btn-sm">
							<i class="bi bi-journal-text me-1"></i>
							Read More
						</a>
						<a class="text-muted text-decoration-none" href="#" aria-label="View category" onclick="event.preventDefault(); setCategoryFilter('${categoryName}');">
							<i class="bi bi-tag me-1"></i>${categoryName}
						</a>
					</div>
				</div>
			</div>
		</div>
	`;
}

function filterBlogs() {
	const filteredBlogs = currentCategory === 'all' 
		? allBlogs 
		: allBlogs.filter(blog => {
			const category = allCategories.find(c => c.id === blog.category_id);
			if (!category) return false;
			return category.name.toLowerCase() === currentCategory.toLowerCase();
		});
	
	return filteredBlogs;
}

function displayBlogs() {
	const container = document.getElementById('blogContainer');
	const filteredBlogs = filterBlogs();
	const blogsToShow = filteredBlogs.slice(0, displayedCount);
	
	if (blogsToShow.length === 0) {
		container.innerHTML = `
			<div class="col-12 text-center">
				<div class="alert alert-info">
					<i class="bi bi-info-circle"></i>
					No blog posts found for the selected category. Try a different filter or add some posts through the admin panel.
				</div>
			</div>
		`;
		return;
	}
	
	container.innerHTML = blogsToShow.map(renderBlogCard).join('');
	
	// Show/hide load more button
	const loadMoreBtn = document.getElementById('loadMoreBtn');
	if (filteredBlogs.length > displayedCount) {
		loadMoreBtn.style.display = 'inline-block';
	} else {
		loadMoreBtn.style.display = 'none';
	}
	
	// Reset displayed count when filtering
	if (currentCategory !== 'all') {
		displayedCount = 6;
	}
}

async function loadBlogs() {
	const container = document.getElementById('blogContainer');
	
	try {
		// Load both blogs and categories
		const [blogs, categories] = await Promise.all([
			fetchJSON('/api/blogs'),
			fetchJSON('/api/categories')
		]);
		
		allBlogs = blogs;
		allCategories = categories;
		renderCategoryFilters();
		
		if (allBlogs.length === 0) {
			container.innerHTML = `
				<div class="col-12 text-center">
					<div class="alert alert-warning">
						<i class="bi bi-exclamation-triangle"></i>
						No blog posts found. Add some posts through the admin panel to get started.
					</div>
				</div>
			`;
			return;
		}
		
		displayBlogs();
		
	} catch (error) {
		console.error('Error loading blogs:', error);
		container.innerHTML = `
			<div class="col-12 text-center">
				<div class="alert alert-danger">
					<i class="bi bi-exclamation-triangle"></i>
					Failed to load blog posts. Please try again later.
				</div>
			</div>
		`;
	}
}

function renderCategoryFilters() {
	const container = document.getElementById('categoryFilters');
	if (!container) return;
	const buttons = [];
	buttons.push(`<button type="button" class="btn btn-outline-primary ${currentCategory==='all'?'active':''}" data-category="all">All</button>`);
	allCategories.forEach(cat => {
		const active = currentCategory.toLowerCase() === (cat.name||'').toLowerCase();
		buttons.push(`<button type=\"button\" class=\"btn btn-outline-primary ${active?'active':''}\" data-category=\"${cat.name}\">${cat.name}</button>`);
	});
	container.innerHTML = buttons.join('');
	setupCategoryFilters();
}

function setupCategoryFilters() {
	const filterButtons = document.querySelectorAll('#categoryFilters [data-category]');
	
	filterButtons.forEach(button => {
		button.addEventListener('click', () => {
			// Remove active class from all buttons
			filterButtons.forEach(btn => btn.classList.remove('active'));
			
			// Add active class to clicked button
			button.classList.add('active');
			
			// Update filter and display
			currentCategory = button.getAttribute('data-category');
			displayedCount = 6;
			displayBlogs();
		});
	});
}

function setupLoadMore() {
	const loadMoreBtn = document.getElementById('loadMoreBtn');
	if (loadMoreBtn) {
		loadMoreBtn.addEventListener('click', () => {
			displayedCount += 6;
			displayBlogs();
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
	loadBlogs();
	setupLoadMore();
	setupAnimations();
});
