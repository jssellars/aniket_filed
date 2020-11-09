from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Breakdowns.BreakdownsEnumeration import BreakdownsEnumeration

action_breakdown_id = Autoincrement(100)


class ActionBreakdowns:
    device = BreakdownsEnumeration(action_breakdown_id.increment(), FieldsMetadata.action_device.name, "Action device")
    canvas_component = BreakdownsEnumeration(action_breakdown_id.increment(), FieldsMetadata.action_canvas_component_name.name,
                                             "Canvas name")
    carouse_card_id = BreakdownsEnumeration(action_breakdown_id.increment(), FieldsMetadata.action_carousel_card_id.name,
                                            "Carousel card")
    carouse_card_name = BreakdownsEnumeration(action_breakdown_id.increment(), FieldsMetadata.action_carousel_card_name.name,
                                              "Carousel card name")
    action_destination = BreakdownsEnumeration(action_breakdown_id.increment(),
                                               FieldsMetadata.action_destination.name, "Action destination")
    action_reaction = BreakdownsEnumeration(action_breakdown_id.increment(), FieldsMetadata.action_reaction.name,
                                            "Action reaction")
    target = BreakdownsEnumeration(action_breakdown_id.increment(), FieldsMetadata.action_target_id.name, "Action target")
    video_sound = BreakdownsEnumeration(action_breakdown_id.increment(), FieldsMetadata.action_video_sound.name,
                                        "Action video sound")
    video_type = BreakdownsEnumeration(action_breakdown_id.increment(), FieldsMetadata.action_video_type.name,
                                       "Action video type")
