from FiledInfluencer.Api.models import FiledInfluencers
from FiledInfluencer.Api.startup import fixtures
from FiledInfluencer.Api.schemas import FiledInfluencersPydantic


class InfluencerProfilesHandler:
    # TODO: session lifecycle?
    session = fixtures.sql_db_session()

    @staticmethod
    def convert_to_json(influencer):
        pydantic_influencer = FiledInfluencersPydantic.from_orm(influencer)
        return pydantic_influencer.json()

    @classmethod
    def get_profiles(cls, influencer_id):
        if influencer_id:
            result = cls.session.query(FiledInfluencers).filter_by(Id=influencer_id).first()
            return cls.convert_to_json(result)
        else:
            results = cls.session.query(FiledInfluencers).all()
            return [cls.convert_to_json(result) for result in results]
