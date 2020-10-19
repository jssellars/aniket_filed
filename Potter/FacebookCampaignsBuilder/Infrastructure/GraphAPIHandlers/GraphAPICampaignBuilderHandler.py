from copy import deepcopy

from facebook_business.adobjects.campaign import Campaign


class CampaignBudgetAllocationType(object):
    lifetime = 'Lifetime'
    daily = 'Daily'


class GraphAPICampaignBuilderHandler(object):

    def __init__(self):
        self.campaign_template = {}
        self.campaigns = []

    def _build_campaign_core(self, campaign_template):
        if 'campaign_budget_optimization' in campaign_template.keys() and \
                campaign_template['campaign_budget_optimization']:
            self._build_campaign_core_with_budget_optimization(campaign_template)
        else:
            self._build_campaign_core_without_budget_optimization(campaign_template)

        # add special ad category to campaign
        if Campaign.Field.special_ad_category in campaign_template.keys():
            self.campaign_template[Campaign.Field.special_ad_categories] = [
                campaign_template[Campaign.Field.special_ad_category]
            ]
        else:
            self.campaign_template[Campaign.Field.special_ad_categories] = []

    def _build_campaign_core_without_budget_optimization(self, campaign_template):
        self.campaign_template[Campaign.Field.name] = campaign_template['name']
        self.campaign_template[Campaign.Field.objective] = campaign_template['objective']
        if 'spend_cap' in campaign_template.keys() and campaign_template['spend_cap']:
            self.campaign_template[Campaign.Field.spend_cap] = int(float(campaign_template['spend_cap']))
        self.campaign_template[Campaign.Field.buying_type] = campaign_template['buying_type']
        self.campaign_template[Campaign.Field.status] = Campaign.Status.paused
        self.campaign_template[Campaign.Field.effective_status] = Campaign.EffectiveStatus.paused

    def _build_campaign_core_with_budget_optimization(self, campaign_template):
        self._build_campaign_core_without_budget_optimization(campaign_template)

        # Add campaign budget optimization options to campaign core
        campaign_budget_optimization_details = campaign_template['campaign_budget_optimization']

        # Set bid strategy
        self.campaign_template[Campaign.Field.bid_strategy] = \
            campaign_budget_optimization_details['campaign_bid_strategy']['value']

        # Set delivery type
        self.campaign_template[Campaign.Field.pacing_type] = [
            campaign_budget_optimization_details['delivery_type']['value']]

        # Set budget
        if campaign_budget_optimization_details['budget_allocated_type']['name'] == CampaignBudgetAllocationType.lifetime:
            self.campaign_template[Campaign.Field.lifetime_budget] = int(
                campaign_budget_optimization_details['amount'] * 100)
        elif campaign_budget_optimization_details['budget_allocated_type']['name'] == CampaignBudgetAllocationType.daily:
            self.campaign_template[Campaign.Field.daily_budget] = int(campaign_budget_optimization_details['amount'] * 100)
        else:
            raise ValueError(
                'Invalid budget allocation type: %s' % campaign_budget_optimization_details['budget_allocated_type'][
                    'name'])

    def build_campaigns(self,
                        campaign_structure=None,
                        campaign_template=None,
                        targeting_devices=None,
                        targeting_locations=None):
        self._build_campaign_core(campaign_template)

        # Set targeting_devices and targeting_locations to a list with a None element for the case when they come empty or None
        # This covers the usecase when the user enters no countries and no locations, but they still want to split by them.
        if not targeting_devices:
            targeting_devices = [None]

        if not targeting_locations:
            targeting_locations = [None]

        if campaign_structure['split_by_device'] and campaign_structure['split_by_location']:
            for device in targeting_devices:
                for location in targeting_locations:
                    if device is not None and location is not None:
                        campaign = deepcopy(self.campaign_template)
                        campaign[Campaign.Field.name] = self.campaign_template[
                                                            Campaign.Field.name] + " - " + device.title() + " - " + location
                    elif device is None and location is not None:
                        campaign = deepcopy(self.campaign_template)
                        campaign[Campaign.Field.name] = self.campaign_template[Campaign.Field.name] + " - " + location
                    elif device is not None and location is None:
                        campaign = deepcopy(self.campaign_template)
                        campaign[Campaign.Field.name] = self.campaign_template[Campaign.Field.name] + " - " + device
                    else:
                        raise ValueError('Missing device and location split: (%s, %s)' % (device, location))
                    self.campaigns.append(campaign)
        elif campaign_structure['split_by_device'] and not campaign_structure['split_by_location']:
            for device in targeting_devices:
                if device is not None:
                    campaign = self.campaign_template
                    campaign[Campaign.Field.name] = self.campaign_template[Campaign.Field.name] + " - " + device.title()
                    self.campaigns.append(self.campaign_template)
                else:
                    raise ValueError('Missing device to split: %s' % device)
        elif not campaign_structure['split_by_device'] and campaign_structure['split_by_location']:
            for location in targeting_locations:
                if location is not None:
                    campaign = self.campaign_template
                    campaign[Campaign.Field.name] = self.campaign_template[
                                                        Campaign.Field.name] + " - " + location.capitalize()
                    self.campaigns.append(self.campaign_template)
                else:
                    raise ValueError('Missing location to split: %s' % location)
        else:
            self.campaigns.append(deepcopy(self.campaign_template))
