from pydantic.main import BaseModel


class InfluencersEndpoint(BaseModel):
    page_size = ""
    last_influencer_id = ""
    name = ""
    get_total_count = ""
    account_type = ""
    is_verified = ""
    engagement_rate_min_count = ""
    engagement_rate_max_count = ""
    engagements_per_post_min_count = ""
    engagements_per_post_max_count = ""
    followers_min_count = ""
    followers_max_count = ""

    @property
    def url(self):
        url = "/api/v1/influencer-profiles?"
        query_params = []
        for k, v in self.dict().items():
            if v:
                query_params.append(f"{k}={v}")
        return f"{url}{'&'.join(query_params)}"


if __name__ == "__main__":
    x = InfluencersEndpoint()
    print(x.url)
