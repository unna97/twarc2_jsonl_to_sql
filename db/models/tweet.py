from django.db.models import *


class Author(Model):
    id = CharField(max_length=256, primary_key=True)
    # vector search
    # full text search, indexing ->> django
    name = TextField()
    username = TextField()
    location = TextField()
    pinned_tweet = ForeignKey('Tweet', null=True, default=None, on_delete=CASCADE)  # tweet can be pinned by multiple authors
    # but an author can pin one tweet
    profile_image_url = TextField()
    protected = BooleanField()
    url = TextField()
    verified = BooleanField()

    class Meta:
        db_table = "author_data"


class Tweet(Model):
    class Meta:
        db_table = "tweet_data"

    id = CharField(max_length=256, primary_key=True)
    created_at = DateTimeField()
    text = TextField()
    # Figure out type of relationship
    author = ForeignKey('Author', null=True, default=True, on_delete=CASCADE)  # one author to many tweets
    possibly_sensitive = BooleanField()
    conversation_id = TextField()
    source = TextField()
    reply_settings = (TextField(),)
    lang = TextField()
    retweet_count = IntegerField()
    like_count = IntegerField()
    quote_count = IntegerField()
    reply_count = IntegerField()
    # 0: tweet, 1: quoted tweet, 2: retweeted tweet, 3: replied to tweet, 4: quoted tweet + replied to tweet
    tweet_type = IntegerField()


class ReTweet(Model):
    ### Association Table type: 1:1
    class Meta:
        db_table = "retweet_data"

    tweet = ForeignKey('Tweet', primary_key=True, on_delete=CASCADE)  # primary key
    referenced_tweet_id = ForeignKey('Tweet', on_delete=CASCADE)


class Quote(Model):
    class Meta:
        db_table = "quote_data"

    tweet = ForeignKey('Tweet', primary_key=True, on_delete=CASCADE)  # primary key
    referenced_tweet_id = ForeignKey('Tweet', on_delete=CASCADE)


class Reply(Model):
    class Meta:
        db_table = "reply_data"

    tweet = ForeignKey('Tweet', primary_key=True, on_delete=CASCADE)  # primary key
    referenced_tweet_id = ForeignKey('Tweet', on_delete=CASCADE)
    in_reply_to_user_id = ForeignKey('Author', on_delete=CASCADE)


# ----------------------------------------------------------------------------------------------------------------------#
class HashTags(Model):
    class Meta:
        db_table = "hashtags_data"  # Tweet_id  + start

    id = CharField(max_length=256, primary_key=True)  # Tweet_id + start
    hashtag = TextField()


class HashtagTweetMap(Model):
    class Meta:
        db_table = "hashtag_tweet_map"

    id = CharField(max_length=256, primary_key=True)  # Tweet_id + start
    tweet = ForeignKey('Tweet', primary_key=True, on_delete=CASCADE)  # primary key
    hashtag_id = TextField()
    start = IntegerField()
    end = IntegerField()


class HashtagAuthorMap(Model):
    class Meta:
        db_table = "hashtag_author_map"

    id = CharField(max_length=256, primary_key=True)  # Tweet_id + start
    author = ForeignKey('Author', primary_key=True, on_delete=CASCADE)  # primary key
    hashtag_id = TextField()
    start = IntegerField()
    end = IntegerField()


class CashTags(Model):
    class Meta:
        db_table = "cashtags_data"  # Tweet_id  + start

    id = CharField(max_length=256, primary_key=True)
    cashtag = TextField()


class CashtagTweetMap(Model):
    class Meta:
        db_table = "hashtag_tweet_map"

    id = CharField(max_length=256, primary_key=True)
    tweet = ForeignKey('Tweet', primary_key=True, on_delete=CASCADE)  # primary key
    cashtag = ForeignKey('Cashtags', on_delete=CASCADE)
    start = IntegerField()
    end = IntegerField()


class CashtagAuthorMap(Model):
    class Meta:
        db_table = "hashtag_author_map"

    id = CharField(max_length=256, primary_key=True)  # Tweet_id + start
    author = ForeignKey('Author', primary_key=True, on_delete=CASCADE)  # primary key
    hashtag_id = TextField()
    start = IntegerField()
    end = IntegerField()


class Mentions(Model):
    class Meta:
        db_table = "mentions_data"

    id = CharField(max_length=256, primary_key=True)  ## Combinations author_id + tweet_id +start
    tweet = ForeignKey('Tweet', primary_key=True, on_delete=CASCADE)  # primary key
    author = ForeignKey('Author', primary_key=True, on_delete=CASCADE)  # primary key
    start = IntegerField()
    end = IntegerField()


class Urls(Model):
    class Meta:
        db_table = "urls_data"

    id = CharField(max_length=256, primary_key=True)  # Combination of tweet_id + url + start
    tweet = ForeignKey('Tweet', on_delete=CASCADE)  # Many urls in one tweet
    url = TextField()
    start = IntegerField()
    end = IntegerField()
    expanded_url = TextField()
    display_url = TextField()
    status = TextField()
    title = TextField()
    description = TextField()
    unwound_url = TextField()


class Annonations(Model):
    id = CharField(max_length=256, primary_key=True)  # Combination of tweet_id + start
    start = IntegerField()
    end = IntegerField()
    probability = FloatField()
    type = TextField()  ## Person + Politician
    normalized_text = TextField()
    tweet = ForeignKey('Tweet', on_delete=CASCADE)
