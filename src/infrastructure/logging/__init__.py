import logging

class AppLogger:
  _logger: logging.Logger = None

  @classmethod
  def setup(cls) -> None:
    logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
      datefmt='%Y-%m-%d %H:%M:%S',
    )

    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    cls._logger = logging.getLogger('WaterIntakeApp')
    cls._logger.info('Logging is configured.')

  @classmethod
  def info(cls, message: str) -> None:
    cls._logger.info(message)

  @classmethod
  def debug(cls, message: str) -> None:
    cls._logger.debug(message)

  @classmethod
  def warning(cls, message: str) -> None:
    cls._logger.warning(message)

  @classmethod
  def error(cls, message: str) -> None:
    cls._logger.error(message)

  @classmethod
  def critical(cls, message: str) -> None:
    cls._logger.critical(message)

  @classmethod
  def exception(cls, message: str) -> None:
    cls._logger.exception(message)
