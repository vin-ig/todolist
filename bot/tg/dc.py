from dataclasses import dataclass
from typing import List
from marshmallow import EXCLUDE
from datetime import datetime


@dataclass
class MessageFrom:
	id: int
	is_bot: bool
	first_name: str
	username: str
	language_code: str


@dataclass
class Chat:
	id: int
	first_name: str
	username: str
	type: str


@dataclass
class Message:
	message_id: int
	message_from: MessageFrom
	chat: Chat
	date: datetime.timestamp
	text: str


@dataclass
class SendMessageResponse:
	ok: bool
	result: Message

	class Meta:
		unknown = EXCLUDE


@dataclass
class UpdateObj:
	update_id: int
	message: Message


@dataclass
class GetUpdatesResponse:
	ok: bool
	result: List[UpdateObj]

	class Meta:
		unknown = EXCLUDE
