import traceback
from typing import Callable
from urllib.parse import parse_qs
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from iocontrol import logging
from iocontrol import meta
from iocontrol.api import auth
from iocontrol.api import config
from iocontrol.api import debug
from iocontrol.api import requests
from iocontrol.api import static
from iocontrol.api import system
from iocontrol.api.debug import trace
from iocontrol.config import config as app_config
from iocontrol.config.deploy import DeployPlatform
from iocontrol.errors import AppException
from iocontrol.errors import ErrorMessage


#: the FastAPI application
app = FastAPI(
    version=str(meta.this().version),
    title=meta.this().name,
    docs_url="/openapi",
)

# Set up CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config().api.cors.allow_origins,
    allow_credentials=app_config().api.cors.allow_credentials,
    allow_methods=app_config().api.cors.allow_methods,
    allow_headers=app_config().api.cors.allow_headers,
)

# Set up gzip middleware if necessary.
if app_config().deploy.platform == DeployPlatform.LAMBDA:
    app.add_middleware(GZipMiddleware, minimum_size=1000)


# If we're debugging the API...
if app_config().api.debug:
    # ...add the debug middleware.
    @app.middleware("http")
    async def debug_middleware(request: Request, call_next: Callable):
        """
        Debug incoming requests.

        :param request: the request
        :param call_next: the next function in the middleware chain
        """
        tracer = trace(request)
        method = request.method
        url_info = urlparse(str(request.url))
        body = await requests.body(request=request, reset=True)
        logging.debug(
            f"DEBUG {method} {url_info.path} (TRACER {tracer})",
            tracer=tracer,
            url=str(request.url),
            method=request.method,
            headers=dict(request.headers),
            cookies=dict(request.cookies),
            path_params=request.path_params,
            query_params=dict(request.query_params),
            body_params=dict(parse_qs(body)),
            body=body,
            url_info={
                attr: getattr(url_info, attr)
                for attr in {
                    "scheme",
                    "netloc",
                    "path",
                    "params",
                    "query",
                    "fragment",
                    "username",
                    "password",
                    "hostname",
                    "port",
                }
            },
            client={"host": request.client.host, "port": request.client.port},
            tags=debug.tags(),
        )
        return await call_next(request)


# Add the routers.
app.include_router(auth.router, prefix="/api/auth")
app.include_router(config.router, prefix="/api/config")
# Add the root router and keep a reference.
app.include_router(system.router, prefix="")
# Configure static files.
static.configure(app)


@app.exception_handler(Exception)
async def on_exception(_: Request, ex: Exception):
    """
    Handle uncaught exceptions.

    :param _: the request
    :param ex: the exception
    """
    # Whatever we got, we want a structured exception.
    ex_ = (
        ex if isinstance(ex, AppException) else AppException.from_exception(ex)
    )

    # Make note.
    logging.exception(
        ex_.event,
        type=ex.__class__.__name__,
        detail=str(ex),
        code=ex_.status_code,
        headers=ex_.headers,
    )

    # Prepare the response content.
    content = ErrorMessage(
        status_code=ex_.status_code,
        event=ex_.event,
        tags=ex_.tags,
        traceback=(
            tuple(traceback.format_exc().split("\n"))
            if app_config().api.debug
            else None
        ),
    ).dict(by_alias=True, exclude_none=True)

    # Prepare the content of the response.
    response = {
        "status_code": ex_.status_code,
        "content": content,
        "headers": ex_.headers,
    }
    # That's that.
    return JSONResponse(**response)


@app.on_event("startup")
async def startup():
    """Perform FastAPI application startup."""
    # Configure logging.
    logging.configure()


@app.on_event("shutdown")
async def shutdown():
    """Perform FastAPI application shutdown."""
    # TODO: Clean up.
    pass
