# Generated by Django 4.0.6 on 2022-07-18 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('username', models.TextField()),
                ('location', models.TextField()),
                ('profile_image_url', models.TextField()),
                ('protected', models.BooleanField()),
                ('url', models.TextField()),
                ('verified', models.BooleanField()),
            ],
            options={
                'db_table': 'author_data',
            },
        ),
        migrations.CreateModel(
            name='CashTags',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('cashtag', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.cashtags')),
            ],
            options={
                'db_table': 'cashtags_data',
            },
        ),
        migrations.CreateModel(
            name='HashTags',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('hashtag', models.TextField()),
            ],
            options={
                'db_table': 'hashtags_data',
            },
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('text', models.TextField()),
                ('possibly_sensitive', models.BooleanField()),
                ('conversation_id', models.TextField()),
                ('source', models.TextField()),
                ('lang', models.TextField()),
                ('retweet_count', models.IntegerField()),
                ('like_count', models.IntegerField()),
                ('quote_count', models.IntegerField()),
                ('reply_count', models.IntegerField()),
                ('tweet_type', models.IntegerField()),
                ('author', models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.author')),
            ],
            options={
                'db_table': 'tweet_data',
            },
        ),
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('url', models.TextField()),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('expanded_url', models.TextField()),
                ('display_url', models.TextField()),
                ('status', models.TextField()),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('unwound_url', models.TextField()),
                ('tweet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.tweet')),
            ],
            options={
                'db_table': 'urls_data',
            },
        ),
        migrations.CreateModel(
            name='MentionTweet',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('mention_author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.author')),
                ('tweet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.tweet')),
            ],
            options={
                'db_table': 'mentions_tweet_map',
            },
        ),
        migrations.CreateModel(
            name='HashtagTweetMap',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('hashtag', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.hashtags')),
                ('tweet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.tweet')),
            ],
            options={
                'db_table': 'hashtag_tweet_map',
            },
        ),
        migrations.CreateModel(
            name='HashtagAuthorMap',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.author')),
                ('hashtag', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.hashtags')),
            ],
            options={
                'db_table': 'hashtag_author_map',
            },
        ),
        migrations.CreateModel(
            name='CashtagTweetMap',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('cashtag', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.cashtags')),
                ('tweet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.tweet')),
            ],
            options={
                'db_table': 'cashtag_tweet_map',
            },
        ),
        migrations.CreateModel(
            name='CashtagAuthorMap',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.author')),
                ('hashtag', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.hashtags')),
            ],
            options={
                'db_table': 'cashtag_author_map',
            },
        ),
        migrations.AddField(
            model_name='author',
            name='pinned_tweet',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pinned_tweets', to='db.tweet'),
        ),
        migrations.CreateModel(
            name='Annonations',
            fields=[
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('probability', models.FloatField()),
                ('type', models.TextField()),
                ('normalized_text', models.TextField()),
                ('tweet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.tweet')),
            ],
        ),
        migrations.CreateModel(
            name='ReTweet',
            fields=[
                ('tweet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='re_tweet', serialize=False, to='db.tweet')),
                ('referenced_tweet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referenced_retweets', to='db.tweet')),
            ],
            options={
                'db_table': 'retweet_data',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('tweet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='tweet_replies', serialize=False, to='db.tweet')),
                ('in_reply_to_user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.author')),
                ('referenced_tweet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.tweet')),
            ],
            options={
                'db_table': 'reply_data',
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('tweet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='tweet_quotes', serialize=False, to='db.tweet')),
                ('referenced_tweet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.tweet')),
            ],
            options={
                'db_table': 'quote_data',
            },
        ),
    ]
