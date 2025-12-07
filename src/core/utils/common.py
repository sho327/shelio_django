import os
import random
import string
from typing import Any, Dict, Optional, Union

# 役割: 上記のテーマ（日付/ストレージ/メール）に分類されない、汎用的なヘルパー関数やデータクレンジング処理を定義する。
# 利用例: ランダムなトークンの生成、フォーム入力値のNull/空白チェック。


def set_str_or_blank_format(pStr: Optional[str]) -> str:
    """
    文字列型に対するフォーマット。対象値がNoneまたはNoneでない場合に空文字列を設定する。
    """
    if isinstance(pStr, str):
        return pStr
    else:
        # pStrがNoneの場合に空文字列を返す。
        return "" if pStr is None else str(pStr)


def set_str_or_none_format(pStr: Optional[str]) -> Optional[str]:
    """
    文字列型に対するフォーマット。対象値がNoneの場合にそのままNone設定。
    """
    if isinstance(pStr, str):
        return pStr
    else:
        # Noneでない場合は文字列化を試みる
        return None if pStr is None else str(pStr)


def set_int_format(pInt: Optional[Union[int, str]]) -> Optional[int]:
    """
    数値型に対するフォーマット。対象値がNoneの場合にそのままNone設定。
    文字列を数値に変換する処理も行う。
    """
    if pInt is None:
        return None

    try:
        return int(pInt)
    except (ValueError, TypeError):
        # 変換できない場合はNoneを返す
        return None


def generate_random_string(length: int = 20) -> str:
    """
    指定された長さのランダムな英数字文字列（一時パスワード、トークンなど）を生成する。
    注意: セキュリティが重要な用途（トークンなど）には generate_secure_token を使用してください。
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))


def generate_secure_token(byte_length: int = 32) -> str:
    """
    暗号学的に安全なランダムトークンを生成する（16進数文字列として返す）。
    トークン生成など、セキュリティが重要な用途に使用する。

    Args:
        byte_length: 生成するバイト数（デフォルト: 32バイト = 64文字の16進数）

    Returns:
        16進数文字列（例: "a1b2c3d4..."）
    """
    return os.urandom(byte_length).hex()


def clean_input_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    辞書内の文字列データから前後の空白文字を削除し、データの前処理を行う。
    """
    cleaned_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned_data[key] = value.strip()
        else:
            cleaned_data[key] = value
    return cleaned_data
