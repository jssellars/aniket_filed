from enum import Enum

from GoogleTuring.Infrastructure.Models.GoogleFieldMetadata import GoogleFieldMetadata


class ActionBreakdown(Enum):
    DEVICE = 'device'

    DEFAULT = 'none'


ACTION_BREAKDOWN_TO_FIELD = {
    ActionBreakdown.DEVICE: GoogleFieldMetadata.device,
    ActionBreakdown.DEFAULT: None
}
