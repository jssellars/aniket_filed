from datetime import datetime, timezone


def get_utc_aware_date():
    # UTC AWARE Time information without millisecond, and Z indicates UTC
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()[:-6] + "Z"
