from enum import Enum

from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata


class ActionBreakdown(Enum):
    DEVICE = 'device'

    DEFAULT = 'none'


ACTION_BREAKDOWN_TO_FIELD = {
    ActionBreakdown.DEVICE: GoogleFieldsMetadata.device,
    ActionBreakdown.DEFAULT: None
}
