from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from core.models import BaseModel


class M_UserSettings(BaseModel):
    """
    ユーザー設定マスタ
    通知設定やアプリケーション設定を管理
    """

    # ユーザマスタ（1対1）
    m_user = models.OneToOneField(
        "account.M_User",
        db_column="m_user_id",
        verbose_name="ユーザマスタ",
        db_comment="ユーザマスタ",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="user_settings",
    )

    # --- 通知設定 ---
    # メール通知一括設定
    is_email_notify_enabled = models.BooleanField(
        db_column="is_email_notify_enabled",
        verbose_name="メール通知一括設定フラグ",
        db_comment="メール通知一括設定フラグ",
        db_default=True,
        default=True,
    )

    # 個別の通知設定
    is_notify_like = models.BooleanField(
        db_column="is_notify_like",
        verbose_name="通知:いいね設定フラグ",
        db_comment="通知:作品に「いいね」がついた時のメール設定フラグ",
        db_default=True,
        default=True,
    )

    is_notify_comment = models.BooleanField(
        db_column="is_notify_comment",
        verbose_name="通知:コメント設定フラグ",
        db_comment="通知:コメントや返信が来た時のメール設定フラグ",
        db_default=True,
        default=True,
    )

    is_notify_follow = models.BooleanField(
        db_column="is_notify_follow",
        verbose_name="通知:フォロー設定フラグ",
        db_comment="通知:誰かにフォローされた時のメール設定フラグ",
        db_default=True,
        default=True,
    )

    # --- 各テーブル共通(AbstractBaseModelは列順が変わってしまうので使用しない) ---
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # M_Userモデルを参照
        db_column="created_by",
        verbose_name="作成者",
        db_comment="作成を行ったユーザー",
        related_name="%(app_label)s_%(class)s_created",  # 関連名の一意性を確保
        on_delete=models.SET_NULL,  # ユーザーが消えてもデータは残す
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        db_column="created_at",
        verbose_name="作成日時",
        db_comment="作成日時",
        null=True,
        blank=True,
        auto_now_add=True,
    )
    created_method = models.CharField(
        db_column="created_method",
        verbose_name="作成処理",
        db_comment="作成処理",
        max_length=128,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="updated_by",
        verbose_name="更新者",
        db_comment="更新を行ったユーザー",
        related_name="%(app_label)s_%(class)s_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        db_column="updated_at",
        verbose_name="更新日時",
        db_comment="更新日時",
        null=True,
        blank=True,
        auto_now=True,
    )
    updated_method = models.CharField(
        db_column="updated_method",
        verbose_name="更新処理",
        db_comment="更新処理",
        max_length=128,
        null=True,
        blank=True,
    )
    deleted_at = models.DateTimeField(
        db_column="deleted_at",
        verbose_name="削除日時",
        db_comment="削除日時",
        null=True,
        blank=True,
        db_default=None,
        default=None,
    )
    # --- 各テーブル共通 ---

    # 履歴管理
    history = HistoricalRecords(
        # table_name="h_m_user_settings",
        # history_id_field=models.BigAutoField(),
        # excluded_fields=["deleted_at"],
    )

    class Meta:
        db_table = "m_user_settings"
        db_table_comment = "ユーザー設定マスタ"
        verbose_name = "ユーザー設定マスタ"
        verbose_name_plural = "ユーザー設定マスタ"

    def __str__(self):
        return f"Settings for {self.m_user.email}"
