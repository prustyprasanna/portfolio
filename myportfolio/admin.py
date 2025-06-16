from django.contrib import admin
from django.utils.html import format_html
from .models import Register, Intro, Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_email', 'industry', 'company_size', 'created_at']
    search_fields = ['company_name', 'company_email', 'industry']
    list_filter = ['industry', 'company_size', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    def save_model(self, request, obj, form, change):
        print(f"Saving company in admin: {obj.company_name}")
        super().save_model(request, obj, form, change)

# Keep your existing admin registrations
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']

@admin.register(Intro)
class IntroAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user_email', 'tagline', 'location', 'display_profile_picture', 'created_at']
    list_filter = ['location', 'created_at']
    search_fields = ['full_name', 'user__email', 'tagline', 'about_me']
    readonly_fields = ['created_at', 'display_profile_picture']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'tagline', 'about_me', 'location')
        }),
        ('Media', {
            'fields': ('profile_picture', 'display_profile_picture', 'resume')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Social Links', {
            'fields': ('linkedin', 'github', 'twitter', 'website')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        })
    )

    @admin.display(description='User Email')
    def user_email(self, obj):
        return obj.user.email if obj.user else '-'

    @admin.display(description='Profile Picture')
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', 
                             obj.profile_picture.url)
        return "No picture"

    def save_model(self, request, obj, form, change):
        print(f"Saving portfolio for user: {obj.user}")
        super().save_model(request, obj, form, change)
        print(f"Portfolio saved successfully with ID: {obj.pk}")
