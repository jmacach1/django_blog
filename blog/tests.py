from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

class BlogTest(TestCase):
  def setUp(self):
    self.user = get_user_model().objects.create_user(
      username="testUser",
      email="test@email.com",
      password="secret"
    )

    self.post = Post.objects.create(
      title="A Title",
      body="A Body",
      author=self.user
    ) 

  def test_string_represenation(self):
    post = Post(title="A Title")
    self.assertEqual(str(post), post.title)

  def test_post_content(self):
    self.assertEqual(f"{self.post.title}", "A Title")
    self.assertEqual(f"{self.post.body}", "A Body")
    self.assertEqual(f"{self.post.author}", "testUser")

  def test_post_list_view(self):
    response = self.client.get(reverse("home"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'A Body')
    self.assertTemplateUsed(response, 'home.html')

  def test_post_detail_view(self):
    response = self.client.get('/post/1/')
    no_response = self.client.get('/post/1000/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(no_response.status_code, 404)
    self.assertContains(response, 'A Title')
    self.assertTemplateUsed(response, 'post_detail.html')