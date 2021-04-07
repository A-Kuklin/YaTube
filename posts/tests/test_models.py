from django.test import TestCase

from posts.models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            first_name="test_name",
            last_name="test_family_name",
            username="test_user",
            email="test_user@test_site.ru"
        )
        cls.post = Post.objects.create(
            text="Тест | текст | " * 10,
            author=User.objects.get(username="test_user")
        )
        cls.group = Group.objects.create(
            title="t" * 200,
            slug="test-slug",
            description="Тест | Описание сообщества",
        )

    def test_str_verbose_name(self):
        """__str__ post & group / verbose_name is valid."""
        post = PostModelTest.post
        group = PostModelTest.group

        expected_object_name_post = post.text[:15]
        expected_object_name_group = group.title[:100]
        verbose_text = post._meta.get_field("text").verbose_name
        verbose_group = post._meta.get_field("group").verbose_name
        text_help = post._meta.get_field("text").help_text
        group_help = post._meta.get_field("group").help_text

        texts = {
            expected_object_name_post: str(post),
            expected_object_name_group: str(group),
            text_help: "Напишите текст поста",
            group_help: "Выберите группу",
            verbose_text: "Текст поста",
            verbose_group: "Группа",
        }

        for value, expected in texts.items():
            with self.subTest(value=value):
                self.assertEquals(value, expected)
