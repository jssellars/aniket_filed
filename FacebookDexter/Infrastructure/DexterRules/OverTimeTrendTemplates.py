from enum import Enum

from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import ApplyActionType
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterRecommendationOutput, RecommendationPriority


class OverTimeTrendTemplate(Enum):
    CR_DOWN_CTR_DOWN_CPC_UP = DexterRecommendationOutput(
        (
            "Your cost per click is increasing and your click-through rate is decreasing. Over the last {no_of_days}"
            " days it's become {trigger_variance:.2f}% more expensive to run your ad(s)."
        ),
        RecommendationPriority.HIGH,
        "Improve Ad Copy & Creatives",
        "Fewer people are clicking on your ad(s) and interacting with your landing page.",
        (
            "Dexter recommends trying a new Ad Copy and Creative."
            " Try aligning your Ad Copy with your landing page, and make sure the call to actions are clear."
        ),
    )

    CR_DOWN_CPM_UP = DexterRecommendationOutput(
        (
            "Your cost per impression is increasing. Over the last {no_of_days} days your results have also decreased "
            "by {trigger_variance:.2f}%"
        ),
        RecommendationPriority.HIGH,
        "Change Interest Targeting",
        "Fewer people are viewing your ad(s).",
        (
            "Dexter recommends changing the interests that you're targeting. Head over to Dexter Labs to try some "
            "hidden interests. These aren't available on Facebook Ads Manager and so may be cheaper to target."
        ),
    )

    RESULTS_DOWN_CPM_UP_CR_DOWN = DexterRecommendationOutput(
        (
            "Your cost per impression is increasing. Over the last {no_of_days} days your results have also "
            "decreased by {trigger_variance:.2f}%"
        ),
        RecommendationPriority.MEDIUM,
        "Change Interest Targeting",
        "Fewer people are viewing your ad(s) and results are decreasing.",
        (
            "Dexter recommends changing the interests that you’re targeting. Head over to Dexter Labs to try some "
            "hidden interests. These interests aren't available on Facebook Ads Manager and so may be "
            "cheaper to target."
        ),
    )

    RESULTS_DOWN_CPC_UP_CTR_UP = DexterRecommendationOutput(
        (
            "Your cost per click is increasing and your click-through rate is increasing."
            " However, over the last {no_of_days} days your results have decreased by {trigger_variance:.2f}%."
        ),
        RecommendationPriority.MEDIUM,
        "Launch AB Testing",
        "Fewer people are clicking on your ad(s) but they are interacting with your landing page.",
        (
            "Dexter recommends creating an AB test to test new Ad Copies and Creatives."
            " Try to maintain the same message as the landing page but make the Ad(s) more exciting."
        ),
    )

    RESULTS_DOWN_CPC_UP_CTR_DOWN = DexterRecommendationOutput(
        (
            "Your cost per click is increasing and your click-through rate is decreasing."
            " Over the last {no_of_days} days your results have decreased by {trigger_variance:.2f}%."
        ),
        RecommendationPriority.HIGH,
        "Reduce Budget",
        "Fewer people are clicking on your ad(s) and interacting with your landing page.",
        "Dexter recommends reducing your budget by 20%. Click apply and I’ll do this for you!",
        apply_action_type=ApplyActionType.BUDGET_DECREASE,
    )

    RESULTS_DOWN_CR_DOWN_CPR_UP = DexterRecommendationOutput(
        (
            "Your cost per result is increasing and your conversion rate is decreasing. Over the last {no_of_days} days"
            " your results have decreased by {trigger_variance:.2f}%."
        ),
        RecommendationPriority.HIGH,
        "New Interest Targeting",
        "Fewer people are converting and it’s becoming more expensive to target them",
        (
            "Dexter recommends changing the interests that you’re targeting. Head over to Dexter Labs to try "
            "some hidden interests. These interests aren't available on Facebook Ads Manager and so may be "
            "cheaper to target."
        ),
    )

    RESULTS_DOWN_UNIQUE_CTR_UP = DexterRecommendationOutput(
        (
            "Your results have fallen by {trigger_variance:.2f}% over the last {no_of_days} days but your "
            "click-through rate has increased."
        ),
        RecommendationPriority.MEDIUM,
        "Launch AB Testing",
        "Your results have fallen but your click-through rate has increased.",
        (
            "Your landing page is well optimised! However, your results are still decreasing."
            " Dexter recommends creating an AB test to test new Ad Copies and Creatives."
            " Try to maintain the same message as the landing page but make the Ad(s) more exciting."
        ),
    )

    RESULTS_DOWN_UNIQUE_CTR_DOWN = DexterRecommendationOutput(
        (
            "Your results have decreased by {trigger_variance:.2f}% over the last {no_of_days} days and your "
            "click-through rate has decreased as well."
        ),
        RecommendationPriority.HIGH,
        "Improve Ad Copy & Creatives",
        "Fewer people are clicking on your ad(s) and interacting with your landing page",
        (
            "Dexter recommends trying a new Ad Copy and Creative."
            " Try aligning your Ad Copy with your landing page and making sure the call to actions are clear."
        ),
    )

    RESULTS_DOWN_AMOUNT_SPENT_UP_CPC_UP = DexterRecommendationOutput(
        (
            "Your amount spent has increased however your cost per click has increased and"
            " your results have decreased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Reduce Budget",
        "Fewer people are clicking on your ad(s)",
        "Dexter recommends reducing your budget by 20%. Click apply and I’ll do this for you!",
        apply_action_type=ApplyActionType.BUDGET_DECREASE,
    )

    RESULTS_DOWN_CPR_UP_CPC_UP = DexterRecommendationOutput(
        (
            "Your cost per click and cost per result have increased causing your results to decrease by "
            "{trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Reduce Budget",
        "Fewer people are clicking on your ad(s) and results are getting more expensive",
        "Dexter recommends reducing your budget by 20%. Click apply and I’ll do this for you!",
        apply_action_type=ApplyActionType.BUDGET_DECREASE,
    )

    RESULTS_UP_UNIQUE_CLICKS_UP = DexterRecommendationOutput(
        (
            "Your unique clicks are increasing and your results have increased by "
            "{trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Create a lookalike audience",
        "More people are clicking on your ads!",
        (
            "Well done, your campaign is performing well. Dexter recommends creating a lookalike audience "
            "to take advantage of this. Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.CREATE_LOOKALIKE,
    )

    RESULTS_UP_UNIQUE_CTR_DOWN = DexterRecommendationOutput(
        (
            "Your click-through rate has decreased but results have increased by {trigger_variance:.2f}% "
            "over the last {no_of_days} days."
        ),
        RecommendationPriority.LOW,
        "Improve Ad Copy & Creatives",
        "Your results have increased but your click-through rate has decreased.",
        (
            "Dexter recommends trying a new Ad Copy and Creative."
            " Try aligning your Ad Copy with your landing page and making sure the call to actions are clear."
        ),
    )

    RESULTS_UP_CPC_DOWN_CTR_UP = DexterRecommendationOutput(
        (
            "Your cost-per click has decreased and your click-through rate has increased."
            " Your results have also increased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "More people are clicking on your ad(s) and interacting with your landing page",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    RESULTS_UP_CPC_DOWN_CPM_DOWN = DexterRecommendationOutput(
        (
            "Your cost per click and your cost per impression have decreased."
            " Your results have also increased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "More people are viewing and clicking on your ad(s)",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    RESULTS_UP_CPC_DOWN_CTR_UP_CPM_DOWN = DexterRecommendationOutput(
        (
            "Your cost per click and your cost per impression have decreased and your click-through rate has increased."
            " Your results have also increased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "More people are viewing and clicking on your ad(s) as well as interacting with your landing page.",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    RESULTS_UP_AMOUNT_SPENT_UP_CPC_DOWN_CPM_DOWN = DexterRecommendationOutput(
        (
            "Your amount spent has increased and your cost per click and cost per impression have decreased."
            " Your results have also increased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "More people are viewing and clicking on your ad(s)",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    RESULTS_UP_CPR_DOWN_CPM_DOWN = DexterRecommendationOutput(
        (
            "Your cost per impression and your cost per result have decreased."
            " Your results have also increased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "More people are viewing your ads making conversions cheaper",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    CTR_DOWN_CPM_UP_CPC_UP = DexterRecommendationOutput(
        (
            "Your cost per impression and your cost per click have increased whilst your click-through rate has "
            "decreased."
        ),
        RecommendationPriority.MEDIUM,
        "New Interest Targeting",
        "Fewer people are viewing and clicking on your ad(s)",
        (
            "Your audience has become more competitive to target. Dexter recommends changing the interests that "
            "you’re targeting. Head over to Dexter Labs to try some hidden interests. These interests aren't available "
            "on Facebook Ads Manager and so may be cheaper to target."
        ),
    )

    CTR_DOWN_CPR_UP_CPM_UP = DexterRecommendationOutput(
        "Your cost per result and cost per impression have increased.",
        RecommendationPriority.HIGH,
        "Reset AdSet",
        "Fewer people are viewing your ad(s) making conversions more expensive",
        "Dexter recommends resetting the AdSet. Click apply and I’ll do this for you!",
        apply_action_type=ApplyActionType.DUPLICATE_AND_PAUSE_STRUCTURE,
    )

    CTR_UP_CPM_DOWN_CPC_DOWN = DexterRecommendationOutput(
        (
            "Your cost per impression and your cost per click have decreased."
            " Your click-through rate has increased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "More people are viewing and clicking on your ad(s) as well as interacting with your landing page.",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    CPM_UP_RESULTS_DOWN_CTR_UP = DexterRecommendationOutput(
        (
            "Your results have decreased and your click-through rate has increased."
            " Your cost per impression has also increased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.MEDIUM,
        "Improve Ad Copy & Creatives",
        "Fewer people are viewing your ad(s) but they are interacting with your landing page.",
        (
            "Dexter recommends trying a new Ad Copy and Creative. "
            "Try aligning your Ad Copy with your landing page and making sure the call to actions are clear."
        ),
    )

    CPM_UP_RESULTS_DOWN_CPR_UP = DexterRecommendationOutput(
        (
            "Your results have decreased and your cost per result has increased."
            " Your cost per impression has also increased by {trigger_variance:.2f}% over the last {no_of_days} days."
        ),
        RecommendationPriority.MEDIUM,
        "Reduce Budget",
        "Fewer people are viewing your ad(s) and conversions are getting more expensive.",
        ("Dexter recommends reducing your budget by 20%. Click apply and I’ll do this for you!"),
        apply_action_type=ApplyActionType.BUDGET_DECREASE,
    )

    CLICKS_DOWN_CPC_UP = DexterRecommendationOutput(
        ("Your cost per click has increased and your overall clicks has decreased."),
        RecommendationPriority.MEDIUM,
        "Improve Ad Copy & Creatives",
        "Fewer people are clicking on your ad(s)",
        (
            "Dexter recommends trying a new Ad Copy and Creative. Try aligning your Ad Copy with your landing page and "
            "making sure the call to actions are clear."
        ),
    )

    CLICKS_DOWN_CPM_UP = DexterRecommendationOutput(
        ("Your cost per impression has increased and your overall clicks has decreased."),
        RecommendationPriority.MEDIUM,
        "New Interest Targeting",
        "Fewer people are viewing and clicking on your ad(s)",
        (
            "Dexter recommends changing the interests that you’re targeting."
            " Head over to Dexter Labs to try some hidden interests."
            " These interests aren't available on Facebook Ads Manager and so may be cheaper to target."
        ),
    )

    CLICK_UP_CTR_UP_CPC_DOWN_CPM_DOWN = DexterRecommendationOutput(
        "Your click-through rate has increased. Your cost per click and cost per impression has decreased.",
        RecommendationPriority.LOW,
        "Increase Budget",
        "More people are viewing and clicking on your ad(s) and people are interacting with your landing page.",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    AMOUNT_SPENT_DOWN_CPR_UP = DexterRecommendationOutput(
        "Your cost per result has increased by {trigger_variance:.2f} % over the last {no_of_days} days.",
        RecommendationPriority.MEDIUM,
        "Improve Ad Copy & Creatives",
        "Conversions are getting more expensive.",
        (
            "Dexter recommends trying a new Ad Copy and Creative."
            " Try aligning your Ad Copy with your landing page and making sure the call to actions are clear."
        ),
    )

    AMOUNT_SPENT_DOWN_CPR_DOWN = DexterRecommendationOutput(
        ("Your cost per result has decreased by {trigger_variance:.2f} % over the last {no_of_days} days."),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Conversions are getting cheaper",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    AMOUNT_SPENT_DOWN_RESULTS_UP = DexterRecommendationOutput(
        "Your results have increased by {trigger_variance:.2f} % over the last {no_of_days} days.",
        RecommendationPriority.MEDIUM,
        "Increase Budget",
        "Your results have increased",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    AMOUNT_SPENT_UP_CPR_UP = DexterRecommendationOutput(
        (
            "You raised the amount spent and your cost per result have both increased. It changed by"
            " {trigger_variance:.2f}% in the last {no_of_days} days average. "
        ),
        RecommendationPriority.MEDIUM,
        "Increase Budget",
        "Your amount spent and cost per result have increased. Consider increasing the budget!",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%."
            " Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    AMOUNT_SPENT_UP_CPR_DOWN = DexterRecommendationOutput(
        "Your cost per result has decreased by {trigger_variance:.2f} % over the last {no_of_days} days.",
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Conversions are becoming cheaper",
        (
            "Well done, your campaign is performing well. Dexter recommends increasing your budget by 20%. "
            "Click apply and I’ll do this for you!"
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    CPR_UP_IMPRESSIONS_DOWN = DexterRecommendationOutput(
        (
            "Your impressions have decreased and your cost per result has increased by {trigger_variance:.2f} % "
            "over the last {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Improve Ad Copy & Creatives",
        "Fewer people are seeing your ad(s) and conversions are getting more expensive.",
        (
            "Dexter recommends trying a new Ad Copy and Creative."
            " Try aligning your Ad Copy with your landing page and making sure the call to actions are clear."
        ),
    )

    LANDING_PAGE_CONVERSION_RATE_DOWN_UNIQUE_CLICKS_UP = DexterRecommendationOutput(
        "Your clicks have increased but your landing page conversion rate has decreased.",
        RecommendationPriority.HIGH,
        "Improve Ad Copy & Creatives",
        "More people are clicking on your ad(s) but people aren't interacting with your landing page",
        (
            "Dexter recommends trying a new Ad Copy and Creative."
            " Try aligning your Ad Copy with your landing page and making sure the call to actions are clear."
        ),
    )
