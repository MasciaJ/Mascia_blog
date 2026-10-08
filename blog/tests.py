from io import BytesIO
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from blog.models import Post


class PostImageTests(TestCase):
	def test_admin_form_accepts_image_and_detail_displays_it(self):
		user = get_user_model().objects.create_superuser(
			username="admin",
			email="admin@example.com",
			password="test-password",
		)
		self.client.force_login(user)

		image_buffer = BytesIO()
		Image.new("RGB", (2, 2), color="green").save(image_buffer, format="PNG")

		with tempfile.TemporaryDirectory() as media_root:
			with override_settings(MEDIA_ROOT=media_root):
				admin_response = self.client.get(reverse("admin:blog_post_add"))
				self.assertContains(admin_response, 'name="image"', html=False)

				post = Post.objects.create(
					title="Post con imagen",
					body="Contenido de prueba",
					image=SimpleUploadedFile(
						"post.png",
						image_buffer.getvalue(),
						content_type="image/png",
					),
				)
				detail_response = self.client.get(
					reverse("blog_detail", args=[post.pk])
				)

				self.assertContains(detail_response, post.image.url)
				self.assertTrue(post.image.storage.exists(post.image.name))
