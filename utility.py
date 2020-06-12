'定义一个用于判断是否是管理员装饰器'
from learn.models import UserProfile
def permission_check(user):
    permission = UserProfile.objects.get(user=user).permission
    if permission == 0:
        return True
    else:
        return False
