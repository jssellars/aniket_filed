from dataclasses import asdict, dataclass
from typing import Dict, Optional

from facebook_business.adobjects.adset import AdSet

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import LevelToGraphAPIStructure
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import (
    duplicate_fb_adset,
    update_turing_structure,
)
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyParameters,
    RecommendationAction,
)
from FacebookDexter.Infrastructure.IntegrationEvents.DexterNewCreatedStructuresHandler import (
    DexterCreatedEventMapping,
    DexterNewCreatedStructureEvent,
    NewCreatedStructureKeys,
)


@dataclass
class DuplicateAdset(RecommendationAction):
    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:

        action_details = {"details": {FieldsMetadata.status.name: "PAUSED"}}

        return action_details

    def process_action(self, recommendation: Dict, headers: str):

        update_turing_structure(self.config, recommendation, headers)
        duplicate_fb_adset(recommendation, self.fixtures)
