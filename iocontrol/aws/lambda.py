from mangum import Mangum

from iocontrol.api.main import app

handler = Mangum(app)
