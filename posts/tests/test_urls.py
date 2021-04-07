from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.post = Post.objects.create(
            text="Тест | текст | " * 10,
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = TaskURLTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url(self):
        """url → valid status code"""
        group = TaskURLTests.group
        user = TaskURLTests.user
        response_index = self.guest_client.get("/")
        response_slug = self.guest_client.get(f"/group/{group.title}")
        response_new = self.authorized_client.get("/new/")
        response_404 = self.guest_client.get("/weird/page/")
        response_non_exist = self.authorized_client.get(
            f"/{user.username}/888/edit/"
            # Комментарий на ревью: «888 - это что?»
            # Тут проверяю, что страница редактирования поста с несуществующим
            # id — 888 — отдаёт код 404.
            # Это лучше сделать как-то иначе?
        )

        test_dict = {
            response_index.status_code: 200,
            response_slug.status_code: 200,
            response_new.status_code: 200,
            response_404.status_code: 404,
            response_non_exist.status_code: 404,
        }

        for value, expected in test_dict.items():
            with self.subTest(value=value):
                self.assertEquals(value, expected)

    def test_new_url_redirect_anonymous(self):
        """Страница /new/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get("/new/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/")

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        group = TaskURLTests.group
        templates_url_names = {
            "index.html": "/",
            "group.html": f"/group/{group.slug}/",
            "new.html": "/new/",
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_add_comment_guest_client(self):
        user = TaskURLTests.user
        post = TaskURLTests.post

        response = self.guest_client.get(
            reverse("add_comment", kwargs={
                "username": user.username,
                "post_id": post.pk,
            })
        )
        self.assertRedirects(response,
                             f"/auth/login/?next=/"
                             f"{user.username}/{str(post.pk)}/comment/")
