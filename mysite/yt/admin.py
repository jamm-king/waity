from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Channel)
admin.site.register(Tag)
admin.site.register(KingTag)
admin.site.register(BoardMember)
admin.site.register(Comment)
admin.site.register(Category)


class UpdateAdmin(admin.ModelAdmin):

    list_display = ['tag', 'address_name', 'kingtag']

    actions = ['Commit']

    def Commit(self, request, queryset):

        for i in queryset:
            channelSet = i.tag.tagged.all()
            new_item = KingTag()
            new_item.parentTag = i.kingtag
            new_item.address_name = i.address_name
            new_item.tag_name = i.tag.tag_name
            new_item.save()
            for channel in channelSet:
                channel.tag.add(new_item)
                if new_item.parentTag.tag_name != 'NOTHING':
                    channel.tag.add(new_item.parentTag)
                channel.save()
            i.tag.delete()
        self.message_user(request, 'Upgrade complete')

admin.site.register(Update, UpdateAdmin)

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title','writer','created_at','updated_at')

admin.site.register(Board,BoardAdmin)

