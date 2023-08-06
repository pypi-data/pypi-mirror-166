"""
  Project Tongji-EasyAPI
  session.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

import threading
import requests

try:
    from . import models
except ImportError and ModuleNotFoundError:
    import models

class Session:

    class keepAliveThread(threading.Thread):
        session: requests.Session = None
        waitTime: int = None
        needDestroy: threading.Event = None
        id: int = None
        def __init__(self:Session.keepAliveThread, fatherName: str, waitTime: int, session:requests.Session, needDestroy: threading.Event)->None:
            ...
        def run(self:Session.keepAliveThread)->None: ...

    keepAlive: Session.keepAliveThread = None
    studentID: str = None
    islogin: bool = None
    id: int = None
    studentData: models.Student = None
    session: requests.Session = None
    keepaliveDestroy: threading.Event = None

    def __init__(self:Session,studentID:str|int|None=...,studentPassword:str|int|None=...,proxy:str|None=...)->bool:
        ...
    
    def testConnection(self:Session,url:str|None=...)->bool: ...

    def login(self:Session,studentID:str|int|None=...,studentPassword:str|int|None=...,cookie:str|None=...,manual:bool|None=...)->str: ...

    def request(self:Session,method:str,url:str,data:bytes|str|None=...,json:dict|list|None=...,params:dict|None=...)->requests.Response:...

    def getSchoolCalender(self:Session) -> dict:...

    def getHolidayByYear(self:Session, year:int|None=...) -> dict :...

    def getScore(self)->models.Scores: