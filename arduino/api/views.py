from rest_framework import generics
from ..models import Subject
from .serializers import SubjectSerializer
from rest_framework.response import Response


class SubjectListView(generics.ListAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

	def get(self, request, format=None):
		snippets = Subject.objects.all()
		#snippets = [{'data': {'id':1, 0}}]
		serializer = SubjectSerializer(snippets, many=True)
		return Response(serializer.data)

class SubjectDetailView(generics.RetrieveAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer