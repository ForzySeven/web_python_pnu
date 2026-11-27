import unittest
from app import create_app, db
from app.posts.models import Post


class PostCRUDTestCase(unittest.TestCase):

  def setUp(self):
    self.app = create_app("testing")
    self.client = self.app.test_client()
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_create_post(self):
    """US01: Створити новий пост."""
    response = self.client.post(
        "/post/create",
        data={
            "title": "Test Flask Post",
            "content": "Content for testing SQLAlchemy CRUD.",
            "category": "tech",
            "enabled": "y",
        },
        follow_redirects=True,
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Post added successfully", response.data)
    self.assertIn(b"Test Flask Post", response.data)

  def test_list_posts(self):
    """US02: Перегляд усіх постів."""
    post = Post(title="Visible Post", content="Body text", category="news")
    db.session.add(post)
    db.session.commit()

    response = self.client.get("/post/")
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Visible Post", response.data)

  def test_view_post_detail(self):
    """US03: Перегляд одного поста."""
    post = Post(
        title="Detail Title", content="Detailed content", category="publication"
    )
    db.session.add(post)
    db.session.commit()

    response = self.client.get(f"/post/{post.id}")
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Detail Title", response.data)
    self.assertIn(b"Detailed content", response.data)

  def test_update_post(self):
    """US04: Редагування поста."""
    post = Post(title="Old Title", content="Old content", category="other")
    db.session.add(post)
    db.session.commit()

    response = self.client.post(
        f"/post/{post.id}/update",
        data={
            "title": "Updated Title",
            "content": "Updated content",
            "category": "tech",
            "enabled": "y",
        },
        follow_redirects=True,
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Post updated successfully", response.data)
    self.assertIn(b"Updated Title", response.data)

  def test_delete_post(self):
    """US05: Видалення поста."""
    post = Post(title="Post To Delete", content="Delete me", category="news")
    db.session.add(post)
    db.session.commit()
    post_id = post.id

    response = self.client.post(
        f"/post/{post_id}/delete", follow_redirects=True
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Post deleted successfully", response.data)
    self.assertIsNone(db.session.get(Post, post_id))

  def test_404_not_found(self):
    """US06: 404 при відсутньому пості."""
    response = self.client.get("/post/9999")
    self.assertEqual(response.status_code, 404)
    self.assertIn(b"Page Not Found", response.data)


if __name__ == "__main__":
  unittest.main()