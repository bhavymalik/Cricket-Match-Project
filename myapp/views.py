from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from django.core.cache import cache
from rest_framework.response import Response
from .models import match
from .serializer import matchserializer, patchmatchserializer

# this class deals with listing all the matches and giving the option to create a new match
class indexLC(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    queryset = match.objects.all()
    serializer_class = matchserializer

    def get(self, request):
        cache_key = 'livelist'
        result = cache.get(cache_key) # i could have used get_or_set method as well
        if result:
            return Response(result)
        result = self.list(request)
        cache.set(cache_key,result.data, 60*60)
        return result

    def post(self, request):
        cache.delete('livelist')
        return self.create(request)


# Modifies, Deletes and Shows a particular match
class indexRU(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset= match.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return patchmatchserializer
        return matchserializer

    def get(self, request, pk):
        cache_key= f"retrieve {pk}"
        result = cache.get(cache_key)
        if result:
            return Response(result)
        result = self.retrieve(request)
        cache.set(cache_key,result.data, 60*60)
        return result

    def patch(self,request, pk):
        cache.delete('livelist')
        cache.delete(f"retrieve {pk}")
        return self.partial_update(request)

    def delete(self,request,pk):
        cache.delete('livelist')
        cache.delete(f"retrieve {pk}")
        return self.destroy(request)