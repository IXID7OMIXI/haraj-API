from pydantic import BaseModel
from typing import List, Optional, Any

class CarInfo(BaseModel):
    gear: Optional[str] = None
    model: Optional[str] = None
    mileage: Optional[str] = None
    fuel: Optional[str] = None

class PriceInfo(BaseModel):
    formattedPrice: Optional[str] = None

class PostItem(BaseModel):
    id: int
    title: Optional[str] = None
    URL: Optional[str] = None
    city: Optional[str] = None
    geoCity: Optional[str] = None
    tags: List[str] = []
    bodyTEXT: Optional[str] = None # Description
    postDate: Optional[int] = None
    updateDate: Optional[int] = None
    carInfo: Optional[CarInfo] = None
    price: Optional[PriceInfo] = None

    @property
    def full_url(self) -> str:
        if self.URL:
            return "https://haraj.com.sa/" + self.URL.lstrip("/")
        return ""

class PageInfo(BaseModel):
    hasNextPage: bool

class PostsResponse(BaseModel):
    items: List[PostItem]
    pageInfo: PageInfo

class GraphQLData(BaseModel):
    posts: PostsResponse

class GraphQLResponse(BaseModel):
    data: Optional[GraphQLData] = None
    errors: Optional[List[Any]] = None
