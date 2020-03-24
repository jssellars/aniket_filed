from Algorithms.Algorithm1.Rules.RuleModels import MetricTrends, Antecedent, Rule, NonTrendAttributes
from Algorithms.Models.Types.TypesWrapper import LevelNames
from Algorithms.Tools.Columns import RecommendationTypes
from Algorithms.Tools.ColumnsEnum import Metrics, Costs

# TODO: make a better enum that includes all metrics and relevancy score

Rules = {
    LevelNames.Ad.value: [
        # Rule([Antecedent(Metrics.Clicks.value, MetricTrends.Decreasing.value),
        #       Antecedent(Metrics.RelevancyScore.value, NonTrendAttributes.Low.value, isTrend=False)],
        #      "This {level}'s Clicks are decreasing! Improve your ads' relevancy score by targeting a different audience that would relate better "
        #      "to your ads", RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Clicks.value, MetricTrends.Decreasing.value),
              Antecedent(Metrics.Frequency.value, NonTrendAttributes.High.value, isTrend=False)],
             "This {level}'s Clicks are decreasing! Try a different creative, copy or CTA to reduce your frequency (your audience is seeing "
             "the same ads over and over again)", RecommendationTypes.Creative.value),
        # Rule([Antecedent(Costs.Cpm.value, MetricTrends.Increasing.value),
        #       Antecedent(Metrics.RelevancyScore.value, NonTrendAttributes.Low.value, isTrend=False)],
        #      "This {level}'s Cpm is increasing! Improve your ads' relevancy score by targeting a different audience that would relate better to"
        #      " your ads", RecommendationTypes.Creative.value),
        Rule([Antecedent(Costs.Cpm.value, MetricTrends.Increasing.value),
              Antecedent(Metrics.Frequency.value, NonTrendAttributes.High.value, isTrend=False)],
             "This {level}'s Cpm is increasing! Consider lowering your budget. (your audience is seeing the same ads over and over again)",
             RecommendationTypes.BudgetAndBid.value),
        Rule([Antecedent(Metrics.Ctr.value, MetricTrends.Decreasing.value)],
             "This {level}'s CTR is decreasing. Try a new, more engaging creative or expand your audience",
             RecommendationTypes.Performance.value),
        # Positive Alerts
        Rule([Antecedent(Costs.Cpm.value, MetricTrends.Decreasing.value)],
             "Great job! This {level} is performing really well. CPM decreases! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Costs.Cpc.value, MetricTrends.Decreasing.value)],
             "Great job! This {level} is performing really well. CPC decreases! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Reach.value, MetricTrends.Increasing.value)],
             "Your ads are taking off! This {level} is performing really well. Reach is increasing! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Clicks.value, MetricTrends.Increasing.value)],
             "Your ads are resonating! This {level} is performing really well. Clicks are increasing! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Roas.value, MetricTrends.Increasing.value)],
             "Your ads profitability is looking great! This {level} is performing really well. Should we increase the budget?",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Ctr.value, MetricTrends.Increasing.value)],
             "Great job! This {level} is performing really well. CTR Increases! Check it out!",
             RecommendationTypes.Performance.value)
    ],

    LevelNames.AdSet.value: [
        Rule([Antecedent(Costs.Cpc.value, MetricTrends.Increasing.value),
              Antecedent(Metrics.Reach.value, NonTrendAttributes.High.value, isTrend=False)],
             "This {level}'s Cpc is increasing and it's reach is higher than 1 million. Consider targeting a more specific audience by removing"
             " the worst performing interests",
             RecommendationTypes.Audience.value),
        Rule([Antecedent(Costs.Cpc.value, MetricTrends.Increasing.value),
              Antecedent(Metrics.Reach.value, NonTrendAttributes.Low.value, isTrend=False)],
             "This {level}'s Cpc is increasing! Consider adding new relevant audiences so that reach is higher!",
             RecommendationTypes.Audience.value),
        Rule([Antecedent(Metrics.Reach.value, MetricTrends.Decreasing.value)],
             "This {level}'s reach is decreasing. Consider targeting more relevant interests.",
             RecommendationTypes.Audience.value),
        # Positive Alerts
        Rule([Antecedent(Costs.Cpm.value, MetricTrends.Decreasing.value)],
             "Great job! This {level} is performing really well. CPM decreases! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Costs.Cpc.value, MetricTrends.Decreasing.value)],
             "Great job! This {level} is performing really well. CPC decreases! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Reach.value, MetricTrends.Increasing.value)],
             "Your ads are taking off! This {level} is performing really well. Reach is increasing! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Clicks.value, MetricTrends.Increasing.value)],
             "Your ads are resonating! This {level} is performing really well. Clicks are increasing! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Roas.value, MetricTrends.Increasing.value)],
             "Your ads profitability is looking great! This {level} is performing really well. Should we increase the budget?",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Ctr.value, MetricTrends.Increasing.value)],
             "Great job! This {level} is performing really well. CTR Increases! Check it out!",
             RecommendationTypes.Performance.value)
    ],
    LevelNames.Campaign.value: [
        Rule([Antecedent(Costs.Cpc.value, MetricTrends.Increasing.value)],
             "This {level}'s cpc is increasing. Video is 10% of the cost of carousel or single image ads. Have you considered launching video"
             " campaigns?", RecommendationTypes.Creative.value),
        # Rule([Antecedent(Metrics.Impressions.value, MetricTrends.Decreasing.value),
        #       Antecedent(Metrics.RelevancyScore.value, NonTrendAttributes.Low.value, isTrend=False)],
        #      "This {level}'s Impressions are decreasing! Your ads are not relevant to your audience. Turn off the worst performing ones.",
        #      RecommendationTypes.Creative.value),
        Rule([Antecedent(Metrics.Reach.value, MetricTrends.Decreasing.value)],

             "This {level}'s Impressions are decreasing! Make sure you have the correct bidding strategy",
             RecommendationTypes.BudgetAndBid.value),
        Rule([Antecedent(Metrics.Reach.value, MetricTrends.Decreasing.value)],
             "This {level}'s Impressions are decreasing! Try setting up a A/B test Campaign",
             RecommendationTypes.BudgetAndBid.value),
        Rule([Antecedent(Metrics.Clicks.value, MetricTrends.Decreasing.value)],
             "This {level}'s Clicks are decreasing! Make sure you have the correct bidding strategy",
             RecommendationTypes.BudgetAndBid.value),
        # Positive Alerts
        Rule([Antecedent(Costs.Cpm.value, MetricTrends.Decreasing.value)],
             "Great job! This {level} is performing really well. CPM decreases! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Costs.Cpc.value, MetricTrends.Decreasing.value)],
             "Great job! This {level} is performing really well. CPC decreases! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Reach.value, MetricTrends.Increasing.value)],
             "Your ads are taking off! This {level} is performing really well. Reach is increasing! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Clicks.value, MetricTrends.Increasing.value)],
             "Your ads are resonating! This {level} is performing really well. Clicks are increasing! Check it out!",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Roas.value, MetricTrends.Increasing.value)],
             "Your ads profitability is looking great! This {level} is performing really well. Should we increase the budget?",
             RecommendationTypes.Performance.value),
        Rule([Antecedent(Metrics.Ctr.value, MetricTrends.Increasing.value)],
             "Great job! This {level} is performing really well. CTR Increases! Check it out!",
             RecommendationTypes.Performance.value)
    ]
}

# Rule([Antecedent(Costs.Cpm.value, MetricTrends.Increasing.value)],
#        "This {level}'s CPM is increasing! Consider A/B test different approaches: a.Try to create sharable content b.Try different ad copy c.Try different creatives"),
# Rule([Antecedent(Metrics.Impressions.value, MetricTrends.Decreasing.value)],
#        "This {level}'s Impressions are decreasing. Creating new campaings is a great way to rekindle interest in your brand."),
