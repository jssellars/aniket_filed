from sqlalchemy import Column, BIGINT, NVARCHAR, INTEGER

from FiledInfluencer.Api.Common.models import AuditFields


class Influencers(AuditFields):
    __tablename__ = 'Influencers'

    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=256))
    Biography = Column(NVARCHAR())
    Engagement = Column(NVARCHAR())
    Details = Column(NVARCHAR())
    AccountType = Column(NVARCHAR(128))
    IsVerified = Column(INTEGER)
    Followers = Column(BIGINT)

    PlatformId = Column(BIGINT)
    InfluencerCategoryId = Column(BIGINT)
    MinEngagementPerPost = Column(INTEGER)
    MaxEngagementPerPost = Column(INTEGER)

    def __repr__(self):
        return f"<User(name={self.Name}')>"
