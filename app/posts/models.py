from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Post(db.Model):
  __tablename__ = "posts"

  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  title: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
  content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
  posted: so.Mapped[datetime] = so.mapped_column(
      sa.DateTime, default=lambda: datetime.now(timezone.utc)
  )
  category: so.Mapped[str] = so.mapped_column(
      sa.Enum("news", "publication", "tech", "other", name="post_category"),
      default="other",
      nullable=False,
  )

  is_active: so.Mapped[bool] = so.mapped_column(
      sa.Boolean, default=True, nullable=False
  )
  author: so.Mapped[str] = so.mapped_column(
      sa.String(20), default="Anonymous", nullable=False
  )

  def __repr__(self):
    return f"<Post(title={self.title})>"