from Algorithms.Tools.ColumnsEnum import Metrics, Costs


class FacebookMapper:
    mapping = {
        Costs.CPC.value: 'cpc_all',
        Costs.CPM.value: 'cpm',
        Costs.CPP.value: 'ccp_all',
        Metrics.SPEND.value: 'amount_spent',
        Metrics.REACH.value: 'reach',
        Metrics.CLICKS.value: 'clicks_all',
        Metrics.IMPRESSIONS.value: 'impressions',
        Metrics.CTR.value: 'ctr_all',
        Metrics.ROAS.value: 'website_purchase_roas',
        Metrics.FREQUENCY.value: 'frequency',
        Metrics.RELEVANCY_SCORE.value: 'relevancy_score',  # Not used
        None : None
    }
