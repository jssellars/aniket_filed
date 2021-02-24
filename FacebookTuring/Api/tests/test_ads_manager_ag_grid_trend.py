import pytest
from FacebookTuring.Api.tests.test_accounts_ag_grid_trend import TestAccountsAgGridTrend


class TestAdsManagerAgGridTrend(TestAccountsAgGridTrend):

    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/ads-manager/ag-grid-insights-trend/account"
        return client.post(url, json=self.post_data, headers=config["headers"])
