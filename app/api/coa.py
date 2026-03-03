"""Endpoint read-only Chart of Accounts (COA)."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.coa import COAAccount, COAAccountResponse, COAAccountTreeNode

router = APIRouter(prefix="/coa", tags=["COA"])


def _build_tree(accounts: list[COAAccount]) -> list[COAAccountTreeNode]:
    """Build tree response from flat account rows."""
    node_map: dict[int, COAAccountTreeNode] = {}
    roots: list[COAAccountTreeNode] = []

    for account in accounts:
        node_map[account.id] = COAAccountTreeNode.from_orm(account)

    for account in accounts:
        node = node_map[account.id]
        parent_id = account.parent_id
        if parent_id is not None and parent_id in node_map:
            node_map[parent_id].children.append(node)
        else:
            roots.append(node)

    def sort_recursive(nodes: list[COAAccountTreeNode]) -> None:
        nodes.sort(key=lambda item: item.code)
        for child in nodes:
            sort_recursive(child.children)

    sort_recursive(roots)
    return roots


@router.get("/", response_model=list[COAAccountResponse])
def list_coa_accounts(
    include_inactive: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> list[COAAccountResponse]:
    """Get flat COA account list."""
    query = select(COAAccount)
    if not include_inactive:
        query = query.where(COAAccount.is_active.is_(True))
    query = query.order_by(COAAccount.code.asc())

    accounts = db.scalars(query).all()
    return [COAAccountResponse.from_orm(account) for account in accounts]


@router.get("/tree", response_model=list[COAAccountTreeNode])
def list_coa_tree(
    include_inactive: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> list[COAAccountTreeNode]:
    """Get hierarchical COA tree for explorer UI."""
    query = select(COAAccount)
    if not include_inactive:
        query = query.where(COAAccount.is_active.is_(True))
    query = query.order_by(COAAccount.level.asc(), COAAccount.code.asc())

    accounts = db.scalars(query).all()
    return _build_tree(accounts)
