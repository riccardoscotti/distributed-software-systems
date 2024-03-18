from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessage(_message.Message):
    __slots__ = ["time", "senderName", "body"]
    TIME_FIELD_NUMBER: _ClassVar[int]
    SENDERNAME_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    time: str
    senderName: str
    body: str
    def __init__(self, time: _Optional[str] = ..., senderName: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...

class Nothing(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
