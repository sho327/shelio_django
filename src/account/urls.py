from django.urls import path

from account.views.activate_user import ActivateUserView
from account.views.initial_setup import InitialSetupView
from account.views.login import LoginView
from account.views.logout import LogoutView
from account.views.password_reset_confirm import PasswordResetConfirmView
from account.views.password_reset_pending import PasswordResetPendingView
from account.views.password_reset_request import PasswordResetRequestView
from account.views.profile_edit import ProfileEditView
from account.views.public_profile import PublicProfileView
from account.views.register import RegisterView
from account.views.register_pending import RegisterPendingView
from account.views.user_search import UserSearchView
from account.views.user_settings import UserSettingsView

# app_nameを設定すると reverse_lazy("account:register_pending") が動作します
app_name = "account"

urlpatterns = [
    # ログイン画面を表示し、POSTで送信されたログイン情報を処理する
    path(
        "activate_user/<str:token_value>/",
        ActivateUserView.as_view(),
        name="activate_user",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("register_pending/", RegisterPendingView.as_view(), name="register_pending"),
    path(
        "password_reset_request/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password_reset_pending",
        PasswordResetPendingView.as_view(),
        name="password_reset_pending",
    ),
    path(
        "password_reset_confirm/<str:token_value>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "initial_setup/",
        InitialSetupView.as_view(),
        name="initial_setup",
    ),
    # プロフィール関連（統一）
    # 注意: profile/edit/ を profile/<str:pk>/ より先に定義
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/<str:pk>/", PublicProfileView.as_view(), name="profile"),  # 'me' または数値ID
    path("settings/", UserSettingsView.as_view(), name="settings"),
    # 検索
    path("search/", UserSearchView.as_view(), name="user_search"),
    # 後方互換性のため残す（将来的に削除予定）
    path("users/<int:pk>/", PublicProfileView.as_view(), name="public_profile"),
]
