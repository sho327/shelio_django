from django.views.generic import TemplateView

process_name = "RegisterPendingView"

class RegisterPendingView(TemplateView):
    """
    サインアップ後、ユーザーにメールを確認するように促す画面
    """

    template_name = "account/register_pending.html"
    # テンプレート内で、登録完了メッセージや再送リンクなどを表示します。
