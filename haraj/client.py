import requests
import json
from typing import List, Optional, Dict, Any
from haraj.utils import get_client_id
from haraj.models import GraphQLResponse, PostItem

API_URL = "https://graphql.haraj.com.sa/"
HEADERS = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Accept-Language": "en-US,en;q=0.9,ar-SA;q=0.8,ar;q=0.7",
    "Origin": "https://haraj.com.sa",
    "Referer": "https://haraj.com.sa/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "priority": "u=1, i"
}

CLIENT_ID = "DJK4SWlM-OQ12-L5J1-lKBx-ZJ4KaeELFAJkv3"

QUERY = """
query Search($id: [Int], $cities: [String], $search: String!, $city: String, $authorUsername: String, $page: Int, $limit: Int, $afterPostDate: Int, $afterUpdateDate: Int, $tag: String, $tags: [String], $carExtraInfo: CarExtraInfo, $near: String, $onlyWithImage: Boolean, $duringDate: String, $userLocation: GeoPoint, $notTag: String, $hideShowRooms: Boolean, $orderByPostId: Boolean) {
  search(
    id: $id
    search: $search
    city: $city
    cities: $cities
    authorUsername: $authorUsername
    page: $page
    limit: $limit
    afterPostDate: $afterPostDate
    afterUpdateDate: $afterUpdateDate
    tag: $tag
    tags: $tags
    CarExtraInfo: $carExtraInfo
    near: $near
    onlyWithImage: $onlyWithImage
    userLocation: $userLocation
    duringDate: $duringDate
    notTag: $notTag
    hideShowRooms: $hideShowRooms
    orderByPostId: $orderByPostId
  ) {
    items {
      ...PostFields
    }
    pageInfo {
      hasNextPage
    }
    viewOptions {
      hasSellersList
    }
  }
}

fragment PostFields on Post {
  id
  title
  postDate
  updateDate
  authorUsername
  authorId
  URL
  bodyTEXT
  bodyHTML
  thumbURL
  hasImage
  hasVideo
  city
  geoCity
  geoNeighborhood
  geoHash
  tags
  imagesList
  commentEnabled
  commentStatus
  commentCount
  upRank
  downRank
  status
  postType
  generalInfo {
    key
    value
  }
  price {
    formattedPrice
  }
  realEstateInfo {
    ...realEstateOptions
  }
  carInfo {
    sellOrWaiver
    is4DW
    model
    mileage
    fuel
    gear
    carOrRelated
    Bank
  }
  tagsFilters
  jobsInfo {
    jobs_OfferType
    jobs_ExperienceLevel
    jobs_ContractType
    jobs_Qualification
    jobs_CommercialeRgisterNumber
  }
  postNotesList {
    iconName
    iconUrl
    note
    link
  }
  BuyButton {
    Link
    StoreName
    Name
    canRequestWasataService
  }
}

fragment realEstateOptions on reInfo {
  re_AdvertiserType
  re_Direction
  re_StreetType
  re_AccommType
  re_IsKitchenIncluded
  re_IsFurnished
  re_IsDriverRoomAvilable
  re_IsMaidRoomAvilable
  re_IsFireRoomAvilable
  re_IsOutsideRoomAvilable
  re_IsCarGateAvilable
  re_IsElevatorAvilable
  re_IsParkingAvilable
  re_IsCellarIncludedAvilable
  re_IsGardenAvilable
  re_IsACIncludedAvilable
  re_IsPoolAvilable
  re_IsVolleyBallAvilable
  re_IsFootBallAvilable
  re_IsKidsGamesAvilable
  re_IsStairInsideAvilable
  re_IsYardAvilable
  re_IsBooked
  re_Area
  re_PropertyAge
  re_StreetWide
  re_RoomCount
  re_LivingRoomCount
  re_WCCount
  re_ApartmentCount
  re_CheckInDate
  re_CheckOutDate
  re_VillaCount
  re_PlanNum
  re_LandNum
  re_MachineCount
  re_PalmCount
  re_MeterPrice
  re_FloorNum
  re_REGA_Advertiser_registration_number
  re_REGA_Authorization_number
  re_VillaType
  re_IsOutdoorSessionsAvailable
  re_IsLivingRoomAvailable
  re_IsTransformerAvailable
  re_IsWCAvailable
  re_IsStageAvailable
  re_IsStorehouseAvailable
  re_IsWaterAvailable
  re_IsProtectoratesAvailable
  re_IsElectricityAvailable
  re_IsPrivateHallAvailable
  re_IsPrivateEntranceAvailable
  re_IsWorkersHouseAvailable
  re_IsTentHouseAvailable
  re_IsFoodHallAvailable
  re_IsTwoDepartment
  re_IsWaterTankAvailable
  re_IsPrivateHouseAvailable
  re_IsBridalDepartmentAvailable
  re_IsPlowAvailable
  re_IsGymAvailable
  re_IsWaterSprinklerAvailable
  re_TentCount
  re_WellsCount
  re_HallsCount
  re_FloorsCount
  re_TentHouseCount
  re_SessionsCount
  re_ShopsCount
  re_SupportDailyRentSystem
  re_SupportMonthlyRentSystem
  re_SupportYearlyRentSystem
}
"""

class HarajClient:
    def __init__(self):
        # Use provided correct Client ID
        self.client_id = CLIENT_ID
            
    def search(self, tag: str, page: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
        params = {
            "queryName": "search", # Changed from posts
            "clientId": self.client_id,
            "version": "N0.0.1"
        }
        
        # The user provided query uses 'search' variable for the search term
        # It seems the previous 'tag' logic might map to 'search' or 'tag' in the new query
        # The curl used {"search": "bmw"}, so let's map input 'tag' to 'search' variable.
        
        payload = {
            "query": QUERY,
            "variables": {
                "search": tag,
                "limit": limit,
                "page": page
            }
        }

        try:
            print(f"DEBUG: Sending to {API_URL} with clientId={self.client_id}")
            r = requests.post(API_URL, params=params, json=payload, headers=HEADERS, timeout=10)
            print(f"DEBUG: Status Code: {r.status_code}")
            
            r.raise_for_status()
            data = r.json()
            
            # Validation with Pydantic
            # Note: The response structure is now data.search instead of data.posts
            # We might need to adjust pydantic or just extract dict directly for now to be safe
            
            if 'errors' in data:
                print(f"GraphQL Errors: {data['errors']}")
                return []
                
            search_data = data.get('data', {}).get('search', {})
            if search_data and 'items' in search_data:
                return search_data['items']
            
            return []

        except Exception as e:
            print(f"API Request failed: {e}")
            if 'r' in locals():
                 print(f"Failed Response text: {r.text[:1000]}")
            return []

client = HarajClient()
