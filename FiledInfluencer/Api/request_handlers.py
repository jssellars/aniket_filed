import dataclasses
import json

from Core.mongo_adapter import MongoRepositoryBase
from FiledInfluencer.Api.model import FiledInfluencer, InfluencerPost
from FiledInfluencer.Api.startup import config


class InfluencerProfilesHandler:
    instagram_profiles = MongoRepositoryBase(
        config=config.mongo,
        collection_name=config.mongo.influencer_profiles_collection_name,
        database_name=config.mongo.influencer_database_name,
    )

    @staticmethod
    def serialize_users(data):
        # data_dict = json.loads(data, strict=False)
        data_dict = data
        user = FiledInfluencer(
            _id=data_dict['id'],
            filed_platform_id=None,
            filed_category_id=None,
            name=data_dict['full_name'],
            biography=data_dict['biography'],
            engagement=data_dict['edge_followed_by']['count'],
            details={
                'username': data_dict['username'],
                'external_url': data_dict['external_url'],
                'profile_pic': data_dict['profile_pic_url_hd'],
                'hashtags_freq': data_dict.get("hashtags_frequency"),
            },
        )
        return dataclasses.asdict(user)

    @staticmethod
    def serialize_posts(data):
        data_dict = json.loads(data, strict=False)
        for post in data_dict['posts']:
            post_data = InfluencerPost(
                filed_platform_id=None,
                influencer_id=None,
                post_content=post['caption'],
                posted_at=post['date_utc']['$date'],
                engagement=post['likes'],
            )
            yield dataclasses.asdict(post_data)

    @classmethod
    def get_profiles(cls, search_param):
        query = {}
        if search_param:
            query = {"$text": {"$search": search_param}}

        profiles = cls.instagram_profiles.get(query=query)

        return [user for user in profiles]
