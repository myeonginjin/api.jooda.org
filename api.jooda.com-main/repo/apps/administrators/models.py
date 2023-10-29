from django.db import models
from uuid import uuid4


class Administrator(models.Model):
    """
    교회 관리자 테이블
    """

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid4,
        verbose_name="관리자 계정 pk",
    )
    login_id = models.CharField(
        max_length=20,
        unique=True,
        editable=True,
        blank=True,
        null=True,
        verbose_name="로그인 id",
    )
    password = models.CharField(
        max_length=70,
        editable=True,
        blank=True,
        default="",
        verbose_name="로그인 비밀번호",
    )
    church = models.ForeignKey(
        "churchs.Church",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="administrator",
        verbose_name="교회",
        db_index=True,
    )
    # 관리자 전화번호
    phone_number = models.CharField(
        max_length=20,
        verbose_name="전화번호",
        blank=True,
        null=True,
    )
    # 인증 토큰
    authorization_token = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        verbose_name="인증 토큰",
    )

    def __str__(self):
        if self.church:
            return self.church.name + " 관리자"
        else:
            return "삭제된 교회 관리자"

    class Meta:
        verbose_name = "3.1 교회 관리자 기본 정보"
        verbose_name_plural = "3.1 교회 관리자 기본 정보"
