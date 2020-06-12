from django.urls import path
from learn import views as learn_view

urlpatterns = [

    path('',learn_view.home,name='home'),
    path('sign/', learn_view.sign, name='sign'), #登录
    path('out/', learn_view.out, name='out'), #退出登录
    path('join/', learn_view.join, name='join'), #注册普通用户
    path('pwd_change/', learn_view.pwd_change, name='pwd_change'), #修改密码
    path('list/<int:a>',learn_view.list,name='list'),#笔记列表
    path('list/classificationInfo/<int:a>/<int:b>',learn_view.classificationInfo,name='classficationInfo'),#分类详细信息,参数a代表用户，参数b代表笔记类别
    path('noteContent/<int:a>/<int:b>', learn_view.noteContent, name='noteContent'),  # 笔记内容,参数a代表当前访问的用户，b代表笔记id
    path('bigThumb/',learn_view.bigThumb,name="bigThumb"),#点赞排行榜
    path('addInfo/',learn_view.addInfo,name="addInfo"),#添加笔记
    path('searchInfo/', learn_view.searchInfo, name="searchInfo"), # 查找笔记
    path('delNote/', learn_view.delNote, name="delNote"),  # 删除笔记
    path('editNote/', learn_view.editNote, name="editNote"),  # 编辑笔记
    path('like/', learn_view.like, name="like"),  # 点赞
    path('comment/', learn_view.comment, name="comment"),  # 评论笔记内容
    path('collect/', learn_view.collect, name="collect"),  # 收藏笔记
    path('myNote/', learn_view.myNote, name="myNote"),  # 关注用户
    path('signFirst/', learn_view.signFirst, name="signFirst"),  # 请先登录/注册
    path('personData/', learn_view.personData, name="personData"),  # 个人资料展示
    path('editPersonData/', learn_view.editPersonData, name="editPersonData"),  # 个人资料编辑
    path('delete1/<int:a>', learn_view.deleteuser1, name="deleteuser1"),#删除用户
    path('delete', learn_view.deleteuser, name="deleteuser"),
    path('manage/', learn_view.manage, name="manage"),  # 管理用户
    # path('changepe1/<int:a>', learn_view.changepe, name="changepe1"),#修改用户权限
    path('404/', learn_view.page_not_found, name="404"),  # 404页面

]