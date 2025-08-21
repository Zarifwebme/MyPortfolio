import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, jsonify, send_from_directory, request
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException, BadRequest, RequestEntityTooLarge

from .extensions import db
from .config import Config


def create_app() -> Flask:
	load_dotenv()

	app = Flask(__name__, instance_relative_config=True, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"))

	# Ensure instance folder exists
	Path(app.instance_path).mkdir(parents=True, exist_ok=True)

	# Load configuration from Config class
	app.config.from_object(Config)
	
	# Override with instance config if available
	app.config.from_pyfile('config.py', silent=True)

	# Init extensions
	db.init_app(app)

	# Register blueprints
	from .api import api_bp
	from .admin import admin_bp
	from .auth import auth_bp
	from .github import github_bp
	from .public import public_bp

	app.register_blueprint(api_bp, url_prefix="/api")
	app.register_blueprint(github_bp, url_prefix="/api")
	app.register_blueprint(auth_bp, url_prefix="/admin")
	app.register_blueprint(admin_bp, url_prefix="/admin")
	app.register_blueprint(public_bp)

	# Error handlers
	def _is_api_request() -> bool:
		try:
			return request.path.startswith("/api")
		except Exception:
			return False

	@app.errorhandler(404)
	def not_found(error):  # type: ignore[no-redef]
		if app.config.get("PREFERRED_URL_SCHEME") == "api" or _is_api_request():
			return jsonify({"error": "Not found"}), 404
		return (app.jinja_env.get_or_select_template("404.html").render(), 404)

	@app.errorhandler(500)
	def server_error(error):  # type: ignore[no-redef]
		app.logger.exception("Server error: %s", error)
		if app.config.get("PREFERRED_URL_SCHEME") == "api" or _is_api_request():
			return jsonify({"error": "Internal server error"}), 500
		return (app.jinja_env.get_or_select_template("500.html").render(), 500)

	@app.errorhandler(BadRequest)
	def handle_bad_request(error: BadRequest):
		message = getattr(error, "description", "Bad request") or "Bad request"
		if _is_api_request():
			return jsonify({"error": message}), 400
		return (app.jinja_env.get_or_select_template("500.html").render(), 400)

	@app.errorhandler(RequestEntityTooLarge)
	def handle_too_large(error: RequestEntityTooLarge):
		if _is_api_request():
			return jsonify({"error": "Uploaded file is too large"}), 413
		return ("File too large", 413)

	@app.errorhandler(HTTPException)
	def handle_http_exception(error: HTTPException):
		"""Return JSON for API requests instead of HTML for generic HTTP errors."""
		if _is_api_request():
			payload = {"error": error.name or "HTTP error", "detail": error.description}
			return jsonify(payload), error.code or 500
		return error

	# Logging
	_log_level = getattr(logging, str(app.config.get("LOG_LEVEL", "INFO")).upper(), logging.INFO)
	app.logger.setLevel(_log_level)
	log_path = os.path.join(app.instance_path, "app.log")
	file_handler = RotatingFileHandler(log_path, maxBytes=512 * 1024, backupCount=3)
	file_handler.setLevel(_log_level)
	formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
	file_handler.setFormatter(formatter)
	app.logger.addHandler(file_handler)

	# Create DB tables if not exist and run light migrations
	with app.app_context():
		from . import models  # noqa: F401
		db.create_all()
		# Lightweight migration: ensure projects.image_url column exists (SQLite only)
		try:
			from sqlalchemy import text
			with db.engine.connect() as conn:
				res = conn.execute(text("PRAGMA table_info(projects)"))
				cols = [row[1] for row in res]  # type: ignore[index]
				if "image_url" not in cols:
					conn.execute(text("ALTER TABLE projects ADD COLUMN image_url VARCHAR(300)"))
					conn.commit()
				# ensure blog_images table exists
				res2 = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='blog_images'"))
				if not list(res2):
					conn.execute(text("CREATE TABLE blog_images (id INTEGER PRIMARY KEY, blog_id INTEGER NOT NULL, image_url VARCHAR(300) NOT NULL, image_data BLOB, image_mime VARCHAR(100), alt_text VARCHAR(200), created_at DATETIME, FOREIGN KEY(blog_id) REFERENCES blogs(id) ON DELETE CASCADE)"))
					conn.commit()
				else:
					# add alt_text column if missing
					cols_bi = conn.execute(text("PRAGMA table_info(blog_images)")).fetchall()
					col_names_bi = [row[1] for row in cols_bi]
					if "alt_text" not in col_names_bi:
						conn.execute(text("ALTER TABLE blog_images ADD COLUMN alt_text VARCHAR(200)"))
						conn.commit()
					if "image_data" not in col_names_bi:
						conn.execute(text("ALTER TABLE blog_images ADD COLUMN image_data BLOB"))
						conn.commit()
					if "image_mime" not in col_names_bi:
						conn.execute(text("ALTER TABLE blog_images ADD COLUMN image_mime VARCHAR(100)"))
						conn.commit()

				# ensure project image columns exist
				cols_proj = conn.execute(text("PRAGMA table_info(projects)")).fetchall()
				col_names_proj = [row[1] for row in cols_proj]
				if "image_data" not in col_names_proj:
					conn.execute(text("ALTER TABLE projects ADD COLUMN image_data BLOB"))
					conn.commit()
				if "image_mime" not in col_names_proj:
					conn.execute(text("ALTER TABLE projects ADD COLUMN image_mime VARCHAR(100)"))
					conn.commit()

				# ensure site_settings table exists
				res3 = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='site_settings'"))
				if not list(res3):
					conn.execute(text("CREATE TABLE site_settings (id INTEGER PRIMARY KEY, key VARCHAR(120) UNIQUE NOT NULL, value TEXT, image_data BLOB, image_mime VARCHAR(100), created_at DATETIME)"))
					conn.commit()
		except Exception as exc:
			app.logger.warning("Skipping image_url migration: %s", exc)

	# Serve frontend assets
	frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

	@app.route("/assets/<path:filename>")
	def assets(filename: str):
		return send_from_directory(os.path.join(frontend_dir, "assets"), filename)

	# Ensure DB session cleanup and rollback on errors to avoid cascading failures
	@app.teardown_request
	def teardown_request_func(exc):  # type: ignore[no-redef]
		try:
			if exc is not None:
				db.session.rollback()
		finally:
			db.session.remove()

	return app
# Expose a module-level app instance for platforms that don't support --factory
app = create_app()
