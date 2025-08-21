async function fetchJSON(url) {
	const res = await fetch(url);
	if (!res.ok) throw new Error(`Request failed: ${res.status}`);
	return res.json();
}

function getQueryParam(name) {
	const params = new URLSearchParams(window.location.search);
	return params.get(name);
}

async function loadBlogDetail() {
	const container = document.getElementById('blogDetail');
	const id = getQueryParam('id');
	if (!id) {
		container.innerHTML = '<div class="alert alert-warning">Missing blog id.</div>';
		return;
	}
	try {
		const b = await fetchJSON(`/api/blogs/${id}`);
		// Render markdown to HTML using a simple renderer if available (e.g., marked). Fallback to basic line breaks.
		const markdown = b.content || '';
		let htmlContent = '';
		if (window.marked) {
			htmlContent = window.marked.parse(markdown);
		} else {
			htmlContent = markdown
				.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
				.replace(/\*(.*?)\*/g, '<em>$1</em>')
				.replace(/`([^`]+)`/g, '<code>$1</code>')
				.replace(/\n/g, '<br/>');
		}

		// Images gallery
		const images = Array.isArray(b.images) ? b.images : [];
		const gallery = images.length ? `
			<div class="row g-3 my-3">
				${images.map(img => `
					<div class="col-md-4">
						<img src="${img.image_url}" alt="${b.title}" class="img-fluid rounded border" />
					</div>
				`).join('')}
			</div>
		` : '';

		container.innerHTML = `
			<h1 class="mb-2">${b.title}</h1>
			<div class="text-muted mb-3">${b.category_name || ''} • ${new Date(b.created_at).toLocaleDateString()}</div>
			${gallery}
			<div>${htmlContent}</div>
		`;
	} catch (e) {
		container.innerHTML = `<div class="alert alert-danger">Failed to load blog.</div>`;
	}
}

window.addEventListener('DOMContentLoaded', loadBlogDetail);
