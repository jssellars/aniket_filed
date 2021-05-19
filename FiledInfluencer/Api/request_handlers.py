import json

import humps
from typing import Dict, List

from FiledInfluencer.Api.models import Influencers
from FiledInfluencer.Api.schemas import InfluencersResponse
from FiledInfluencer.Api.startup import session_scope


class InfluencerProfilesHandler:
    @staticmethod
    def convert_to_json(influencer: Influencers) -> Dict[str, str]:
        """
        Convert a sqlalchemy model to pydantic schema camelized json

        :returns: camelized dictionary keys
        """
        details = json.loads(influencer.Details)

        pydantic_influencer = InfluencersResponse(
            Id=influencer.Id,
            Name=influencer.Name,
            Biography=influencer.Biography,
            Engagement=influencer.Engagement,
            ProfilePicture=details['profile_pic_url'],
            CategoryName=details['category_name'],
        )
        return humps.camelize(pydantic_influencer.dict())

    @classmethod
    def get_profiles(cls, name: str, last_influencer_id: int, page_size: int) -> List[Dict[str, str]]:
        # last_influencer_id was already sent in previous request
        last_influencer_id += 1

        with session_scope() as session:
            # for infinite scrolling
            # offset queries are inefficient
            if name:
                search = f"%{name}%"
                results = session.query(Influencers).filter(
                    Influencers.Id >= last_influencer_id, Influencers.Name.like(search)).limit(page_size)
            else:
                results = session.query(Influencers).filter(Influencers.Id >= last_influencer_id).limit(page_size)

        return [cls.convert_to_json(result) for result in results]
