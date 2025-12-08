from django import forms


class UserSettingsForm(forms.Form):
    """
    ユーザー設定フォーム（通知設定）
    """

    # メール通知一括設定
    is_email_notify_enabled = forms.BooleanField(
        required=False,
        label="メール通知を有効にする",
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
    )

    # 個別の通知設定
    is_notify_like = forms.BooleanField(
        required=False,
        label="いいね通知",
        help_text="作品に「いいね」がついた時に通知",
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
    )

    is_notify_comment = forms.BooleanField(
        required=False,
        label="コメント通知",
        help_text="コメントや返信が来た時に通知",
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
    )

    is_notify_follow = forms.BooleanField(
        required=False,
        label="フォロー通知",
        help_text="誰かにフォローされた時に通知",
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
    )
