import os
import shutil
from datetime import datetime
from unittest import mock

import pytz
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.apps import PostsConfig
from posts.models import Follow, Group, Post, User
from yatube.settings import BASE_DIR

temp_media = os.path.join(BASE_DIR, "temp_media")


@override_settings(MEDIA_ROOT="temp_media")
class PostPagesTests(TestCase):
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
        cls.user_2 = User.objects.create(
            username="test_user_2",
        )
        cls.user_3 = User.objects.create(
            username="test_user_3",
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

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded_gif = SimpleUploadedFile(
            name="small.gif",
            content=small_gif,
            content_type="image/gif"
        )

        cls.post_on_page = PostsConfig.pages_on_list

        cls.mocked = datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now',
                        mock.Mock(return_value=cls.mocked)):
            cls.post_1 = Post.objects.create(
                text="Тест | текст | " * 10,
                author=cls.user,
                group=cls.group,
                image=cls.uploaded_gif
            )
            for i in range(1, cls.post_on_page):
                Post.objects.create(
                    text=f"{i}",
                    author=cls.user,
                )
            cls.post_user_2 = Post.objects.create(
                text="Author",
                author=cls.user_2,
            )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(temp_media, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.user = PostPagesTests.user
        self.user_2 = PostPagesTests.user_2
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        post_pk = PostPagesTests.post_1.pk
        user = PostPagesTests.user
        group = PostPagesTests.group

        templates_pages_names = {
            reverse("index"): "index.html",
            reverse("new_post"): "new.html",
            reverse("group", kwargs={"slug": group.slug}): "group.html",
            reverse("post", kwargs={
                "post_id": post_pk,
                "username": user.username
            }): "post.html",
            reverse("profile", kwargs={"username": user}): "profile.html",
            reverse("post_edit", kwargs={
                "post_id": post_pk,
                "username": user.username
            }): "new.html"}

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_list_is_10(self):
        post_on_page = PostPagesTests.post_on_page
        response = self.authorized_client.get(reverse("index"))
        self.assertEquals(len(response.context["page"]), post_on_page)

    def test_home_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        mocked = PostPagesTests.mocked
        response = self.authorized_client.get(reverse("index"))
        user = PostPagesTests.user
        post = PostPagesTests.post_1
        group = PostPagesTests.group
        post_0 = response.context["page"][0]
        post_image = post_0.image
        test_dict = {
            post_0.text: post.text,
            post_0.author.get_full_name(): user.get_full_name(),
            post_0.pub_date: mocked,
            post_0.group.title: group.title,
            post_image: "posts/small.gif",
        }
        for value, expected in test_dict.items():
            with self.subTest(value=value):
                self.assertEquals(value, expected)

    def test_group_detail_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        mocked = PostPagesTests.mocked
        user = PostPagesTests.user
        post = PostPagesTests.post_1
        group = PostPagesTests.group
        group_2 = PostPagesTests.group_2

        response = self.authorized_client.get(
            reverse("group", kwargs={"slug": "test-slug"})
        )
        self.assertEquals(response.context["group"].title, group.title)
        self.assertEquals(response.context["group"].description,
                          group.description)

        post_0 = response.context["page"][0]
        post_text_0 = post_0.text
        post_author_0 = post_0.author.get_full_name()
        post_pub_date_0 = post_0.pub_date
        post_group_0 = post_0.group.title
        post_image = post_0.image
        self.assertEquals(post_text_0, post.text)
        self.assertEquals(post_author_0, user.get_full_name())
        self.assertEquals(post_pub_date_0, mocked)
        self.assertEquals(post_group_0, group.title)
        self.assertNotEqual(post_group_0, group_2.title)
        self.assertEquals(post_image, "posts/small.gif")

    def test_new_page_show_correct_context(self):
        """Шаблон new сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("new_post"))
        form_fields = {
            "group": forms.fields.ChoiceField,
            "text": forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_username_post_id_edit_context(self):
        """Шаблон post_id_edit сформирован с правильным контекстом."""
        post_pk = PostPagesTests.post_1.pk
        response = self.authorized_client.get(
            reverse("post_edit",
                    kwargs={"post_id": post_pk,
                            "username": self.user.username})
        )
        form_fields = {
            "group": forms.fields.ChoiceField,
            "text": forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_profile_pages_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        mocked = PostPagesTests.mocked
        user = PostPagesTests.user
        post = PostPagesTests.post_1
        group = PostPagesTests.group

        response = self.authorized_client.get(reverse("profile", kwargs={
            "username": self.user.username,
        }))

        post_0 = response.context["page"][0]
        post_text_0 = post_0.text
        post_author_0 = post_0.author.get_full_name()
        post_pub_date_0 = post_0.pub_date
        post_group_0 = post_0.group.title
        post_image = post_0.image
        self.assertEquals(post_text_0, post.text)
        self.assertEquals(post_author_0, user.get_full_name())
        self.assertEquals(post_pub_date_0, mocked)
        self.assertEquals(post_group_0, group.title)
        self.assertEquals(post_image, "posts/small.gif")

    def test_post_id_show_correct_context(self):
        """Шаблон post_id сформирован с правильным контекстом."""
        mocked = PostPagesTests.mocked
        user = PostPagesTests.user
        post = PostPagesTests.post_1
        group = PostPagesTests.group

        response = self.authorized_client.get(reverse("post", kwargs={
            "username": self.user.username,
            "post_id": post.pk,
        }))
        response = response.context["post"]
        post_text_0 = response.text
        post_author_0 = response.author.get_full_name()
        post_pub_date_0 = response.pub_date
        post_group_0 = response.group.title
        post_image = response.image
        self.assertEquals(post_text_0, post.text)
        self.assertEquals(post_author_0, user.get_full_name())
        self.assertEquals(post_pub_date_0, mocked)
        self.assertEquals(post_group_0, group.title)
        self.assertEquals(post_image, "posts/small.gif")

    def test_first_page_contains_ten_records(self):
        """Проверка: количество постов на первой странице равно 10."""
        response = self.client.get(reverse("index"))
        pages = PostPagesTests.post_on_page
        self.assertEquals(len(response.context["page"].object_list), pages)

    def test_auth_user_follow(self):
        user = PostPagesTests.user
        user_2 = PostPagesTests.user_2

        self.authorized_client.get(
            reverse("profile_follow", kwargs={"username": user_2.username})
        )
        self.assertEquals(Follow.objects.get(user=user).author, user_2)

    def test_auth_user_unfollow(self):
        user = PostPagesTests.user
        user_2 = PostPagesTests.user_2

        self.authorized_client.get(
            reverse("profile_follow", kwargs={"username": user_2.username})
        )
        self.authorized_client.get(
            reverse("profile_unfollow", kwargs={"username": user_2.username})
        )
        self.assertFalse(Follow.objects.filter(user=user).exists())

    def test_new_post_in_following(self):
        user_2 = PostPagesTests.user_2
        user_3 = PostPagesTests.user_3
        post = PostPagesTests.post_user_2

        self.authorized_client.get(
            reverse("profile_follow", kwargs={"username": user_2.username})
        )
        response = self.authorized_client.get(reverse("follow_index"))
        post_0 = response.context["page"][0]
        post_text_0 = post_0.text
        self.assertEquals(post_text_0, post.text)

        self.authorized_client.force_login(user_3)
        response = self.authorized_client.get(reverse("follow_index"))
        self.assertEquals(len(response.context["page"]), 0)
