class CaseConverter:
    @staticmethod
    def snake_to_camel_case(text):
        components = text.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
