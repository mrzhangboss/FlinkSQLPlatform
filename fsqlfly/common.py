# -*- coding:utf-8 -*-
import re
import functools
import urllib
import traceback
import attr
from urllib.parse import urlencode
from re import _pattern_type
from typing import Any, Optional, NamedTuple, Callable, Awaitable, Union, List, Type
from tornado.web import RequestHandler, HTTPError
from logzero import logger

SUPPORT_TABLE_TYPE = {'sink', 'source', 'both', 'view', 'temporal-table'}
SUPPORT_MANAGER = {'hive', 'db', 'kafka', 'hbase', 'elasticsearch', 'file'}
CONNECTOR_TYPE = {'canal', 'system'}


class CodeMsg(NamedTuple):
    code: int
    msg: str


class RespCode:
    Success = CodeMsg(200, 'Success')
    ServerError = CodeMsg(500, 'Web Server Error')
    NeedLogin = CodeMsg(503, 'You Need Login')
    LoginFail = CodeMsg(501, 'Wrong Password or Token')
    APIFail = CodeMsg(502, 'Invalid API Request')
    InvalidHttpMethod = CodeMsg(405, 'Invalid HTTP method.')


@attr.s
class DBRes:
    data: Any = attr.ib(default=None)
    code: int = attr.ib(default=200)
    msg: Optional[str] = attr.ib(default=None)
    success: bool = attr.ib()

    @success.default
    def get_success(self):
        return self.code == 200

    @classmethod
    def login_error(cls, msg: str = RespCode.LoginFail.code):
        return DBRes(code=RespCode.LoginFail.code, msg=msg)

    @classmethod
    def api_error(cls, msg: str = RespCode.APIFail.msg):
        return DBRes(code=RespCode.APIFail.code, msg=msg)

    @classmethod
    def not_found(cls, msg: str = "Can't found Object"):
        return DBRes(code=RespCode.APIFail.code, msg=msg)

    @classmethod
    def resource_locked(cls, msg: str = "Resource Locked"):
        return DBRes(code=RespCode.APIFail.code, msg=msg)

    @classmethod
    def sever_error(cls, msg: str = RespCode.ServerError.msg):
        return DBRes(code=RespCode.ServerError.code, msg=msg)


def safe_authenticated(
        method: Callable[..., Optional[Awaitable[None]]]
) -> Callable[..., Union[Optional[Awaitable[None]], DBRes]]:
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """

    @functools.wraps(method)
    def wrapper(  # type: ignore
            self: RequestHandler, *args, **kwargs
    ) -> Union[Optional[Awaitable[None]], DBRes]:
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urllib.parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        assert self.request.uri is not None
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return None
            raise HTTPError(403)
        try:
            return method(self, *args, **kwargs)
        except Exception as error:
            from fsqlfly import settings
            if settings.FSQLFLY_DEBUG:
                raise error
            err = traceback.format_exc()
            logger.error(err)
            return DBRes.sever_error(msg=f'meet {err}')

    return wrapper


class NameFilter:
    @classmethod
    def get_pattern(cls, s: str) -> List[Type[_pattern_type]]:
        s = s.replace('，', ',')
        patterns = [s.strip()] if ',' not in s else s.split(',')
        res = [re.compile(pattern=x + '$') for x in patterns]
        return res

    def __init__(self, include: str = '', exclude: str = ''):
        self.includes = self.get_pattern(include) if include else [re.compile(r'.*')]
        self.excludes = self.get_pattern(exclude) if exclude else []

    def __contains__(self, item: str) -> bool:
        if any(map(lambda x: x.match(item) is not None, self.includes)):
            if self.excludes and any(map(lambda x: x.match(item), self.excludes)):
                return False
            return True
        return False


@attr.s
class SchemaField:
    name: str = attr.ib()
    type: str = attr.ib()
    comment: Optional[str] = attr.ib(default=None)
    nullable: Optional[bool] = attr.ib(default=True)
    autoincrement: Optional[bool] = attr.ib(default=None)


@attr.s
class SchemaContent:
    name: str = attr.ib()
    type: str = attr.ib()
    database: Optional[str] = attr.ib(default=None)
    comment: Optional[str] = attr.ib(default=None)
    primary_key: Optional[str] = attr.ib(default=None)
    fields: List[SchemaField] = attr.ib(factory=list)
    partitionable: bool = attr.ib(default=False)


@attr.s
class VersionConfig:
    exclude: Optional[str] = attr.ib(default=None)
    include: Optional[str] = attr.ib(default=None)
    update_mode: Optional[str] = attr.ib(default=None)
    query: Optional[str] = attr.ib(default=None)
    history_table: Optional[str] = attr.ib(default=None)
    primary_key: Optional[str] = attr.ib(default=None)
    time_attribute: Optional[str] = attr.ib(default=None)
    format: Optional[Any] = attr.ib(default=None)
    schema: list = attr.ib(factory=list)