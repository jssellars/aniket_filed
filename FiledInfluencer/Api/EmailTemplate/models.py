from sqlalchemy import Column, BIGINT, NVARCHAR

from FiledInfluencer.Api.Common.models import AuditFields


class EmailTemplates(AuditFields):
    __tablename__ = 'EmailTemplates'

    Id = Column(BIGINT, primary_key=True)
    Name = Column(NVARCHAR(length=50))
    Subject = Column(NVARCHAR(length=50))
    Body = Column(NVARCHAR())
    CampaignId = Column(BIGINT)

    def __repr__(self):
        return f"<EmailTemplate(name={self.Name})>"
