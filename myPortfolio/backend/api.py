from flask import Blueprint, request, jsonify, current_app, session
from sqlalchemy.exc import SQLAlchemyError
import requests
import os

from .extensions import db
from .models import Project, Skill, Contact, ContactMessage, Blog, BlogCategory, BlogImage

api_bp = Blueprint("api", __name__)


# ---------- Helpers ----------

def commit_or_rollback():
	try:
		db.session.commit()
	except SQLAlchemyError as exc:
		current_app.logger.exception("DB error: %s", exc)
		db.session.rollback()
		raise


def send_telegram_message(message_text):
	"""Send message to Telegram bot"""
	try:
		# Get bot token from config (environment variable)
		bot_token = current_app.config.get('TELEGRAM_BOT_TOKEN')
		chat_id = current_app.config.get('TELEGRAM_CHAT_ID')
		
		if not bot_token:
			current_app.logger.error("TELEGRAM_BOT_TOKEN not set in environment variables")
			return False
		
		if not chat_id:
			current_app.logger.error("TELEGRAM_CHAT_ID not set in environment variables")
			return False
		
		url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
		data = {
			"chat_id": chat_id,
			"text": message_text,
			"parse_mode": "HTML"
		}
		
		response = requests.post(url, data=data, timeout=10)
		response.raise_for_status()
		
		current_app.logger.info("Telegram message sent successfully")
		return True
		
	except Exception as e:
		current_app.logger.error(f"Failed to send Telegram message: {e}")
		return False


# ---------- Contact Form ----------

@api_bp.post("/contact")
def submit_contact():
	"""Handle contact form submission and send to Telegram"""
	try:
		data = request.get_json(force=True)
		
		# Validate required fields
		required_fields = ['firstName', 'lastName', 'phoneNumber', 'message']
		for field in required_fields:
			if not data.get(field, '').strip():
				return jsonify({"error": f"{field} is required"}), 400
		
		# Format message for Telegram
		message_text = f"""
<b>📧 New Contact Form Submission</b>

👤 <b>Name:</b> {data['firstName']} {data['lastName']}
📱 <b>Phone:</b> {data['phoneNumber']}
💬 <b>Message:</b>

{data['message']}

---
<i>Sent from your portfolio website</i>
		""".strip()
		
		# Send to Telegram
		telegram_sent = send_telegram_message(message_text)
		
		# Save to database if available
		try:
			contact = ContactMessage(
				first_name=data['firstName'],
				last_name=data['lastName'],
				phone_number=data['phoneNumber'],
				message=data['message']
			)
			db.session.add(contact)
			commit_or_rollback()
		except Exception as db_error:
			current_app.logger.warning(f"Failed to save contact to database: {db_error}")
			# Continue even if database save fails
		
		# Return success response
		response_data = {
			"message": "Message sent successfully!",
			"telegram_sent": telegram_sent
		}
		
		return jsonify(response_data), 200
		
	except Exception as e:
		current_app.logger.error(f"Contact form error: {e}")
		return jsonify({"error": "Failed to process contact form"}), 500


# ---------- Projects ----------

@api_bp.get("/projects")
def list_projects():
	items = Project.query.order_by(Project.created_at.desc()).all()
	return jsonify([i.to_dict() for i in items])


@api_bp.post("/projects")
def create_project():
	data = request.get_json(force=True)
	item = Project(
		title=data.get("title", ""),
		description=data.get("description", ""),
		tech_stack=data.get("tech_stack"),
		github_link=data.get("github_link"),
		demo_link=data.get("demo_link"),
		image_url=data.get("image_url"),
	)
	db.session.add(item)
	commit_or_rollback()
	return jsonify(item.to_dict()), 201


@api_bp.get("/projects/<int:item_id>")
def get_project(item_id: int):
	item = Project.query.get_or_404(item_id)
	return jsonify(item.to_dict())


@api_bp.put("/projects/<int:item_id>")
@api_bp.patch("/projects/<int:item_id>")
def update_project(item_id: int):
	item = Project.query.get_or_404(item_id)
	data = request.get_json(force=True)
	for field in ["title", "description", "tech_stack", "github_link", "demo_link", "image_url"]:
		if field in data:
			setattr(item, field, data[field])
	commit_or_rollback()
	return jsonify(item.to_dict())


@api_bp.delete("/projects/<int:item_id>")
def delete_project(item_id: int):
	item = Project.query.get_or_404(item_id)
	db.session.delete(item)
	commit_or_rollback()
	return jsonify({"deleted": True})


# ---------- Skills ----------

@api_bp.get("/skills")
def list_skills():
	items = Skill.query.all()
	return jsonify([i.to_dict() for i in items])


@api_bp.post("/skills")
def create_skill():
	data = request.get_json(force=True)
	item = Skill(name=data.get("name", ""), level=data.get("level", ""))
	db.session.add(item)
	commit_or_rollback()
	return jsonify(item.to_dict()), 201


@api_bp.get("/skills/<int:item_id>")
def get_skill(item_id: int):
	item = Skill.query.get_or_404(item_id)
	return jsonify(item.to_dict())


@api_bp.put("/skills/<int:item_id>")
@api_bp.patch("/skills/<int:item_id>")
def update_skill(item_id: int):
	item = Skill.query.get_or_404(item_id)
	data = request.get_json(force=True)
	for field in ["name", "level"]:
		if field in data:
			setattr(item, field, data[field])
	commit_or_rollback()
	return jsonify(item.to_dict())


@api_bp.delete("/skills/<int:item_id>")
def delete_skill(item_id: int):
	item = Skill.query.get_or_404(item_id)
	db.session.delete(item)
	commit_or_rollback()
	return jsonify({"deleted": True})


# ---------- Blog Categories ----------

@api_bp.get("/categories")
def list_categories():
	items = BlogCategory.query.all()
	return jsonify([i.to_dict() for i in items])


@api_bp.post("/categories")
def create_category():
	# Only allow when admin session present
	if not session.get("admin_logged_in"):
		return jsonify({"error": "Unauthorized"}), 401
	data = request.get_json(force=True)
	item = BlogCategory(name=data.get("name", ""))
	db.session.add(item)
	commit_or_rollback()
	return jsonify(item.to_dict()), 201


@api_bp.get("/categories/<int:item_id>")
def get_category(item_id: int):
	item = BlogCategory.query.get_or_404(item_id)
	return jsonify(item.to_dict())


@api_bp.put("/categories/<int:item_id>")
@api_bp.patch("/categories/<int:item_id>")
def update_category(item_id: int):
	item = BlogCategory.query.get_or_404(item_id)
	data = request.get_json(force=True)
	if "name" in data:
		item.name = data["name"]
	commit_or_rollback()
	return jsonify(item.to_dict())


@api_bp.delete("/categories/<int:item_id>")
def delete_category(item_id: int):
	item = BlogCategory.query.get_or_404(item_id)
	db.session.delete(item)
	commit_or_rollback()
	return jsonify({"deleted": True})


# ---------- Blogs ----------

@api_bp.get("/blogs")
def list_blogs():
	category_id = request.args.get("category_id", type=int)
	query = Blog.query
	if category_id:
		query = query.filter(Blog.category_id == category_id)
	items = query.order_by(Blog.created_at.desc()).all()
	return jsonify([i.to_dict() for i in items])


@api_bp.post("/blogs")
def create_blog():
	data = request.get_json(force=True)
	item = Blog(
		title=data.get("title", ""),
		category_id=data.get("category_id"),
		content=data.get("content", ""),
	)
	db.session.add(item)
	commit_or_rollback()
	return jsonify(item.to_dict()), 201


@api_bp.get("/blogs/<int:item_id>")
def get_blog(item_id: int):
	item = Blog.query.get_or_404(item_id)
	return jsonify(item.to_dict())


@api_bp.get("/blogimages/<int:blog_id>")
def list_blog_images(blog_id: int):
	imgs = BlogImage.query.filter_by(blog_id=blog_id).all()
	return jsonify([i.to_dict() for i in imgs])


@api_bp.put("/blogs/<int:item_id>")
@api_bp.patch("/blogs/<int:item_id>")
def update_blog(item_id: int):
	item = Blog.query.get_or_404(item_id)
	data = request.get_json(force=True)
	for field in ["title", "category_id", "content"]:
		if field in data:
			setattr(item, field, data[field])
	commit_or_rollback()
	return jsonify(item.to_dict())


@api_bp.delete("/blogs/<int:item_id>")
def delete_blog(item_id: int):
	item = Blog.query.get_or_404(item_id)
	db.session.delete(item)
	commit_or_rollback()
	return jsonify({"deleted": True})
