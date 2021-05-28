from sqlalchemy import or_

from FiledInfluencer.Api.models import Influencers, InfluencerPosts
from FiledInfluencer.Api.startup import session_scope


class InfluencerProfileQuery:
    def __init__(self):
        with session_scope() as session:
            self.session = session

    def get_total_count_query(self):
        count = self.session.query(Influencers).count()
        results = {"count": count}
        return results

    def get_name_postengagement_accountype_query(
                                self, name, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                Engagement_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        if account_type == 3:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                        InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Engagement_filters)
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
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Engagement_filters)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .limit(page_size)
            )
        return results

    def get_postengagement_accountype_query(
                                    self, post_engagement, account_type, account_type_enum1, account_type_enum2,
                                    Engagement_filters, last_influencer_id, page_size):
        if account_type == 3:
            results = (
                self.session.query(Influencers)
                .distinct()
                .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
                .filter(InfluencerPosts.Engagement > post_engagement['min_count'], InfluencerPosts.Engagement < post_engagement['max_count'])
                .filter(Influencers.Id >= last_influencer_id, *Engagement_filters)
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
                .filter(Influencers.Id >= last_influencer_id, *Engagement_filters)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .limit(page_size)
            )
        return results

    def get_name_accounttype_query(self, name, account_type, account_type_enum1, account_type_enum2,
                                   Engagement_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        if account_type == 3:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Engagement_filters)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Engagement_filters)
                .limit(page_size)
            )
        return results

    def get_name_postengagement_query(self, name, post_engagement,
                                      Engagement_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .distinct()
            .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
            .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                    InfluencerPosts.Engagement < post_engagement['max_count'])
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Engagement_filters)
            .limit(page_size)
        )
        return results

    def get_postengagement_query(self, post_engagement,
                                Engagement_filters, last_influencer_id, page_size):
        results = (
            self.session.query(Influencers)
            .distinct()
            .join(InfluencerPosts, InfluencerPosts.InfluencerId == Influencers.Id, isouter=True)
            .filter(InfluencerPosts.Engagement > post_engagement['min_count'],
                    InfluencerPosts.Engagement < post_engagement['max_count'])
            .filter(Influencers.Id >= last_influencer_id, *Engagement_filters)
            .limit(page_size)
        )
        return results

    def get_name_query(self, name,
                       Engagement_filters, last_influencer_id, page_size):
        search = f"%{name}%"
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, Influencers.Name.like(search), *Engagement_filters)
            .limit(page_size)
        )
        return results

    def get_accounttype_query(self, account_type, account_type_enum1, account_type_enum2,
                              Engagement_filters, last_influencer_id, page_size):
        if account_type == 3:
            results = (
                self.session.query(Influencers)
                .filter(Influencers.AccountType == account_type_enum1)
                .filter(Influencers.Id >= last_influencer_id, *Engagement_filters)
                .limit(page_size)
            )
        else:
            results = (
                self.session.query(Influencers)
                .filter(or_(Influencers.AccountType == account_type_enum1, Influencers.AccountType == account_type_enum2))
                .filter(Influencers.Id >= last_influencer_id, *Engagement_filters)
                .limit(page_size)
            )
        return results

    def get_default_query(self, Engagement_filters, last_influencer_id, page_size):
        results = (
            self.session.query(Influencers)
            .filter(Influencers.Id >= last_influencer_id, *Engagement_filters)
            .limit(page_size)
        )
        return results