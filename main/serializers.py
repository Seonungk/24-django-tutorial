from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from main.models import Study, User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from main.models import Study, User, StudyParticipation


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def save(self, **kwargs):
        hashed_password = make_password(self.validated_data["password"])
        return super().save(password=hashed_password, **kwargs)


class StudyParticipationSerializer(serializers.ModelSerializer):
    """
    StudyParticipation에 해당하는 Serializer
    """

    ### assignment3: 이곳에 과제를 작성해주세요
    class Meta:
        model = StudyParticipation
        fields = ["id", "study", "user"]
    ### end assignment3


class StudySerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    studyparticipation_set = StudyParticipationSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = ["id", "name", "description", "created_by", "studyparticipation_set"]
