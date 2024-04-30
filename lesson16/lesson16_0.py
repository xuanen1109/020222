import requests
from requests import Response
from pydantic import BaseModel,RootModel,Field,field_validator
import pandas as pd

def get_urldata() -> Response | None:
    json_url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    try:
        responseData:Response = requests.get(json_url)
        responseData.raise_for_status()
        if responseData.status_code == 200:
            print("下載成功")
            return responseData
        else:
            print("下載失敗")
            return None
    except Exception as a:
        print(a)
        print("連線失敗")
        return None

class Site(BaseModel):
    站點名稱:str = Field(alias='sna')
    行政區:str = Field(alias='sarea')
    總車輛數:float = Field(alias='tot')
    可借:float = Field(alias='sbi')
    可還:float = Field(alias='bemp')
    時間:str = Field(alias='mday')
    
    @field_validator("總車輛數","可借","可還",mode='before')
    @classmethod
    def empty_to_zero(cls, value):
        if value == '':
            return '0.0'
        else:
            return value

class Sites(RootModel):
    root:list[Site]
    def __iter__(self):
        return iter(self.root)
    def __getitem__(self, item):
        return self.root(item)
    
def main():
    rawData:Response | None = get_urldata()
    rawstr:str = rawData.text
    datas:Sites = Sites.model_validate_json(rawstr)
    download_data:list[dict] = datas.model_dump()
    youbike_df = pd.DataFrame(download_data)
    print(youbike_df)

if __name__ == '__main__':
    main()