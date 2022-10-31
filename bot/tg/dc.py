from dataclasses import dataclass
from typing import List
from marshmallow import EXCLUDE


@dataclass
class UpdateObj:
	pass


@dataclass
class GetUpdatesResponse:
	ok: bool
	result: List[UpdateObj]

	class Meta:
		unknown = EXCLUDE


@dataclass
class Message:
	text: str


@dataclass
class SendMessageResponse:
	ok: bool
	result: Message

	class Meta:
		unknown = EXCLUDE
