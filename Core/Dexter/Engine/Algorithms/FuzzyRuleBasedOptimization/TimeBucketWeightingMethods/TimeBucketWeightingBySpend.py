def time_bucket_weighting_by_spend(spend, time_bucket_period):
    return -4 * spend * (time_bucket_period - 1)
