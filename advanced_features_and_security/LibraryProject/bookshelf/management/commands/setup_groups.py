from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create groups and assign permissions for Book model'

    def handle(self, *args, **kwargs):
        # Define groups
        groups = ['Admins', 'Editors', 'Viewers']
        permissions = ['can_view', 'can_create', 'can_edit', 'can_delete']

        # Get the Book model content type
        book_ct = ContentType.objects.get_for_model(Book)

        # Create permissions if they don't exist
        for perm in permissions:
            Permission.objects.get_or_create(
                codename=perm,
                name=f'Can {perm.replace("can_", "")} book',
                content_type=book_ct
            )

        # Create groups and assign permissions
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            
            if group_name == 'Admins':
                # Admins get all permissions
                perms = Permission.objects.filter(content_type=book_ct)
            elif group_name == 'Editors':
                # Editors can create and edit
                perms = Permission.objects.filter(codename__in=['can_create', 'can_edit'])
            elif group_name == 'Viewers':
                # Viewers can only view
                perms = Permission.objects.filter(codename='can_view')
            
            group.permissions.set(perms)
            group.save()

        self.stdout.write(self.style.SUCCESS('Groups and permissions successfully created!'))
