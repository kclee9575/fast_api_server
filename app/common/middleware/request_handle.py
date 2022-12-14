import time, json, traceback
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_429_TOO_MANY_REQUESTS,
)
from datetime import datetime
from app.common.logger import access_logger

class RequestHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/", "/token"]:
            result = await call_next(request)
            return result
        process_time = None
        start_time = time.time()
        response = None

        try:
            authorize = await self.authorize(request)

            if authorize == 200:
                response = await call_next(request)
                access_logger.info(
                    f"PATH : {request.url.path}, HEADERS : {dict(request.headers).get('authorization')}, CLIENT: {request.client.host}"
                )
            else:
                result = self._render_4xx_error(authorize, start_time)
                return result
            if response.status_code == 200:
                content = await self._parse_body(response)
                result = self._render_json(response, content, start_time)
            else:
                result = self._render_4xx_error(response.status_code, start_time)
        except Exception as e:
            error_message = traceback.format_exc()
            result = self._render_5xx_error(response, start_time, error_message)
            return result
        return result

    async def authorize(self, request):
        # 추가적 인증 필요할 경우 입력
        # auth 서버로부터 jwt 토큰 발급, 사용 시 decode/
        # 만료기간이 지난경우 사용불가/
        # 사용가능한 경우 decode code format에 맞춰 사용
        #if not request.headers.get('authorization'):
            #return 501 # unauthorization
        #token = request.headers.get('authorization').replace("Bearer " , "")
        # decode_data 로 필요에따라 사용
        #decode_data = auth_manager.decode_jwt(token)    
        return 200

    def _render_4xx_error(self, status_code, start_time):
        process_time = time.time() - start_time
        result = None
        if status_code == 404:
            result = JSONResponse(
                {
                    "result": None,
                    "processTime": process_time,
                    "message": "Not found",
                    "code": status_code,
                },
                status_code=HTTP_404_NOT_FOUND,
            )
        elif status_code == 400:
            result = JSONResponse(
                {
                    "result": None,
                    "processTime": process_time,
                    "message": "Bad Request",
                    "code": status_code,
                },
                status_code=HTTP_401_UNAUTHORIZED,
            )
        elif status_code == 401:
            result = JSONResponse(
                {
                    "result": None,
                    "processTime": process_time,
                    "message": "Unauthorized",
                    "code": status_code,
                },
                status_code=HTTP_401_UNAUTHORIZED,
            )
        elif status_code == 422:
            result = JSONResponse(
                {
                    "result": None,
                    "processTime": process_time,
                    "message": "Unprocessable Entity",
                    "code": status_code,
                },
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            )
        elif status_code == 429:
            result = JSONResponse(
                {
                    "result": None,
                    "processTime": process_time,
                    "message": "Too many requests",
                    "code": status_code,
                },
                status_code=HTTP_429_TOO_MANY_REQUESTS,
            )
        else:
            result = JSONResponse(
                {
                    "result": None,
                    "processTime": process_time,
                    "message": "",
                    "code": status_code,
                },
                status_code=status_code,
            )
        return result

    def _render_5xx_error(self, response, start_time, error_message):
        process_time = time.time() - start_time
        return JSONResponse(
            {
                "result": None,
                "processTime": process_time,
                "message": "Internal Server Error",
                "code": 500,
            },
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    async def _parse_body(self, response):
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        result = json.loads(body)
        return result

    def _render_json(self, response, content, start_time):
        process_time = time.time() - start_time
        result = {
            "result": content.get("result"),
            "message": content.get("message"),
            "code": content.get("code"),
            "processTime": process_time,
        }

        content = json.dumps(result)
        response.headers.update({"Content-Length": str(len(content))})
        return Response(
            content=content,
            status_code=result.get("code"),
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    def _render_unkown(self, content_type, start_time):
        process_time = time.time() - start_time
        content = {
            "message": f"unkown content type type: {content_type}",
            "code": 500,
            "processTime": process_time,
            "result": {},
        }
        return JSONResponse(content, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    def _render_file(self, response, content, start_time):
        process_time = time.time() - start_time
        return (
            FileResponse(
                path=content.get("result").get("path"),
                filename=content.get("result").get("filename"),
            ),
            process_time,
        )

    async def _get_log_data(self, request):
        try:

            body = b""
            async for chunk in request.stream():
                body += chunk
            result = json.loads(body)
            print(
                f" [date] {datetime.now()} / [host] {request.client.host} / [query_param] {request.query_params} /\n [body] {result}"
            )

        except Exception as e:
            pass
