import argparse


class CommonService:

    @classmethod
    def check_positive_value(cls, value: str):
        value = int(value)
        if value <= 0:
            raise argparse.ArgumentTypeError(f"{value} must be greater than 0")
        return value
