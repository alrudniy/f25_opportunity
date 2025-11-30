from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = 'student', 'Student'
        ORGANIZATION = 'organization', 'Organization'
        # ADMINISTRATOR = 'administrator', 'Administrator' # 暂时移除，根据需求添加

    user_type = models.CharField(
        max_length=15,
        choices=UserType.choices,
        default=UserType.STUDENT,
    )

    # 个人资料字段，可以直接在 User 模型中管理
    # 注意：Django 的 AbstractUser 已经包含了 first_name 和 last_name，
    # 这里我们只是确保它们在模型定义中可见，并且可以被表单编辑。
    # 如果需要更复杂的个人资料管理，可以考虑使用单独的 Profile 模型。
    # first_name = models.CharField(_('first name'), max_length=150, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    class_year = models.CharField(max_length=4, blank=True, null=True) # e.g., "2025", "2026"

    # email 字段在 AbstractUser 中已经存在，并且默认是 unique=True
    # 如果您想让 email 作为登录用户名，需要修改 AUTH_USER_MODEL 和 LOGIN_URL 等设置
    # 并可能需要调整 REQUIRED_FIELDS
    # email = models.EmailField(_('email address'), unique=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username'] # 如果 email 是 USERNAME_FIELD，则 username 可能不再是必需的，或者需要调整

    def save(self, *args, **kwargs):
        # 如果是新用户且 user_type 未设置，则默认设置为 STUDENT
        if not self.pk and not self.user_type:
            self.user_type = self.UserType.STUDENT
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        # 优先显示 first_name 和 last_name，如果为空则显示 username
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

# 如果您更倾向于使用一个单独的 Profile 模型，可以取消注释以下代码块：
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     university = models.CharField(max_length=255, blank=True, null=True)
#     class_year = models.CharField(max_length=4, blank=True, null=True) # e.g., "2025", "2026"
#
#     def __str__(self):
#         return f"{self.user.display_name}'s Profile"

