from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from account.forms.user_settings import UserSettingsForm
from account.services.user_service import UserService
from core.consts import LOG_METHOD
from core.decorators.logging_sql_queries import logging_sql_queries
from core.exceptions import IntegrityError
from core.utils.log_helpers import log_output_by_msg_id

process_name = "UserSettingsView"


class UserSettingsView(LoginRequiredMixin, FormView):
    """
    ユーザー設定画面（通知設定）
    """

    template_name = "account/settings.html"
    form_class = UserSettingsForm
    success_url = reverse_lazy("account:settings")

    @logging_sql_queries(process_name=process_name)
    def get_initial(self):
        """
        現在の設定値を取得してフォームに渡す
        """
        initial = super().get_initial()
        user = self.request.user
        service = UserService()

        if user.is_authenticated:
            try:
                setting = service.get_user_setting(user)
                initial["is_email_notify_enabled"] = setting.is_email_notify_enabled
                initial["is_notify_like"] = setting.is_notify_like
                initial["is_notify_comment"] = setting.is_notify_comment
                initial["is_notify_follow"] = setting.is_notify_follow
            except IntegrityError:
                # 設定が存在しない場合はデフォルト値
                pass

        return initial

    @logging_sql_queries(process_name=process_name)
    def form_valid(self, form):
        data = form.cleaned_data
        user_id = str(self.request.user.pk)
        service = UserService()

        try:
            # サービス層を呼び出し、設定を更新
            service.update_user_setting(
                user=self.request.user,
                process_name=process_name,
                is_email_notify_enabled=data.get("is_email_notify_enabled"),
                is_notify_like=data.get("is_notify_like"),
                is_notify_comment=data.get("is_notify_comment"),
                is_notify_follow=data.get("is_notify_follow"),
            )

            messages.success(self.request, "設定を更新しました。")
            return super().form_valid(form)

        except IntegrityError as e:
            # ログ出力: データベース整合性エラーを記録
            log_output_by_msg_id(
                log_id="MSGE901",
                params=[user_id, e.message_id, str(e.details)],
                logger_name=LOG_METHOD.APPLICATION.value,
                exc_info=True,
            )
            form.add_error(None, e.message)
            return self.form_invalid(form)

        except Exception as e:
            # ログ出力: 予期せぬエラーを記録
            error_detail = f"設定更新処理中にエラーが発生しました。ユーザーID: {user_id} エラー: {str(e)}"
            log_output_by_msg_id(
                log_id="MSGE002",
                params=[error_detail],
                logger_name=LOG_METHOD.APPLICATION.value,
                exc_info=True,
            )
            form.add_error(None, "予期せぬエラーが発生しました。")
            return self.form_invalid(form)
