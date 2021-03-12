from enum import Enum

from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import ApplyActionType
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterRecommendationOutput, RecommendationPriority


class OverTimeTrendTemplate(Enum):
    CR_DOWN_CTR_DOWN_CPC_UP = DexterRecommendationOutput(
        (
            "We noticed your cost is increasing and people are less interested in your ads. This is a trend we’ve seen"
            " over the last {no_of_days} days and it's becoming more expensive to run ads by {trigger_variance:.2f}%."
        ),
        RecommendationPriority.HIGH,
        "Improve Ad Copy & Creatives",
        "Your cost is increasing and there is less interest in your ads.",
        (
            "Dexter recommends looking at your ads, if the budget is high, to consider lowering. You should also make"
            " sure to ad copy matches what displays on your landing page to make sure it aligns and the CTA on the"
            " landing page and ads are very clear."
        ),
    )

    CR_DOWN_CPM_UP = DexterRecommendationOutput(
        (
            "We’ve noticed your conversions are getting more expensive and results are decreasing by"
            " {trigger_variance:.2f}% over the last {no_of_days} days on average."
        ),
        RecommendationPriority.HIGH,
        "Change Interest Targeting",
        "Your conversions are getting more expensive.",
        (
            "Dexter suggests that since your ads have been running long enough using this interests, to consider"
            " duplicating your adset and targeting new interests."
        ),
    )

    RESULTS_DOWN_CPM_UP_CR_DOWN = DexterRecommendationOutput(
        (
            "We’ve noticed your conversions are getting more expensive and results are decreasing by"
            " {trigger_variance:.2f}% over the last {no_of_days} days on average."
        ),
        RecommendationPriority.MEDIUM,
        "Change Interest Targeting",
        "Your results are decreasing and are getting more expensive.",
        (
            "Dexter suggests that since your ads have been running long enough using this interests, to consider"
            " duplicating your adset and targeting new interests."
        ),
    )

    RESULTS_DOWN_CPC_UP_CTR_UP = DexterRecommendationOutput(
        (
            "We noticed the cost is getting more expensive to run your ads. People are clicking on your ads, but"
            " results are trending down by {trigger_variance:.2f}% in the last {no_of_days} days on average. Your"
            " audience is excited about your message, but they aren't converting."
        ),
        RecommendationPriority.MEDIUM,
        "Launch AB Testing",
        "Your results are decreasing and it’s getting more competitive to run your ads",
        (
            "Dexter suggests creating an AB or to launch a dynamic ad to test new ad copy or creatives to know what"
            " will work best with this audience."
        ),
    )

    RESULTS_DOWN_CPC_UP_CTR_DOWN = DexterRecommendationOutput(
        (
            "There is less interest in with your ad, results have decreased by {trigger_variance:.2f}% over the last"
            " {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Reduce Budget",
        "There is less interest with your ads and results have decreased over time.",
        (
            "Dexter recommends reducing your budget by 20% to see if that helps stabilize your adset in a"
            " competitive market."
        ),
    )

    RESULTS_DOWN_CR_DOWN_CPR_UP = DexterRecommendationOutput(
        (
            "We’ve noticed your results, conversion rate and cost per result are all moving in the wrong direction over"
            " the last {no_of_days} days. Dexter thinks your message isn’t resonating with your interest targeting. "
        ),
        RecommendationPriority.HIGH,
        "New Interest Targeting",
        "Results and conversion rate are decreasing while cost per result is increasing. ",
        (
            "Dexter suggests finding 3 new interests and creating a new adset for each of them to see which one"
            " performs the best."
        ),
    )

    RESULTS_DOWN_UNIQUE_CTR_UP = DexterRecommendationOutput(
        (
            "Your results are falling, but CTR is increasing. We noticed a change in results by"
            " {trigger_variance:.2f}% in the last {no_of_days} days on average."
        ),
        RecommendationPriority.MEDIUM,
        "Launch AB Testing",
        "Your results are falling while your CTR is increasing. ",
        (
            "Dexter suggests you check the landing page and run some A/B testing of your copy and creative elements"
            " within the landing page to find what works best and helps keep your results up."
        ),
    )

    RESULTS_DOWN_UNIQUE_CTR_DOWN = DexterRecommendationOutput(
        (
            "Dexter noticed your CTR and results both have decreasing trends. For example, your results changed by"
            " {trigger_variance:.2f}% in the last {no_of_days} days on average. "
        ),
        RecommendationPriority.HIGH,
        "Improve Ad Copy & Creatives",
        "Your results and click-through rates are falling.",
        (
            "Improve your ad copy and creatives in order keep your audience interested. Find the ads that are least"
            " performing and consider turning them off."
        ),
    )

    RESULTS_DOWN_AMOUNT_SPENT_UP_CPC_UP = DexterRecommendationOutput(
        (
            "Following your recent increase in the amount spent, the cost of running your ads has increased and results"
            " are falling by {trigger_variance:.2f}% over the last {no_of_days} days as a result. "
        ),
        RecommendationPriority.HIGH,
        "Decrease Budget",
        "Following your recent increase in the amount spent, the cost has increased and results are falling.",
        "Dexter suggests lowering your budget by 20%. ",
        apply_action_type=ApplyActionType.BUDGET_DECREASE,
    )

    RESULTS_DOWN_CPR_UP_CPC_UP = DexterRecommendationOutput(
        (
            "We noticed that it’s becoming increasingly more expensive to keep your ads running. Your results are more"
            " expensive, your CPCs have increased and results have decreased by {trigger_variance:.2f}% over the last"
            " {no_of_days} days."
        ),
        RecommendationPriority.HIGH,
        "Decrease Budget",
        "Your results are getting expensive and results have decreased over time.",
        "Dexter suggests lowering your budget by 20% to see if that helps bring your cost down. ",
        apply_action_type=ApplyActionType.BUDGET_DECREASE,
    )

    RESULTS_UP_UNIQUE_CTR_DOWN = DexterRecommendationOutput(
        (
            "Your results are increasing, but CTR has also decreased so stay alert. Dexter noticed a change in results"
            " by {trigger_variance:.2f}% in the last {no_of_days} days on average. "
        ),
        RecommendationPriority.LOW,
        "Improve Ad Copy & Creatives",
        "Your results are increasing but click-through rate has decreased. Stay alert.",
        (
            "Consider changing or improving your ad copy and creatives to help improve your CTR. Find the least"
            " performing ads and consider taking action by improving them or shutting them off."
        ),
    )

    RESULTS_UP_CPC_DOWN_CTR_UP = DexterRecommendationOutput(
        "Your campaign is performing well, don't touch it. ",
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "Dexter suggests you should increase budget by 20%. ",
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    RESULTS_UP_CPC_DOWN_CPM_DOWN = DexterRecommendationOutput(
        "Your campaign is performing well, don't touch it. ",
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "Dexter suggests you should increase budget by 20%. ",
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    RESULTS_UP_CPC_DOWN_CTR_UP_CPM_DOWN = DexterRecommendationOutput(
        "Your campaign is performing well, don't touch it. ",
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "Dexter suggests you should increase budget by 20%. ",
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    RESULTS_UP_AMOUNT_SPENT_UP_CPC_DOWN_CPM_DOWN = DexterRecommendationOutput(
        "Following your increase in the amount spent, your ads are performing well. ",
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "Consider increasing your budget by 20% more. ",
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    RESULTS_UP_CPR_DOWN_CPM_DOWN = DexterRecommendationOutput(
        "Your campaign is performing well, don't touch it. ",
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "Dexter suggests increasing budget by 20%. ",
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    CTR_DOWN_CPM_UP_CPC_UP = DexterRecommendationOutput(
        (
            "Dexter wants you to be aware, It's getting more competitive to run your ads in the marketplace and your"
            " CTR has decreased by {trigger_variance:.2f}% in the last {no_of_days} days. "
        ),
        RecommendationPriority.MEDIUM,
        "New Interest Targeting",
        "It’s getting more competitive to run your ads, but we have some new ideas for you.",
        "Have you considered running new interest targeting? ",
    )

    CTR_DOWN_CPR_UP_CPM_UP = DexterRecommendationOutput(
        ("We've noticed that your adset is fatiguing. Consider recreating the adset. "),
        RecommendationPriority.HIGH,
        "Recreate adset",
        "Looks like your adset if fatiguing",
        "Dexter suggests you to recreate the adset",
        apply_action_type=ApplyActionType.DUPLICATE_AND_PAUSE_STRUCTURE,
    )

    CTR_UP_CPM_DOWN_CPC_DOWN = DexterRecommendationOutput(
        (
            "Your campaign is performing really well. Dexter has noticed that your CTR has increased by"
            " {trigger_variance:.2f}% in the last {no_of_days} days. Your CPMs and CPCs have also both decreased during this period,"
            " which is great. "
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "Increase your budget by 20%. ",
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    CPM_UP_RESULTS_DOWN_CTR_UP = DexterRecommendationOutput(
        (
            "We’ve noticed that it’s increasingly becoming more competitive to run your ad right now, your CPMs have"
            " increased by {trigger_variance:.2f}%. There’s also less interest in your ads over the last {no_of_days}"
            " days as your CTR has fallen. "
        ),
        RecommendationPriority.MEDIUM,
        "Improve Ad Copy & Creatives",
        "It’s getting more competitive to run your ads right now, but we have some new ideas for you.",
        "Dexter suggests reducing your budget or refreshing your creatives by testing different ad creatives or copy. ",
    )

    CPM_UP_RESULTS_DOWN_CPR_UP = DexterRecommendationOutput(
        (
            "We’ve noticed your cost per result has increased and your CPMs have increased by {trigger_variance:.2f}%"
            " over the last {no_of_days} days. There’s also less interest in your ads over the last {no_of_days} days"
            " as your results have fallen. "
        ),
        RecommendationPriority.MEDIUM,
        "Decrease Budget",
        "Your cost is increasing and there is less interest in your ads.",
        (
            "Dexter suggests reducing your budget or trying a new interest targeting to help your overall campaign"
            " performance. "
        ),
        apply_action_type=ApplyActionType.BUDGET_DECREASE,
    )

    CLICKS_DOWN_CPC_UP = DexterRecommendationOutput(
        "Dexter noticed your clicks are decreasing and getting more expensive to run your ads. ",
        RecommendationPriority.MEDIUM,
        "Improve Ad Copy & Creatives",
        "Less people are clicking on your ads and the cost per click has increased.",
        "Consider pausing your campaign or targeting some new interests. ",
    )

    CLICKS_DOWN_CPM_UP = DexterRecommendationOutput(
        "Dexter noticed your clicks are decreasing and getting more expensive to run your ads. ",
        RecommendationPriority.MEDIUM,
        "New Interest Targeting",
        "Your clicks are decreasing and it’s getting more expensive to run your ads.",
        "Consider pausing your campaign or targeting some new interests. ",
    )

    CLICK_UP_CTR_UP_CPC_DOWN_CPM_DOWN = DexterRecommendationOutput(
        "Your campaign is performing well, don't touch it. ",
        RecommendationPriority.LOW,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "Dexter suggests increasing your budget by 20%. ",
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    AMOUNT_SPENT_DOWN_CPR_UP = DexterRecommendationOutput(
        (
            "You decreased the amount spent and your cost per result is increasing. It changed by"
            " {trigger_variance:.2f}% in the last {no_of_days} days on average. Your bid for this audience might not be"
            " competitive enough or the audience does not match the ad creative or offer. "
        ),
        RecommendationPriority.MEDIUM,
        "Improve Ad Copy & Creatives",
        "You decreased your budget and your cost per result is increasing.",
        (
            "Dexter suggests you pause this campaign and refine it, to better resonate with the audience you are"
            " targeting."
        ),
    )

    AMOUNT_SPENT_DOWN_CPR_DOWN = DexterRecommendationOutput(
        (
            "Good job! You decreased the amount spent and your cost per result is decreasing as a result. It changed by"
            " {trigger_variance:.2f} % in the last {no_of_days} days average. "
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "At this point, it’s safe to say your ad performance looks great. Don't make any changes at this time.",
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    AMOUNT_SPENT_DOWN_RESULTS_UP = DexterRecommendationOutput(
        (
            "Good job! You decreased the amount spent and your results are increasing as a result. It changed by"
            " {trigger_variance:.2f}% in the last {no_of_days} days average. "
        ),
        RecommendationPriority.MEDIUM,
        "Increase Budget",
        "Your campaign is performing really well, consider increasing the budget!",
        "Dexter suggests increasing your budget by 20% in order to get even more results.",
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
            "Breakdown your campaign by age, gender or placements to see which target is spending budget without"
            " notable results. "
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    AMOUNT_SPENT_UP_CPR_DOWN = DexterRecommendationOutput(
        (
            "Good job! Your amount spent and your cost per result are decreasing. It changed by {trigger_variance:.2f}%"
            " in the last {no_of_days} days on average. "
        ),
        RecommendationPriority.HIGH,
        "Increase Budget",
        "Your amount spent and cost per result are decreasing. ",
        (
            "Dexter suggests increasing your budget by  20% and keep a close eye on performance to ensure your cost per"
            " result doesn’t increase over time."
        ),
        apply_action_type=ApplyActionType.BUDGET_INCREASE,
    )

    CPR_UP_IMPRESSIONS_DOWN = DexterRecommendationOutput(
        "Your cost per result is increasing while impressions have decreased overtime. ",
        RecommendationPriority.HIGH,
        "Improve Ad Copy & Creatives",
        "Your cost per result is increasing while your impressions have decreased over time. ",
        (
            "Consider increasing your audience, change the ad creatives, or improve the landing page message. Try to"
            " add some call-to-actions in your landing page copy. Check your ads now and find out which one is the"
            " least performing, then consider making improvements, or turn it off."
        ),
    )

    LANDING_PAGE_CONVERSION_RATE_DOWN_UNIQUE_CLICKS_UP = DexterRecommendationOutput(
        "Your landing page conversion rate is decreasing while your clicks are increasing. ",
        RecommendationPriority.HIGH,
        "Improve Ad Copy & Creatives",
        "Your landing page conversion rate is decreasing while clicks are increasing. ",
        (
            "Make sure you matched the audience and ad copy with what your landing page says. Check your ads now to see"
            " which one is the less performing and make the appropriate changes."
        ),
    )
