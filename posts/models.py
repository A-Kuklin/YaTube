from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Group(models.Model):
    """ Describes the groups. """
    title = models.CharField(max_length=200,
                             blank=True,
                             null=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title[:100]


class Post(models.Model):
    """ Describes the posts. """
    text = models.TextField(verbose_name="Текст поста",
                            help_text="Напишите текст поста")
    pub_date = models.DateTimeField(verbose_name="дата публикации",
                                    auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey(Group,
                              verbose_name="Группа",
                              help_text="Выберите группу",
                              on_delete=models.SET_NULL,
                              blank=True, null=True, related_name="posts")
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """ Describes the comments. """
    text = models.TextField(verbose_name="Комментарий",
                            help_text="Напишите комментарий")
    created = models.DateTimeField(verbose_name="дата публикации",
                                   auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comments")
    post = models.ForeignKey(Post,
                             on_delete=models.SET_NULL,
                             blank=True, null=True, related_name="comments")

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.text[:100]


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name="follower")
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name="following")

    def __str__(self):
        return self.author.username

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "author"],
                             name="unique_subscriber")
        ]
