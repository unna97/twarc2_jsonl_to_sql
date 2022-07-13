import pandas as pd


class TweetObject_to_DataTable:

    def __init__(self, tweets_df:pd.DataFrame):
        self.base_data = tweets_df
        self.columns_in_tweet_table = ['author_id', 'possibly_sensitive', 'conversation_id', 'source', 
                                'reply_settings', 'text', 'created_at', 'id', 'lang']
    

    def public_metric_column_processing(self):
        new_cols = self.base_data['public_metrics'].iloc[0].keys()
        for key in new_cols:
            self.base_data[key] = self.base_data['public_metrics'].apply(lambda x: x[key])
        self.base_data.drop(columns=['public_metrics'], inplace=True)
        self.columns_in_tweet_table.extend(new_cols)



