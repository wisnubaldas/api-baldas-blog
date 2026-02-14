"""Service reusable untuk memproses request DataTables server-side."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Callable

from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select


@dataclass
class DataTablesOrder:
    column: str
    direction: str


@dataclass
class DataTablesParams:
    draw: int
    start: int
    length: int
    search_value: str
    orders: list[DataTablesOrder]


class DataTablesService:
    """Service generik untuk query pagination/sort/search ala DataTables."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def parse_params(self, query_params: Mapping[str, str]) -> DataTablesParams:
        draw = self._to_int(query_params.get("draw"), default=1, min_value=0)
        start = self._to_int(query_params.get("start"), default=0, min_value=0)
        length = self._to_int(query_params.get("length"), default=10, min_value=1)
        search_value = (query_params.get("search[value]") or "").strip()

        orders: list[DataTablesOrder] = []
        index = 0
        while True:
            column_index_key = f"order[{index}][column]"
            if column_index_key not in query_params:
                break

            column_index = self._to_int(
                query_params.get(column_index_key), default=-1, min_value=-1
            )
            if column_index >= 0:
                column_name = (
                    query_params.get(f"columns[{column_index}][name]")
                    or query_params.get(f"columns[{column_index}][data]")
                    or ""
                ).strip()
                direction = (
                    "desc"
                    if (query_params.get(f"order[{index}][dir]") or "").lower() == "desc"
                    else "asc"
                )
                if column_name:
                    orders.append(DataTablesOrder(column=column_name, direction=direction))
            index += 1

        return DataTablesParams(
            draw=draw, start=start, length=length, search_value=search_value, orders=orders
        )

    def build_response(
        self,
        *,
        base_query: Select[Any],
        query_params: Mapping[str, str],
        searchable_columns: dict[str, Any],
        orderable_columns: dict[str, Any],
        row_mapper: Callable[[Any], dict[str, Any]],
        default_order_column: str | None = None,
        default_order_direction: str = "asc",
    ) -> dict[str, Any]:
        params = self.parse_params(query_params)

        total_records = self._count_rows(base_query)

        filtered_query = base_query
        if params.search_value and searchable_columns:
            keyword = f"%{params.search_value.lower()}%"
            filters = [
                func.lower(cast(column, String)).like(keyword)
                for column in searchable_columns.values()
            ]
            filtered_query = filtered_query.where(or_(*filters))

        filtered_records = self._count_rows(filtered_query)

        ordered_query = self._apply_ordering(
            filtered_query,
            params.orders,
            orderable_columns,
            default_order_column=default_order_column,
            default_order_direction=default_order_direction,
        )

        paged_query = ordered_query.offset(params.start).limit(params.length)
        rows = list(self.db.execute(paged_query).scalars().all())

        return {
            "draw": params.draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": [row_mapper(row) for row in rows],
        }

    def _count_rows(self, query: Select[Any]) -> int:
        sub_query = query.order_by(None).subquery()
        count_query = select(func.count()).select_from(sub_query)
        count_value = self.db.execute(count_query).scalar()
        return int(count_value or 0)

    def _apply_ordering(
        self,
        query: Select[Any],
        orders: list[DataTablesOrder],
        orderable_columns: dict[str, Any],
        *,
        default_order_column: str | None,
        default_order_direction: str,
    ) -> Select[Any]:
        ordered_query = query
        applied = False
        for order in orders:
            column = orderable_columns.get(order.column)
            if column is None:
                continue
            applied = True
            ordered_query = ordered_query.order_by(
                column.desc() if order.direction == "desc" else column.asc()
            )

        if applied:
            return ordered_query

        if default_order_column and default_order_column in orderable_columns:
            default_column = orderable_columns[default_order_column]
            return ordered_query.order_by(
                default_column.desc()
                if default_order_direction.lower() == "desc"
                else default_column.asc()
            )

        return ordered_query

    @staticmethod
    def _to_int(
        value: str | None, *, default: int, min_value: int | None = None
    ) -> int:
        try:
            parsed = int(value) if value is not None else default
        except (TypeError, ValueError):
            parsed = default

        if min_value is not None:
            return max(parsed, min_value)
        return parsed
