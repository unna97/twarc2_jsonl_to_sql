from datetime import datetime
import pandas as pd
import numpy as np

"""
References:
    https://developer.twitter.com/en/docs/twitter-api/data-dictionary/

"""


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
        self.columns_from_original_processed = self.columns_in_tweet_table.copy()
        self.tables_created = {}

    def public_metric_column_processing(self):
        print("Processing public metrics")
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
        print("Processing referenced tweets")
        columns_needed = ["id", "in_reply_to_user_id", "referenced_tweets"]

        data = (
            self.base_data[columns_needed]
            .explode("referenced_tweets")
            .dropna(subset="referenced_tweets")
        )
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

    def entity_processing(self):
        print("Processing entities")
        columns_needed = ["id", "entities"]

        data = self.base_data[columns_needed].dropna()
        data.rename(columns={"id": "tweet_id"}, inplace=True)

        possible_entities = ["hashtags", "mentions", "cashtags", "annonations", "urls"]

        for entity in possible_entities:

            data[entity] = data.apply(
                lambda x: x["entities"].get(entity, np.nan), axis=1
            )  # trial

            table_name = entity + "_entity_mapping"

            self.tables_created[table_name] = (
                data[["tweet_id", entity]].explode(column=entity).dropna()
            )

            if len(self.tables_created[table_name]) > 0:
                for key in self.tables_created[table_name][entity].iloc[0].keys():
                    self.tables_created[table_name][key] = self.tables_created[
                        table_name
                    ][entity].apply(lambda x: x.get(key, np.nan))
                self.tables_created[table_name].drop(columns=[entity], inplace=True)

            else:
                del self.tables_created[table_name]

        self.columns_from_original_processed.extend(columns_needed)
        self.columns_from_original_processed = list(
            set(self.columns_from_original_processed)
        )

    def attachments_processing(self):
        print("Processing attachments")
        columns_needed = ["id", "attachments"]
        data = self.base_data[columns_needed].dropna()
        data.rename(columns={"id": "tweet_id"}, inplace=True)

        attachment_types = ["poll_ids", "media_keys"]

        for attachment_type in attachment_types:
            data[attachment_type] = data.apply(
                lambda x: x["attachments"].get(attachment_type, np.nan), axis=1
            )
            table_name = attachment_type + "_tweet_mapping"
            self.tables_created[table_name] = (
                data[["tweet_id", attachment_type]]
                .explode(column=attachment_type)
                .dropna()
            )

            if len(self.tables_created[table_name]) == 0:
                del self.tables_created[table_name]

        self.columns_from_original_processed.extend(columns_needed)
        self.columns_from_original_processed = list(
            set(self.columns_from_original_processed)
        )

    def processing_overall(self):
        self.public_metric_column_processing()
        self.referenced_tweets_processing()
        self.entity_processing()
        self.attachments_processing()
        self.tables_created["tweet_table"] = self.base_data[self.columns_in_tweet_table]


class UserObject_to_DataTable:
    def __init__(self, user_df) -> None:
        self.base_data = user_df
        self.columns_in_user_table = [
            "id",
            "name",
            "username",
            "created_at",
            "description",
            "location",
            "pinned_tweet_id",
            "profile_image_url",
            "protected",
            "url",
            "verified",
        ]
        self.columns_from_original_processed = self.columns_in_user_table.copy()
        self.tables_created = {}

    def public_metric_column_processing(self):

        print("Processing public metrics")
        new_cols = self.base_data["public_metrics"].iloc[0].keys()
        for key in new_cols:
            self.base_data[key] = self.base_data["public_metrics"].apply(
                lambda x: x[key]
            )
        self.base_data.drop(columns=["public_metrics"], inplace=True)
        self.columns_in_user_table.extend(new_cols)
        self.columns_from_original_processed.append("public_metrics")

    def set_datatypes(self):
        self.datatype = {
            "id": str,
            "name": str,
            "username": str,
            "created_at": datetime,
            "description": str,
            "location": str,
            "pinned_tweet_id": str,  ## Foriegn key
            "profile_image_url": str,
            "protected": bool,
            "url": str,
            "verified": bool,
        }
        for key in self.base_data.columns:
            self.base_data[key] = self.base_data[key].astype(
                self.columns_in_user_table[key]
            )

    def entity_processing(self):
        print("Processing entities")
        columns_needed = ["id", "entities"]

        data = self.base_data[columns_needed].dropna()
        data.rename(columns={"id": "tweet_id"}, inplace=True)

        possible_entities = ["hashtags", "mentions", "cashtags", "annonations", "urls"]

        for entity in possible_entities:

            data[entity] = data.apply(
                lambda x: x["entities"].get(entity, np.nan), axis=1
            )  # trial

            table_name = entity + "_user_mapping"

            self.tables_created[table_name] = (
                data[["tweet_id", entity]].explode(column=entity).dropna()
            )

            if len(self.tables_created[table_name]) > 0:
                for key in self.tables_created[table_name][entity].iloc[0].keys():
                    self.tables_created[table_name][key] = self.tables_created[
                        table_name
                    ][entity].apply(lambda x: x.get(key, np.nan))
                self.tables_created[table_name].drop(columns=[entity], inplace=True)

            else:
                del self.tables_created[table_name]

        self.columns_from_original_processed.extend(columns_needed)
        self.columns_from_original_processed = list(
            set(self.columns_from_original_processed)
        )

    def processing_overall(self):
        self.public_metric_column_processing()
        self.entity_processing()
        self.tables_created["user_table"] = self.base_data[self.columns_in_user_table]
