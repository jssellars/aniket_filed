from FiledInfluencer.Api.models import Influencers
from FiledInfluencer.Api.schemas import InfluencersPydantic
from FiledInfluencer.Api.startup import session_scope


class InfluencerProfilesHandler:
    @staticmethod
    def convert_to_json(influencer):
        pydantic_influencer = InfluencersPydantic.from_orm(influencer)
        return pydantic_influencer.json()

    @classmethod
    def get_profiles(cls, last_influencer_id: int, page_size: int):
        # last_influencer_id was already sent in previous request
        last_influencer_id += 1
        with session_scope() as session:
            # for infinite scrolling
            # offset queries are inefficient
            results = session.query(Influencers).filter(Influencers.Id >= last_influencer_id).limit(page_size)

        return [cls.convert_to_json(result) for result in results]
