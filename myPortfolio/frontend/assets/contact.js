async function submitContactForm(formData) {
	try {
		const response = await fetch('/api/contact', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(formData)
		});
		
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		
		const result = await response.json();
		return { success: true, data: result };
	} catch (error) {
		console.error('Error submitting form:', error);
		return { success: false, error: error.message };
	}
}

function showMessage(message, type = 'success') {
	const messageDiv = document.getElementById('formMessage');
	const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
	const icon = type === 'success' ? 'bi-check-circle' : 'bi-exclamation-triangle';
	
	messageDiv.innerHTML = `
		<div class="alert ${alertClass} alert-dismissible fade show" role="alert">
			<i class="bi ${icon} me-2"></i>
			${message}
			<button type="button" class="btn-close" data-bs-dismiss="alert"></button>
		</div>
	`;
	
	messageDiv.style.display = 'block';
	
	// Auto-hide success messages after 5 seconds
	if (type === 'success') {
		setTimeout(() => {
			messageDiv.style.display = 'none';
		}, 5000);
	}
}

function validateForm(formData) {
	const errors = [];
	
	// Required field validation
	if (!formData.firstName?.trim()) {
		errors.push('First name is required');
	}
	
	if (!formData.lastName?.trim()) {
		errors.push('Last name is required');
	}
	
	if (!formData.phoneNumber?.trim()) {
		errors.push('Phone number is required');
	} else if (!isValidPhoneNumber(formData.phoneNumber)) {
		errors.push('Please enter a valid phone number');
	}
	
	if (!formData.message?.trim()) {
		errors.push('Message is required');
	} else if (formData.message.length < 10) {
		errors.push('Message must be at least 10 characters long');
	}
	
	return errors;
}

function isValidPhoneNumber(phone) {
	// Basic phone number validation - allows various formats
	const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
	return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
}

function resetForm() {
	document.getElementById('contactForm').reset();
	document.getElementById('formMessage').style.display = 'none';
}

function setupFormSubmission() {
	const form = document.getElementById('contactForm');
	
	form.addEventListener('submit', async (e) => {
		e.preventDefault();
		
		// Get form data
		const formData = new FormData(form);
		const data = Object.fromEntries(formData.entries());
		
		// Validate form
		const errors = validateForm(data);
		if (errors.length > 0) {
			showMessage(errors.join('<br>'), 'error');
			return;
		}
		
		// Show loading state
		const submitBtn = form.querySelector('button[type="submit"]');
		const originalText = submitBtn.innerHTML;
		submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Sending...';
		submitBtn.disabled = true;
		
		try {
			// Submit form
			const result = await submitContactForm(data);
			
			if (result.success) {
				showMessage('Thank you for your message! I\'ll get back to you soon.', 'success');
				resetForm();
			} else {
				showMessage('Failed to send message. Please try again or contact me directly via email.', 'error');
			}
		} catch (error) {
			showMessage('An unexpected error occurred. Please try again later.', 'error');
		} finally {
			// Reset button state
			submitBtn.innerHTML = originalText;
			submitBtn.disabled = false;
		}
	});
}

// Form field focus effects
function setupFormFieldEffects() {
	const formFields = document.querySelectorAll('.form-control');
	
	formFields.forEach(field => {
		// Add focus effect
		field.addEventListener('focus', () => {
			field.parentElement.classList.add('focused');
		});
		
		// Remove focus effect
		field.addEventListener('blur', () => {
			field.parentElement.classList.remove('focused');
		});
		
		// Real-time validation feedback
		field.addEventListener('input', () => {
			validateField(field);
		});
	});
}

function validateField(field) {
	const value = field.value.trim();
	const fieldName = field.name;
	let isValid = true;
	let errorMessage = '';
	
	// Remove existing validation classes
	field.classList.remove('is-valid', 'is-invalid');
	
	// Field-specific validation
	switch (fieldName) {
		case 'firstName':
			if (!value) {
				isValid = false;
				errorMessage = 'First name is required';
			} else if (value.length < 2) {
				isValid = false;
				errorMessage = 'First name must be at least 2 characters';
			}
			break;
			
		case 'lastName':
			if (!value) {
				isValid = false;
				errorMessage = 'Last name is required';
			} else if (value.length < 2) {
				isValid = false;
				errorMessage = 'Last name must be at least 2 characters';
			}
			break;
			
		case 'phoneNumber':
			if (!value) {
				isValid = false;
				errorMessage = 'Phone number is required';
			} else if (!isValidPhoneNumber(value)) {
				isValid = false;
				errorMessage = 'Please enter a valid phone number';
			}
			break;
			
		case 'message':
			if (!value) {
				isValid = false;
				errorMessage = 'Message is required';
			} else if (value.length < 10) {
				isValid = false;
				errorMessage = 'Message must be at least 10 characters';
			}
			break;
	}
	
	// Apply validation styling
	if (isValid) {
		field.classList.add('is-valid');
	} else {
		field.classList.add('is-invalid');
	}
	
	// Show/hide error message
	let errorDiv = field.parentElement.querySelector('.invalid-feedback');
	if (!errorDiv) {
		errorDiv = document.createElement('div');
		errorDiv.className = 'invalid-feedback';
		field.parentElement.appendChild(errorDiv);
	}
	
	if (isValid) {
		errorDiv.style.display = 'none';
	} else {
		errorDiv.textContent = errorMessage;
		errorDiv.style.display = 'block';
	}
}

// Initialize when DOM is loaded
window.addEventListener('DOMContentLoaded', () => {
	setupFormSubmission();
	setupFormFieldEffects();
	
	// Add smooth scrolling for anchor links
	document.querySelectorAll('a[href^="#"]').forEach(anchor => {
		anchor.addEventListener('click', function (e) {
			e.preventDefault();
			const target = document.querySelector(this.getAttribute('href'));
			if (target) {
				target.scrollIntoView({
					behavior: 'smooth',
					block: 'start'
				});
			}
		});
	});
});
