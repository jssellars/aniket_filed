from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import (
    duplicate_fb_adset,
    update_turing_structure,
)
from FacebookDexter.Infrastructure.DexterApplyActions.RecommendationApplyActions import (
    ApplyParameters,
    RecommendationAction,
)


@dataclass
class DuplicateAdset(RecommendationAction):
    APPLY_TOOLTIP: ClassVar[str] = "Selecting apply will create a new duplicate for the selected adset"

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:

        action_details = {"details": {FieldsMetadata.status.name: "PAUSED"}}

        return action_details

    def process_action(self, recommendation: Dict, headers: str):

        update_turing_structure(self.config, recommendation, headers)
        duplicate_fb_adset(recommendation, self.fixtures)
