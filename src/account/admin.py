from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from account.models import M_User, M_UserProfile, T_LoginHisory, T_UserToken

admin.site.register(M_User, SimpleHistoryAdmin)
admin.site.register(M_UserProfile, SimpleHistoryAdmin)
admin.site.register(T_LoginHisory, SimpleHistoryAdmin)
admin.site.register(T_UserToken, SimpleHistoryAdmin)
