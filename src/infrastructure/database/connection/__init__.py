from prisma import Prisma

class DatabaseConnection:
  _client: Prisma = None

  @classmethod
  def get_client(cls) -> Prisma:
    if cls._client is None:
      cls._client = Prisma()
    return cls._client

  @classmethod
  async def connect(cls):
    if cls._client is None:
      cls._client = Prisma()
    if not cls._client.is_connected():
      await cls._client.connect()

  @classmethod
  async def disconnect(cls):
    if cls._client and cls._client.is_connected():
      await cls._client.disconnect()
