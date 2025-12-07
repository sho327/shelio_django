from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from core.consts import LOG_METHOD
from core.utils.log_helpers import log_output_by_msg_id


class LogoutView(View):
    """
    ユーザーをログアウトさせ、ログインページにリダイレクトするビュー。
    """

    # ログアウト後のリダイレクト先 (通常はログインページ)
    # reverse_lazy を使うことで、URLがまだ読み込まれていなくても安全に参照できます
    redirect_url = reverse_lazy("account:login")

    def get(self, request):
        user_id = None
        if request.user.is_authenticated:
            user_id = str(request.user.pk)

        try:
            # Django標準のログアウト関数を呼び出す
            logout(request)
            # messages.success(request, "ログアウトしました。")

        except Exception as e:
            # ログ出力: ログアウト処理中のエラーを記録（スタックトレースを含む）
            error_detail = f"ログアウト処理中にエラーが発生しました。ユーザーID: {user_id} エラー: {str(e)}"
            log_output_by_msg_id(
                log_id="MSGE002",
                params=[error_detail],
                logger_name=LOG_METHOD.APPLICATION.value,
                exc_info=True,  # 予測不可能なエラーのためスタックトレースを含める
            )
            # セッション削除失敗などの場合でも、ログイン画面にリダイレクト
            # messages.error(request, "ログアウト処理中にエラーが発生しました。")

        return redirect(reverse("account:login"))

    # ユーザーが誤ってログアウトリンクを画像として貼った場合のセキュリティ対策
    def post(self, request):
        return self.get(request)
