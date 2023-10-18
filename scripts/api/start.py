import uvicorn

from iocontrol.config import config

api = config().api
uvicorn.run(
    app=api.app,
    host=str(api.bind),
    port=api.port,
    log_level=config().logging.level.lower(),
    reload=False,
)
