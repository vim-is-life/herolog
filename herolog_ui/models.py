from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Game(models.Model):
    """
    Model to represent all the information needed to go into a game that someone
    would add to their backlog. We want to decouple the actual details of the
    game being added to the backlog from the entry in the backlog itself, as it
    is not unreasonable that multiple users might add the same game to their
    backlog.

    The general intent here of how the model would be populated is that the user
    would at least give the name of the game, and optionally a release year, and
    then the backend would query an api to fill in the rest of the information.

    We also intend that a given game will not be modified except by the DB admin
    after it is added to the database. I think of it as us caching a game after
    one user adds it, so there should not be a case where something from a user
    is updating any `Game` model.
    """

    # TODO(consider) add something to store the game cover
    # TODO(consider) add something to represent a link to a store page, eg GOG or steam
    title = models.CharField(max_length=200)
    release_year = models.DateField()
    genre = models.CharField("genre(s) of the game", max_length=512)
    developer = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    story_length = models.DecimalField(max_digits=6, decimal_places=3)
    full_length = models.DecimalField("time to 100%", max_digits=6, decimal_places=3)
    meta_score = models.DecimalField("metacritic score", max_digits=4, decimal_places=2)
    average_rating = models.DecimalField(max_digits=4, decimal_places=2)
    platforms = models.CharField("platforms the game can be played on", max_length=512)


class BacklogItem(models.Model):
    """
    Model to represent an entry in a user's backlog. We track various
    information about a given BacklogItem, included housekeeping stuff, fields
    to fill out before finishing, and then fields to fill out after finishing
    """

    owning_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now_add=True)

    ## PRE-FINISH FIELDS
    # don't think a game would ever be deleted, but maybe this is good to set
    # for if something is deleted from admin interface
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_format = models.TextChoices("GameFormat", "DIGITAL PHYSICAL")
    excitement_level = models.PositiveIntegerField(
        "excitement to play game", validators=[MaxValueValidator(10)]
    )
    start_date = models.DateField()

    ## POST-FINISH FIELDS: quantitative stuffs
    hours_played = models.PositiveIntegerField()
    did_finish = models.BooleanField()
    end_date = models.DateField("date user finished or dropped the game")
    interval_of_play = models.DurationField()
    user_score = models.DecimalField(
        "user rating of the game post-completion",
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    ## POST-FINISH FIELDS: qualitative stuffs
    completion_reason = models.TextChoices(
        "CompletionReason", "GAMEPLAY STORY BOTH NEITHER"
    )
    stand_out_status = models.TextChoices("StandOutStatus", "NEITHER STUNNER BUMMER")
    duration_reception = models.TextChoices(
        "DurationReception", "NEITHER SHORT LONG"
    )  # answers question of was game too long/short?
    was_worth_time = models.BooleanField()
    reflection = models.TextField("user's post-game reflection", max_length=2048)
