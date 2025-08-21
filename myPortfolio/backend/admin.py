import os
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from .auth import login_required
from .extensions import db
from .models import Project, Skill, Contact, Blog, BlogCategory, BlogImage, SiteSetting

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/")
@login_required
def dashboard():
	def safe_count(model, table_name: str) -> int:
		try:
			return model.query.count()
		except Exception:
			try:
				from sqlalchemy import text
				res = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
				row = res.first()
				return int(row[0]) if row and row[0] is not None else 0
			except Exception:
				return 0

	stats = {
		"projects": safe_count(Project, "projects"),
		"skills": safe_count(Skill, "skills"),
		"contacts": safe_count(Contact, "contact"),
		"blogs": safe_count(Blog, "blogs"),
		"categories": safe_count(BlogCategory, "blog_categories"),
	}
	return render_template("admin/dashboard.html", stats=stats)


# ------------- Site Settings -------------

@admin_bp.route("/settings/hero", methods=["GET", "POST"])
@login_required
def admin_settings_hero():
	setting = SiteSetting.query.filter_by(key="hero_image").first()
	if request.method == "POST":
		file = request.files.get("image")
		if not setting:
			setting = SiteSetting(key="hero_image")
			db.session.add(setting)
		if file and file.filename:
			setting.image_data = file.read()
			setting.image_mime = file.mimetype or "image/png"
		db.session.commit()
		flash("Hero image updated", "success")
		return redirect(url_for("admin.admin_settings_hero"))
	return render_template("admin/setting_hero.html", setting=setting)


# ------------- CV Settings -------------

@admin_bp.route("/settings/cv", methods=["GET", "POST"])
@login_required
def admin_settings_cv():
	setting = SiteSetting.query.filter_by(key="cv_file").first()
	if request.method == "POST":
		file = request.files.get("cv")
		if not setting:
			setting = SiteSetting(key="cv_file")
			db.session.add(setting)
		if file and file.filename:
			filename = secure_filename(file.filename)
			ext = os.path.splitext(filename)[1].lower()
			# Allow only PDF files for CV uploads
			if ext in {".pdf"}:
				setting.image_data = file.read()
				setting.image_mime = file.mimetype or "application/pdf"
				db.session.commit()
				flash("CV updated", "success")
			else:
				flash("Only PDF files are allowed", "danger")
				db.session.rollback()
		else:
			db.session.commit()
			flash("CV setting saved", "success")
		return redirect(url_for("admin.admin_settings_cv"))
	return render_template("admin/setting_cv.html", setting=setting)

# ------------- Projects -------------

@admin_bp.get("/projects")
@login_required
def admin_projects():
	items = Project.query.order_by(Project.created_at.desc()).all()
	return render_template("admin/projects.html", items=items)


@admin_bp.route("/projects/create", methods=["GET", "POST"])
@login_required
def admin_project_create():
	if request.method == "POST":
		item = Project(
			title=request.form.get("title", ""),
			description=request.form.get("description", ""),
			tech_stack=request.form.get("tech_stack"),
			github_link=request.form.get("github_link"),
			demo_link=request.form.get("demo_link"),
		)
		# Handle image upload
		file = request.files.get("image")
		if file and file.filename:
			filename = secure_filename(file.filename)
			ext = os.path.splitext(filename)[1].lower()
			if ext := ext_validation(ext=ext):
				saved_name = f"{uuid4().hex}{ext}"
				upload_path = _get_upload_path()
				os.makedirs(upload_path, exist_ok=True)
				# Save to disk for backward compatibility
				file_path = os.path.join(upload_path, saved_name)
				file.save(file_path)
				item.image_url = f"/uploads/{saved_name}"
				# Also store in database
				file.seek(0)
				item.image_data = file.read()
				item.image_mime = file.mimetype or "application/octet-stream"
		db.session.add(item)
		db.session.commit()
		flash("Project created", "success")
		return redirect(url_for("admin.admin_projects"))
	return render_template("admin/project_form.html", item=None)


@admin_bp.route("/projects/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def admin_project_edit(item_id: int):
	item = Project.query.get_or_404(item_id)
	if request.method == "POST":
		item.title = request.form.get("title", item.title)
		item.description = request.form.get("description", item.description)
		item.tech_stack = request.form.get("tech_stack", item.tech_stack)
		item.github_link = request.form.get("github_link", item.github_link)
		item.demo_link = request.form.get("demo_link", item.demo_link)
		# Remove existing image if requested
		if request.form.get("remove_image") == "on" and item.image_url:
			try:
				_delete_uploaded_file(item.image_url)
			except Exception:
				pass
			item.image_url = None
		# Handle new upload (replaces existing)
		file = request.files.get("image")
		if file and file.filename:
			# Delete old file if exists
			if item.image_url:
				try:
					_delete_uploaded_file(item.image_url)
				except Exception:
					pass
			filename = secure_filename(file.filename)
			ext = os.path.splitext(filename)[1].lower()
			if ext := ext_validation(ext=ext):
				saved_name = f"{uuid4().hex}{ext}"
				upload_path = _get_upload_path()
				os.makedirs(upload_path, exist_ok=True)
				file.save(os.path.join(upload_path, saved_name))
				item.image_url = f"/uploads/{saved_name}"
		db.session.commit()
		flash("Project updated", "success")
		return redirect(url_for("admin.admin_projects"))
	return render_template("admin/project_form.html", item=item)


@admin_bp.post("/projects/<int:item_id>/delete")
@login_required
def admin_project_delete(item_id: int):
	item = Project.query.get_or_404(item_id)
	# Remove uploaded image file if present
	if getattr(item, "image_url", None):
		try:
			_delete_uploaded_file(item.image_url)
		except Exception:
			pass
	db.session.delete(item)
	db.session.commit()
	flash("Project deleted", "info")
	return redirect(url_for("admin.admin_projects"))


# ---------- Helpers for upload handling ----------

def ext_validation(*, ext: str) -> str | None:
	allowed = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
	return ext if ext in allowed else None


def _get_upload_path() -> str:
	"""Get the correct upload path that matches the public route"""
	return os.path.join(current_app.instance_path, "uploads")


def _delete_uploaded_file(image_url: str) -> None:
	if image_url.startswith("/uploads/"):
		fname = image_url.split("/uploads/", 1)[1]
		path = os.path.join(_get_upload_path(), fname)
		if os.path.exists(path):
			os.remove(path)


# ------------- Skills -------------

@admin_bp.get("/skills")
@login_required
def admin_skills():
	items = Skill.query.all()
	return render_template("admin/skills.html", items=items)


@admin_bp.route("/skills/create", methods=["GET", "POST"])
@login_required
def admin_skill_create():
	if request.method == "POST":
		item = Skill(name=request.form.get("name", ""), level=request.form.get("level", ""))
		db.session.add(item)
		db.session.commit()
		flash("Skill created", "success")
		return redirect(url_for("admin.admin_skills"))
	return render_template("admin/skill_form.html", item=None)


@admin_bp.route("/skills/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def admin_skill_edit(item_id: int):
	item = Skill.query.get_or_404(item_id)
	if request.method == "POST":
		item.name = request.form.get("name", item.name)
		item.level = request.form.get("level", item.level)
		db.session.commit()
		flash("Skill updated", "success")
		return redirect(url_for("admin.admin_skills"))
	return render_template("admin/skill_form.html", item=item)


@admin_bp.post("/skills/<int:item_id>/delete")
@login_required
def admin_skill_delete(item_id: int):
	item = Skill.query.get_or_404(item_id)
	db.session.delete(item)
	db.session.commit()
	flash("Skill deleted", "info")
	return redirect(url_for("admin.admin_skills"))


# ------------- Contact -------------

@admin_bp.get("/contact")
@login_required
def admin_contact():
	items = Contact.query.all()
	return render_template("admin/contact.html", items=items)


@admin_bp.route("/contact/create", methods=["GET", "POST"])
@login_required
def admin_contact_create():
	if request.method == "POST":
		item = Contact(
			email=request.form.get("email"),
			phone=request.form.get("phone"),
			linkedin=request.form.get("linkedin"),
			github=request.form.get("github"),
		)
		db.session.add(item)
		db.session.commit()
		flash("Contact created", "success")
		return redirect(url_for("admin.admin_contact"))
	return render_template("admin/contact_form.html", item=None)


@admin_bp.route("/contact/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def admin_contact_edit(item_id: int):
	item = Contact.query.get_or_404(item_id)
	if request.method == "POST":
		item.email = request.form.get("email", item.email)
		item.phone = request.form.get("phone", item.phone)
		item.linkedin = request.form.get("linkedin", item.linkedin)
		item.github = request.form.get("github", item.github)
		db.session.commit()
		flash("Contact updated", "success")
		return redirect(url_for("admin.admin_contact"))
	return render_template("admin/contact_form.html", item=item)


@admin_bp.post("/contact/<int:item_id>/delete")
@login_required
def admin_contact_delete(item_id: int):
	item = Contact.query.get_or_404(item_id)
	db.session.delete(item)
	db.session.commit()
	flash("Contact deleted", "info")
	return redirect(url_for("admin.admin_contact"))


# ------------- Categories -------------

@admin_bp.get("/categories")
@login_required
def admin_categories():
	items = BlogCategory.query.all()
	return render_template("admin/categories.html", items=items)


@admin_bp.route("/categories/create", methods=["GET", "POST"])
@login_required
def admin_category_create():
	if request.method == "POST":
		item = BlogCategory(name=request.form.get("name", ""))
		db.session.add(item)
		db.session.commit()
		flash("Category created", "success")
		return redirect(url_for("admin.admin_categories"))
	return render_template("admin/category_form.html", item=None)


@admin_bp.route("/categories/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def admin_category_edit(item_id: int):
	item = BlogCategory.query.get_or_404(item_id)
	if request.method == "POST":
		item.name = request.form.get("name", item.name)
		db.session.commit()
		flash("Category updated", "success")
		return redirect(url_for("admin.admin_categories"))
	return render_template("admin/category_form.html", item=item)


@admin_bp.post("/categories/<int:item_id>/delete")
@login_required
def admin_category_delete(item_id: int):
	item = BlogCategory.query.get_or_404(item_id)
	db.session.delete(item)
	db.session.commit()
	flash("Category deleted", "info")
	return redirect(url_for("admin.admin_categories"))


# ------------- Blogs -------------

@admin_bp.get("/blogs")
@login_required
def admin_blogs():
	items = Blog.query.order_by(Blog.created_at.desc()).all()
	cats = BlogCategory.query.all()
	return render_template("admin/blogs.html", items=items, categories=cats)


@admin_bp.route("/blogs/create", methods=["GET", "POST"])
@login_required
def admin_blog_create():
	cats = BlogCategory.query.all()
	if request.method == "POST":
		item = Blog(
			title=request.form.get("title", ""),
			category_id=request.form.get("category_id", type=int),
			content=request.form.get("content", ""),
		)
		db.session.add(item)
		db.session.commit()

		# handle multiple images
		files = request.files.getlist("images")
		upload_path = _get_upload_path()
		os.makedirs(upload_path, exist_ok=True)
		for file in files:
			if file and file.filename:
				filename = secure_filename(file.filename)
				ext = os.path.splitext(filename)[1].lower()
				if ext_validation(ext=ext):
					saved_name = f"{uuid4().hex}{ext}"
					# Save file to disk
					file_path = os.path.join(upload_path, saved_name)
					file.save(file_path)
					# Store both URL and blob
					file.seek(0)
					bi = BlogImage(blog_id=item.id, image_url=f"/uploads/{saved_name}")
					bi.image_data = file.read()
					bi.image_mime = file.mimetype or "application/octet-stream"
					db.session.add(bi)
		db.session.commit()
		flash("Blog created", "success")
		return redirect(url_for("admin.admin_blogs"))
	return render_template("admin/blog_form.html", item=None, categories=cats)


@admin_bp.route("/blogs/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def admin_blog_edit(item_id: int):
	item = Blog.query.get_or_404(item_id)
	cats = BlogCategory.query.all()
	if request.method == "POST":
		item.title = request.form.get("title", item.title)
		item.category_id = request.form.get("category_id", type=int) or None
		item.content = request.form.get("content", item.content)
		db.session.commit()

		# optional remove images
		for img in list(item.images):
			if request.form.get(f"remove_image_{img.id}") == "on":
				try:
					_delete_uploaded_file(img.image_url)
				except Exception:
					pass
				db.session.delete(img)

		# add new images
		files = request.files.getlist("images")
		upload_path = _get_upload_path()
		os.makedirs(upload_path, exist_ok=True)
		for file in files:
			if file and file.filename:
				filename = secure_filename(file.filename)
				ext = os.path.splitext(filename)[1].lower()
				if ext_validation(ext=ext):
					saved_name = f"{uuid4().hex}{ext}"
					file_path = os.path.join(upload_path, saved_name)
					file.save(file_path)
					file.seek(0)
					bi = BlogImage(blog_id=item.id, image_url=f"/uploads/{saved_name}")
					bi.image_data = file.read()
					bi.image_mime = file.mimetype or "application/octet-stream"
					db.session.add(bi)

		db.session.commit()
		flash("Blog updated", "success")
		return redirect(url_for("admin.admin_blogs"))
	return render_template("admin/blog_form.html", item=item, categories=cats)


@admin_bp.post("/blogs/<int:item_id>/delete")
@login_required
def admin_blog_delete(item_id: int):
	item = Blog.query.get_or_404(item_id)
	# delete images from disk
	for img in item.images:
		try:
			_delete_uploaded_file(img.image_url)
		except Exception:
			pass
	db.session.delete(item)
	db.session.commit()
	flash("Blog deleted", "info")
	return redirect(url_for("admin.admin_blogs"))
