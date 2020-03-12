from django.db import models

# Create your models here.
import uuid
from django.apps import apps
from django.utils import timezone
from coreapp.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser


class AbstractBaseModel(models.Model):
    # abstract model with basic necessary fields to be included in all models
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True,)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return str(self.id)

    def get_connectedsellingplatform(self):
        ConnectedSellingPlatform = apps.get_model(
            "dashboard", "ConnectedSellingPlatform"
        )
        return ConnectedSellingPlatform.objects.get(user=self)

    def get_active_workspace_membership(self):
        try:
            return WorkspaceMember.objects.get(user=self)
        except Exception as e:
            print(f"Error in getting workspace: {e}")

    def create_new_user_supporting_objects(self):
        workspace = Workspace.objects.create()
        workspacemember = WorkspaceMember.objects.create(
            workspace=workspace, user=self, is_admin=True, is_active=True
        )

    def create_workspace(self):
        workspace = Workspace.objects.create(user=self)
        workspacemember = WorkspaceMember.objects.create(
            user=self, workspace=workspace, is_admin=True
        )


class Workspace(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class WorkspaceMemberInvite(AbstractBaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    invitee = models.EmailField()
    accepted = models.BooleanField(default=False)

    def is_used(self):
        return WorkspaceMember.objects.filter(workspacememberinvite=self).exists()


class WorkspaceMember(AbstractBaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    workspacememberinvite = models.ForeignKey(
        WorkspaceMemberInvite, blank=True, null=True, on_delete=models.CASCADE
    )
