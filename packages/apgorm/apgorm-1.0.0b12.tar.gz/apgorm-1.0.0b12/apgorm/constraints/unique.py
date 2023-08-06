# MIT License
#
# Copyright (c) 2021 TrigonDev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable

from apgorm.sql.sql import Block, join, raw

from .constraint import Constraint

if TYPE_CHECKING:  # pragma: no cover
    from apgorm.field import BaseField


class Unique(Constraint):
    __slots__: Iterable[str] = ("fields",)

    def __init__(
        self, *fields: BaseField[Any, Any, Any] | Block[Any] | str
    ) -> None:
        """Specify a unique constraint for a table.

        ```
        class User(Model):
            ...
            nickname = VarChar(32).field()
            nickname_unique = Unique(nickname)
            ...
        ```
        """

        self.fields = fields

    def _creation_sql(self) -> Block[Any]:
        fields = (
            raw(f)
            if isinstance(f, str)
            else f
            if isinstance(f, Block)
            else raw(f.name)
            for f in self.fields
        )
        return Block(
            raw("CONSTRAINT"),
            raw(self.name),
            raw("UNIQUE ("),
            join(raw(","), *fields),
            raw(")"),
            wrap=True,
        )
