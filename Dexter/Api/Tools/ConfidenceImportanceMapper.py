class ConfidenceImportanceMapper:

    @staticmethod
    def getConfidenceImportanceString(confidence):
        if (confidence == 1):
            return 'LOW'
        if (confidence == 2):
            return 'MEDIUM'
        if (confidence == 3):
            return 'HIGH'

    @staticmethod
    def getConfidenceImportanceValue(confidence):
        if (confidence == 'LOW'):
            return 1
        if (confidence == 'MEDIUM'):
            return 2
        if (confidence == 'HIGH'):
            return 3
