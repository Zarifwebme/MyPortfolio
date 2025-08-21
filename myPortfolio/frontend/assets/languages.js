const languages = {
	en: {
		// Navigation
		nav: {
			home: "Home",
			about: "About Me",
			projects: "Projects",
			skills: "Skills",
			contact: "Contact"
		},
		
		// Hero Section
		hero: {
			greeting: "Hi, I'm",
			subtitle: "Full-stack developer crafting reliable, scalable web applications with modern technologies.",
			viewProjects: "View Projects",
			githubRepos: "GitHub Repos"
		},
		
		// About Section
		about: {
			title: "About Me",
			description: "I am a software engineer specialized in creating efficient, optimized, and user-friendly solutions. Through my portfolio projects, you can explore my programming skills, creativity, and passion for technology. In every project, I focus on delivering both quality and impactful results.",
			downloadCV: "Download CV",
			features: {
				cleanCode: {
					title: "Clean Code",
					description: "Writing maintainable, well-documented code"
				},
				performance: {
					title: "Performance",
					description: "Optimizing for speed and efficiency"
				},
				responsive: {
					title: "Responsive",
					description: "Mobile-first design approach"
				}
			}
		},
		
		// Projects Section
		projects: {
			title: "Featured Projects",
			description: "A selection of my recent work showcasing different technologies and solutions."
		},
		
		// Skills Section
		skills: {
			title: "Skills",
			description: "A quick overview of my technical skills and proficiency levels."
		},
		
		// GitHub Section
		github: {
			title: "GitHub Repositories",
			description: "Explore my open-source contributions and personal projects."
		},
		
		// Contact Section
		contact: {
			title: "Contact Me",
			description: "Have a question or want to work together? Send me a message.",
			form: {
				title: "Send a Message",
				firstName: "First Name *",
				lastName: "Last Name *",
				phoneNumber: "Phone Number *",
				message: "Message *",
				messagePlaceholder: "Tell me about your project, question, or how I can help you...",
				sendMessage: "Send Message"
			}
		},
		
		// Footer
		footer: {
			copyright: "All rights reserved."
		}
	},
	
	uz: {
		// Navigation
		nav: {
			home: "Bosh sahifa",
			about: "Men haqimda",
			projects: "Loyihalar",
			skills: "Ko'nikmalar",
			contact: "Aloqa"
		},
		
		// Hero Section
		hero: {
			greeting: "Salom, men",
			subtitle: "Zamonaviy texnologiyalar bilan ishonchli va kengaytiriladigan veb-ilovalar yaratuvchi full-stack dasturchi.",
			viewProjects: "Loyihalarni ko'rish",
			githubRepos: "GitHub Repolar"
		},
		
		// About Section
		about: {
			title: "Men haqida",
			description: "Men samarali, optimallashtirilgan va foydalanuvchilar uchun qulay yechimlar yaratishda ixtisoslashgan dastur muhandisiman. Portfoliomdagi loyihalar orqali mening dasturlash ko'nikmalarim, ijodkorligim va texnologiyaga bo'lgan ishtiyoqimni ko'rishingiz mumkin. Har bir loyihada men sifat va samarali natijalarni taqdim etishga e'tibor beraman.",
			downloadCV: "CV yuklab olish",
			features: {
				cleanCode: {
					title: "Toza kod",
					description: "Saqlash mumkin, yaxshi hujjatlashtirilgan kod yozish"
				},
				performance: {
					title: "Samaradorlik",
					description: "Tezlik va samaradorlik uchun optimallashtirish"
				},
				responsive: {
					title: "Moslashuvchan",
					description: "Mobil birinchi dizayn yondashuvi"
				}
			}
		},
		
		// Projects Section
		projects: {
			title: "Asosiy loyihalar",
			description: "Turli texnologiyalar va yechimlarni ko'rsatadigan so'nggi ishlarimning tanlovi."
		},
		
		// Skills Section
		skills: {
			title: "Ko'nikmalar",
			description: "Mening texnik ko'nikmalarim va darajalarim haqida qisqacha ma'lumot."
		},
		
		// GitHub Section
		github: {
			title: "GitHub Repolar",
			description: "Mening ochiq manba hissasi va shaxsiy loyihalarimni kashf eting."
		},
		
		// Contact Section
		contact: {
			title: "Men bilan bog'laning",
			description: "Savolingiz bormi yoki birgalikda ishlashni xohlaysizmi? Menga xabar yuboring.",
			form: {
				title: "Xabar yuborish",
				firstName: "Ism *",
				lastName: "Familiya *",
				phoneNumber: "Telefon raqami *",
				message: "Xabar *",
				messagePlaceholder: "Loyihangiz, savolingiz yoki men qanday yordam bera olishim haqida gapirib bering...",
				sendMessage: "Xabar yuborish"
			}
		},
		
		// Footer
		footer: {
			copyright: "Barcha huquqlar himoyalangan."
		}
	}
};

// Language switching functionality
let currentLanguage = 'en';

function getPreferredLanguage() {
	// 1) URL param override
	try {
		const params = new URLSearchParams(window.location.search);
		const urlLang = params.get('lang');
		if (urlLang && languages[urlLang]) return urlLang;
	} catch (e) {}
	// 2) Saved preference
	const saved = localStorage.getItem('portfolioLanguage');
	if (saved && languages[saved]) return saved;
	// 3) Browser locale
	const navLang = (navigator.language || navigator.userLanguage || '').toLowerCase();
	if (navLang.startsWith('uz')) return 'uz';
	return 'uz';
}

function switchLanguage(lang) {
	currentLanguage = lang;
	updatePageContent();
	
	updateLanguageSelectorUI(lang);
	
	// Store preference in localStorage
	localStorage.setItem('portfolioLanguage', lang);

	// Reflect in URL without reload
	try {
		const url = new URL(window.location.href);
		url.searchParams.set('lang', lang);
		history.replaceState(null, '', url);
	} catch (e) {}

	// Inform other scripts
	window.dispatchEvent(new Event('languageChanged'));
}

function updatePageContent() {
	const lang = languages[currentLanguage];
	
	// Update navigation
	updateElementText('[data-lang="nav.home"]', lang.nav.home);
	updateElementText('[data-lang="nav.about"]', lang.nav.about);
	updateElementText('[data-lang="nav.projects"]', lang.nav.projects);
	updateElementText('[data-lang="nav.skills"]', lang.nav.skills);
	updateElementText('[data-lang="nav.contact"]', lang.nav.contact);
	
	// Update hero section
	updateElementText('[data-lang="hero.greeting"]', lang.hero.greeting);
	updateElementText('[data-lang="hero.subtitle"]', lang.hero.subtitle);
	updateElementText('[data-lang="hero.viewProjects"]', lang.hero.viewProjects);
	updateElementText('[data-lang="hero.githubRepos"]', lang.hero.githubRepos);
	
	// Update about section
	updateElementText('[data-lang="about.title"]', lang.about.title);
	updateElementText('[data-lang="about.description"]', lang.about.description);
	updateElementText('[data-lang="about.features.cleanCode.title"]', lang.about.features.cleanCode.title);
	updateElementText('[data-lang="about.features.cleanCode.description"]', lang.about.features.cleanCode.description);
	updateElementText('[data-lang="about.features.performance.title"]', lang.about.features.performance.title);
	updateElementText('[data-lang="about.features.performance.description"]', lang.about.features.performance.description);
	updateElementText('[data-lang="about.features.responsive.title"]', lang.about.features.responsive.title);
	updateElementText('[data-lang="about.features.responsive.description"]', lang.about.features.responsive.description);
	
	// Update projects section
	updateElementText('[data-lang="projects.title"]', lang.projects.title);
	updateElementText('[data-lang="projects.description"]', lang.projects.description);
	
	// Update skills section
	updateElementText('[data-lang="skills.title"]', lang.skills.title);
	updateElementText('[data-lang="skills.description"]', lang.skills.description);
	
	// Update GitHub section
	updateElementText('[data-lang="github.title"]', lang.github.title);
	updateElementText('[data-lang="github.description"]', lang.github.description);
	
	// Update contact section
	updateElementText('[data-lang="contact.title"]', lang.contact.title);
	updateElementText('[data-lang="contact.description"]', lang.contact.description);
	updateElementText('[data-lang="contact.form.title"]', lang.contact.form.title);
	updateElementText('[data-lang="contact.form.firstName"]', lang.contact.form.firstName);
	updateElementText('[data-lang="contact.form.lastName"]', lang.contact.form.lastName);
	updateElementText('[data-lang="contact.form.phoneNumber"]', lang.contact.form.phoneNumber);
	updateElementText('[data-lang="contact.form.message"]', lang.contact.form.message);
	updateElementText('[data-lang="contact.form.messagePlaceholder"]', lang.contact.form.messagePlaceholder);
	updateElementText('[data-lang="contact.form.sendMessage"]', lang.contact.form.sendMessage);
	
	// Update footer
	updateElementText('[data-lang="footer.copyright"]', lang.footer.copyright);
}

function updateLanguageSelectorUI(lang) {
	const labelMap = { en: 'EN', uz: "UZ" };
	const langSelectors = document.querySelectorAll('.language-selector');
	langSelectors.forEach(selector => {
		selector.textContent = labelMap[lang] || lang.toUpperCase();
	});

	// Update dropdown active state and aria
	document.querySelectorAll('[data-language-option]').forEach(item => {
		const isActive = item.getAttribute('data-language-option') === lang;
		item.classList.toggle('active', isActive);
		item.setAttribute('aria-checked', isActive ? 'true' : 'false');
	});
}

function updateElementText(selector, text) {
	const elements = document.querySelectorAll(selector);
	elements.forEach(element => {
		if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
			if (element.hasAttribute('placeholder')) {
				element.placeholder = text;
			} else {
				element.value = text;
			}
		} else {
			element.textContent = text;
		}
	});
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
	// Determine initial language
	currentLanguage = getPreferredLanguage();
	updateLanguageSelectorUI(currentLanguage);
	updatePageContent();

	// Event delegation for language options
	document.addEventListener('click', (e) => {
		const target = e.target.closest('[data-language-option]');
		if (!target) return;
		e.preventDefault();
		const lang = target.getAttribute('data-language-option');
		if (lang && languages[lang]) {
			switchLanguage(lang);
			// Close dropdown if open
			try {
				const dropdownEl = document.getElementById('languageDropdown');
				if (dropdownEl) {
					const dropdown = bootstrap.Dropdown.getOrCreateInstance(dropdownEl);
					dropdown.hide();
				}
			} catch (e) {}
		}
	});
});

// Export for use in other scripts
window.languages = languages;
window.switchLanguage = switchLanguage;
window.currentLanguage = currentLanguage;
