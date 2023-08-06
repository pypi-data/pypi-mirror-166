import sys
import types

from . import MutableMapping, Awaitable, Callable, Dict, Iterable, Optional, Tuple, Type, Union, Any

if sys.version_info >= (3, 8):
    from . import Literal, Protocol, TypedDict
else:
    from typing_extensions import Literal, Protocol, TypedDict

__all__ = [
    "Message",
    "Scope",
    "Receive",
    "Send",
    "ASGIVersions",
    "HTTPScope",
    "WebSocketScope",
    "LifespanScope",
    "WWWScope",
    "Scope",
    "HTTPRequestEvent",
    "HTTPResponseStartEvent",
    "HTTPResponseBodyEvent",
    "HTTPServerPushEvent",
    "HTTPDisconnectEvent",
    "WebSocketConnectEvent",
    "WebSocketAcceptEvent",
    "WebSocketReceiveEvent",
    "WebSocketSendEvent",
    "WebSocketResponseStartEvent",
    "WebSocketResponseBodyEvent",
    "WebSocketDisconnectEvent",
    "WebSocketCloseEvent",
    "LifespanStartupEvent",
    "LifespanShutdownEvent",
    "LifespanStartupCompleteEvent",
    "LifespanStartupFailedEvent",
    "LifespanShutdownCompleteEvent",
    "LifespanShutdownFailedEvent",
    "LifespanReceiveMessage",
    "LifespanSendMessage",
    "ASGIReceiveEvent",
    "ASGISendEvent",
    "ASGIReceiveCallable",
    "ASGISendCallable",
    "ASGI2Protocol",
    "Environ",
    "ExcInfo",
    "StartResponse",
    "WSGIApplication",
    "ASGI2Application",
    "ASGI3Application",
    "ASGIApplication",
]

Message = MutableMapping[str, Any]

Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]


class ASGIVersions(TypedDict):
    spec_version: str
    version: Union[Literal["2.0"], Literal["3.0"]]


class HTTPScope(TypedDict):
    type: Literal["http"]
    asgi: ASGIVersions
    http_version: str
    method: str
    scheme: str
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[Tuple[bytes, bytes]]
    client: Optional[Tuple[str, int]]
    server: Optional[Tuple[str, Optional[int]]]
    extensions: Optional[Dict[str, Dict[object, object]]]


class WebSocketScope(TypedDict):
    type: Literal["websocket"]
    asgi: ASGIVersions
    http_version: str
    scheme: str
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[Tuple[bytes, bytes]]
    client: Optional[Tuple[str, int]]
    server: Optional[Tuple[str, Optional[int]]]
    subprotocols: Iterable[str]
    extensions: Optional[Dict[str, Dict[object, object]]]


class LifespanScope(TypedDict):
    type: Literal["lifespan"]
    asgi: ASGIVersions


WWWScope = Union[HTTPScope, WebSocketScope]
Scope = Union[HTTPScope, WebSocketScope, LifespanScope]


class HTTPRequestEvent(TypedDict):
    type: Literal["http.request"]
    body: bytes
    more_body: bool


class HTTPResponseStartEvent(TypedDict):
    type: Literal["http.response.start"]
    status: int
    headers: Iterable[Tuple[bytes, bytes]]


class HTTPResponseBodyEvent(TypedDict):
    type: Literal["http.response.body"]
    body: bytes
    more_body: bool


class HTTPServerPushEvent(TypedDict):
    type: Literal["http.response.push"]
    path: str
    headers: Iterable[Tuple[bytes, bytes]]


class HTTPDisconnectEvent(TypedDict):
    type: Literal["http.disconnect"]


class WebSocketConnectEvent(TypedDict):
    type: Literal["websocket.connect"]


class WebSocketAcceptEvent(TypedDict):
    type: Literal["websocket.accept"]
    subprotocol: Optional[str]
    headers: Iterable[Tuple[bytes, bytes]]


class WebSocketReceiveEvent(TypedDict):
    type: Literal["websocket.receive"]
    bytes: Optional[bytes]
    text: Optional[str]


class WebSocketSendEvent(TypedDict):
    type: Literal["websocket.send"]
    bytes: Optional[bytes]
    text: Optional[str]


class WebSocketResponseStartEvent(TypedDict):
    type: Literal["websocket.http.response.start"]
    status: int
    headers: Iterable[Tuple[bytes, bytes]]


class WebSocketResponseBodyEvent(TypedDict):
    type: Literal["websocket.http.response.body"]
    body: bytes
    more_body: bool


class WebSocketDisconnectEvent(TypedDict):
    type: Literal["websocket.disconnect"]
    code: int


class WebSocketCloseEvent(TypedDict):
    type: Literal["websocket.close"]
    code: int
    reason: Optional[str]


class LifespanStartupEvent(TypedDict):
    type: Literal["lifespan.startup"]


class LifespanShutdownEvent(TypedDict):
    type: Literal["lifespan.shutdown"]


class LifespanStartupCompleteEvent(TypedDict):
    type: Literal["lifespan.startup.complete"]


class LifespanStartupFailedEvent(TypedDict):
    type: Literal["lifespan.startup.failed"]
    message: str


class LifespanShutdownCompleteEvent(TypedDict):
    type: Literal["lifespan.shutdown.complete"]


class LifespanShutdownFailedEvent(TypedDict):
    type: Literal["lifespan.shutdown.failed"]
    message: str


LifespanReceiveMessage = Union[LifespanStartupEvent, LifespanShutdownEvent]
LifespanSendMessage = Union[
    LifespanStartupFailedEvent,
    LifespanShutdownFailedEvent,
    LifespanStartupCompleteEvent,
    LifespanShutdownCompleteEvent,
]

ASGIReceiveEvent = Union[
    HTTPRequestEvent,
    HTTPDisconnectEvent,
    WebSocketConnectEvent,
    WebSocketReceiveEvent,
    WebSocketDisconnectEvent,
    LifespanStartupEvent,
    LifespanShutdownEvent,
]

ASGISendEvent = Union[
    HTTPResponseStartEvent,
    HTTPResponseBodyEvent,
    HTTPServerPushEvent,
    HTTPDisconnectEvent,
    WebSocketAcceptEvent,
    WebSocketSendEvent,
    WebSocketResponseStartEvent,
    WebSocketResponseBodyEvent,
    WebSocketCloseEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupFailedEvent,
    LifespanShutdownCompleteEvent,
    LifespanShutdownFailedEvent,
]

ASGIReceiveCallable = Callable[[], Awaitable[ASGIReceiveEvent]]
ASGISendCallable = Callable[[ASGISendEvent], Awaitable[None]]


class ASGI2Protocol(Protocol):
    def __init__(self, scope: Scope) -> None:
        ...

    async def __call__(
            self, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        ...


Environ = MutableMapping[str, Any]
ExcInfo = Tuple[
    Type[BaseException], BaseException, Optional[types.TracebackType]
]
StartResponse = Callable[
    [str, Iterable[Tuple[str, str]], Optional[ExcInfo]],
    None
]
WSGIApplication = Callable[
    [Environ, StartResponse],
    Union[Iterable[bytes], BaseException]
]
ASGI2Application = Type[ASGI2Protocol]
ASGI3Application = Callable[
    [
        Scope,
        ASGIReceiveCallable,
        ASGISendCallable,
    ],
    Awaitable[None],
]
ASGIApplication = Union[ASGI2Application, ASGI3Application]
