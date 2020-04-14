from Core.Tools.Misc.Autoincrement import Autoincrement
from FacebookTuring.Api.Catalogs.Breakdowns.BreakdownsEnumeration import BreakdownsEnumeration
from FacebookTuring.Infrastructure.Models.FacebookFieldsMetadata import FieldsMetadata

id = Autoincrement(0)


class ActionBreakdowns:
    device = BreakdownsEnumeration(id.increment(), FieldsMetadata.device.name, "Device")
    canvas_component = BreakdownsEnumeration(id.increment(), FieldsMetadata.canvas_component.name, "Canvas name")
    carouse_card_id = BreakdownsEnumeration(id.increment(), FieldsMetadata.carousel_card_id.name, "Carousel card")
    carouse_card_name = BreakdownsEnumeration(id.increment(), FieldsMetadata.carousel_card_name.name, "Carousel card name")
    destination = BreakdownsEnumeration(id.increment(), FieldsMetadata.destination.name, "Destination")
    reaction = BreakdownsEnumeration(id.increment(), FieldsMetadata.reaction.name, "Reaction")
    target = BreakdownsEnumeration(id.increment(), FieldsMetadata.target.name, "Target")
    video_sound = BreakdownsEnumeration(id.increment(), FieldsMetadata.video_sound.name, "Video sound")
    video_type = BreakdownsEnumeration(id.increment(), FieldsMetadata.video_type.name, "Video type")
