from django.contrib import admin, messages

# Register your models here.
from django.utils.html import format_html
from django.utils.translation import ngettext

from protfolio.models import General, About, Skills, Education, Project, WorkExperience, References

admin.site.site_header = "Kamruzzman's Portfolio Administration"
admin.site.index_title = "Kamruzzman's Portfolio"
admin.site.site_title = "Kamruzzman's Portfolio"


class GeneralAdmin(admin.ModelAdmin):
    # list_display = ['main_title', 'last_edited', 'mode', 'last_author', 'image_tag']

    @admin.action(description='Change Mode')
    def mode_button(self, request, queryset):
        if queryset.filter(mode='1'):
            updated_mode = queryset.update(mode='2')
        else:
            updated_mode = queryset.update(mode='1')
        self.message_user(request, ngettext(
            '%d mode was successfully changed',
            '%d mode was successfully changed .',
            updated_mode,
        ) % updated_mode, messages.SUCCESS)

    actions = [mode_button]

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'last_author'):
            obj.last_author = request.user
        obj.save()

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 200px; height:100px;" />'.format(obj.hero_image_field.url))

    image_tag.short_description = 'Homepage Image'
    image_tag.allow_tags = True


admin.site.register(General, GeneralAdmin)


class AboutAdmin(admin.ModelAdmin):
    list_display = ['short_about', 'last_edited', 'last_author', 'image_tag']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'last_author'):
            obj.last_author = request.user
        obj.save()

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 70px; height:70px;" />'.format(obj.about_body_image.url))

    image_tag.short_description = 'About Body Image'
    image_tag.allow_tags = True


admin.site.register(About, AboutAdmin)

admin.site.register(Skills)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(WorkExperience)
admin.site.register(References)
