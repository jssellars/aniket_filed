from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType


class UpdateStructureOperandMapper:
    @classmethod
    def map(cls, details, structure_id, additional_info, level):
        operand = {}
        extra_operand = None

        if additional_info and level not in [StructureType.AD, StructureType.CAMPAIGN]:
            operand['xsi_type'] = 'BiddableAdGroupCriterion'
            operand['adGroupId'] = additional_info['adgroup_id']
            operand['criterion'] = {}
            operand['criterion']['id'] = structure_id
        elif additional_info and level == StructureType.AD:
            operand['adGroupId'] = additional_info['adgroup_id']
            operand['ad'] = {}
            operand['ad']['id'] = structure_id
        else:
            operand['id'] = structure_id

        for editable_field, value in details.items():
            if editable_field == GoogleFieldsMetadata.cpc_bid.field_name:
                operand['biddingStrategyConfiguration'] = {
                    'bids': [{
                        'xsi_type': 'CpcBid',
                        'bid': {
                            'microAmount': int(value * 1_000_000),
                        }
                    }]
                }

            elif editable_field == GoogleFieldsMetadata.amount.field_name:
                extra_operand = {
                    'budgetId': additional_info['budget_id'],
                    'amount': {
                        'microAmount': int(value * 1_000_000),
                    }
                }
            elif editable_field == GoogleFieldsMetadata.status.field_name and additional_info and level != StructureType.AD:
                operand[EDITABLE_FIELD_TO_STRUCTURE[editable_field]] = 'userStatus'
            elif editable_field == GoogleFieldsMetadata.final_urls.field_name:
                operand[EDITABLE_FIELD_TO_STRUCTURE[editable_field]] = [value]
            else:
                operand[EDITABLE_FIELD_TO_STRUCTURE[editable_field]] = value

        return operand, extra_operand


EDITABLE_FIELD_TO_STRUCTURE = {
    GoogleFieldsMetadata.campaign_status.field_name: 'status',
    GoogleFieldsMetadata.ad_group_status.field_name: 'status',
    GoogleFieldsMetadata.status.field_name: 'status',
    GoogleFieldsMetadata.campaign_name.field_name: 'name',
    GoogleFieldsMetadata.ad_group_name.field_name: 'name',

    GoogleFieldsMetadata.amount.field_name: 'budget',
    GoogleFieldsMetadata.final_urls.field_name: 'finalUrls'
}
