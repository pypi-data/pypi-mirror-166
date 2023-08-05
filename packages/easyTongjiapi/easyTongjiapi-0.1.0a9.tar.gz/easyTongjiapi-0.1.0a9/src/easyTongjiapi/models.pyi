"""
  Project Tongji-EasyAPI
  models.pyi
  Copyright (c) 2022 Cinea Zhan. All rights reserved
  www.cinea.com.cn
"""

class Student:
    def __init__(self:Student,name:str|None="",studentId:str|None="",sex:int|None=0,faculty:str|None="",facultyName:str|None="",grade:str|None="",studentDataObject:dict|None=None) -> None:
        self.name:str
        self.studentId:str
        self.sex:int
        self.faculty:str
        self.facultyName:str
        self.grade:str
        ...
    
    def __str__(self:Student) -> str:...

    def __repr__(self:Student) -> str:...

class Scores:
    def __init__(self:Scores, sourceData:dict):
        self.gradePoint:float  #学生总寄点
        self.earnedCredits:float  #已修读学分
        self.failedCredits:float  #不及格学分
        self.failedNum:int  #不及格门数
        self.termNum:int   #学期数量
        self.coursesList:list     #课程列表

        self.courseNum:int  #已修读课程数量
        self.gradeExcellence:int   #获优课程门数
        self.gradeGood:int   #获良课程门数
        self.gradeMedium:int   #获中课程门数
        self.gradePass:int   #获及格课程门数
        self.gradeFailed:int   #获不及格课程门数
        ...

    def __str__(self:Scores) -> str:...

    def __repr__(self:Scores) -> str:...