from sqlalchemy.orm import Session

from app.apps.pockets.models import Pocket, PocketTransaction
from app.apps.pockets.schemas import PocketCreate


class PocketRepository:
    """Data access layer for protected pocket entities."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, pocket_id: int) -> Pocket | None:
        return self.db.query(Pocket).filter(Pocket.id == pocket_id).first()

    def list_by_user(self, user_id: int, semester_id: int | None = None) -> list[Pocket]:
        query = self.db.query(Pocket).filter(Pocket.user_id == user_id)
        if semester_id is not None:
            query = query.filter(Pocket.semester_id == semester_id)
        return query.order_by(Pocket.created_at.desc()).all()

    def create(self, user_id: int, semester_id: int, pocket_in: PocketCreate) -> Pocket:
        pocket = Pocket(
            user_id=user_id,
            semester_id=semester_id,
            name=pocket_in.name,
            type=pocket_in.type.value,
            current_balance=pocket_in.initial_balance,
        )
        self.db.add(pocket)
        self.db.commit()
        self.db.refresh(pocket)
        return pocket

    def update_balance(self, pocket: Pocket, amount: float) -> Pocket:
        pocket.current_balance = amount
        self.db.commit()
        self.db.refresh(pocket)
        return pocket

    def lock(self, pocket: Pocket) -> Pocket:
        pocket.locked = True
        self.db.commit()
        self.db.refresh(pocket)
        return pocket

    def create_transaction(self, pocket_id: int, user_id: int, amount: float, transaction_type: str, note: str | None) -> PocketTransaction:
        transaction = PocketTransaction(
            pocket_id=pocket_id,
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            note=note,
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
