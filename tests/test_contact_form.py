import unittest
from app import app


class ContactFormTestCase(unittest.TestCase):

  def setUp(self):
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    self.client = app.test_client()

  def test_contact_page_loads(self):
    response = self.client.get("/contact")
    self.assertEqual(response.status_code, 200)
    self.assertIn(b"Send Message", response.data)

  def test_valid_contact_submission(self):
    response = self.client.post(
        "/contact",
        data={
            "name": "Svyat",
            "email": "svyat@example.com",
            "phone": "+380991234567",
            "subject": "general",
            "message": "Тестове повідомлення для перевірки форми.",
        },
        follow_redirects=True,
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn(
        "Повідомлення успішно відправлено".encode("utf-8"), response.data
    )

  def test_invalid_phone_validation(self):
    response = self.client.post(
        "/contact",
        data={
            "name": "Svyat",
            "email": "svyat@example.com",
            "phone": "0991234567",  # Невірний формат без +380
            "subject": "general",
            "message": "Тест",
        },
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn("+380XXXXXXXXX".encode("utf-8"), response.data)


if __name__ == "__main__":
  unittest.main()