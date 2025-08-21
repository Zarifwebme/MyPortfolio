import os
from flask import Blueprint, current_app, send_from_directory, make_response
from pathlib import Path

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
@public_bp.route("/index.html")
def index():
	frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
	return send_from_directory(frontend_dir, "index.html")


@public_bp.route("/media/hero.jpg")
def media_hero():
	"""Serve hero image from site settings if present, else 404."""
	try:
		from .models import SiteSetting
		setting = SiteSetting.query.filter_by(key="hero_image").first()
		if setting and setting.image_data:
			resp = make_response(setting.image_data)
			resp.headers.set('Content-Type', setting.image_mime or 'image/jpeg')
			return resp
	except Exception as e:
		current_app.logger.warning(f"Hero media fetch failed: {e}")
	return ("", 404)


@public_bp.route("/media/cv")
def media_cv():
	"""Serve CV file stored in site settings (PDF recommended)."""
	try:
		from .models import SiteSetting
		setting = SiteSetting.query.filter_by(key="cv_file").first()
		if setting and setting.image_data:
			resp = make_response(setting.image_data)
			mime = setting.image_mime or 'application/pdf'
			resp.headers.set('Content-Type', mime)
			disposition = 'inline' if mime == 'application/pdf' else 'attachment'
			resp.headers.set('Content-Disposition', f"{disposition}; filename=\"cv.pdf\"")
			return resp
	except Exception as e:
		current_app.logger.warning(f"CV media fetch failed: {e}")
	return ("", 404)


@public_bp.route("/health")
def health_check():
	"""Simple health check endpoint"""
	uploads_dir = os.path.join(current_app.instance_path, "uploads")
	uploads_exists = os.path.exists(uploads_dir)
	uploads_contents = os.listdir(uploads_dir) if uploads_exists else []
	
	return {
		"status": "healthy",
		"uploads_dir": uploads_dir,
		"uploads_exists": uploads_exists,
		"uploads_contents": uploads_contents,
		"instance_path": current_app.instance_path
	}


@public_bp.route("/uploads/<path:filename>")
def serve_upload(filename):
	"""Serve uploaded files from instance/uploads directory"""
	uploads_dir = os.path.join(current_app.instance_path, "uploads")
	
	# Ensure uploads directory exists
	Path(uploads_dir).mkdir(parents=True, exist_ok=True)
	
	# Check if file exists
	file_path = os.path.join(uploads_dir, filename)
	
	# Log the request for debugging
	current_app.logger.info(f"Upload request: {filename}")
	current_app.logger.info(f"Looking for file at: {file_path}")
	current_app.logger.info(f"File exists: {os.path.isfile(file_path)}")
	current_app.logger.info(f"Uploads directory contents: {os.listdir(uploads_dir) if os.path.exists(uploads_dir) else 'Directory not found'}")
	
	if not os.path.isfile(file_path):
		# Attempt to serve from database-backed storage for BlogImage and Project
		try:
			from .extensions import db
			from .models import BlogImage, Project
			# Try blog images
			img = BlogImage.query.filter(BlogImage.image_url == f"/uploads/{filename}").first()
			if img and img.image_data:
				resp = make_response(img.image_data)
				resp.headers.set('Content-Type', img.image_mime or 'application/octet-stream')
				return resp
			# Try project image by URL match
			proj = Project.query.filter(Project.image_url == f"/uploads/{filename}").first()
			if proj and proj.image_data:
				resp = make_response(proj.image_data)
				resp.headers.set('Content-Type', proj.image_mime or 'application/octet-stream')
				return resp
		except Exception as e:
			current_app.logger.warning(f"DB media fallback failed: {e}")
		current_app.logger.warning(f"File not found: {file_path}")
		return f"File not found: {filename}", 404
	
	return send_from_directory(uploads_dir, filename)


@public_bp.route("/<path:filename>")
def public_files(filename):
	frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
	file_path = os.path.join(frontend_dir, filename)
	if os.path.isfile(file_path):
		return send_from_directory(frontend_dir, filename)
	return (current_app.jinja_env.get_or_select_template("404.html").render(), 404)
