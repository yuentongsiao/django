from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#性别
GENDER_CHOICES = ((1,'男'),
                  (0,'女'))
#用户类别
PERMISSION_CHOICES=((0,'administration'),
                    (1,'advisior'))

#用户点赞状态
LIKE_CHOICES=((0,'False'),
              (1,'True'))

#笔记类别
class noteClass(models.Model):
    class_id = models.PositiveSmallIntegerField(primary_key=True,verbose_name='class_id')
    class_name = models.CharField(max_length=30,null=True,unique=True)

    def __str__(self):
        return self.class_name

#用户信息
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    permission = models.SmallIntegerField(choices=PERMISSION_CHOICES,default=1)



    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.username

#标签云
class Tag(models.Model):
    tag_id = models.PositiveSmallIntegerField(primary_key=True,verbose_name='tag_id')
    tag_num = models.IntegerField(null=False,default=1)
    tag_name = models.CharField(max_length=20,null=True,unique=True)

    def __str__(self):
        return self.tag_name

#笔记信息
class Note(models.Model):
    title = models.CharField(max_length=50,null=True)
    classes = models.ForeignKey(noteClass,on_delete=models.CASCADE)
    uptime = models.DateField(auto_now_add=True, null=False)
    like = models.IntegerField(null=False,default=0)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE,null=True)
    content = models.CharField(max_length=9999, null=True)
    comment = models.CharField(max_length=100,null=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Note"



#笔记评论
class usercomment(models.Model):

    note_id = models.ForeignKey(Note,on_delete=models.CASCADE,null=True)
    user_id= models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(max_length=255,null=False)
    time = models.DateField(auto_now_add=True, null=False)
    id = models.IntegerField(primary_key=True)



# 个人笔记点赞
class thumb(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    done = models.IntegerField(default=0)


# 用户收藏笔记
class collection(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    done = models.IntegerField(default=0)


# 用户信息
class person(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    sex = models.SmallIntegerField(choices=GENDER_CHOICES,null=True,default=0)
    age = models.CharField(max_length=10, null=True,default=18)
    time = models.DateField(auto_now_add=True, null=True)
    phone = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=30, null=True)
    photo = models.ImageField(upload_to='photo', blank=True, null=True)
    about = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user_id.username

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "person"
