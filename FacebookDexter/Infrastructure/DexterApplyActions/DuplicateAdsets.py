from dataclasses import asdict, dataclass
from typing import Dict, Optional

from facebook_business.adobjects.adset import AdSet

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import LevelToGraphAPIStructure
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.DexterApplyActions.ApplyActionsUtils import _update_turing_structure
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

        structure = LevelToGraphAPIStructure.get(
            recommendation[RecommendationField.LEVEL.value], recommendation[RecommendationField.STRUCTURE_ID.value]
        )

        new_structure = structure.create_copy(
            params={
                "campaign_id": recommendation.get(RecommendationField.CAMPAIGN_ID.value),
                "deep_copy": True,
                "status_option": AdSet.StatusOption.inherited_from_source,
                "rename_options": {"rename_suffix": " - Duplicate"},
            }
        )

        _update_turing_structure(self.config, recommendation, headers)

        new_created_structures_event = DexterNewCreatedStructureEvent(
            recommendation.get(RecommendationField.BUSINESS_OWNER_ID.value),
            [
                NewCreatedStructureKeys(
                    recommendation.get(RecommendationField.LEVEL.value),
                    recommendation.get(RecommendationField.ACCOUNT_ID.value),
                    new_structure[FacebookMiscFields.copied_adset_id],
                )
            ],
        )
        mapper = DexterCreatedEventMapping(target=DexterNewCreatedStructureEvent)
        response = mapper.load(asdict(new_created_structures_event))
        RecommendationAction.publish_response(response, self.fixtures)
