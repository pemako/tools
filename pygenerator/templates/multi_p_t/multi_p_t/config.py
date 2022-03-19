import datetime

from dynaconf import Dynaconf
from loguru import logger

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.yaml", ".secrets.yaml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.


logger.remove()
logger.add(
    settings.log.path.format(datetime.date.today()),
    level="INFO",
    enqueue=True,
    catch=True,
    rotation=settings.log.rotation,
    retention=settings.log.retention,
    compression=settings.log.compression,
)

log = logger
