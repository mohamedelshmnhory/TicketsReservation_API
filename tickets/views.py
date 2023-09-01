from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation, Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer, PostSerializer
from rest_framework import status, filters
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly


# Create your views here.


# 1 without REST and no model query FBV
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'name': 'Omar',
            'mobile': '01018064080',
        },
        {
            'id': 2,
            'name': 'samir',
            'mobile': '01018064090',
        }
    ]

    return JsonResponse(guests, safe=False)


# 2 model data default django without rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)


# 3 Function based views
# 3.1 GET POST
@api_view(['GET', 'POST'])
def fbv_list(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 3.2 GET PUT DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def fbv_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV Class based views
# 4.1 List and Create == GET and POST
class CBVList(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 4.2 GET PUT DELETE class based views -- pk
class CBVpk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins
# 5.1 mixins list
class MixinsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2 mixins get put delete
class MixinsPk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.DestroyAPIView,
               generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


# 6 Generics
# 6.1 get and post
class GenericsList(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes = [BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# 6.2 get put and delete
class GenericsPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# 7 ViewSets
class ViewSetsGuest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class ViewSetsMovie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']


class ViewSetsReservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# 8 Find movie
@api_view(['POST'])  # GET
def find_movie(request):
    print(request.data)
    movies = Movie.objects.filter(hall=request.data['hall'], movie=request.data['movie'])
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 9 create new reservation
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(hall=request.data['hall'], movie=request.data['movie'])
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    reservation = Reservation()
    reservation.movie = movie
    reservation.guest = guest
    serializer = ReservationSerializer(reservation)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


# 10 post author editor
class PostPk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
