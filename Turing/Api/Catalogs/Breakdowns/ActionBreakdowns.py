from Core.Tools.Misc.Autoincrement import Autoincrement
from Turing.Api.Catalogs.Breakdowns.BreakdownsEnumeration import BreakdownsEnumeration
from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata

id = Autoincrement(0)


class ActionBreakdowns:
    device = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.device.name, "Device")
    canvas_component = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.canvas_component.name, "Canvas name")
    carouse_card_id = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.carousel_card_id.name, "Carousel card")
    carouse_card_name = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.carousel_card_name.name, "Carousel card name")
    destination = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.destination.name, "Destination")
    reaction = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.reaction.name, "Reaction")
    target = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.target.name, "Target")
    video_sound = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.video_sound.name, "Video sound")
    video_type = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.video_type.name, "Video type")
