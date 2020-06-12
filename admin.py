from django.contrib import admin
from learn.models import noteClass,UserProfile,Note,Tag,usercomment,thumb,collection,person
# Register your models here.
admin.site.register(noteClass)
admin.site.register(UserProfile)
admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(usercomment)
admin.site.register(thumb)
admin.site.register(collection)
admin.site.register(person)
