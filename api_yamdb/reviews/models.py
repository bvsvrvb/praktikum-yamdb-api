from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)

from api.validators import validate_max_year


TEXTFIELD_LIMIT = 20


class User(AbstractUser):
    """Класс для модели пользователя"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USERS_ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField('Электронная почта', unique=True, max_length=254)
    role = models.CharField(
        'Роль',
        choices=USERS_ROLE,
        default=USER,
        max_length=10
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=50
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return f'{self.username} {self.first_name} {self.last_name}'

    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def is_moderator(self):
        return self.role == self.MODERATOR

    def is_user(self):
        return self.role == self.USER


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[validate_max_year],
        db_index=True
    )
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанры'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категории'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        db_index=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:TEXTFIELD_LIMIT]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True,
        verbose_name='Автор'
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date', 'author']

    def __str__(self) -> str:
        return self.text[:TEXTFIELD_LIMIT]
