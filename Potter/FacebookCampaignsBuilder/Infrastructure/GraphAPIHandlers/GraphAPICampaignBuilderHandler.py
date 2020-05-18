from copy import deepcopy

from facebook_business.adobjects.campaign import Campaign


class CampaignBudgetAllocationType(object):
    lifetime = 'Lifetime'
    daily = 'Daily'


class GraphAPICampaignBuilderHandler(object):

    def __init__(self):
        self.campaignTemplate = {}
        self.campaigns = []

    def _BuildCampaignCore(self, campaignTemplate):
        if 'campaign_budget_optimization' in campaignTemplate.keys() and campaignTemplate[
            'campaign_budget_optimization']:
            self._BuildCampaignCoreWithBudgetOptimization(campaignTemplate)
        else:
            self._BuildCampaignCoreWithoutBudgetOptimization(campaignTemplate)

        # add special ad category to campaign
        if Campaign.Field.special_ad_category in self.campaignTemplate.keys():
            self.campaignTemplate[Campaign.Field.special_ad_category] = self.campaignTemplate[
                Campaign.Field.special_ad_category]
        else:
            self.campaignTemplate[Campaign.Field.special_ad_category] = Campaign.SpecialAdCategory.none

    def _BuildCampaignCoreWithoutBudgetOptimization(self, campaignTemplate):
        self.campaignTemplate[Campaign.Field.name] = campaignTemplate['name']
        self.campaignTemplate[Campaign.Field.objective] = campaignTemplate['objective']
        if 'spend_cap' in campaignTemplate.keys() and campaignTemplate['spend_cap']:
            self.campaignTemplate[Campaign.Field.spend_cap] = int(float(campaignTemplate['spend_cap']))
        self.campaignTemplate[Campaign.Field.buying_type] = campaignTemplate['buying_type']
        self.campaignTemplate[Campaign.Field.status] = Campaign.Status.paused
        self.campaignTemplate[Campaign.Field.effective_status] = Campaign.EffectiveStatus.paused

    def _BuildCampaignCoreWithBudgetOptimization(self, campaignTemplate):
        self._BuildCampaignCoreWithoutBudgetOptimization(campaignTemplate)

        # Add campaign budget optimization options to campaign core
        campaignBudgetOptimizationDetails = campaignTemplate['campaign_budget_optimization']

        # Set bid strategy
        self.campaignTemplate[Campaign.Field.bid_strategy] = \
            campaignBudgetOptimizationDetails['campaign_bid_strategy']['value']

        # Set delivery type
        self.campaignTemplate[Campaign.Field.pacing_type] = [
            campaignBudgetOptimizationDetails['delivery_type']['value']]

        # Set budget
        if campaignBudgetOptimizationDetails['budget_allocated_type']['name'] == CampaignBudgetAllocationType.lifetime:
            self.campaignTemplate[Campaign.Field.lifetime_budget] = int(
                campaignBudgetOptimizationDetails['amount'] * 100)
        elif campaignBudgetOptimizationDetails['budget_allocated_type']['name'] == CampaignBudgetAllocationType.daily:
            self.campaignTemplate[Campaign.Field.daily_budget] = int(campaignBudgetOptimizationDetails['amount'] * 100)
        else:
            raise ValueError(
                'Invalid budget allocation type: %s' % campaignBudgetOptimizationDetails['budget_allocated_type'][
                    'name'])

    def BuildCampaigns(self, campaignStructure=None, campaignTemplate=None, targetingDevices=None,
                       targetingLocations=None):
        self._BuildCampaignCore(campaignTemplate)

        # Set targetingDevices and targetingLocations to a list with a None element for the case when they come empty or None
        # This covers the usecase when the user enters no countries and no locations, but they still want to split by them.
        if not targetingDevices:
            targetingDevices = [None]

        if not targetingLocations:
            targetingLocations = [None]

        if campaignStructure['split_by_device'] and campaignStructure['split_by_location']:
            for device in targetingDevices:
                for location in targetingLocations:
                    if device is not None and location is not None:
                        campaign = deepcopy(self.campaignTemplate)
                        campaign[Campaign.Field.name] = self.campaignTemplate[
                                                            Campaign.Field.name] + " - " + device.title() + " - " + location
                    elif device is None and location is not None:
                        campaign = deepcopy(self.campaignTemplate)
                        campaign[Campaign.Field.name] = self.campaignTemplate[Campaign.Field.name] + " - " + location
                    elif device is not None and location is None:
                        campaign = deepcopy(self.campaignTemplate)
                        campaign[Campaign.Field.name] = self.campaignTemplate[Campaign.Field.name] + " - " + device
                    else:
                        raise ValueError('Missing device and location split: (%s, %s)' % (device, location))
                    self.campaigns.append(campaign)
        elif campaignStructure['split_by_device'] and not campaignStructure['split_by_location']:
            for device in targetingDevices:
                if device is not None:
                    campaign = self.campaignTemplate
                    campaign[Campaign.Field.name] = self.campaignTemplate[Campaign.Field.name] + " - " + device.title()
                    self.campaigns.append(self.campaignTemplate)
                else:
                    raise ValueError('Missing device to split: %s' % device)
        elif not campaignStructure['split_by_device'] and campaignStructure['split_by_location']:
            for location in targetingLocations:
                if location is not None:
                    campaign = self.campaignTemplate
                    campaign[Campaign.Field.name] = self.campaignTemplate[
                                                        Campaign.Field.name] + " - " + location.capitalize()
                    self.campaigns.append(self.campaignTemplate)
                else:
                    raise ValueError('Missing location to split: %s' % location)
        else:
            self.campaigns.append(deepcopy(self.campaignTemplate))
