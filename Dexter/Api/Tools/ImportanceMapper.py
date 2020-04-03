class ImportanceMapper:

    @staticmethod
    def get_importance_string(confidence):
        if (confidence == 1):
            return 'LOW'
        if (confidence == 2):
            return 'MEDIUM'
        if (confidence == 3):
            return 'HIGH'

    @staticmethod
    def get_importance_value(confidence):
        if (confidence == 'LOW'):
            return 1
        if (confidence == 'MEDIUM'):
            return 2
        if (confidence == 'HIGH'):
            return 3
