# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from DjangoTenCoins.models import Category
from .serializers import CategorySerializer
from django.db.models import F


class CategoryList(APIView):
    def get(self, request, category_id):
        if request.method == 'GET':
            try:
                Categories = Category.objects.filter(id=category_id)
                iLeft = Category.objects.get(id=category_id).lft
                iRight = Category.objects.get(id=category_id).rgt
                iLvl = Category.objects.get(id=category_id).lvl
                serializer = CategorySerializer(Categories, many=True,context={"category_id":category_id,"iLeft":iLeft,"iRight":iRight,"iLvl":iLvl})
            except Category.DoesNotExist:
                serializer = CategorySerializer("",many=True,context={"category_id":0,"iLeft":0,"iRight":0,"iLvl":0})
            
            return Response(serializer.data)

    def createFields(self,dictdata,iLvl,iParentID):
        # (1 (2  (3 4) 5) 6) 7 8 9 10 11 12 13 14 15
        for key, value in dictdata.items():
            if key == 'name':
                iParentLft = 0
                if iParentID != 0:
                    iParentLft = Category.objects.get(id = iParentID).lft
                    Category.objects.filter(rgt__gte = (iParentLft+1)).update(rgt = F('rgt') + 2)
                    Category.objects.filter(lft__gte = (iParentLft+1)).update(lft = F('lft') + 2)
                newitem = Category.objects.create(name = value,lft =iParentLft + 1,rgt=iParentLft + 2, lvl = iLvl)
                iID = newitem.id
                #print(newitem.name + str(newitem.lft) + str(newitem.rgt))
                print(iID)
            if key == "children":
                for children in value[:]:
                    self.createFields(children,iLvl+1,iID)
            
    def post(self,request):
        if request.method == 'POST':
            Category.objects.all().delete()
            self.createFields(request.data,0,0)
            return None
    