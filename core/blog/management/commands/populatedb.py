import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category

category_lists = [
    "IT",
    "Design",
    "Fun",
]


class Command(BaseCommand):
    help = "Populate legacy database using Faker"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker_obj = Faker()

    def handle(self, *args, **options):
        # --- 1. ایجاد کاربر (User) ---
        username = self.faker_obj.user_name()
        email = self.faker_obj.email()

        # بررسی وجود کاربر در دیتابیس legacy
        if User.objects.using("legacy").filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"User with username '{username}' already exists in legacy DB. Skipping user creation."
                )
            )
            user = User.objects.using("legacy").get(username=username)
        else:
            user = User(
                username=username,
                email=email,
            )
            user.set_password("Test@12345")  # رمز عبور تست، در محیط پروداکشن امن نیست
            # ذخیره کاربر در دیتابیس legacy
            user.save(using="legacy")
            self.stdout.write(
                self.style.SUCCESS(f"Created user: {user.email} in legacy DB")
            )

        # --- 2. ایجاد یا به‌روزرسانی پروفایل کاربر (Profile) ---
        # فرض می‌کنیم Profile مدل دارای OneToOneField به User با نام 'user' است
        try:
            # جستجو و ایجاد پروفایل در دیتابیس legacy
            profile, created = Profile.objects.using("legacy").get_or_create(user=user)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created profile for {user.email} in legacy DB")
                )
        except Profile.DoesNotExist:
            # اگر پروفایل پیدا نشد و get_or_create هم نتوانست بسازد (که نباید اتفاق بیفتد اگر get_or_create درست کار کند)
            self.stderr.write(
                self.style.ERROR(
                    f"Profile does not exist for user {user.email} in legacy DB and could not be created."
                )
            )
            return  # خروج اگر پروفایل حیاتی است و ساخته نشد

        profile.first_name = self.faker_obj.first_name()
        profile.last_name = self.faker_obj.last_name()
        profile.bio = self.faker_obj.paragraph(nb_sentences=1)
        # ذخیره پروفایل در دیتابیس legacy
        profile.save(using="legacy")
        self.stdout.write(f"Updated profile for {user.email} in legacy DB")

        # --- 3. ایجاد دسته‌بندی‌ها (Categories) ---
        categories = []
        for cat_name in category_lists:
            # ایجاد یا دریافت دسته‌بندی در دیتابیس legacy
            category, created = Category.objects.using("legacy").get_or_create(
                name=cat_name
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {cat_name} in legacy DB")
                )
            categories.append(category)

        # اطمینان از وجود دسته‌بندی‌ها قبل از ساخت پست
        if not categories:
            self.stderr.write(
                self.style.ERROR(
                    "No categories found or created in legacy DB. Cannot create posts."
                )
            )
            return

        # --- 4. ایجاد پست‌های ساختگی (Posts) با استفاده از حلقه ---
        num_posts_to_create = 4  # تعداد پست‌ها
        posts_to_bulk_create = []
        for _ in range(num_posts_to_create):
            posts_to_bulk_create.append(
                Post(
                    title=self.faker_obj.catch_phrase(),
                    body=self.faker_obj.paragraph(nb_sentences=3),
                    category=random.choice(categories),
                    status=random.choice([True, False]),
                    author=profile,
                    published=self.faker_obj.date_time_between(
                        timezone.datetime(2017, 1, 5), timezone.datetime(2025, 1, 5)
                    ),
                )
            )

        # ایجاد دسته‌ای پست‌ها در دیتابیس legacy
        if posts_to_bulk_create:
            Post.objects.using("legacy").bulk_create(posts_to_bulk_create)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {len(posts_to_bulk_create)} fake posts in legacy DB."
                )
            )
        else:
            self.stdout.write("No posts were generated.")
