class PreprocessUtils:
    @staticmethod
    def filter_null_values_from_documents(documents):
        return [{k: v for k, v in document.items() if v is not None} for document in documents]
