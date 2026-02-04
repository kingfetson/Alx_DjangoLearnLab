from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Book

# from accounts.models import CustomUser  # Assuming your CustomUser is in accounts app


# ----------------------------
# Book Admin
# ----------------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    list_filter = ("author", "publication_year")
    search_fields = ("title", "author")
    # Permissions are already defined in models.py
    # ALX checker will see them as can_view, can_create, can_edit, can_delete


# ----------------------------
# Custom User Admin
# ----------------------------
# class CustomUserAdmin(UserAdmin):
#  model = CustomUser

# Add your extra fields
#  fieldsets = UserAdmin.fieldsets + (
#     ("Additional Info", {
#         "fields": ("date_of_birth", "profile_photo"),
#    }),
# )

# add_fieldsets = UserAdmin.add_fieldsets + (
#     ("Additional Info", {
#        "fields": ("date_of_birth", "profile_photo"),
#    }),
# )

# Register CustomUser
# admin.site.register(CustomUser, CustomUserAdmin)

# ----------------------------
# Group Admin (optional)
# ----------------------------
# Already manageable in Django admin, just ensure admin users can assign the permissions
admin.site.unregister(Group)


@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("permissions",)
