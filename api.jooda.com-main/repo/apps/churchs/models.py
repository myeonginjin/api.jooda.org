from typing import Iterable, Optional
from django.db import models
import uuid

from common.utils import geocoding


BIBLE_EDITION = (
    ("KRB", "개역한글판"),
    ("NKR72H", "개역개정판"),
)

MEMBER_STATE = (
    ("success", "등록 승인"),
    ("confirm", "등록 심사 중"),
    ("reject", "등록 거절"),
)


def thumbnail_upload_url(instance, filename):
    return f"churchs/thumbnail/{str(instance.id)}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


def logo_upload_url(instance, filename):
    return f"churchs/logo/{str(instance.id)}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


def pastor_upload_url(instance, filename):
    return f"churchs/pastor/{str(instance.id)}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


def notice_upload_url(instance, filename):
    return f"churchs/notice/{str(instance.id)}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


def weekly_upload_url(instance, filename):
    return f"churchs/weekly/{str(instance.id)}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


class Church(models.Model):
    # 교회 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="교회 pk",
    )
    # 교회 명
    name = models.CharField(
        max_length=50,
        verbose_name="교회명",
        blank=True,
        null=True,
        help_text="ex) 여의도 순복음교회",
    )
    # 교회 연락처
    contact_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="교회 연락처",
    )
    # 교회 종파
    denomination = models.ForeignKey(
        "churchs.ChurchDenomination",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church",
    )

    ##### introduction text #####
    # 교회 소개글 제목
    introduction_title = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="교회 소개글 제목"
    )
    # 교회 소개글 내용
    introduction_content = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="교회 소개글 내용"
    )

    ##### location #####
    # 교회 주소
    address = models.CharField(
        max_length=200,
        verbose_name="교회 주소",
        blank=True,
        null=True,
    )
    detail_address = models.CharField(
        max_length=50,
        verbose_name="교회 상세 주소",
        blank=True,
        null=True,
    )
    # 경도
    longitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="경도",
        db_index=True,
        help_text="교회 주소 저장 시 자동으로 채워짐",
    )
    # 위도
    latitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="위도",
        db_index=True,
        help_text="교회 주소 저장 시 자동으로 채워짐",
    )

    # 성경
    bible_edition = models.CharField(
        max_length=20,
        choices=BIBLE_EDITION,
        blank=True,
        null=True,
        default="KRB",
        verbose_name="성경판",
    )
    # 교회 공개 여부
    is_exposure = models.BooleanField(default=True, blank=True, verbose_name="교회 공개 여부")
    # 썸네일
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_url, blank=True, null=True, verbose_name="썸네일"
    )
    # 썸네일
    logo = models.ImageField(
        upload_to=logo_upload_url, blank=True, null=True, verbose_name="로고"
    )
    # 등록일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not (self.longitude and self.latitude) and self.address:
            self.longitude, self.latitude = geocoding.convert_address_to_coordinate(
                self.address
            )
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "2.1 교회 정보"
        verbose_name_plural = "2.1 교회 정보"


class ChurchDirections(models.Model):
    # 교회
    church = models.OneToOneField(
        "churchs.Church",
        null=True,
        on_delete=models.CASCADE,
        verbose_name="교회",
    )
    parking = models.CharField(
        null=True,
        blank=True,
        max_length=120,
        verbose_name="주차장",
    )
    own_car = models.CharField(
        null=True,
        blank=True,
        max_length=120,
        verbose_name="자가용",
    )
    public_transport = models.CharField(
        null=True,
        blank=True,
        max_length=120,
        verbose_name="대중교통",
    )
    shuttle_bus = models.CharField(
        null=True,
        blank=True,
        max_length=120,
        verbose_name="셔틀버스",
    )

    def __str__(self):
        return self.church.name + "오시는 길"

    class Meta:
        verbose_name = "2.1-1 교회 오시는 길 정보"
        verbose_name_plural = "2.1-1 교회 오시는 길 정보"


class ChurchMember(models.Model):
    # 유저 교회 중개 테이블 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="교회 유저 중개 테이블 pk",
        db_index=True,
    )

    # 계정
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_member",
    )
    # 교회
    church = models.ForeignKey(
        "churchs.Church",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_member",
        verbose_name="교회",
    )
    # 유저 상태
    state = models.CharField(
        max_length=12,
        choices=MEMBER_STATE,
        default="confirm",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "2.2 교회 회원 정보"
        verbose_name_plural = "2.2 교회 회원 정보"


class ChurchDenomination(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        null=False,
        verbose_name="교회 종파 pk",
    )
    name = models.CharField(
        max_length=50,
        null=True,
        unique=True,
        blank=True,
        verbose_name="교회 종파 이름",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "2.3 교회 종파 정보"
        verbose_name_plural = "2.3 교회 종파 정보"


class ChurchPastor(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        null=False,
        default=uuid.uuid4,
        verbose_name="교회 섬기는 이 pk",
    )
    # 교회
    church = models.ForeignKey(
        "churchs.Church",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_pastor",
        verbose_name="교회",
    )
    name = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="교회 섬기는 이 이름",
    )
    role = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="교회 섬기는 이 직분(역할)",
    )
    image = models.ImageField(
        upload_to=pastor_upload_url,
        blank=True,
        null=True,
        verbose_name="섬기는 이 사진",
    )
    order = models.IntegerField(
        default=10000,
        blank=True,
        verbose_name="섬기는 이 순서",
    )

    def __str__(self):
        return self.church.name + ", " + self.name

    class Meta:
        verbose_name = "2.4 교회 섬기는 이 정보"
        verbose_name_plural = "2.4 교회 섬기는 이 정보"


class ChurchHistory(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="교회 연혁 정보 pk",
    )
    # 교회
    church = models.ForeignKey(
        "churchs.Church",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_history",
        verbose_name="교회",
    )
    year = models.CharField(max_length=4, null=True, blank=True, verbose_name="년도")
    month = models.CharField(max_length=2, null=True, blank=True, verbose_name="월")
    day = models.CharField(max_length=2, null=True, blank=True, verbose_name="일")
    content = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="연혁 내용",
    )

    def __str__(self):
        return self.church.name + " " + self.year + "/" + self.month + "/" + self.day

    class Meta:
        verbose_name = "2.5 교회 연혁 정보"
        verbose_name_plural = "2.5 교회 연혁 정보"


class ChurchNotice(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="교회 공지사항 정보 pk",
    )
    # 교회
    church = models.ForeignKey(
        "churchs.Church",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_notice",
        verbose_name="교회",
    )
    # 공지사항 작성자
    writer = models.ForeignKey(
        "administrators.Administrator",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_notice",
        verbose_name="공지사항 작성자",
    )
    title = models.CharField(
        max_length=40, null=True, blank=True, verbose_name="공지사항 제목"
    )
    content = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="공지사항 내용"
    )
    image = models.ImageField(
        upload_to=notice_upload_url,
        blank=True,
        null=True,
        verbose_name="공지사항 사진",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="공지사항 등록 날짜")

    def __str__(self):
        return self.church.name + " " + self.title

    class Meta:
        verbose_name = "2.6 교회 공지사항 정보"
        verbose_name_plural = "2.6 교회 공지사항 정보"


class ChurchWeekly(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="교회 주보 정보 pk",
    )
    # 교회
    church = models.ForeignKey(
        "churchs.Church",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_weekly",
        verbose_name="교회",
    )
    title = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="주보 제목",
    )
    image = models.ImageField(
        upload_to=weekly_upload_url,
        blank=True,
        null=True,
        verbose_name="주보 사진",
    )
    year = models.CharField(max_length=2, null=True, blank=True, verbose_name="년도")
    month = models.CharField(max_length=2, null=True, blank=True, verbose_name="월")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="주보 등록 날짜")

    def __str__(self):
        return self.church.name + " " + self.title

    class Meta:
        verbose_name = "2.7 교회 주보 정보"
        verbose_name_plural = "2.7 교회 주보 정보"


class ChurchCalendar(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="교회 달력 정보 pk",
    )
    # 교회
    church = models.ForeignKey(
        "churchs.Church",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_calendar",
        verbose_name="교회",
    )
    title = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name="일정 제목",
    )
    content = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="일정 내용",
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="시작 날짜")
    end_date = models.DateField(null=True, blank=True, default="", verbose_name="종료 날짜")

    def __str__(self):
        return self.church.name + " " + self.title

    def save(self, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date

        return super().save()

    class Meta:
        verbose_name = "2.8 교회 달력 정보"
        verbose_name_plural = "2.8 교회 달력 정보"


class ChurchWorshipSchedule(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="교회 예배 일정 정보 pk",
    )
    # 교회
    church = models.ForeignKey(
        "churchs.Church",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="church_worship_schedule",
        verbose_name="교회",
    )
    title = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name="예배 일정 제목",
    )
    subtitle = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name="예배 일정 소제목",
    )

    weekday = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name="요일",
        help_text="일요일: -1, 월요일: 0, ~ 토요일: 5",
    )

    place = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="예배 장소",
    )
    mc = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="예배 진행자",
    )
    target = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="예배 대상",
    )
    reference = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="예배 참고",
    )
    start_time = models.TimeField(null=True, blank=True, verbose_name="시작 시간")
    end_time = models.TimeField(null=True, blank=True, verbose_name="종료 시간")

    def __str__(self):
        return self.church.name + " " + self.title

    class Meta:
        verbose_name = "2.9 교회 예배 일정 정보"
        verbose_name_plural = "2.9 교회 예배 일정 정보"
