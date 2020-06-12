from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from learn.Forms import LoginForm, RegistrationForm, PwdChangeForm
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from learn.models import UserProfile, Note, noteClass, usercomment, thumb, collection, Tag, person
from learn.utility import permission_check


# 首页
def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse('learn:sign'))
    else:
        note = Note.objects.order_by("-uptime")
        comment = usercomment.objects.order_by("-time")
        count = Note.objects.all().count()
        classes = noteClass.objects.all()
        context = {'note': note, 'comment': comment, 'classes': classes, 'count': count}
        return render(request, 'learn/home.html', context)


# 用户登录
def sign(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                    auth.login(request,user)
                    people = person.objects.filter(user_id=user)
                    print(people)
                    if people:
                        if user.is_superuser:
                            return render(request, "learn/manageUsers.html")
                        else:
                            return redirect(reverse('learn:home'))  #如果不是第一次登陆 就跳转到首页
                    else:
                        people = person.objects.create(user_id=user)
                        people.save()
                        return redirect(reverse('learn:editPersonData')) #如果是注册后第一次登陆 要先填个人资料
            else:
                return render(request, 'learn/sign.html', {'form': form, 'message': 'Wrong password. Please try again.'})
        else:# 登陆失败
            return render(request, 'learn/sign.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'learn/sign.html', {'form': form})

#管理用户
def manage(request):
    return render(request, "learn/deleteuser.html")


#删除用户
def deleteuser1(request,a):
    user=User.objects.get(id=a);
    userprofile=UserProfile.objects.filter(user_id=user)
    userprofile.delete()
    people = person.objects.filter(user_id=user)
    people.delete()
    user.delete()
    user1 = User.objects.all();
    return render(request, "learn/deleteuser.html", {'user': user1})


def deleteuser(request):
    user=User.objects.all();
    return render(request, "learn/deleteuser.html", {'user': user})


def adduser(request):
    if request.method=='POST':
        name = request.POST.get("ruser")
        query = User.objects.filter(username=name)
        pwd = request.POST.get("rpwd")
        pwd1 = request.POST.get("rcpwd")
        if pwd == pwd1:
            user = User.objects.create_user(username=name, password=pwd,is_superuser=1)
            user.save()
            count = 1
            num = UserProfile.objects.all()
            for item in num:
                print(count)
                if count == item.profile_id:
                    count = count + 1
                else:
                    break
            userprofile = UserProfile.objects.create(user_id=user.id, profile_id=count)
            userprofile.save()
        user = User.objects.all();
        return render(request, "calc/selfInfo.html", {'user': user})
    else:
        user=User.objects.all();
        return render(request, "calc/adduser.html", {'user': user})

def changepe(request,a):
    user=User.objects.get(id=a);
    user.is_superuser=1
    user.save()
    user = User.objects.all();
    return render(request, "learn/changepermission.html",{'user': user})



def selfInfo(request,a):
     return render(request, "learn/manageUsers.html",{'user':a})

# 用户退出
@login_required
def out(request):
    auth.logout(request)  # 清除当前用户的session信息
    return redirect(reverse('learn:sign'))

# 用户注册
def join(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password, email=email)
            # 如果直接使用objects.create()方法后不需要使用save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect("/sign/")
    else:
        form = RegistrationForm()

    return render(request, 'learn/join.html', {'form': form})



# 修改密码(只有pyt登录的用户才能够修改)
@login_required
def pwd_change(request):
    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['old_password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return redirect(reverse('learn:sign'))

            else:                            #修改密码页面
                return render(request, 'learn/pwd_change.html', {'form': form, 'user': user, 'message': '旧密码输入错误，重新输入！'})
    else:
        form = PwdChangeForm()
    return render(request, 'learn/pwd_change.html', {'form': form})


# 笔记列表
def list(request,a):
    result = noteClass.objects.all()
    tags = Tag.objects.all()
    comment = usercomment.objects.order_by("-time")
    detail = User.objects.get(id=a)
    print("detail",detail.id)
    res={'result':result,'detail':detail.id, 'tags':tags, 'comment':comment}
    return render(request,'learn/list.html',res)


# 笔记类别
def classificationInfo(request,a,b):
    notes = Note.objects.filter(classes_id=b)
    user_id = a

    tags = Tag.objects.all()
    comment = usercomment.objects.order_by("-time")
    context = {'notes':notes,'user_id':user_id, 'tags':tags, 'comment':comment}
    return render(request, 'learn/classification.html',context)


# 笔记内容
def noteContent(request,a,b):
    user_id = a
    content = Note.objects.get(id=b)
    if request.user.username == content.user_id.username:
        result = True
    else :
        result=False
    comm=usercomment.objects.filter(note_id=b)
    comment = usercomment.objects.order_by("-time")
    count = Note.objects.all().count()
    print(content)
    context = {'note':content,'comm':comm,'user_id':user_id,'comment':comment,'count':count, 'result':result}
    return render(request, 'learn/noteContent.html',context)


# 个人点赞排行
def bigThumb(request):
    if not request.user.is_authenticated:
        return render(request,'learn/signFirst.html')
    else:
        # if request.method == 'GET':
        #     thumb = Note.objects.all().order_by("like")
        #     return render(request, 'learn/bigThumb.html', {"content": thumb})
        # else:

        tags = Tag.objects.all()
        comment = usercomment.objects.order_by("-time")

        thumb = Note.objects.all().order_by("-like")
        context = {'content':thumb,'tags':tags,'comment':comment}
        return render(request, 'learn/bigThumb.html',context)


# 添加笔记
def addInfo(request):
    if not request.user.is_authenticated:
        return render(request,'learn/signFirst.html')
    else:
        if request.method == 'POST':
            number = request.POST.get('num')
            title = request.POST.get('title')
            tag = request.POST.get('tag')
            classification = request.POST.get('class')
            content = request.POST.get('content')
            obj=noteClass.objects.filter(class_name=classification)
            obj1=Tag.objects.filter(tag_name=tag)

            if not obj:
                count = noteClass.objects.all().count()+1
                x = noteClass.objects.create(class_id=count,class_name=classification)
                obj = x
                class_id = obj.class_id

                if not obj1:
                    num = Tag.objects.all().count() + 1
                    t = Tag.objects.create(tag_id=num, tag_name=tag)
                    # tag_id = t.tag_id
                    k = Note.objects.create(id=number, title=title, tag=t, content=content, classes_id=class_id,user_id=request.user)
                    k.save()
                else:
                    obj1[0].tag_num = obj1[0].tag_num + 1
                    obj1[0].save()
                    tag_id = obj1[0].tag_id
                    t = Tag.objects.get(tag_id=tag_id)
                    k = Note.objects.create(id=number, title=title, tag=t, content=content, classes_id=class_id,user_id=request.user)
                    k.save()

            else:
                class_id = obj[0].class_id

                if not obj1:
                    num = Tag.objects.all().count() + 1
                    t = Tag.objects.create(tag_id=num, tag_name=tag)
                    k = Note.objects.create(id=number, title=title, tag=t, content=content, classes_id=class_id,user_id=request.user)
                    k.save()
                else:
                    obj1[0].tag_num = obj1[0].tag_num + 1
                    obj1[0].save()
                    tag_id = obj1[0].tag_id
                    t = Tag.objects.get(tag_id=tag_id)
                    k = Note.objects.create(id=number, title=title, tag=t, content=content, classes_id=class_id,user_id=request.user)
                    k.save()
            return redirect(reverse('learn:home'))
        else:
            noteQuery = Note.objects.all()
            count2 = 1
            for item in noteQuery:
                if item.id == count2:
                    count2 = count2 + 1
                else:
                    break

            cla = Note.objects.all()
            nowNoteCount = Note.objects.all().count()
            return render(request, 'learn/addInfo.html', {'count': count2,"cla":cla,'nowNoteCount':nowNoteCount})


# 查询笔记信息
def searchInfo(request):

    dropdown = request.POST.get('dropdown')
    keyword = request.POST.get('keyword')

    tags = Tag.objects.all()
    comment = usercomment.objects.order_by("-time")

    context = {}

    if dropdown == 'title':
        info = Note.objects.filter(title=keyword)
        if info:
            context = {'note': info,'tags':tags,'comment':comment,'dropdown':"标题",'keyword':keyword}
        else:
            context = {'info': "很抱歉，没有找到这个标题",'tags':tags,'comment':comment,'dropdown':"标题",'keyword':keyword}
    if dropdown == 'tag':
        tag = Tag.objects.filter(tag_name=keyword)
        if tag:
            if tag[0].tag_num == 0:
                context = {'info': "很抱歉，没有找到这个标签",'tags':tags,'comment':comment,'dropdown':"标签",'keyword':keyword}
            info = Note.objects.filter(tag=tag[0])
            context = {'note': info,'tags':tags,'comment':comment,'dropdown':"标签",'keyword':keyword}
        else:
            context = {'info': "很抱歉，没有找到这个标签",'tags':tags,'comment':comment,'dropdown':"标签",'keyword':keyword}

    if dropdown == 'class':
        cla = noteClass.objects.filter(class_name=keyword)
        if cla:
            class_id = cla[0].class_id
            info = Note.objects.filter(classes_id=class_id)
            context = {'note': info,'tags':tags,'comment':comment,'dropdown':"类别",'keyword':keyword}
        else:
            context = {'info': "很抱歉，没有找到这个类别",'tags':tags,'comment':comment,'dropdown':"类别",'keyword':keyword}

    if keyword=="":
        context={"info":"输入框中空空如也~",'tags':tags,'comment':comment,'dropdown':"类别",'keyword':keyword}

    return render(request,"learn/searchInfo.html",context)


# 删除笔记
def delNote(request):
    id = request.GET.get("id")
    note = Note.objects.get(id=id)
    note.delete()

    tag_id = note.tag_id
    tag = Tag.objects.get(tag_id=tag_id)
    tag.tag_num = tag.tag_num -1
    tag.save()

    note_id = note.id
    thumb0 = thumb.objects.filter(note_id=note_id)
    thumb0.delete()

    usercomment0 = usercomment.objects.filter(note_id=note_id)
    usercomment0.delete()

    return redirect(reverse('learn:home'))


# 修改编辑笔记
def editNote(request):
    if request.method == 'GET':
        note_id = request.GET.get("id")
        note = Note.objects.get(id=note_id)
        tags = Tag.objects.all()
        comment = usercomment.objects.order_by("-time")
        context = {'note':note,'tags':tags,'comment':comment}
        return render(request,'learn/editNote.html',context)
    if request.method == 'POST':
        noteId = request.POST.get('id')
        note = Note.objects.get(id=noteId)
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')

        tag_name = request.POST.get('tag')
        if tag_name != note.tag.tag_name :

            before_tag = Tag.objects.get(tag_id=note.tag.tag_id)
            before_tag.tag_num = before_tag.tag_num - 1
            # if before_tag.tag_num == 0:
            #     before_tag.delete()
            # else:
            before_tag.save()

            tag = Tag.objects.filter(tag_name=tag_name)
            if not tag:
                num = Tag.objects.all().count() + 1
                t = Tag.objects.create(tag_id=num, tag_name=tag_name)
                t.save()
                note.tag = t
                note.save()
            else:
                tag[0].tag_num = tag[0].tag_num + 1
                tag[0].save()
                note.tag = tag[0]
                note.save()
        else:
            note.save()

        # context = {'note':note}
        return redirect(reverse('learn:home'))
    return render(request,'learn/home.html')


# 点赞
def like(request):
    like = request.POST.get("like")
    class_id = request.POST.get("id")#笔记号数
    user_id = request.POST.get("user")
    note = Note.objects.get(id=class_id)
    user = User.objects.get(id=user_id)
    query = thumb.objects.filter(note_id=note,user_id=user)

    if not query:
        thumbQuery = thumb.objects.all()
        count2 = 1
        for item in thumbQuery:
            if item.id == count2:
                count2 = count2 + 1
            else:
                break
        thumb.objects.create(id=count2,note_id=note,user_id=user)
        query = thumb.objects.filter(note_id=note, user_id=user)

    if query[0].done==1:

            like=int(like)-1
            query[0].done=0
            query[0].save()

            print(query[0].done)
            note = Note.objects.get(id=class_id)
            data = like
            note.like = data
            note.save()
            return HttpResponse(data,query[0].done)
    elif query[0].done==0:

            query[0].done=1
            query[0].save()
            print(query[0].done)
            like = int(like) + 1
            note = Note.objects.get(id=class_id)
            data = like
            note.like = data
            note.save()

            return HttpResponse(data,query[0].done)
    return HttpResponse(1,1)


# 评论
def comment(request):
    content = request.POST.get("content")
    class_id = request.POST.get("id")  # 笔记号数
    user_id = request.POST.get("user")
    note = Note.objects.get(id=class_id)
    user = User.objects.get(id=user_id)
    userComment = usercomment.objects.all()
    count2 = 1
    for item in userComment:
        if item.id == count2:
            count2 = count2 + 1

        else:
            break
    new = usercomment.objects.create(user_id=user, note_id=note,content=content,id=count2)
    return HttpResponse("评论成功")


# 收藏笔记
def collect(request):
    if request.method == 'POST':
        class_id = request.POST.get("id")  # 笔记号数
        user_id = request.POST.get("user")
        note = Note.objects.get(id=class_id)
        user = User.objects.get(id=user_id)

        query = collection.objects.filter(note_id=note,user_id=user_id)

        if query:
            if query[0].done == 0:
                query[0].done = 1
                query[0].save()
            else:
                query[0].done = 0
                query[0].save()
        else:
            collect = collection.objects.all()
            count2 = 1

            for item in collect:
                if item.id == count2:
                    count2 = count2 + 1
                else:
                    break
            query = collection.objects.create(user_id=user, note_id=note,done=1, id=count2)
        if query[0].done == 1:
             return HttpResponse("收藏成功")
        else:
            return HttpResponse("取消收藏")
    if request.method == 'GET':
        collect = collection.objects.all()
        tags = Tag.objects.all()
        comment = usercomment.objects.order_by("-time")
        context = {'collect': collect,'tags':tags,'comment':comment}
        return render(request,'learn/collect.html',context)


def myNote(request):
    note = Note.objects.all()
    tags = Tag.objects.all()
    comment = usercomment.objects.order_by("-time")
    context = {'note': note, 'tags': tags, 'comment': comment}
    return render(request,"learn/myNote.html",context)


# def share(request):
#     return render(request,"learn/home.html")


# 个人主页
def personData(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    people = person.objects.get(user_id=user)
    count = Note.objects.all().count()
    comment = usercomment.objects.order_by("-time")
    context = {'person':people,'count':count,'comment':comment}
    return render(request,'learn/personData.html',context)


# 完善个人资料
def editPersonData(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        time = request.POST.get('time')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        about = request.POST.get('about')
        photo = request.FILES.get('photo')
        people = person.objects.get(user_id=user)
        people.sex = sex
        people.age = age
        people.time = time
        people.phone = phone
        people.email = email
        people.about = about
        people.photo = photo
        people.save()
        return redirect(reverse('learn:personData'))
    else:
        # people1 = person.objects.filter(user_id=user)
        # if not people1:
        #     people = person.objects.create(user_id=user)
        people = person.objects.get(user_id=user)
        count = Note.objects.all().count()
        comment = usercomment.objects.order_by("-time")
        context = {'person':people,'count':count,'comment':comment}
        return render(request,'learn/editPersonData.html',context)



# 提示请登录/注册页面
def signFirst(request):
    return render(request,'learn/signFirst.html')



# 404页面找不到
def page_not_found(request):
   return render(request,'learn/404.html')

