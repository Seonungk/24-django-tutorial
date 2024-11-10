from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from main.models import Study, StudyParticipation
from main.serializers import (
    StudySerializer,
    LoginSerializer,
    UserSerializer,
    StudyParticipationSerializer
)
from rest_framework import generics


class LoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            raise AuthenticationFailed("아이디 또는 비밀번호가 틀렸습니다")

        login(request, user)

        return Response()


class SignupView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer


class StudyListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class StudyDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return super().get_queryset()

        return super().get_queryset().filter(created_by=self.request.user)


class StudyParticipationListView(
    ListModelMixin,
    CreateModelMixin,
    GenericAPIView,
):
    """
    GET: 내 스터디 참여 목록. 남의 것이 조회되면 안됩니다.
    POST: 내 스터디 참여 목록 추가. 남의 것을 추가할 수 없습니다(HTTP 403 에러)
    """

    ### assignment3: 이곳에 과제를 작성해주세요
    permission_classes = [IsAuthenticated]
    serializer_class = StudyParticipationSerializer

    def get_queryset(self):
        # 현재 로그인된 사용자의 참여 목록만 조회
        return StudyParticipation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 요청자가 자신의 스터디만 추가하도록 제한
        if serializer.validated_data.get('user') != self.request.user:
            raise PermissionDenied("다른 사용자의 참여를 추가할 권한이 없습니다.")
        serializer.save(user=self.request.user)
    ### end assignment3


class StudyParticipationView(
    DestroyModelMixin,
    GenericAPIView,
):
    """
    DELETE: 내 스터디 참여 목록 제거. 남의 것을 제거할 수 없습니다(HTTP 404 에러)
    """

    ### assignment3: 이곳에 과제를 작성해주세요
    permission_classes = [IsAuthenticated]
    serializer_class = StudyParticipationSerializer

    def get_queryset(self):
        # 요청 사용자의 참여 이력만 삭제 가능
        return StudyParticipation.objects.filter(user=self.request.user)
    ### end assignment3
