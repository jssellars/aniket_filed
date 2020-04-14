import typing
from string import Formatter

from FacebookDexter.Infrastructure.Domain.TemplateInfoFactory import TemplateInfoFactory


class RecommendationTemplateBuilder:
    @classmethod
    def build_template(cls, template: typing.AnyStr) -> typing.Union[typing.AnyStr, typing.NoReturn]:

        # TODO: you need the data associated with this trigger of the rule template. That means that either you have to pass me some data or fetch it from mongoDB
        PLACEHOLDER_DATA = None

        keywords =  [fname for _, fname, _, _ in Formatter().parse(template.template) if fname]
        info_for_keywords = TemplateInfoFactory.get_info_for_keywords(keywords=keywords, data=PLACEHOLDER_DATA)

        if info_for_keywords:
            dict_info_keywords = dict(info_for_keywords)
            template = template.format(**dict_info_keywords)

        return template
