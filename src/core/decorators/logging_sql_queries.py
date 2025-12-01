# utils/decorators.py (修正案)

from functools import wraps
from typing import Any, Callable, List, Tuple

from django.conf import settings
from django.db import connection

# --- 共通モジュールの新しいパス ---
from core.consts import LOG_METHOD
from core.utils.log_helpers import log_output_by_msg_id


# デコレータを二重にし、引数 (process_name) を受け取れるようにする
def logging_sql_queries(process_name: str) -> Callable:
    """
    デコレートされた関数が実行された際に発行されたSQLクエリをキャプチャし、
    ACCESSロガーまたはAPPLICATIONロガーに出力するデコレータ。

    Args:
        process_name (str): ログのヘッダーに含める処理名。
    """

    # process_name を受け取った後に、実際のデコレータ関数を返す
    def actual_decorator(func: Callable) -> Callable:

        class QueryLogger:
            """
            connection.execute_wrapper に渡され、実行されたクエリを収集するクラス
            """

            def __init__(self):
                self.queries: List[Tuple[str, Any]] = []

            def __call__(
                self, execute: Callable, sql: str, params: Any, many: bool, context: Any
            ) -> Any:
                """クエリ実行時に呼び出されるフック"""
                self.queries.append((sql, params))
                return execute(sql, params, many, context)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # self (Viewインスタンス) を取得
            # *argsの最初の要素がクラスインスタンス(self)であることを想定
            if args and hasattr(args[0], "__class__"):
                instance = args[0]
                class_name = instance.__class__.__name__
            else:
                class_name = "Function"

            logger_instance = QueryLogger()

            # settings.DEBUG が False の場合はロギングをスキップ (パフォーマンスのため)
            if not settings.DEBUG:
                return func(*args, **kwargs)

            # 1. クエリロガーを接続に設定し、デコレートされた関数を実行
            with connection.execute_wrapper(logger_instance):
                result = func(*args, **kwargs)

            # 2. ロギング処理

            header_message = (
                f"=== SQL START: {class_name}.{func.__name__} ({process_name}) ==="
            )
            footer_message = (
                f"=== SQL END: Total Queries ({len(logger_instance.queries)}) ==="
            )

            # --- ヘッダーログ出力 ---
            log_output_by_msg_id(
                log_id="MSGI001",
                params=[header_message],
                logger_name=LOG_METHOD.APPLICATION.value,
            )

            # --- クエリとパラメータのログ出力 ---
            for sql, params in logger_instance.queries:
                full_sql_message = f"{sql} / Params: {str(params)}"

                log_output_by_msg_id(
                    log_id="MSGI001",
                    params=[full_sql_message],
                    logger_name=LOG_METHOD.APPLICATION.value,
                )

            # --- フッターログ出力 ---
            log_output_by_msg_id(
                log_id="MSGI001",
                params=[footer_message],
                logger_name=LOG_METHOD.APPLICATION.value,
            )

            return result

        return wrapper

    return actual_decorator
