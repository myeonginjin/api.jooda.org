from django.db import models
import uuid

GENDER_TYPE = (
    ("M", "남성"),
    ("F", "여성"),
)
STATE_TYPE = (
    ("ACTIVE", "정상 계정"),
    ("IN_ACTIVE", "비정상 계정"),
    ("WAIT_FOR", "대기 중인 계정"),
)


class Account(models.Model):
    # 계정 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="계정 pk",
    )
    # 회원 실명
    name = models.CharField(max_length=20, verbose_name="이름", blank=True, null=True)
    # 회원 전화번호
    phone_number = models.CharField(
        max_length=20,
        verbose_name="전화번호",
        blank=True,
        null=True,
    )
    # 비밀번호
    password = models.CharField(
        max_length=100, verbose_name="비밀번호", blank=True, null=True
    )
    # 성별
    gender = models.CharField(
        max_length=1,
        choices=GENDER_TYPE,
        blank=True,
        null=True,
        verbose_name="성별",
    )
    # 생년원일
    birth_date = models.CharField(
        max_length=10,
        verbose_name="출생년도",
        help_text="ex) 19981021",
        blank=True,
        null=True,
    )
    # OS
    os = models.CharField(max_length=10, verbose_name="OS", blank=True, null=True)
    # 기기 id
    device_id = models.CharField(
        max_length=50, verbose_name="기기 id", blank=True, null=True
    )
    # 앱 버전
    app_version = models.CharField(
        max_length=10, verbose_name="앱 버전", blank=True, null=True
    )
    # fcm 토큰
    fcm_token = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="fcm 토큰"
    )
    # 회원 가입 날짜
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="회원 가입 날짜")
    # 회원 상태
    state = models.CharField(
        max_length=15,
        default="ACTIVE",
        choices=STATE_TYPE,
        verbose_name="회원 상태",
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "탈퇴한 회원"

    class Meta:
        verbose_name = "1.1 회원 기본 정보"
        verbose_name_plural = "1.1 회원 기본 정보"
