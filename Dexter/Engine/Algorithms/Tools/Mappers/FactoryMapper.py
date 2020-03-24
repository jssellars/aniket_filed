from Algorithms.Tools.Mappers.FacebookMapper import FacebookMapper
from Algorithms.Tools.Columns import ChannelEnum


class FactoryMapper:
    @staticmethod
    def get_mapper(channel):
        if channel == ChannelEnum.FACEBOOK:
            return FacebookMapper.mapping
        # TODO: implement google mapper
        elif channel == ChannelEnum.GOOGLE:
            return None
