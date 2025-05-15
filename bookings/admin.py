from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Gym, Booking, Hall

# 🔒 Кастомный UserAdmin
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)

# 🏋️ Спортзал
admin.site.register(Gym)

# 📅 Бронирование
admin.site.register(Booking)

# 🏟️ Зал внутри спортзала
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'capacity', 'type', 'description')
    search_fields = ('name', 'gym__name')
    list_filter = ('gym', 'type')
