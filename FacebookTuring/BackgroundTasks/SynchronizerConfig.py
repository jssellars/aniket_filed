import typing
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import (
    TuringAdAccountJournalRepository,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


@dataclass
class SynchronizerConfigStatic:
    levels: List
    account_journal_repository: Optional[TuringAdAccountJournalRepository] = None


@dataclass(frozen=True)
class SynchronizerConfigRuntime:
    business_owner_id: str
    account_id: str
    date_start: datetime
