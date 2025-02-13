from __future__ import annotations
from requests import Session
from requests.auth import HTTPDigestAuth
import json
from typing import Optional


class Eddi():
    def __init__(self, parent: MyEnergiData):
        self.__parent__: MyEnergiData = parent
        self.deviceClass: str
        self.batteryDischargeEnabled: str = ""
        self.bsm: int = 0
        self.bst: int = 0
        self.che: float = 0.0
        self.cmt: str = ""
        self.dat: str = ""
        self.deviceClass: str = ""
        self.div: int = 0
        self.dst: int = 0
        self.ectp1: int = 0
        self.ectp2: int = 0
        self.ectp3: int = 0
        self.ectt1: str = ""
        self.ectt2: str = ""
        self.ectt3: str = ""
        self.frq: float = 0.0
        self.fwv: str = ""
        self.g100LockoutState: str = ""
        self.gen: int = 0
        self.grd: str = ""
        self.hno: str = ""
        self.hpri: str = ""
        self.ht1: str = ""
        self.ht2: str = ""
        self.isVHubEnabled: str = ""
        self.newAppAvailable: str = ""
        self.newBootloaderAvailable: str = ""
        self.pha: int = 0
        self.pri: int = 0
        self.productCode: str = ""
        self.r1a: str = ""
        self.r2a: str = ""
        self.rbc: str = ""
        self.sno: int = 0
        self.sta: int = 0
        self.tim: str = ""
        self.tp1: str = ""
        self.tp2: str = ""
        self.tz: int = 0
        self.vol: float = 0.0
    
    def to_json(self) -> dict:
        return json.dumps(self.__dict__)
    
    def from_json(self, json_obj: dict) -> Eddi:
        if json_obj:
            for k, v in json_obj.items():
                if hasattr(self, k):
                    setattr(self, k, v)
        return self

    def boost(self, minutes: int, heater_number: int = 1, url: str = "") -> bool:
        boost_url = url if url else f"{self.__parent__.__parent__.base_url}/cgi-eddi-boost-E{self.sno}-10-{heater_number}-{minutes}"
        res = self.__parent__.__parent__.__session__.get(boost_url)
        if res.status_code == 200:
            self.__parent__.__parent__.__get_data__()
            return True
        else:
            return False
    
    def cancel_boost(self, heater_number: int = 1, url: str = "") -> bool:
        cancel_url = url if url else f"{self.__parent__.__parent__.base_url}/cgi-eddi-boost-E{self.sno}-1-{heater_number}-0"
        res = self.__parent__.__parent__.__session__.get(cancel_url)
        if res.status_code == 200:
            self.__parent__.__parent__.__get_data__()
            return True
        else:
            return False

    def get_heater_priority(self, url: str = "") -> int:
        heater_url = url if url else f"{self.__parent__.__parent__.base_url}/cgi-set-heater-priority-E{self.sno}"
        res = self.__parent__.__parent__.__session__.get(heater_url)
        if res.status_code == 200:
            res_json = res.json()
            hpri = res_json.get('hpri', 0)
            return hpri
        else:
            return 0
    
    def set_heater_priority(self, heater_number: int, url: str = "") -> int:
        heater_url = url if url else f"{self.__parent__.__parent__.base_url}/cgi-set-heater-priority-E{self.sno}-{heater_number}"
        res = self.__parent__.__parent__.__session__.get(heater_url)
        if res.status_code == 200:
            self.__parent__.__parent__.__get_data__()
            return True
        else:
            return False


class Harvi():
    def __init__(self, parent: MyEnergiData):
        self.__parent__: MyEnergiData = parent
        self.dat: str = ""
        self.deviceClass: str = ""
        self.ect1p: int = 0
        self.ect2p: int = 0
        self.ect3p: int = 0
        self.ectp1: int = 0
        self.ectp2: int = 0
        self.ectp3: int = 0
        self.ectt1: str = ""
        self.ectt2: str = ""
        self.ectt3: str = ""
        self.fwv: str = ""
        self.productCode: str = ""
        self.sno: int = 0
        self.tim: str = ""
    
    def to_json(self) -> dict:
        return json.dumps(self.__dict__)
    
    def from_json(self, json_obj: dict) -> Harvi:
        if json_obj:
            for k, v in json_obj.items():
                if hasattr(self, k):
                    setattr(self, k, v)
        return self


class MyEnergiData():
    def __init__(self, parent: Optional[MyEnergi] = None):
        self.__parent__: Optional[MyEnergi] = parent
        self.eddi: list[Eddi] = []
        self.harvi: list[Harvi] = []
    
    def from_json(self, json_obj: list) -> MyEnergiData:
        if json_obj:
            for item in json_obj:
                for device_type, devices in item.items():
                    if device_type == "eddi":
                        for device in devices:
                            new_obj = Eddi(self)
                            new_obj.from_json(device)
                            self.eddi.append(new_obj)
                    elif device_type == "harvi":
                        for device in devices:
                            new_obj = Harvi(self)
                            new_obj.from_json(device)
                            self.harvi.append(new_obj)
    
    def to_json(self) -> dict:
        json_obj = {}
        json_obj['eddi'] = [x for x in self.eddi]


class MyEnergi():
    def __init__(self, serial_number: str, api_key: str, base_url: str = ""):
        self.__serial_number__: str = serial_number
        self.__api_key__: str = api_key
        self.base_url: str = base_url if base_url else "https://s18.myenergi.net"
        self.myenergi_data: MyEnergiData = MyEnergiData(parent=self)
        self.__session__: Session = Session()
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        auth = HTTPDigestAuth(self.__serial_number__, self.__api_key__)
        self.__session__.auth = auth
        self.__session__.headers = headers
        self.__get_data__()
    
    def __get_data__(self):        
        res = self.__session__.get(f"{self.base_url}/cgi-jstatus-*")
        if res.status_code == 200:
            res_json = res.json()
            self.myenergi_data.from_json(res_json)