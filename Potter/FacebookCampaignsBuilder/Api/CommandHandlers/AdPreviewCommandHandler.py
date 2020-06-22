import typing

from facebook_business.adobjects.adaccount import AdAccount

from Potter.FacebookCampaignsBuilder.Api.Commands.AdPreviewCommand import AdPreviewCommand
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIAdPreviewBuilderHandler import \
    GraphAPIAdPreviewBuilderHandler


class AdPreviewCommandHandler:

    @classmethod
    def handle(cls,
               command: AdPreviewCommand = None,
               facebook_config: typing.Any = None,
               permanent_token: typing.AnyStr = None) -> typing.AnyStr:
        ad_builder = GraphAPIAdPreviewBuilderHandler(facebook_config=facebook_config,
                                                     permanent_token=permanent_token)
        ad_builder.build_ad_creative(account_id=command.account_id,
                                     ad_template=command.ad_template,
                                     page_facebook_id=command.page_facebook_id,
                                     instagram_facebook_id=command.instagram_facebook_id)
        params = {
            'ad_format': command.ad_format,
            'creative': ad_builder.ad_creative_details,
        }

        ad_account = AdAccount(fbid=command.account_id)

        ad_preview = ad_account.get_generate_previews(params=params)
        if ad_preview:
            ad_preview = ad_preview[0].export_all_data()
            ad_preview = ad_preview['body']
            ad_preview = ad_preview.replace('scrolling="yes"', 'scrolling="no"')
        else:
            ad_preview = None

        return ad_preview
