from sqlalchemy import or_

from FiledInfluencer.Api.models import Influencers, InfluencerPosts
from FiledInfluencer.Api.startup import session_scope
from FiledInfluencer.enum import AccountTypeEnum


class InfluencerProfileQuery:
    def __init__(self):
        with session_scope() as session:
            self.session = session

    def get_total_count_query(self):
        count = self.session.query(Influencers).count()
        results = {"count": count}
        return results

    def get_name_postengagement_isverified_accountype_query(
                                self, name, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                is_verified, Followers_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                        InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
                .filter(Influencers.IsVerified == is_verified)
                .filter(Influencers.AccountType == account_type_enum1)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                        InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
                .filter(Influencers.IsVerified == is_verified)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .limit(page_size)
            )
        return results

    def get_name_postengagement_accountype_query(
                                self, name, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                Followers_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                        InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
                .filter(Influencers.AccountType == account_type_enum1)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                        InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .limit(page_size)
            )
        return results

    def get_name_postengagement_isverified_query(
                                self, name, post_engagement, is_verified,
                                Followers_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .distinct()
            .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
            .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                    InfluencerPosts.Engagement < post_engagement['max_count'])
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
            .filter(Influencers.IsVerified == is_verified)
            .limit(page_size)
        )
        return results

    def get_name_isverified_accountype_query(
                                self, name, is_verified, account_type, account_type_enum1, account_type_enum2,
                                Followers_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.IsVerified == is_verified)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .filter(Influencers.IsVerified == is_verified)
                .limit(page_size)
            )
        return results

    def get_isverified_postengagement_accountype_query(
                                self, is_verified, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                Followers_filters, last_influencer_id, page_size):
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                        InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
                .filter(Influencers.IsVerified == is_verified)
                .filter(Influencers.AccountType == account_type_enum1)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                        InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
                .filter(Influencers.IsVerified == is_verified)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .limit(page_size)
            )
        return results

    def get_postengagement_accountype_query(
                                    self, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                    Followers_filters, last_influencer_id, page_size):
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'], InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
                .filter(Influencers.AccountType == account_type_enum1)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                        InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .limit(page_size)
            )
        return results

    def get_name_accounttype_query(self, name, account_type, account_type_enum1, account_type_enum2,
                                   Followers_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
                .limit(page_size)
            )
        return results

    def get_name_postengagement_query(self, name, post_engagement,
                                      Followers_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .distinct()
            .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
            .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                    InfluencerPosts.Engagement < post_engagement['max_count'])
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
            .limit(page_size)
        )
        return results

    def get_postengagement_isverified_query(self, post_engagement, is_verified,
                                      Followers_filters, last_influencer_id, page_size):
        results = (
            self.session.query(Influencers)
            .distinct()
            .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
            .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                    InfluencerPosts.Engagement < post_engagement['max_count'])
            .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
            .filter(Influencers.IsVerified == is_verified)
            .limit(page_size)
        )
        return results

    def get_isverified_accountype_query(self, is_verified, account_type, account_type_enum1, account_type_enum2,
                                   Followers_filters, last_influencer_id, page_size):
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
                .filter(Influencers.IsVerified == is_verified)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
                .filter(Influencers.IsVerified == is_verified)
                .limit(page_size)
            )
        return results

    def get_isverified_name_query(self, is_verified, name,
                                      Followers_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
            .filter(Influencers.IsVerified == is_verified)
            .limit(page_size)
        )
        return results

    def get_postengagement_query(self, post_engagement,
                                Followers_filters, last_influencer_id, page_size):
        results = (
            self.session.query(Influencers)
            .distinct()
            .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
            .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                    InfluencerPosts.Engagement < post_engagement['max_count'])
            .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
            .limit(page_size)
        )
        return results

    def get_name_query(self, name,
                       Followers_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Followers_filters)
            .limit(page_size)
        )
        return results

    def get_accounttype_query(self, account_type, account_type_enum1, account_type_enum2,
                              Followers_filters, last_influencer_id, page_size):
        if account_type == AccountTypeEnum.PERSONAL.value:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
                .limit(page_size)
            )
        return results

    def get_isverified_query(self, is_verified,
                       Followers_filters, last_influencer_id, page_size):
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, Influencers.IsVerified == is_verified, *Followers_filters)
            .limit(page_size)
        )
        return results

    def get_default_query(self, Followers_filters, last_influencer_id, page_size):
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, *Followers_filters)
            .limit(page_size)
        )
        return results