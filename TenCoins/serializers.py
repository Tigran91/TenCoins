# -*- coding: utf-8 -*-

from rest_framework import serializers
from DjangoTenCoins.models import Category
from rest_framework.fields import SerializerMethodField
   
class CategorySerializer(serializers.ModelSerializer):
    children = SerializerMethodField()
    parent = SerializerMethodField()
    sibling = SerializerMethodField()
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'children',
            'parent',
            'sibling',
        ]
        
    def get_children(self,obj):
        return CategoryNodeSerializer(obj.children(self.context["iLeft"],self.context["iRight"]),many=True).data
    
    def get_parent(self,obj):
        return CategoryNodeSerializer(obj.parent(self.context["iLeft"],self.context["iRight"]),many=True).data
    
    def get_sibling(self,obj):
        return CategoryNodeSerializer(obj.sibling(self.context["iLeft"],self.context["iLvl"]),many=True).data
        
class CategoryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]