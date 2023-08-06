import asyncio
import base64
import hashlib
import hmac
from typing import Any, Dict

import nautilus_trader
import orjson
from aiohttp import ClientConnectorError
from aiohttp import ClientResponse
from aiohttp import ClientResponseError
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import Logger

# from nautilus_trader.network.http import HttpClient
from tenacity import retry
from tenacity.retry import retry_if_exception
from tenacity.stop import stop_after_delay

from nacre.adapters.utils import after_log
from nacre.adapters.zb.http.error import ZbClientError
from nacre.adapters.zb.http.error import ZbOperationError
from nacre.adapters.zb.http.error import ZbServerError
from nacre.adapters.zb.http.error import ZbSpotOperationError
from nacre.network.http import HttpClient


def retry_if_connect_error(exception):
    if isinstance(exception, ZbOperationError):
        if exception.status in [10023, 10026, 10027, 10028, 10029, 12027]:
            return True
        return False
    elif isinstance(exception, ZbSpotOperationError):
        if exception.status in [1002, 3007]:
            return True
        return False

    return isinstance(exception, (ClientConnectorError, ZbClientError))


NAUTILUS_VERSION = nautilus_trader.__version__


class ZbHttpClient(HttpClient):
    """
    Provides a `Zb` asynchronous HTTP client.
    """

    BASE_URL = "https://fapi.zb.com"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        key=None,
        secret=None,
        base_url=None,
        timeout=None,
        show_limit_usage=False,
        proxy=None,
    ):
        super().__init__(
            loop=loop,
            logger=logger,
        )
        self._clock = clock
        self._key = key
        self._hashed_secret = hashlib.sha1(  # noqa: S303, S324
            (secret or "").encode("utf-8")
        ).hexdigest()
        self._base_url = base_url or self.BASE_URL
        self._show_limit_usage = show_limit_usage
        self._proxies = None
        self._headers: Dict[str, str] = {
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "nautilus-trader/" + NAUTILUS_VERSION,
            "ZB-APIKEY": key,
            "ZB-LAN": "cn",
        }
        self._timeout = timeout
        self._proxy = proxy

        # TODO(cs): Implement limit usage

    @property
    def api_key(self) -> str:
        return self._key

    @property
    def hashed_secret(self) -> str:
        return self._hashed_secret

    @property
    def headers(self):
        return self._headers

    async def query(self, url_path, payload: Dict[str, str] = None) -> Any:
        return await self.send_request("GET", url_path, payload=payload)

    async def limit_request(
        self,
        http_method: str,
        url_path: str,
        payload: Dict[str, Any] = None,
    ) -> Any:
        """
        Limit request is for those endpoints requiring an API key in the header.
        """
        return await self.send_request(http_method, url_path, payload=payload)

    async def sign_request(
        self,
        http_method: str,
        url_path: str,
        payload: Dict[str, str] = None,
    ) -> Any:
        if payload is None:
            payload = {}
        timestamp = self._clock.utc_now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        query_string = self._prepare_params(payload)
        signature = self._get_sign(timestamp, http_method, url_path, query_string)
        extra_headers = {}
        extra_headers["ZB-SIGN"] = signature
        extra_headers["ZB-TIMESTAMP"] = timestamp
        return await self.send_request(http_method, url_path, payload, extra_headers)

    @retry(
        reraise=True,
        retry=retry_if_exception(retry_if_connect_error),
        after=after_log(),
        stop=stop_after_delay(15),
    )
    async def send_request(  # noqa: C901
        self,
        http_method: str,
        url_path: str,
        payload: Dict[str, str] = None,
        extra_headers: Dict[str, str] = None,
    ) -> Any:
        # TODO(cs): Uncomment for development
        # print(f"{http_method} {url_path} {payload}")
        self._log.debug(f"{http_method} {url_path} {payload}")
        if payload is None:
            payload = {}

        headers = self._headers
        if extra_headers:
            headers = dict(extra_headers, **headers)
        try:
            kwargs = dict(
                method=http_method,
                url=self._base_url + url_path,
                headers=headers,
                params=self._prepare_params(payload),
            )
            if self._proxy:
                kwargs["proxy"] = self._proxy
            if self._timeout:
                kwargs["timeout"] = self._timeout

            if http_method == "POST":
                kwargs["json"] = payload
                kwargs.pop("params")

            resp: ClientResponse = await self.request(**kwargs)
        except ClientResponseError as ex:
            await self._handle_exception(ex)
            return

        try:
            resp_data = orjson.loads(resp.data)
            self._raise_if_operation_code_error(resp_data)
            return resp_data
        except orjson.JSONDecodeError:
            self._log.error(f"Could not decode data to JSON: {resp.data}.")

    def _prepare_params(self, params: Dict[str, str]) -> str:
        keys = sorted(params)
        return "&".join(
            [k + "=" + str(params[k]) for k in keys if params[k] is not None and params[k] != ""]
        )

    def _get_sign(self, timestamp, http_method, url_path, data) -> str:
        whole_data = timestamp + http_method + url_path + data
        m = hmac.new(self._hashed_secret.encode(), whole_data.encode(), hashlib.sha256)
        return str(base64.b64encode(m.digest()), "utf-8")

    async def _handle_exception(self, error: ClientResponseError) -> None:
        if error.status < 400:
            return
        elif 400 <= error.status < 500:
            raise ZbClientError(
                status=error.status,
                message=error.message,
                headers=error.headers,
            )
        else:
            raise ZbServerError(
                status=error.status,
                message=error.message,
                headers=error.headers,
            )

    def _raise_if_operation_code_error(self, resp: Dict):
        code = resp.get("code")
        if code is None:
            return
        elif code == 10000:
            return
        else:
            raise ZbOperationError(status=code, message=resp.get("desc"))
