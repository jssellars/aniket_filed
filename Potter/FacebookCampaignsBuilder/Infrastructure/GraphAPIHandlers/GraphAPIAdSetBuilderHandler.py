import json
from copy import deepcopy

from facebook_business.adobjects.adset import AdSet


class AdSetBudgetAllocationType(object):
    lifetime = 'Lifetime'
    daily = 'Daily'


class GraphAPIAdSetBuilderHandler(object):
    _maximumFacebookAge = 65
    _defaultAgeSplit = 5

    def __init__(self):
        self.adSetTemplate = {}
        self.adSets = []

    @staticmethod
    def _convertBidStrategy(bidStrategy):
        if bidStrategy == 'Cost Cap':
            return 'LOWEST_COST_WITHOUT_CAP'
        elif bidStrategy == 'Target Cost':
            return 'TARGET_COST'
        elif bidStrategy == 'Bid Cap':
            return 'LOWEST_COST_WITH_BID_CAP'
        else:
            raise ValueError('Unknown bid strategy value: %s' % bidStrategy)

    @staticmethod
    def _convertPacingType(pacingType):
        if pacingType == 'Standard':
            return ['standard']
        elif pacingType == 'Accelerated':
            return ['no_pacing']
        else:
            raise ValueError('Unknown pacing type value: %s' % pacingType)

    def _appendAdSetBudget(self, adSetTemplate):
        if adSetTemplate['budget_allocate_type'] == AdSetBudgetAllocationType.daily:
            self.adSetTemplate[AdSet.Field.daily_budget] = int(adSetTemplate['budget_amount'] * 100)
        elif adSetTemplate['budget_allocate_type'] == AdSetBudgetAllocationType.lifetime:
            self.adSetTemplate[AdSet.Field.lifetime_budget] = int(adSetTemplate['budget_amount'] * 100)

    def _appendAdSetMinMaxBudget(self, adSetTemplate):
        if adSetTemplate['budget_allocate_type'] == AdSetBudgetAllocationType.daily:
            self.adSetTemplate[AdSet.Field.daily_min_spend_target] = int(adSetTemplate['budget_min_amount'] * 100)
            self.adSetTemplate[AdSet.Field.daily_spend_cap] = int(adSetTemplate['budget_max_amount'] * 100)
        elif adSetTemplate['budget_allocate_type'] == AdSetBudgetAllocationType.lifetime:
            self.adSetTemplate[AdSet.Field.lifetime_min_spend_target] = int(adSetTemplate['budget_min_amount'] * 100)
            self.adSetTemplate[AdSet.Field.lifetime_spend_cap] = int(adSetTemplate['budget_max_amount'] * 100)

    def _appendAdSetSchedule(self, adSetTemplate):
        if adSetTemplate['schedule_type'] == 'Run my campaign on a schedule':
            if adSetTemplate['schedule_entries']:
                adset_schedule = []
                for scheduleEntry in adSetTemplate['schedule_entries']:
                    adset_schedule.append({
                        'start_minute': scheduleEntry['start_minute'],
                        'end_minute': scheduleEntry['end_minute'],
                        'days': scheduleEntry['days'],
                        'timezone_type': adSetTemplate['schedule_time_zone_type']
                    })
                self.adSetTemplate[AdSet.Field.adset_schedule] = adset_schedule
                # TODO: Potentially add this to campaignTemplate if adset schedule is on (campaign budget optimization)
                self.adSetTemplate[AdSet.Field.pacing_type] = ['day_parting']
            else:
                raise ValueError('Missing schedule entries from adset template.')
        elif adSetTemplate['schedule_type'] != 'Run my campaign all the time':
            raise ValueError('Unknown schedule type: %s' % adSetTemplate['schedule_type'])

    def _appendAdSetBudgetSpendCap(self, adSetTemplate):
        if hasattr(adSetTemplate, 'spend_cap') and adSetTemplate['budget_allocate_type'] == 'Daily':
            self.adSetTemplate[AdSet.Field.daily_spend_cap] = adSetTemplate['spend_cap']
        elif hasattr(adSetTemplate, 'spend_cap') and adSetTemplate['budget_allocate_type'] == 'Lifetime':
            self.adSetTemplate[AdSet.Field.lifetime_spend_cap] = adSetTemplate['spend_cap']

    def _appendAdSetBidAmount(self, adSetTemplate):
        if 'budget_bid_cap_amount' in adSetTemplate.keys() and adSetTemplate['budget_bid_cap_amount']:
            self.adSetTemplate[AdSet.Field.bid_amount] = int(adSetTemplate['budget_bid_cap_amount'] * 100)

    def _appendAdSetPromotedObject(self, adSetTemplate):
        if 'promoted_object' in adSetTemplate.keys():
            self.adSetTemplate[AdSet.Field.promoted_object] = adSetTemplate['promoted_object']
        if 'promoted_object' in self.adSetTemplate.keys():
            if 'pixel_rule' in self.adSetTemplate['promoted_object'].keys() and isinstance(
                    adSetTemplate['promoted_object']['pixel_rule'], str):
                pixelRule = json.loads(adSetTemplate['promoted_object']['pixel_rule']).replace('\\', '')
                self.adSetTemplate['promoted_object']['pixel_rule'] = pixelRule
            elif 'pixel_rule' in self.adSetTemplate['promoted_object'].keys() and not isinstance(
                    adSetTemplate['promoted_object']['pixel_rule'], str):
                self.adSetTemplate['promoted_object']['pixel_rule'] = adSetTemplate['promoted_object']['pixel_rule']

    def _appendAdSetMobileTargeting(self, adSetTemplate):
        pass

    def _buildAdSetCore(self, adSetTemplate, isUsingCampaignBudgetOptimization=False):
        if AdSet.Field.tune_for_category in adSetTemplate.keys():
            self.adSetTemplate[AdSet.Field.tune_for_category] = adSetTemplate[AdSet.Field.tune_for_category]
        else:
            self.adSetTemplate[AdSet.Field.tune_for_category] = AdSet.TuneForCategory.none
        self.adSetTemplate[AdSet.Field.name] = adSetTemplate['name']
        self.adSetTemplate[AdSet.Field.campaign_id] = None
        self.adSetTemplate[AdSet.Field.effective_status] = AdSet.EffectiveStatus.paused
        self.adSetTemplate[AdSet.Field.status] = AdSet.Status.paused
        self.adSetTemplate[AdSet.Field.start_time] = adSetTemplate['budget_start_time']
        if 'budget_end_time' in adSetTemplate.keys():
            self.adSetTemplate[AdSet.Field.end_time] = adSetTemplate['budget_end_time']
        self.adSetTemplate[AdSet.Field.bid_strategy] = self._convertBidStrategy(adSetTemplate['budget_bid_cap_type'])
        self.adSetTemplate[AdSet.Field.optimization_goal] = adSetTemplate['budget_objective_optimization_goal_type']
        self.adSetTemplate[AdSet.Field.billing_event] = adSetTemplate['budget_billing_event']
        self.adSetTemplate[AdSet.Field.pacing_type] = self._convertPacingType(adSetTemplate['budget_delivery_type'])

        self._appendAdSetSchedule(adSetTemplate)

        if isUsingCampaignBudgetOptimization:
            self._appendAdSetMinMaxBudget(adSetTemplate)
        else:
            self._appendAdSetBudget(adSetTemplate)
            self._appendAdSetBudgetSpendCap(adSetTemplate)

        self._appendAdSetBidAmount(adSetTemplate)
        self._appendAdSetPromotedObject(adSetTemplate)

    def _buildAdSetName(self, templateName, age, placement, interest, gender, language, addGender=False):
        name = templateName + ' - ' + str(age['age_min']) + "-" + str(age['age_max'])

        if placement and placement['name']:
            name += ' - ' + placement['name']

        if interest and interest['name']:
            name += ' - ' + interest['name']

        if addGender:
            if gender and gender['genders'][0] == 0:
                name += ' - ' + 'Undefined'
            elif gender and gender['genders'][0] == 1:
                name += ' - ' + 'Male'
            elif gender and gender['genders'][0] == 2:
                name += ' - ' + 'Female'

        if language and language['name']:
            name += ' - ' + language['name']

        return name

    def _getAdSetBudgets(self, adsetName, budgetDetails, adsetBudgetDefault=None):
        for budget_detail in budgetDetails:
            if budget_detail['adset_name'] == adsetName:
                return int(budget_detail['budget'] * 100)

        return int(adsetBudgetDefault * 100)

    def _getAdSetMinMaxBudgets(self, adsetName, budgetDetails):
        minMaxBudgets = [None, None]
        for budget_detail in budgetDetails:
            if budget_detail['adset_name'] == adsetName:
                if 'min_budget' in budget_detail.keys():
                    minMaxBudgets[0] = int(budget_detail['min_budget'] * 100)
                if 'max_budget' in budget_detail.keys():
                    minMaxBudgets[1] = int(budget_detail['max_budget'] * 100)

                return minMaxBudgets

        return minMaxBudgets

    def _splitAdSetAge(self, ageMin, ageMax, ageRangeSplit):
        ageGroups = []
        for minAge in range(ageMin, ageMax, ageRangeSplit):
            maxAge = minAge + ageRangeSplit
            if maxAge > self._maximumFacebookAge:
                maxAge = self._maximumFacebookAge
            entry = {
                'age_min': minAge,
                'age_max': maxAge
            }
            ageGroups.append(entry)

        if ageGroups[-1]['age_max'] > ageMax:
            ageGroups[-1]['age_max'] = ageMax

        return ageGroups

    def _splitAdSetDevices(self, adSetTemplate):
        devicePlatforms = []
        for device in adSetTemplate['targeting']['device_platforms']:
            devicePlatforms.append([device])

        return devicePlatforms

    def _splitAdSetLocations(self, adSetTemplate):
        locations = []
        for location in adSetTemplate['targeting']['geo_locations']['countries']:
            locations.append([location])
        return locations

    @staticmethod
    def _CreateGenderGroups(splitByGender=False, adSetTemplate=None):
        if splitByGender:
            genderGroups = [{'genders': [1]},
                            {'genders': [2]}]
        else:
            genderGroups = [{'genders': adSetTemplate['targeting']['genders']}]
        return genderGroups

    @staticmethod
    def _CreatePlacementGroups(campaignStructurePlacementGroups, adSetTemplate):
        if not campaignStructurePlacementGroups:
            placementGroups = [{
                "name": "",
                "value": {
                    "publisher_platforms": adSetTemplate['targeting']['publisher_platforms'],
                    "facebook_positions": adSetTemplate['targeting']['facebook_positions'],
                    "instagram_positions": adSetTemplate['targeting']['instagram_positions'],
                    "messenger_positions": adSetTemplate['targeting']['messenger_positions'],
                    "audience_network_positions": adSetTemplate['targeting']['audience_network_positions']
                }
            }]
        else:
            placementGroups = campaignStructurePlacementGroups
        return placementGroups

    @staticmethod
    def _CreateLanguageGroups(campaignStructureLanguageGroups, adSetTemplate):
        if not campaignStructureLanguageGroups:
            languageGroups = [{
                "name": "",
                "value": {
                    "locales": adSetTemplate['targeting']['locales']
                }
            }]
        else:
            languageGroups = campaignStructureLanguageGroups
        return languageGroups

    @staticmethod
    def _CreateInterestGroups(campaignStructureInterestGroups, adSetTemplate):
        if not campaignStructureInterestGroups:
            if len(adSetTemplate['targeting']['flexible_spec']):
                interestGroups = [{
                    "name": "",
                    "value": {
                        "flexible_spec": adSetTemplate['targeting']['flexible_spec'][0]
                    }}]
            else:
                interestGroups = [{
                    "name": "",
                    "value": {
                        "flexible_spec": None
                    }
                }]
        else:
            interestGroups = campaignStructureInterestGroups
        return interestGroups

    def _CreateLocationGroups(self, splitByLocation, adSetTemplate):
        if splitByLocation:
            locationGroups = self._splitAdSetLocations(adSetTemplate)
        elif 'geo_locations' in adSetTemplate['targeting'] and 'countries' in adSetTemplate['targeting'][
            'geo_locations']:
            locationGroups = [adSetTemplate['targeting']['geo_locations']['countries']]
        else:
            raise ValueError('Failed to create location groups. Please try again without spliting by country.')
        return locationGroups

    def _CreateDeviceGroups(self, splitByDevice, adSetTemplate):
        if splitByDevice:
            deviceGroups = self._splitAdSetDevices(adSetTemplate)
        else:
            deviceGroups = [adSetTemplate['targeting']['device_platforms']]
        return deviceGroups

    def _CreateAgeGroups(self, splitByAgeRange, adSetTemplate, ageRangeSplit):
        if splitByAgeRange:
            ageGroups = self._splitAdSetAge(adSetTemplate['targeting']['age_min'],
                                            adSetTemplate['targeting']['age_max'], ageRangeSplit)
        else:
            ageGroups = [{
                "age_min": adSetTemplate['targeting']['age_min'],
                "age_max": adSetTemplate['targeting']['age_max']
            }]
        return ageGroups

    def buildAdSetsFull(self, campaignStructure, adSetTemplate, adSetBudgetTemplate,
                        isUsingCampaignBudgetOptimization=False):
        self._buildAdSetCore(adSetTemplate, isUsingCampaignBudgetOptimization)

        # Split by device
        deviceGroups = self._CreateDeviceGroups(campaignStructure['split_by_device'], adSetTemplate)

        # Split by location
        locationGroups = self._CreateLocationGroups(campaignStructure['split_by_location'], adSetTemplate)

        # Split by age range
        ageGroups = self._CreateAgeGroups(campaignStructure['split_by_age_range'], adSetTemplate,
                                          campaignStructure['age_range_split'])

        # Split by gender 
        genderGroups = self._CreateGenderGroups(campaignStructure['split_by_gender'], adSetTemplate)

        # Split by placement 
        placementGroups = self._CreatePlacementGroups(campaignStructure['placement_groups'], adSetTemplate)

        # Split by language 
        languageGroups = self._CreateLanguageGroups(campaignStructure['language_groups'], adSetTemplate)

        # Split by interest 
        interestGroups = self._CreateInterestGroups(campaignStructure['interest_groups'], adSetTemplate)

        # Build all adsets 
        for deviceGroup in deviceGroups:
            for locationGroup in locationGroups:
                for ageGroup in ageGroups:
                    for genderGroup in genderGroups:
                        for placementGroup in placementGroups:
                            for languageGroup in languageGroups:
                                for interestGroup in interestGroups:
                                    self._buildAdSetCore(adSetTemplate, isUsingCampaignBudgetOptimization)

                                    # Get template targeting
                                    targeting = adSetTemplate['targeting']

                                    # Remove unused field
                                    targeting.pop('inMemoryTargetingData', None)

                                    #  Change device
                                    targeting['device_platforms'] = deviceGroup

                                    # Change locations
                                    targeting['geo_locations']['countries'] = locationGroup

                                    # Change age
                                    targeting['age_min'] = ageGroup['age_min']
                                    targeting['age_max'] = ageGroup['age_max']

                                    # Change gender
                                    targeting['genders'] = genderGroup['genders']

                                    # Change placements
                                    for key, value in placementGroup['value'].items():
                                        targeting[key] = value

                                    # Change language
                                    targeting['locales'] = languageGroup['value']['locales']

                                    # Change interests
                                    if interestGroup['value']['flexible_spec']:
                                        targeting['flexible_spec'][0] = interestGroup['value']['flexible_spec']

                                    # Create adset name
                                    self.adSetTemplate['name'] = self._buildAdSetName(adSetTemplate['name'], ageGroup,
                                                                                      placementGroup, interestGroup,
                                                                                      genderGroup, languageGroup,
                                                                                      campaignStructure[
                                                                                          'split_by_gender'])

                                    # Search for adset budget and update the corresponding field in adset
                                    if isUsingCampaignBudgetOptimization:
                                        # change default budget to user input for cases when campaign budget optimization is ON
                                        if adSetTemplate['budget_allocate_type'] == AdSetBudgetAllocationType.daily and \
                                                adSetBudgetTemplate['budget_details']:
                                            budgets = self._getAdSetMinMaxBudgets(self.adSetTemplate['name'],
                                                                                  adSetBudgetTemplate[
                                                                                      'budget_details'])
                                            self.adSetTemplate[AdSet.Field.daily_min_spend_target] = budgets[0]
                                            self.adSetTemplate[AdSet.Field.daily_spend_cap] = budgets[1]
                                        elif adSetTemplate[
                                            'budget_allocate_type'] == AdSetBudgetAllocationType.lifetime and \
                                                adSetBudgetTemplate[
                                                    'budget_details']:
                                            budgets = self._getAdSetMinMaxBudgets(self.adSetTemplate['name'],
                                                                                  adSetBudgetTemplate[
                                                                                      'budget_details'])
                                            self.adSetTemplate[AdSet.Field.lifetime_min_spend_target] = budgets[0]
                                            self.adSetTemplate[AdSet.Field.lifetime_spend_cap] = budgets[1]
                                    else:
                                        # change default budget to user input for cases when campaign budget optimization is OFF
                                        if adSetTemplate['budget_allocate_type'] == AdSetBudgetAllocationType.daily and \
                                                adSetBudgetTemplate['budget_details']:
                                            self.adSetTemplate[AdSet.Field.daily_budget] = self._getAdSetBudgets(
                                                self.adSetTemplate['name'],
                                                adSetBudgetTemplate['budget_details'],
                                                adSetTemplate['budget_amount'])
                                        elif adSetTemplate[
                                            'budget_allocate_type'] == AdSetBudgetAllocationType.lifetime and \
                                                adSetBudgetTemplate[
                                                    'budget_details']:
                                            self.adSetTemplate[AdSet.Field.lifetime_budget] = self._getAdSetBudgets(
                                                self.adSetTemplate['name'],
                                                adSetBudgetTemplate['budget_details'],
                                                adSetTemplate['budget_amount'])

                                    # Add adset to collection
                                    self.adSetTemplate['targeting'] = targeting

                                    # Change 'targeting_optimization' to None from 'none'
                                    if self.adSetTemplate['targeting']['targeting_optimization'] == 'none':
                                        self.adSetTemplate['targeting']['targeting_optimization'] = None

                                    self.adSets.append(deepcopy(self.adSetTemplate))
