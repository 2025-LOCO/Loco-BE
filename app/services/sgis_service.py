import httpx
from typing import List, Dict, Any
from app.core.config import settings


class SGISService:
    def __init__(self):
        self.base_url = "https://sgisapi.kostat.go.kr/OpenAPI3"
        self.consumer_key = settings.SGIS_CONSUMER_KEY
        self.consumer_secret = settings.SGIS_CONSUMER_SECRET
        self.access_token = None

    async def get_access_token(self) -> str:
        if self.access_token:
            return self.access_token

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/auth/authentication.json",
                params={
                    "consumer_key": self.consumer_key,
                    "consumer_secret": self.consumer_secret,
                }
            )
            data = response.json()
            self.access_token = data["result"]["accessToken"]
            return self.access_token

    async def get_regions_by_code(self, region_code: str) -> List[Dict[str, Any]]:
        token = await self.get_access_token()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/addr/stage.json",
                params={
                    "accessToken": token,
                    "cd": region_code,
                }
            )
            data = response.json()
            return data.get("result", [])


sgis_service = SGISService()