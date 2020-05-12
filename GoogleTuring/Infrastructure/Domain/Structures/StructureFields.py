CAMPAIGN_STRUCTURE_FIELDS = ['AdServingOptimizationStatus',
                             'AdvertisingChannelSubType',
                             'AdvertisingChannelType',
                             'Amount',
                             'AppId',
                             'AppVendor',
                             'BaseCampaignId',
                             'BiddingStrategyGoalType',
                             'BiddingStrategyId',
                             'BiddingStrategyName',
                             'BiddingStrategyType',
                             'BudgetId',
                             'BudgetName',
                             'BudgetReferenceCount',
                             'BudgetStatus',
                             'CampaignGroupId',
                             'CampaignTrialType',
                             'DeliveryMethod',
                             'Eligible',
                             'EndDate',
                             'EnhancedCpcEnabled',
                             'FinalUrlSuffix',
                             'FrequencyCapMaxImpressions',
                             'Id',
                             'IsBudgetExplicitlyShared',
                             'Labels',
                             'Level',
                             'MaximizeConversionValueTargetRoas',
                             'Name',
                             'RejectionReasons',
                             'SelectiveOptimization',
                             'ServingStatus',
                             'Settings',
                             'StartDate',
                             'Status',
                             'TargetContentNetwork',
                             'TargetCpa',
                             'TargetCpaMaxCpcBidCeiling',
                             'TargetCpaMaxCpcBidFloor',
                             'TargetGoogleSearch',
                             'TargetPartnerSearchNetwork',
                             'TargetRoas',
                             'TargetRoasBidCeiling',
                             'TargetRoasBidFloor',
                             'TargetSearchNetwork',
                             'TargetSpendSpendTarget',
                             'TimeUnit',
                             'TrackingUrlTemplate',
                             'UrlCustomParameters',
                             'VanityPharmaDisplayUrlMode',
                             'VanityPharmaText',
                             'ViewableCpmEnabled']

AD_GROUP_STRUCTURE_FIELDS = [
    'AdGroupType',
    'AdRotationMode',
    'BaseAdGroupId',
    'BaseCampaignId',
    'BiddingStrategyId',
    'BiddingStrategyName',
    'BiddingStrategyType',
    'CampaignId',
    'CampaignName',
    'ContentBidCriterionTypeGroup',
    'CpcBid',
    'CpmBid',
    'EnhancedCpcEnabled',
    'Id',
    'Labels',
    'Name',
    'Settings',
    'Status',
    'TargetCpa',
    'TargetCpaBid',
    'TargetCpaBidSource',
    'TargetRoasOverride',
    'TrackingUrlTemplate',
    'UrlCustomParameters'
]

AD_STRUCTURE_FIELDS = [
    'Id',
    'Status',
    'AdGroupId',
    'PolicySummary',
    'Labels',
    'BaseCampaignId',
    'BaseAdGroupId',
    'AdStrengthInfo',
    'Url',
    'DisplayUrl',
    'CreativeFinalUrls',
    'CreativeFinalMobileUrls',
    'CreativeFinalAppUrls',
    'CreativeTrackingUrlTemplate',
    'CreativeFinalUrlSuffix',
    'CreativeUrlCustomParameters',
    'UrlData',
    'Automated',
    'AdType',
    'DevicePreference',
    'SystemManagedEntitySource',
    'Name',
    'Type',
    'Description1',
    'Description2',
    'ExpandedDynamicSearchCreativeDescription2',
    'Description',
    'HeadlinePart1',
    'HeadlinePart2',
    'ExpandedTextAdHeadlinePart3',
    'ExpandedTextAdDescription2',
    'Path1',
    'Path2',
    'GmailHeaderImage',
    'GmailMarketingImage',
    'MarketingImageHeadline',
    'MarketingImageDescription',
    'ProductImages',
    'ProductVideoList',
    'ImageCreativeName',
    'MultiAssetResponsiveDisplayAdMarketingImages',
    'MultiAssetResponsiveDisplayAdFormatSetting',
    'MultiAssetResponsiveDisplayAdDynamicSettingsPromoText',
    'MultiAssetResponsiveDisplayAdDynamicSettingsPricePrefix',
    'MultiAssetResponsiveDisplayAdCallToActionText',
    'MultiAssetResponsiveDisplayAdAllowFlexibleColor',
    'MultiAssetResponsiveDisplayAdAccentColor',
    'MultiAssetResponsiveDisplayAdMainColor',
    'MultiAssetResponsiveDisplayAdBusinessName',
    'MultiAssetResponsiveDisplayAdYouTubeVideos',
    'MultiAssetResponsiveDisplayAdDescriptions',
    'MultiAssetResponsiveDisplayAdLongHeadline',
    'MultiAssetResponsiveDisplayAdHeadlines',
    'MultiAssetResponsiveDisplayAdLandscapeLogoImages',
    'MultiAssetResponsiveDisplayAdLogoImages',
    'MultiAssetResponsiveDisplayAdSquareMarketingImages',
    'MarketingImage',
    'LogoImage',
    'SquareMarketingImage',
    'ShortHeadline',
    'LongHeadline',
    'BusinessName',
    'MainColor',
    'AccentColor',
    'AllowFlexibleColor',
    'CallToActionText',
    'FormatSetting',
    'ResponsiveSearchAdHeadlines',
    'ResponsiveSearchAdDescriptions',
    'ResponsiveSearchAdPath1',
    'ResponsiveSearchAdPath2',
    'RichMediaAdName',
    'RichMediaAdSnippet',
    'RichMediaAdImpressionBeaconUrl',
    'RichMediaAdDuration',
    'RichMediaAdCertifiedVendorFormatId',
    'RichMediaAdSourceUrl',
    'RichMediaAdType',
    'TemplateId',
    'TemplateAdUnionId',
    'TemplateAdName',
    'TemplateAdDuration',
    'TemplateOriginAdId',
    'Headline',
    'UniversalAppAdHeadlines',
    'UniversalAppAdDescriptions',
    'UniversalAppAdMandatoryAdText',
    'UniversalAppAdImages',
    'UniversalAppAdYouTubeVideos',
    'UniversalAppAdHtml5MediaBundles'
]

AD_GROUP_KEYWORDS_STRUCTURE_FIELDS = [
    'AdGroupId',
    'CriterionUse',
    'Id',
    'CriteriaType',
    'KeywordText',
    'KeywordMatchType',
    'Labels',
    'BaseCampaignId',
    'BaseAdGroupId',
    'Status',
    'SystemServingStatus',
    'ApprovalStatus',
    'DisapprovalReasons',
    'FirstPageCpc',
    'TopOfPageCpc',
    'FirstPositionCpc',
    'QualityScore',
    'BiddingStrategyId',
    'BiddingStrategyName',
    'BiddingStrategyType',
    'BiddingStrategySource',
    # 'BiddingSchemeType',
    # 'EnhancedCpcEnabled',
    'BidModifier',
    'FinalUrls',
    'FinalMobileUrls',
    'FinalAppUrls',
    'TrackingUrlTemplate',
    'FinalUrlSuffix',
    'UrlCustomParameters'
]

AD_GROUP_CRITERIA_FIELDS = [
    'AdGroupId',
    'CriterionUse',
    'Id',
    'CriteriaType',
    'KeywordText',
    'KeywordMatchType',
    'AgeRangeType',
    'AppPaymentModelType',
    'CustomAffinityId',
    'CustomIntentId',
    'GenderType',
    'IncomeRangeType',
    'MobileAppCategoryId',
    'AppId',
    'ParentType',
    'PlacementUrl',
    'ParentCriterionId',
    'CaseValue',
    'UserInterestId',
    'UserInterestParentId',
    'UserInterestName',
    'UserListId',
    'UserListName',
    'UserListMembershipStatus',
    'UserListEligibleForSearch',
    'UserListEligibleForDisplay',
    'VerticalId',
    'VerticalParentId',
    'Path',
    'Parameter',
    'CriteriaCoverage',
    'CriteriaSamples',
    'ChannelId',
    'ChannelName',
    'VideoId',
    'VideoName',

    'Labels',
    'BaseCampaignId',
    'BaseAdGroupId',
    'Status',
    'SystemServingStatus',
    'ApprovalStatus',
    'DisapprovalReasons',
    'FirstPageCpc',
    'TopOfPageCpc',
    'FirstPositionCpc',
    'QualityScore',
    'BiddingStrategyId',
    'BiddingStrategyName',
    'BiddingStrategyType',
    'BiddingStrategySource',

    'BidModifier',
    'FinalUrls',
    'FinalMobileUrls',
    'FinalAppUrls',
    'TrackingUrlTemplate',
    'FinalUrlSuffix',
    'UrlCustomParameters'
]