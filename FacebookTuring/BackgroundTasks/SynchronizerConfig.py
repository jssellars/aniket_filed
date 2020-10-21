import typing
from dataclasses import dataclass
from datetime import datetime

from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import \
    TuringMongoRepository


@dataclass(frozen=True)
class SynchronizerConfigStatic:
    levels: typing.List
    breakdowns: typing.List
    action_breakdowns: typing.List
    requested_fields: typing.List


@dataclass(frozen=True)
class SynchronizerConfigRuntime:
    insights_repository: TuringMongoRepository
    structure_repository: TuringMongoRepository
    account_journal_repository: TuringAdAccountJournalRepository
    business_owner_id: typing.AnyStr
    account_id: typing.AnyStr
    date_start: datetime
