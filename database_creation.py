from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey

Base = declarative_base()


class Author(Base):
    __tablename__ = "author_data"
    id = Column(String, primary_key=True)  ## One author can have multiple tweets
    name = Column(String)
    username = Column(String)
    created_at = Column(DateTime)
    description = Column(String)
    location = Column(String)
    pinned_tweet_id = Column(
        String, ForeignKey("tweet_data.id")
    )  # tweet can be pinned by multiple authors
    # but an author can pin one tweet
    profile_image_url = Column(String)
    protected = Column(Boolean)
    url = Column(String)
    verified = Column(Boolean)


class Tweet(Base):
    __table__ = "tweet_data"
    id = Column(String, primary_key=True)
    created_at = Column(DateTime)
    text = Column(String)
    ## Figure out type of relationship:
    author_id = Column(
        String, ForeignKey("author_data.id")
    )  # one author to many tweets
    possibly_sensitive = Column(Boolean)
    conversation_id = Column(String)
    source = Column(String)
    reply_settings = (Column(String),)
    lang = Column(String)
    retweet_count = Column(Integer)
    like_count = Column(Integer)
    qoute_count = Column(Integer)
    reply_count = Column(Integer)
    tweet_type = Column(
        Integer
    )  # 0: tweet, 1: quoted tweet, 2: retweeted tweet, 3: replied to tweet, 4: quoted tweet + replied to tweet


class ReTweet(Base):
    ### Association Table type: 1:1
    __table__ = "retweet_data"
    tweet_id = Column(
        String, ForeignKey("tweet_data.id"), primary_key=True
    )  # primary key
    referenced_tweet_id = Column(String, ForeignKey("tweet_data.id"))


class Quote(Base):
    __table__ = "quote_data"
    tweet_id = Column(
        String, ForeignKey("tweet_data.id"), primary_key=True
    )  # primary key
    referenced_tweet_id = Column(String, ForeignKey("tweet_data.id"))


class Reply(Base):
    __table__ = "reply_data"
    tweet_id = Column(
        String, ForeignKey("tweet_data.id"), primary_key=True
    )  ## primary key
    referenced_tweet_id = Column(String, ForeignKey("tweet_data.id"))
    in_reply_to_user_id = Column(String, ForeignKey("author_data.id"))


# ----------------------------------------------------------------------------------------------------------------------#
class HashTags(Base):
    __table__ = "hashtags_data"  # Tweet_id  + start
    id = Column(String, primary_key=True)  ## Need to create a primary key
    hashtag = Column(String)


class HashtagTweetMap(Base):
    __table__ = "hashtag_tweet_map"
    id = Column(String, primary_key=True)  # Tweet_id + start
    tweet_id = Column(String, ForeignKey("tweet_data.id"))
    hashtag_id = Column(String)
    start = Column(Integer)
    end = Column(Integer)


class HashtagAuthorMap(Base):
    __table__ = "hashtag_author_map"
    id = Column(String, primary_key=True)  # Tweet_id + start
    author_id = Column(String, ForeignKey("tweet_data.id"))
    hashtag_id = Column(String)
    start = Column(Integer)
    end = Column(Integer)


class Cashtags(Base):
    __table__ = "cashtags_data"
    id = Column(String, primary_key=True)  # Tweet_id + Cashtag + start
    tweet_id = Column(String, ForeignKey("tweet_data.id"))
    cashtag = Column(String)
    start = Column(Integer)
    end = Column(Integer)


class Mentions(Base):
    __table__ = "mentions_data"
    id = Column(String, primary_key=True)  ## Combinations author_id + tweet_id +start
    tweet_id = Column(String, ForeignKey("tweet_data.id"))  # Many mentions in one tweet
    author_id = Column(
        String, ForeignKey("author_data.id")
    )  ## Many mentions to one author
    start = Column(Integer)
    end = Column(Integer)


class Urls(Base):
    __table__ = "urls_data"
    id = Column(String, primary_key=True)  # Combination of tweet_id + url + start
    tweet_id = Column(String, ForeignKey("tweet_data.id"))  # Many urls in one tweet
    url = Column(String)
    start = Column(Integer)
    end = Column(Integer)
    expanded_url = Column(String)
    display_url = Column(String)
    status = Column(String)
    title = Column(String)
    description = Column(String)
    unwound_url = Column(String)


class Annonations(Base):
    start = Column(Integer)
    end = Column(Integer)
    probability = Column(Float)
    type = Column(String)  ## Person + Politician
    normalized_text = Column(String)
    tweet_id = Column(String, ForeignKey("tweet_data.id"))
    id = Column(String, primary_key=True)


class PollsTweetMap(Base):
    __table__ = "poll_ids_tweet_mapping"
    id = Column(String, primary_key=True)  # Tweet_id + start
    tweet_id = Column(String, ForeignKey("tweet_data.id"))

class MediaKeyTweetMap(Base):
    __table__ = "media_keys_tweet_mapping"
    id = Column(String, primary_key=True)  # Tweet_id + start
    tweet_id = Column(String, ForeignKey("tweet_data.id"))
    media_key = Column(String)
