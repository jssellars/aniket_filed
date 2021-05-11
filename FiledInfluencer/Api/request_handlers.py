import json

import humps

from Core.Tools.Misc.ObjectSerializers import object_to_camelized_dict
from FiledInfluencer.Api.models import Influencers
from FiledInfluencer.Api.schemas import InfluencersResponse
from FiledInfluencer.Api.startup import session_scope


class InfluencerProfilesHandler:
    @staticmethod
    def convert_to_json(influencer: Influencers):
        details = json.loads(influencer.Details)

        pydantic_influencer = InfluencersResponse(
            Id=influencer.Id,
            Name=influencer.Name,
            Biography=influencer.Biography,
            Engagement=influencer.Engagement,
            ProfilePicture=details['profile_pic_url'],
            CategoryName=details['category_name'],
        )
        json_string = pydantic_influencer.json()
        return humps.camelize(json.loads(json_string))

    @classmethod
    def get_profiles(cls, last_influencer_id: int, page_size: int):
        # last_influencer_id was already sent in previous request
        last_influencer_id += 1

        with session_scope() as session:
            # for infinite scrolling
            # offset queries are inefficient
            results = session.query(Influencers).filter(Influencers.Id >= last_influencer_id).limit(page_size)

        return [cls.convert_to_json(result) for result in results]
