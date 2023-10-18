import json
from json.decoder import JSONDecodeError
from logging import StreamHandler


class StructlogJsonStreamHandler(StreamHandler):
    """Emits logs as JSON objects."""

    def emit(self, record):
        """Handle a logging record."""
        try:
            self.format(record)
            # Structlog messages may come in as mappings.  If so, we'll pull
            # out the values and the events.
            try:
                data = {
                    k: v for k, v in json.loads(record.message).items() if v
                }
                message = data.get("event")
            except JSONDecodeError:
                data = {}
                message = record.message

            data_ = {
                "logger": record.name if record.name else None,
                "level": (
                    record.levelname.lower() if record.levelname else None
                ),
                "timestamp": record.asctime,
                "event": message,
                **data,
            }
            data = json.dumps(data_)
            self.stream.write(f"{data}\n")
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:  # noqa  We need to handle exotic unexpected cases.
            self.handleError(record)
