from django.db import models

# Create your models here.
from django.db import models
from core.models import TimeStampedModel


class Genre(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Director(TimeStampedModel):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Actor(TimeStampedModel):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Festival(TimeStampedModel):
    name = models.CharField(max_length=150, unique=True)
    city = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    is_international = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.name} ({self.city})"


class Movie(TimeStampedModel):
    class AgeRating(models.TextChoices):
        G = "G", "ყველასთვის"
        PG = "PG", "მშობლის თანხლებით"
        PG13 = "PG13", "13+"
        R = "R", "18+"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    release_year = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    age_rating = models.CharField(
        max_length=10,
        choices=AgeRating.choices,
        default=AgeRating.G,
    )
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_published = models.BooleanField(default=False)

    # კავშირები
    director = models.ForeignKey(
        Director,
        on_delete=models.PROTECT,
        related_name="movies",
    )
    genres = models.ManyToManyField(
        Genre,
        related_name="movies",
        blank=True,
    )
    cast = models.ManyToManyField(
        Actor,
        through="Role",
        related_name="movies",
        blank=True,
    )
    premiere_festival = models.ForeignKey(
        Festival,
        on_delete=models.SET_NULL,
        related_name="premieres",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-release_year"]
        verbose_name = "ფილმი"
        verbose_name_plural = "ფილმები"

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class BoxOffice(TimeStampedModel):
    movie = models.OneToOneField(
        Movie,
        on_delete=models.CASCADE,
        related_name="box_office",
    )
    tickets_sold = models.PositiveIntegerField()
    gross = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title}: სალარო"


class Role(TimeStampedModel):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="roles",
    )
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        related_name="roles",
    )
    character_name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "actor", "character_name"],
                name="unique_actor_character_per_movie",
            )
        ]

    def __str__(self):
        return f"{self.actor.name} — {self.character_name} ({self.movie.title})"


class Review(TimeStampedModel):
    class Rating(models.IntegerChoices):
        ONE = 1, "★"
        TWO = 2, "★★"
        THREE = 3, "★★★"
        FOUR = 4, "★★★★"
        FIVE = 5, "★★★★★"

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=Rating.choices)
    text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.author_name} ({self.get_rating_display()}) — {self.movie.title}"