import os
from time import time
from flask import Blueprint, jsonify, request, current_app
import requests

github_bp = Blueprint("github", __name__)


# -------- Simple in-memory cache to reduce GitHub API calls --------
_CACHE_TTL_SECONDS = int(os.getenv("GITHUB_CACHE_TTL", "300"))  # default 5 minutes
_cache_store: dict[str, dict] = {}


def _cache_get(key: str):
	entry = _cache_store.get(key)
	if not entry:
		return None
	if time() - entry.get("ts", 0) < _CACHE_TTL_SECONDS:
		return entry.get("data")
	return None


def _cache_set(key: str, data):
	_cache_store[key] = {"ts": time(), "data": data}


def _build_github_headers() -> dict:
	headers = {
		'User-Agent': 'Portfolio-App/1.0',
		'Accept': 'application/vnd.github.v3+json'
	}
	# Use a token when provided to avoid low unauthenticated rate limits
	token = os.getenv("GITHUB_TOKEN")
	if token:
		headers['Authorization'] = f"Bearer {token}"
	return headers


@github_bp.get("/github/stats")
def github_stats():
	username = request.args.get("username") or os.getenv("GITHUB_USERNAME")
	if not username:
		return jsonify({"error": "GitHub username not configured. Please set GITHUB_USERNAME in environment variables."}), 400

	try:
		# Get user info
		user_url = f"https://api.github.com/users/{username}"
		repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
		headers = _build_github_headers()

		# Serve from cache if available
		_cache_key = f"stats:{username}"
		cached = _cache_get(_cache_key)
		if cached is not None:
			return jsonify(cached)

		# Fetch user and repos data
		user_resp = requests.get(user_url, headers=headers, timeout=15)
		repos_resp = requests.get(repos_url, headers=headers, timeout=15)
		
		user_resp.raise_for_status()
		repos_resp.raise_for_status()
		
		user_data = user_resp.json()
		repos_data = repos_resp.json()
		
		# Calculate statistics
		total_stars = sum(r.get("stargazers_count", 0) for r in repos_data)
		total_forks = sum(r.get("forks_count", 0) for r in repos_data)
		total_watchers = sum(r.get("watchers_count", 0) for r in repos_data)
		
		# Get top languages
		languages = {}
		for repo in repos_data:
			lang = repo.get("language")
			if lang:
				languages[lang] = languages.get(lang, 0) + 1
		
		# Sort languages by frequency
		top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
		
		# Get most starred repos
		top_starred = sorted(repos_data, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:5]
		top_starred = [
			{
				"name": r.get("name"),
				"description": r.get("description"),
				"stargazers_count": r.get("stargazers_count", 0),
				"language": r.get("language"),
				"html_url": r.get("html_url")
			}
			for r in top_starred
		]
		
		# Get recently updated repos
		recent_repos = sorted(repos_data, key=lambda x: x.get("updated_at", ""), reverse=True)[:5]
		recent_repos = [
			{
				"name": r.get("name"),
				"description": r.get("description"),
				"updated_at": r.get("updated_at"),
				"language": r.get("language"),
				"html_url": r.get("html_url")
			}
			for r in recent_repos
		]
		
		stats = {
			"user": {
				"login": user_data.get("login"),
				"name": user_data.get("name"),
				"avatar_url": user_data.get("avatar_url"),
				"bio": user_data.get("bio"),
				"location": user_data.get("location"),
				"company": user_data.get("company"),
				"hireable": user_data.get("hireable"),
				"public_repos": user_data.get("public_repos"),
				"followers": user_data.get("followers"),
				"following": user_data.get("following"),
				"created_at": user_data.get("created_at"),
				"html_url": user_data.get("html_url")
			},
			"repositories": {
				"total": len(repos_data),
				"total_stars": total_stars,
				"total_forks": total_forks,
				"total_watchers": total_watchers,
				"average_stars": round(total_stars / len(repos_data), 1) if repos_data else 0,
				"average_forks": round(total_forks / len(repos_data), 1) if repos_data else 0
			},
			"top_languages": top_languages,
			"top_starred": top_starred,
			"recent_repos": recent_repos
		}
		# Cache result to reduce API calls
		_cache_set(_cache_key, stats)

		current_app.logger.info(f"Successfully fetched GitHub stats for user {username}")
		return jsonify(stats)
		
	except requests.exceptions.Timeout:
		current_app.logger.error("GitHub API request timed out")
		return jsonify({"error": "Request to GitHub API timed out. Please try again later."}), 504
		
	except requests.exceptions.RequestException as exc:
		current_app.logger.exception("GitHub stats fetch failed: %s", exc)
		if hasattr(exc, 'response') and exc.response is not None:
			if exc.response.status_code == 404:
				return jsonify({"error": f"GitHub user '{username}' not found"}), 404
			elif exc.response.status_code == 403:
				return jsonify({"error": "GitHub API rate limit exceeded. Please try again later."}), 429
		
		return jsonify({"error": "Failed to fetch GitHub statistics."}), 502
		
	except Exception as exc:
		current_app.logger.exception("Unexpected error in GitHub stats endpoint: %s", exc)
		return jsonify({"error": "An unexpected error occurred while fetching GitHub statistics."}), 500


@github_bp.get("/github/user")
def github_user():
	username = request.args.get("username") or os.getenv("GITHUB_USERNAME")
	if not username:
		return jsonify({"error": "GitHub username not configured. Please set GITHUB_USERNAME in environment variables."}), 400

	url = f"https://api.github.com/users/{username}"
	
	try:
		headers = _build_github_headers()

		# Serve from cache if available
		_cache_key = f"user:{username}"
		cached = _cache_get(_cache_key)
		if cached is not None:
			return jsonify(cached)

		resp = requests.get(url, headers=headers, timeout=15)
		resp.raise_for_status()
		data = resp.json()
		
		# Map user data
		mapped = {
			"login": data.get("login"),
			"id": data.get("id"),
			"name": data.get("name"),
			"email": data.get("email"),
			"bio": data.get("bio"),
			"company": data.get("company"),
			"blog": data.get("blog"),
			"location": data.get("location"),
			"hireable": data.get("hireable"),
			"public_repos": data.get("public_repos"),
			"public_gists": data.get("public_gists"),
			"followers": data.get("followers"),
			"following": data.get("following"),
			"created_at": data.get("created_at"),
			"updated_at": data.get("updated_at"),
			"avatar_url": data.get("avatar_url"),
			"html_url": data.get("html_url"),
			"type": data.get("type"),
			"site_admin": data.get("site_admin")
		}
		
		# Cache
		_cache_set(_cache_key, mapped)

		current_app.logger.info(f"Successfully fetched GitHub user profile for {username}")
		return jsonify(mapped)
		
	except requests.exceptions.Timeout:
		current_app.logger.error("GitHub API request timed out")
		return jsonify({"error": "Request to GitHub API timed out. Please try again later."}), 504
		
	except requests.exceptions.RequestException as exc:
		current_app.logger.exception("GitHub user fetch failed: %s", exc)
		if hasattr(exc, 'response') and exc.response is not None:
			if exc.response.status_code == 404:
				return jsonify({"error": f"GitHub user '{username}' not found"}), 404
			elif exc.response.status_code == 403:
				return jsonify({"error": "GitHub API rate limit exceeded. Please try again later."}), 429
		
		return jsonify({"error": "Failed to fetch user profile from GitHub."}), 502
		
	except Exception as exc:
		current_app.logger.exception("Unexpected error in GitHub user endpoint: %s", exc)
		return jsonify({"error": "An unexpected error occurred while fetching user profile."}), 500


@github_bp.get("/github/repos")
def github_repos():
	username = request.args.get("username") or os.getenv("GITHUB_USERNAME")
	if not username:
		return jsonify({"error": "GitHub username not configured. Please set GITHUB_USERNAME in environment variables."}), 400

	url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
	
	try:
		headers = _build_github_headers()

		# Serve from cache if available
		_cache_key = f"repos:{username}"
		cached = _cache_get(_cache_key)
		if cached is not None:
			return jsonify(cached)

		resp = requests.get(url, headers=headers, timeout=15)
		resp.raise_for_status()
		data = resp.json()
		
		# Map repository data with all necessary fields
		mapped = [
			{
				"id": r.get("id"),
				"name": r.get("name"),
				"full_name": r.get("full_name"),
				"description": r.get("description"),
				"html_url": r.get("html_url"),
				"clone_url": r.get("clone_url"),
				"language": r.get("language"),
				"stargazers_count": r.get("stargazers_count", 0),
				"forks_count": r.get("forks_count", 0),
				"watchers_count": r.get("watchers_count", 0),
				"open_issues_count": r.get("open_issues_count", 0),
				"fork": r.get("fork", False),
				"archived": r.get("archived", False),
				"disabled": r.get("disabled", False),
				"private": r.get("private", False),
				"created_at": r.get("created_at"),
				"updated_at": r.get("updated_at"),
				"pushed_at": r.get("pushed_at"),
				"size": r.get("size", 0),
				"default_branch": r.get("default_branch", "main"),
				"topics": r.get("topics", []),
				"license": r.get("license", {}).get("name") if r.get("license") else None,
				"homepage": r.get("homepage"),
				"has_wiki": r.get("has_wiki", False),
				"has_pages": r.get("has_pages", False),
				"has_downloads": r.get("has_downloads", False),
				"has_issues": r.get("has_issues", True),
				"has_projects": r.get("has_projects", False)
			}
			for r in data
		]
		
		# Sort by stars, then by update date
		mapped.sort(key=lambda x: (x["stargazers_count"], x["updated_at"]), reverse=True)
		
		# Cache
		_cache_set(_cache_key, mapped)

		current_app.logger.info(f"Successfully fetched {len(mapped)} repositories for user {username}")
		return jsonify(mapped)
		
	except requests.exceptions.Timeout:
		current_app.logger.error("GitHub API request timed out")
		return jsonify({"error": "Request to GitHub API timed out. Please try again later."}), 504
		
	except requests.exceptions.RequestException as exc:
		current_app.logger.exception("GitHub fetch failed: %s", exc)
		if hasattr(exc, 'response') and exc.response is not None:
			if exc.response.status_code == 404:
				return jsonify({"error": f"GitHub user '{username}' not found"}), 404
			elif exc.response.status_code == 403:
				return jsonify({"error": "GitHub API rate limit exceeded. Please try again later."}), 429
			elif exc.response.status_code >= 500:
				return jsonify({"error": "GitHub API is currently unavailable. Please try again later."}), 502
		
		return jsonify({"error": "Failed to fetch repositories from GitHub. Please check your username and try again."}), 502
		
	except Exception as exc:
		current_app.logger.exception("Unexpected error in GitHub repos endpoint: %s", exc)
		return jsonify({"error": "An unexpected error occurred while fetching repositories."}), 500
