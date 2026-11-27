import io
import os
import tempfile
import unittest
from app import app
import app.products.db as product_db


class ProductCRUDTestCase(unittest.TestCase):

  def setUp(self):
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    self.client = app.test_client()

    # Створюємо ізольовану тестову БД TinyDB
    self.tmp_fd, self.tmp_db_path = tempfile.mkstemp(suffix=".json")
    os.close(self.tmp_fd)
    product_db.DB_PATH = self.tmp_db_path

  def tearDown(self):
    if os.path.exists(self.tmp_db_path):
      os.remove(self.tmp_db_path)

  def test_create_and_read_product(self):
    # Створення товару із тестовим зображенням
    data = {
        "name": "MacBook Pro",
        "category": "Laptops",
        "price": "2499.99",
        "quantity": "5",
        "content": "Потужний ноутбук для розробки.",
        "image": (io.BytesIO(b"fake image bytes"), "laptop.png"),
    }
    response = self.client.post(
        "/product/add",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"MacBook Pro", response.data)

    # Перегляд детальної сторінки
    detail_resp = self.client.get("/product/1")
    self.assertEqual(detail_resp.status_code, 200)
    self.assertIn(b"2499.99", detail_resp.data)

  def test_update_product(self):
    product_db.create_product("Old Name", "Desc", 100.0, "PC", 2)
    response = self.client.post(
        "/product/1/edit",
        data={
            "name": "Updated PC",
            "category": "PC",
            "price": "150.50",
            "quantity": "10",
            "content": "Оновлений опис комп'ютера.",
        },
        follow_redirects=True,
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Updated PC", response.data)
    self.assertIn(b"150.50", response.data)

  def test_delete_product(self):
      product_db.create_product("To Delete", "Desc", 50.0, "Accessories", 1)
      response = self.client.post("/product/1/delete", follow_redirects=True)
      self.assertEqual(response.status_code, 200)
      self.assertIn("Товар &#39;To Delete&#39; видалено.".encode("utf-8"), response.data)
      self.assertIn("Товарів поки немає".encode("utf-8"), response.data)

      # Перевірка 404 після видалення
      not_found = self.client.get("/product/1")
      self.assertEqual(not_found.status_code, 404)


if __name__ == "__main__":
  unittest.main()