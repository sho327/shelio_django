from typing import Optional

from account.models import M_UserSettings
from core.repositories import BaseRepository


class M_UserSettingsRepository(BaseRepository):
    """
    ユーザー設定マスタ(M_UserSettings)モデル専用のリポジトリクラス。
    """

    model: M_UserSettings = M_UserSettings

    # BaseRepositoryから継承される主なメソッド:
    # - get_alive_by_pk(pk)
    # - get_alive_one_or_none(**kwargs)
    # - create(**kwargs)
    # - update(instance, **kwargs)
    # - soft_delete(instance)
