from django.core.paginator import Paginator

from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rankings.serializers import MatchSerializer
from rankings.models import Match as MatchModel


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="Information for a given match",
)
@api_view(['GET'])
def Match(request, match):
    matches = MatchModel.objects.filter(key=match).all()
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches (WARNING: VERY SLOW)",
)
@api_view(['GET'])
def _Matches(request, year=None, event=None, page=1):
    matches = MatchModel.objects
    if year is not None:
        matches = matches.filter(year=year)
    if event is not None:
        matches = matches.filter(event=event)
    matches = matches.all().order_by('time')
    matches = Paginator(matches, 5000).page(page)
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches (WARNING: VERY SLOW)",
)
@api_view(['GET'])
def Matches(request):
    return _Matches(request._request)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches from a given year (WARNING: VERY SLOW)",  # noqa 502
)
@api_view(['GET'])
def MatchesYear(request, year):
    return _Matches(request._request)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches from a given event",
)
@api_view(['GET'])
def MatchesEvent(request, event):
    return _Matches(request._request)