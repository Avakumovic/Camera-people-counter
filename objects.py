# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 19:41:45 2018

@author: AvaksTeam
"""

class MyObject:
    def __init__(self,oid,x,y,age,death):
        self.x = x
        self.y = y
        self.oid = oid
        self.age = age
        self.death = death
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
        
    def getAge(self):
        return self.age
    
    def getDeath(self):
        return self.death
        
    def setAge(self):
        self.age += 1
        
    def setDeath(self):
        self.death +=1
        
    def updateCoords(self,xn,yn):
        self.x = xn
        self.y = yn