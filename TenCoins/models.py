# -*- coding: utf-8 -*-

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    lft = models.IntegerField(default = 0)
    rgt = models.IntegerField(default = 0)
    lvl = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.name
    
    def children(self,iLeft,iRight):
        return Category.objects.filter(lft__gt = iLeft , rgt__lt = iRight)
    
    def parent(self,iLeft,iRight):
        return Category.objects.filter(lft__lt = iLeft , rgt__gt = iRight) 
    
    def sibling(self,iLeft, iLvl):
        try:
            parent_id = Category.objects.get(lft=iLeft-1).id
        except Category.DoesNotExist:
            parent_id = None
        if parent_id != None:
            iLeft = Category.objects.get(id=parent_id).lft
            iRight = Category.objects.get(id=parent_id).rgt
        else:
            iLeft = 0
            iRight = 0
        return Category.objects.filter(lft__gt = iLeft , rgt__lt = iRight, lvl = iLvl)