"""
MIT License

Copyright (c) 2022 VincentRPS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing_extensions import NotRequired

    from ..enums import OverwriteType, TrackType


class Track(TypedDict):
    id: str
    guild_id: NotRequired[str]
    icon: NotRequired[str | None]
    name: str
    topic: str | None
    position: NotRequired[int]
    type: TrackType
    members: NotRequired[list[str]]
    nsfw: NotRequired[bool]
    last_message_id: NotRequired[str | None]
    parent_id: NotRequired[str | None]
    overwrites: NotRequired[list[Overwrite]]


class Overwrite(TypedDict):
    id: str
    type: OverwriteType
    allow: int
    deny: int


class Message(TypedDict):
    id: str
    author_id: str
    track_id: str
    timestamp: str
    edited_timestamp: str | None
    mention_everyone: bool
    pinned: bool
    type: int
