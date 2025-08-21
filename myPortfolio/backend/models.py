from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, LargeBinary

from .extensions import db


class Project(db.Model):
	__tablename__ = "projects"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	title: Mapped[str] = mapped_column(String(200), nullable=False)
	description: Mapped[str] = mapped_column(Text, nullable=False)
	tech_stack: Mapped[str] = mapped_column(String(300), nullable=True)
	github_link: Mapped[str] = mapped_column(String(300), nullable=True)
	demo_link: Mapped[str] = mapped_column(String(300), nullable=True)
	image_url: Mapped[str | None] = mapped_column(String(300), nullable=True)
	image_data: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
	image_mime: Mapped[str | None] = mapped_column(String(100), nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"title": self.title,
			"description": self.description,
			"tech_stack": self.tech_stack,
			"github_link": self.github_link,
			"demo_link": self.demo_link,
			"image_url": self.image_url,
			"created_at": self.created_at.isoformat() if self.created_at else None,
		}


class Skill(db.Model):
	__tablename__ = "skills"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(String(120), nullable=False)
	level: Mapped[str] = mapped_column(String(120), nullable=False)

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"name": self.name,
			"level": self.level,
		}


class Contact(db.Model):
	__tablename__ = "contact"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	email: Mapped[str | None] = mapped_column(String(200), nullable=True)
	phone: Mapped[str | None] = mapped_column(String(100), nullable=True)
	linkedin: Mapped[str | None] = mapped_column(String(300), nullable=True)
	github: Mapped[str | None] = mapped_column(String(300), nullable=True)

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"email": self.email,
			"phone": self.phone,
			"linkedin": self.linkedin,
			"github": self.github,
		}


class ContactMessage(db.Model):
	__tablename__ = "contact_messages"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	first_name: Mapped[str] = mapped_column(String(100), nullable=False)
	last_name: Mapped[str] = mapped_column(String(100), nullable=False)
	phone_number: Mapped[str] = mapped_column(String(100), nullable=False)
	message: Mapped[str] = mapped_column(Text, nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"first_name": self.first_name,
			"last_name": self.last_name,
			"phone_number": self.phone_number,
			"message": self.message,
			"created_at": self.created_at.isoformat() if self.created_at else None,
		}


class BlogCategory(db.Model):
	__tablename__ = "blog_categories"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
	blogs: Mapped[list["Blog"]] = relationship("Blog", back_populates="category", cascade="all, delete-orphan")

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"name": self.name,
		}


class Blog(db.Model):
	__tablename__ = "blogs"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	title: Mapped[str] = mapped_column(String(200), nullable=False)
	category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("blog_categories.id"), nullable=True)
	content: Mapped[str] = mapped_column(Text, nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	category: Mapped[BlogCategory | None] = relationship("BlogCategory", back_populates="blogs")
	images: Mapped[list["BlogImage"]] = relationship("BlogImage", back_populates="blog", cascade="all, delete-orphan")

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"title": self.title,
			"category_id": self.category_id,
			"category_name": self.category.name if self.category else None,
			"content": self.content,
			"created_at": self.created_at.isoformat() if self.created_at else None,
		}


class BlogImage(db.Model):
	__tablename__ = "blog_images"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	blog_id: Mapped[int] = mapped_column(Integer, ForeignKey("blogs.id"), nullable=False)
	image_url: Mapped[str] = mapped_column(String(300), nullable=False)
	image_data: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
	image_mime: Mapped[str | None] = mapped_column(String(100), nullable=True)
	alt_text: Mapped[str] = mapped_column(String(200), nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	blog: Mapped["Blog"] = relationship("Blog", back_populates="images")

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"blog_id": self.blog_id,
			"image_url": self.image_url,
			"alt_text": self.alt_text,
			"created_at": self.created_at.isoformat() if self.created_at else None,
		}


class SiteSetting(db.Model):
	__tablename__ = "site_settings"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	key: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
	value: Mapped[str | None] = mapped_column(Text, nullable=True)
	image_data: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
	image_mime: Mapped[str | None] = mapped_column(String(100), nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"key": self.key,
			"value": self.value,
			"has_image": bool(self.image_data),
			"created_at": self.created_at.isoformat() if self.created_at else None,
		}
