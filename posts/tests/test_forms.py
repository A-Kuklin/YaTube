import os
import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, User
from yatube.settings import BASE_DIR

temp_media = os.path.join(BASE_DIR, "temp_media")


@override_settings(MEDIA_ROOT="temp_media")
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД:
        cls.user = User.objects.create(
            first_name="test_name",
            last_name="test_family_name",
            username="test_user",
            email="test_user@test_site.ru"
        )
        cls.group = Group.objects.create(
            title="Тест | Название",
            description="Тест | Описание группы",
            slug="test-slug"
        )
        cls.group_2 = Group.objects.create(
            title="Тест | Название 2",
            description="Тест | Описание группы 2",
            slug="test-slug-2"
        )

        cls.post = Post.objects.create(
            text="Тест | текст | " * 10,
            author=cls.user,
            group=cls.group,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(temp_media, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.user = PostCreateFormTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        group_pk = PostCreateFormTests.group.pk
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded_gif = SimpleUploadedFile(
            name="small.gif",
            content=small_gif,
            content_type="image/gif"
        )
        form_data = {
            "text": "New",
            "group": group_pk,
            "image": uploaded_gif
        }
        self.assertEquals(Post.objects.count(), posts_count)
        response = self.authorized_client.post(
            reverse("new_post"),
            data=form_data,
            follow=True
        )
        self.assertEquals(Post.objects.count(), posts_count + 1)
        new_post = Post.objects.filter(
            text="New",
            group=group_pk,
            image="posts/small.gif"
        )
        self.assertTrue(new_post.exists())
        self.assertRedirects(response, reverse("index"))

    def test_edit_post(self):
        """Редактирование поста через /<username>/<post_id>/edit/ работает."""
        group_2 = PostCreateFormTests.group_2
        post = PostCreateFormTests.post
        user = PostCreateFormTests.user

        form_new_data = {
            "text": "Тест | текст 2",
            "group": group_2.pk
        }
        self.authorized_client.post(
            reverse("post_edit", kwargs={
                "post_id": post.pk,
                "username": user,
            }),
            data=form_new_data,
            follow=True
        )

        post.refresh_from_db()
        self.assertEquals(post.text, "Тест | текст 2")
        self.assertEquals(post.group, group_2)
