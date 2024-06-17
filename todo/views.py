from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Todo

from todo.serializers import TodosSerializer


class TodosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodosSerializer
    queryset = Todo.objects.all()

    def get_queryset(self):
        aa = self.queryset.filter(user_logins=self.request.user.user_logins).all()
        print(aa)
        return aa
