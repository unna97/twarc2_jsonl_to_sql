import pandas as pd


class TweetObject_to_DataTable:
    def __init__(self, tweets_df: pd.DataFrame):
        self.base_data = tweets_df
        self.columns_in_tweet_table = [
            "author_id",
            "possibly_sensitive",
            "conversation_id",
            "source",
            "reply_settings",
            "text",
            "created_at",
            "id",
            "lang",
        ]
        self.columns_from_original_processed = self.columns_in_tweet_table
        self.tables_created = {}

    def public_metric_column_processing(self):
        new_cols = self.base_data["public_metrics"].iloc[0].keys()
        for key in new_cols:
            self.base_data[key] = self.base_data["public_metrics"].apply(
                lambda x: x[key]
            )
        self.base_data.drop(columns=["public_metrics"], inplace=True)
        self.columns_in_tweet_table.extend(new_cols)
        self.columns_from_original_processed.append("public_metrics")

    def referenced_tweets_processing(self):
        """
        This functions creates retweet_tweet_mapping, quote_tweet_mapping, reply_tweet_mapping
        """
        columns_needed = ["id", "in_reply_to_user_id", "referenced_tweets"]

        data = self.base_data[columns_needed].explode("referenced_tweets").dropna()
        data.rename(columns={"id": "tweet_id"}, inplace=True)

        data["referenced_tweet_id"] = data["referenced_tweets"].apply(lambda x: x["id"])
        data["tweet_type"] = data["referenced_tweets"].apply(lambda x: x["type"])

        columns_for_each = {
            "quoted": ["tweet_id", "tweet_type", "referenced_tweet_id"],
            "retweeted": ["tweet_id", "tweet_type", "referenced_tweet_id"],
            "replied_to": [
                "tweet_id",
                "tweet_type",
                "referenced_tweet_id",
                "in_reply_to_user_id",
            ],
        }

        for key in columns_for_each:
            self.tables_created[key + "_tweet_mapping"] = data[
                data["tweet_type"] == key
            ][columns_for_each[key]]

        self.columns_from_original_processed.extend(columns_needed)
        self.columns_from_original_processed = list(
            set(self.columns_from_original_processed)
        )

    def processing_overall(self):
        self.public_metric_column_processing()
        self.referenced_tweets_processing()
