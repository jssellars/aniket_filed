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
        self.ad_set_template = {}
        self.ad_sets = []

    @staticmethod
    def _convert_bid_strategy(bid_strategy):
        if bid_strategy == 'Cost Cap':
            return 'LOWEST_COST_WITHOUT_CAP'
        elif bid_strategy == 'Target Cost':
            return 'TARGET_COST'
        elif bid_strategy == 'Bid Cap':
            return 'LOWEST_COST_WITH_BID_CAP'
        else:
            raise ValueError('Unknown bid strategy value: %s' % bid_strategy)

    @staticmethod
    def _convert_pacing_type(pacing_type):
        if pacing_type == 'Standard':
            return ['standard']
        elif pacing_type == 'Accelerated':
            return ['no_pacing']
        else:
            raise ValueError('Unknown pacing type value: %s' % pacing_type)

    def _append_ad_set_budget(self, ad_set_template):
        if ad_set_template['budget_allocate_type'] == AdSetBudgetAllocationType.daily:
            self.ad_set_template[AdSet.Field.daily_budget] = int(ad_set_template['budget_amount'] * 100)
        elif ad_set_template['budget_allocate_type'] == AdSetBudgetAllocationType.lifetime:
            self.ad_set_template[AdSet.Field.lifetime_budget] = int(ad_set_template['budget_amount'] * 100)

    def _append_ad_set_min_max_budget(self, ad_set_template):
        if ad_set_template['budget_allocate_type'] == AdSetBudgetAllocationType.daily:
            self.ad_set_template[AdSet.Field.daily_min_spend_target] = int(ad_set_template['budget_min_amount'] * 100)
            self.ad_set_template[AdSet.Field.daily_spend_cap] = int(ad_set_template['budget_max_amount'] * 100)
        elif ad_set_template['budget_allocate_type'] == AdSetBudgetAllocationType.lifetime:
            self.ad_set_template[AdSet.Field.lifetime_min_spend_target] = int(ad_set_template['budget_min_amount'] * 100)
            self.ad_set_template[AdSet.Field.lifetime_spend_cap] = int(ad_set_template['budget_max_amount'] * 100)

    def _append_ad_set_schedule(self, ad_set_template):
        if ad_set_template['schedule_type'] == 'Run my campaign on a schedule':
            if ad_set_template['schedule_entries']:
                adset_schedule = []
                for schedule_entry in ad_set_template['schedule_entries']:
                    adset_schedule.append({
                        'start_minute': schedule_entry['start_minute'],
                        'end_minute': schedule_entry['end_minute'],
                        'days': schedule_entry['days'],
                        'timezone_type': ad_set_template['schedule_time_zone_type']
                    })
                self.ad_set_template[AdSet.Field.adset_schedule] = adset_schedule
                # TODO: Potentially add this to campaign_template if adset schedule is on (campaign budget optimization)
                self.ad_set_template[AdSet.Field.pacing_type] = ['day_parting']
            else:
                raise ValueError('Missing schedule entries from adset template.')
        elif ad_set_template['schedule_type'] != 'Run my campaign all the time':
            raise ValueError('Unknown schedule type: %s' % ad_set_template['schedule_type'])

    def _append_ad_set_budget_spend_cap(self, ad_set_template):
        if hasattr(ad_set_template, 'spend_cap') and ad_set_template['budget_allocate_type'] == 'Daily':
            self.ad_set_template[AdSet.Field.daily_spend_cap] = ad_set_template['spend_cap']
        elif hasattr(ad_set_template, 'spend_cap') and ad_set_template['budget_allocate_type'] == 'Lifetime':
            self.ad_set_template[AdSet.Field.lifetime_spend_cap] = ad_set_template['spend_cap']

    def _append_ad_set_bid_amount(self, ad_set_template):
        if 'budget_bid_cap_amount' in ad_set_template.keys() and ad_set_template['budget_bid_cap_amount']:
            self.ad_set_template[AdSet.Field.bid_amount] = int(ad_set_template['budget_bid_cap_amount'] * 100)

    def _append_ad_set_promoted_object(self, ad_set_template):
        if 'promoted_object' in ad_set_template.keys():
            self.ad_set_template[AdSet.Field.promoted_object] = ad_set_template['promoted_object']
        if 'promoted_object' in self.ad_set_template.keys():
            if 'pixel_rule' in self.ad_set_template['promoted_object'].keys() and \
                    isinstance(ad_set_template['promoted_object']['pixel_rule'], str):
                pixel_rule = json.loads(ad_set_template['promoted_object']['pixel_rule']).replace('\\', '')
                self.ad_set_template['promoted_object']['pixel_rule'] = pixel_rule
            elif 'pixel_rule' in self.ad_set_template['promoted_object'].keys() and \
                    not isinstance(ad_set_template['promoted_object']['pixel_rule'], str):
                self.ad_set_template['promoted_object']['pixel_rule'] = ad_set_template['promoted_object']['pixel_rule']

        if 'pixel_rule' in self.ad_set_template['promoted_object'].keys() and \
                not self.ad_set_template['promoted_object']['pixel_rule']:
            self.ad_set_template['promoted_object'].pop('pixel_rule')

    def _append_ad_set_mobile_targeting(self, ad_set_template):
        pass

    def _build_ad_set_core(self, ad_set_template, is_using_campaign_budget_optimization=False):
        if AdSet.Field.tune_for_category in ad_set_template.keys():
            self.ad_set_template[AdSet.Field.tune_for_category] = ad_set_template[AdSet.Field.tune_for_category]
        else:
            self.ad_set_template[AdSet.Field.tune_for_category] = AdSet.TuneForCategory.none
        self.ad_set_template[AdSet.Field.name] = ad_set_template['name']
        self.ad_set_template[AdSet.Field.campaign_id] = None
        self.ad_set_template[AdSet.Field.effective_status] = AdSet.EffectiveStatus.paused
        self.ad_set_template[AdSet.Field.status] = AdSet.Status.paused
        self.ad_set_template[AdSet.Field.start_time] = ad_set_template['budget_start_time']
        if 'budget_end_time' in ad_set_template.keys():
            self.ad_set_template[AdSet.Field.end_time] = ad_set_template['budget_end_time']
        self.ad_set_template[AdSet.Field.bid_strategy] = self._convert_bid_strategy(ad_set_template['budget_bid_cap_type'])
        self.ad_set_template[AdSet.Field.optimization_goal] = ad_set_template['budget_objective_optimization_goal_type']
        self.ad_set_template[AdSet.Field.billing_event] = ad_set_template['budget_billing_event']
        self.ad_set_template[AdSet.Field.pacing_type] = self._convert_pacing_type(ad_set_template['budget_delivery_type'])

        self._append_ad_set_schedule(ad_set_template)

        if is_using_campaign_budget_optimization:
            self._append_ad_set_min_max_budget(ad_set_template)
        else:
            self._append_ad_set_budget(ad_set_template)
            self._append_ad_set_budget_spend_cap(ad_set_template)

        self._append_ad_set_bid_amount(ad_set_template)
        self._append_ad_set_promoted_object(ad_set_template)

    def _build_ad_set_name(self, template_name, age, placement, interest, gender, language, add_gender=False):
        name = template_name + ' - ' + str(age['age_min']) + "-" + str(age['age_max'])

        if placement and placement['name']:
            name += ' - ' + placement['name']

        if interest and interest['name']:
            name += ' - ' + interest['name']

        if add_gender:
            if gender and gender['genders'][0] == 0:
                name += ' - ' + 'Undefined'
            elif gender and gender['genders'][0] == 1:
                name += ' - ' + 'Male'
            elif gender and gender['genders'][0] == 2:
                name += ' - ' + 'Female'

        if language and language['name']:
            name += ' - ' + language['name']

        return name

    def _get_ad_set_budgets(self, adset_name, budget_details, adset_budget_default=None):
        for budget_detail in budget_details:
            if budget_detail['adset_name'] == adset_name:
                return int(budget_detail['budget'] * 100)

        return int(adset_budget_default * 100)

    def _get_ad_set_min_max_budgets(self, adset_name, budget_details):
        min_max_budgets = [None, None]
        for budget_detail in budget_details:
            if budget_detail['adset_name'] == adset_name:
                if 'min_budget' in budget_detail.keys():
                    min_max_budgets[0] = int(budget_detail['min_budget'] * 100)
                if 'max_budget' in budget_detail.keys():
                    min_max_budgets[1] = int(budget_detail['max_budget'] * 100)

                return min_max_budgets

        return min_max_budgets

    def _split_ad_set_age(self, age_min, age_max, age_range_split):
        age_groups = []
        for min_age in range(age_min, age_max, age_range_split):
            max_age = min_age + age_range_split
            if max_age > self._maximumFacebookAge:
                max_age = self._maximumFacebookAge
            entry = {
                'age_min': min_age,
                'age_max': max_age
            }
            age_groups.append(entry)

        if age_groups[-1]['age_max'] > age_max:
            age_groups[-1]['age_max'] = age_max

        return age_groups

    def _split_ad_set_devices(self, ad_set_template):
        device_platforms = []
        for device in ad_set_template['targeting']['device_platforms']:
            device_platforms.append([device])

        return device_platforms

    def _split_ad_set_locations(self, ad_set_template):
        locations = []
        for location in ad_set_template['targeting']['geo_locations']['countries']:
            locations.append([location])
        return locations

    @staticmethod
    def _create_gender_groups(split_by_gender=False, ad_set_template=None):
        if split_by_gender:
            gender_groups = [{'genders': [1]},
                             {'genders': [2]}]
        else:
            gender_groups = [{'genders': ad_set_template['targeting']['genders']}]
        return gender_groups

    @staticmethod
    def _create_placement_groups(campaign_structure_placement_groups, ad_set_template):
        if not campaign_structure_placement_groups:
            placement_groups = [{
                "name": "",
                "value": {
                    "publisher_platforms": ad_set_template['targeting']['publisher_platforms'],
                    "facebook_positions": ad_set_template['targeting']['facebook_positions'],
                    "instagram_positions": ad_set_template['targeting']['instagram_positions'],
                    "messenger_positions": ad_set_template['targeting']['messenger_positions'],
                    "audience_network_positions": ad_set_template['targeting']['audience_network_positions']
                }
            }]
        else:
            placement_groups = campaign_structure_placement_groups
        return placement_groups

    @staticmethod
    def _create_language_groups(campaign_structure_language_groups, ad_set_template):
        if not campaign_structure_language_groups:
            language_groups = [{
                "name": "",
                "value": {
                    "locales": ad_set_template['targeting']['locales']
                }
            }]
        else:
            language_groups = campaign_structure_language_groups
        return language_groups

    @staticmethod
    def _create_interest_groups(campaign_structure_interest_groups, ad_set_template):
        if not campaign_structure_interest_groups:
            if len(ad_set_template['targeting']['flexible_spec']):
                interest_groups = [{
                    "name": "",
                    "value": {
                        "flexible_spec": ad_set_template['targeting']['flexible_spec'][0]
                    }}]
            else:
                interest_groups = [{
                    "name": "",
                    "value": {
                        "flexible_spec": None
                    }
                }]
        else:
            interest_groups = campaign_structure_interest_groups
        return interest_groups

    def _create_location_groups(self, split_by_location, ad_set_template):
        if split_by_location:
            location_groups = self._split_ad_set_locations(ad_set_template)
        elif 'geo_locations' in ad_set_template['targeting'] and 'countries' in ad_set_template['targeting']['geo_locations']:
            location_groups = [ad_set_template['targeting']['geo_locations']['countries']]
        else:
            raise ValueError('Failed to create location groups. Please try again without splitting by country.')
        return location_groups

    def _create_device_groups(self, split_by_device, ad_set_template):
        if split_by_device:
            device_groups = self._split_ad_set_devices(ad_set_template)
        else:
            device_groups = [ad_set_template['targeting']['device_platforms']]
        return device_groups

    def _create_age_groups(self, split_by_age_range, ad_set_template, age_range_split):
        if split_by_age_range:
            age_groups = self._split_ad_set_age(ad_set_template['targeting']['age_min'],
                                                ad_set_template['targeting']['age_max'], age_range_split)
        else:
            age_groups = [{
                "age_min": ad_set_template['targeting']['age_min'],
                "age_max": ad_set_template['targeting']['age_max']
            }]
        return age_groups

    def build_ad_sets_full(self, campaign_structure, ad_set_template, ad_set_budget_template,
                           is_using_campaign_budget_optimization=False):
        self._build_ad_set_core(ad_set_template, is_using_campaign_budget_optimization)

        # Split by device
        device_groups = self._create_device_groups(campaign_structure['split_by_device'], ad_set_template)

        # Split by location
        location_groups = self._create_location_groups(campaign_structure['split_by_location'], ad_set_template)

        # Split by age range
        age_groups = self._create_age_groups(campaign_structure['split_by_age_range'], ad_set_template,
                                             campaign_structure['age_range_split'])

        # Split by gender 
        gender_groups = self._create_gender_groups(campaign_structure['split_by_gender'], ad_set_template)

        # Split by placement 
        placement_groups = self._create_placement_groups(campaign_structure['placement_groups'], ad_set_template)

        # Split by language 
        language_groups = self._create_language_groups(campaign_structure['language_groups'], ad_set_template)

        # Split by interest 
        interest_groups = self._create_interest_groups(campaign_structure['interest_groups'], ad_set_template)

        # Build all adsets 
        for device_group in device_groups:
            for location_group in location_groups:
                for age_group in age_groups:
                    for gender_group in gender_groups:
                        for placement_group in placement_groups:
                            for language_group in language_groups:
                                for interest_group in interest_groups:
                                    self._build_ad_set_core(ad_set_template, is_using_campaign_budget_optimization)

                                    # Get template targeting
                                    targeting = ad_set_template['targeting']

                                    # Remove unused field
                                    targeting.pop('in_memory_targeting_data', None)

                                    # Change device
                                    targeting['device_platforms'] = device_group

                                    # Change locations
                                    targeting['geo_locations']['countries'] = location_group

                                    # Change age
                                    targeting['age_min'] = age_group['age_min']
                                    targeting['age_max'] = age_group['age_max']

                                    # Change gender
                                    targeting['genders'] = gender_group['genders']

                                    # Change placements
                                    for key, value in placement_group['value'].items():
                                        targeting[key] = value

                                    # Change language
                                    targeting['locales'] = language_group['value']['locales']

                                    # Change interests
                                    if interest_group['value']['flexible_spec']:
                                        targeting['flexible_spec'][0] = interest_group['value']['flexible_spec']

                                    # Create adset name
                                    self.ad_set_template['name'] = self._build_ad_set_name(ad_set_template['name'], age_group,
                                                                                           placement_group, interest_group,
                                                                                           gender_group, language_group,
                                                                                           campaign_structure[
                                                                                               'split_by_gender'])

                                    # Search for adset budget and update the corresponding field in adset
                                    if is_using_campaign_budget_optimization:
                                        # change default budget to user input for cases when campaign budget optimization is ON
                                        if ad_set_template['budget_allocate_type'] == AdSetBudgetAllocationType.daily and \
                                                ad_set_budget_template['budget_details']:
                                            budgets = self._get_ad_set_min_max_budgets(self.ad_set_template['name'],
                                                                                       ad_set_budget_template[
                                                                                           'budget_details'])
                                            self.ad_set_template[AdSet.Field.daily_min_spend_target] = budgets[0]
                                            self.ad_set_template[AdSet.Field.daily_spend_cap] = budgets[1]
                                        elif ad_set_template['budget_allocate_type'] == AdSetBudgetAllocationType.lifetime and \
                                                ad_set_budget_template['budget_details']:
                                            budgets = self._get_ad_set_min_max_budgets(self.ad_set_template['name'],
                                                                                       ad_set_budget_template['budget_details'])
                                            self.ad_set_template[AdSet.Field.lifetime_min_spend_target] = budgets[0]
                                            self.ad_set_template[AdSet.Field.lifetime_spend_cap] = budgets[1]
                                    else:
                                        # change default budget to user input for cases when campaign budget optimization is OFF
                                        if ad_set_template['budget_allocate_type'] == AdSetBudgetAllocationType.daily and \
                                                ad_set_budget_template['budget_details']:
                                            self.ad_set_template[AdSet.Field.daily_budget] = self._get_ad_set_budgets(
                                                self.ad_set_template['name'],
                                                ad_set_budget_template['budget_details'],
                                                ad_set_template['budget_amount'])
                                        elif ad_set_template['budget_allocate_type'] == AdSetBudgetAllocationType.lifetime and \
                                                ad_set_budget_template[
                                                    'budget_details']:
                                            self.ad_set_template[AdSet.Field.lifetime_budget] = self._get_ad_set_budgets(
                                                self.ad_set_template['name'],
                                                ad_set_budget_template['budget_details'],
                                                ad_set_template['budget_amount'])

                                    # Add adset to collection
                                    self.ad_set_template['targeting'] = targeting

                                    # Change 'targeting_optimization' to None from 'none'
                                    if self.ad_set_template['targeting']['targeting_optimization'] == 'none':
                                        self.ad_set_template['targeting']['targeting_optimization'] = None

                                    self.ad_sets.append(deepcopy(self.ad_set_template))
