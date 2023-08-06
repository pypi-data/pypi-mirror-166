"""
  Project Tongji-EasyAPI
  models.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

class Student:

    name:str
    studentId:str
    sex:int
    faculty:str
    facultyName:str
    grade:str
        
    def __init__(self:Student,name:str|None="",studentId:str|None="",sex:int|None=0,faculty:str|None="",facultyName:str|None="",grade:str|None="",studentDataObject:dict|None=None) -> None:
        ...
    
    def __str__(self:Student) -> str:...

    def __repr__(self:Student) -> str:...

class Scores:

    gradePoint: float  #学生总寄点
    earnedCredits: float  #已修读学分
    failedCredits: float  #不及格学分
    failedNum: int  #不及格门数
    termNum: int  #学期数量
    coursesList: list  #课程列表

    courseNum: int  #已修读课程数量
    gradeExcellence: int  #获优课程门数
    gradeGood: int  #获良课程门数
    gradeMedium: int  #获中课程门数
    gradePass: int  #获及格课程门数
    gradeFailed: int  #获不及格课程门数
    
    def __init__(self:Scores, sourceData:dict):
        ...

    def __str__(self:Scores) -> str:...

    def __repr__(self:Scores) -> str:...