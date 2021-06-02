from sqlalchemy import or_

from FiledInfluencer.Api.models import InfluencerPosts, Influencers
from FiledInfluencer.Api.startup import session_scope
from FiledInfluencer.influencer_enum import AccountTypeEnum


class InfluencerProfileQuery:
    def __init__(self):
        with session_scope() as session:
            self.session = session

    def get_total_count_query(self):
        count = self.session.query(Influencers).count()
        results = {"count": count}
        return results

    def get_name_engagementperpost_isverified_accountype_query(
        self,
        name,
        EngagementPerPost_filters,
        account_type,
        account_type_enum1,
        account_type_enum2,
        is_verified,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        search = f"%{name}%"
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(*EngagementPerPost_filters)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
                .filter(*Followers_filters, *Engagement_filters)
                .filter(Influencers.IsVerified == is_verified)
                .filter(Influencers.AccountType == account_type_enum1)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(*EngagementPerPost_filters)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
                .filter(*Followers_filters, *Engagement_filters)
                .filter(Influencers.IsVerified == is_verified)
                .filter(
                    or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2)
                )
                .limit(page_size)
            )
        return results

    def get_name_engagementperpost_accountype_query(
        self,
        name,
        EngagementPerPost_filters,
        account_type,
        account_type_enum1,
        account_type_enum2,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        search = f"%{name}%"
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(*EngagementPerPost_filters)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
                .filter(*Followers_filters, *Engagement_filters)
                .filter(Influencers.AccountType == account_type_enum1)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(*EngagementPerPost_filters)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
                .filter(*Followers_filters, *Engagement_filters)
                .filter(
                    or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2)
                )
                .limit(page_size)
            )
        return results

    def get_name_engagementperpost_isverified_query(
        self,
        name,
        EngagementPerPost_filters,
        is_verified,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .filter(*EngagementPerPost_filters)
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
            .filter(*Followers_filters, *Engagement_filters)
            .filter(Influencers.IsVerified == is_verified)
            .limit(page_size)
        )
        return results

    def get_name_isverified_accountype_query(
        self,
        name,
        is_verified,
        account_type,
        account_type_enum1,
        account_type_enum2,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        search = f"%{name}%"
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
                .filter(*Followers_filters, *Engagement_filters)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.IsVerified == is_verified)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
                .filter(*Followers_filters, *Engagement_filters)
                .filter(
                    or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2)
                )
                .filter(Influencers.IsVerified == is_verified)
                .limit(page_size)
            )
        return results

    def get_isverified_engagementperpost_accountype_query(
        self,
        is_verified,
        EngagementPerPost_filters,
        account_type,
        account_type_enum1,
        account_type_enum2,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(*EngagementPerPost_filters)
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
                .filter(Influencers.IsVerified == is_verified)
                .filter(Influencers.AccountType == account_type_enum1)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(*EngagementPerPost_filters)
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
                .filter(Influencers.IsVerified == is_verified)
                .filter(
                    or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2)
                )
                .limit(page_size)
            )
        return results

    def get_engagementperpost_accountype_query(
        self,
        EngagementPerPost_filters,
        account_type,
        account_type_enum1,
        account_type_enum2,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(*EngagementPerPost_filters)
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
                .filter(Influencers.AccountType == account_type_enum1)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(*EngagementPerPost_filters)
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
                .filter(
                    or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2)
                )
                .limit(page_size)
            )
        return results

    def get_name_accounttype_query(
        self,
        name,
        account_type,
        account_type_enum1,
        account_type_enum2,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        search = f"%{name}%"
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
                .filter(*Followers_filters, *Engagement_filters)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(
                    or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2)
                )
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
                .filter(*Followers_filters, *Engagement_filters)
                .limit(page_size)
            )
        return results

    def get_name_engagementperpost_query(
        self, name, EngagementPerPost_filters, Followers_filters, last_influencer_id, page_size, Engagement_filters
    ):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .filter(*EngagementPerPost_filters)
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
            .filter(*Followers_filters, *Engagement_filters)
            .limit(page_size)
        )
        return results

    def get_engagementperpost_isverified_query(
        self,
        EngagementPerPost_filters,
        is_verified,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        results = (
            self.session.query(Influencers)
            .filter(*EngagementPerPost_filters)
            .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
            .filter(Influencers.IsVerified == is_verified)
            .limit(page_size)
        )
        return results

    def get_isverified_accountype_query(
        self,
        is_verified,
        account_type,
        account_type_enum1,
        account_type_enum2,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
                .filter(Influencers.IsVerified == is_verified)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(
                    or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2)
                )
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
                .filter(Influencers.IsVerified == is_verified)
                .limit(page_size)
            )
        return results

    def get_isverified_name_query(
        self, is_verified, name, Followers_filters, last_influencer_id, page_size, Engagement_filters
    ):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
            .filter(*Followers_filters, *Engagement_filters)
            .filter(Influencers.IsVerified == is_verified)
            .limit(page_size)
        )
        return results

    def get_engagementperpost_query(
        self, EngagementPerPost_filters, Followers_filters, last_influencer_id, page_size, Engagement_filters
    ):
        results = (
            self.session.query(Influencers)
            .filter(*EngagementPerPost_filters)
            .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
            .limit(page_size)
        )
        return results

    def get_name_query(self, name, Followers_filters, last_influencer_id, page_size, Engagement_filters):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search))
            .filter(*Followers_filters, *Engagement_filters)
            .limit(page_size)
        )
        return results

    def get_accounttype_query(
        self,
        account_type,
        account_type_enum1,
        account_type_enum2,
        Followers_filters,
        last_influencer_id,
        page_size,
        Engagement_filters,
    ):
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(
                    or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2)
                )
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
                .limit(page_size)
            )
        return results

    def get_isverified_query(self, is_verified, Followers_filters, last_influencer_id, page_size, Engagement_filters):
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, Influencers.IsVerified == is_verified)
            .filter(*Followers_filters, *Engagement_filters)
            .limit(page_size)
        )
        return results

    def get_default_query(self, Followers_filters, last_influencer_id, page_size, Engagement_filters):
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, *Followers_filters, *Engagement_filters)
            .limit(page_size)
        )
        return results
