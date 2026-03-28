from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- ПРОФІЛЬ КОРИСТУВАЧА ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=100, verbose_name="По батькові", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Номер телефону", blank=True)
    address = models.CharField(max_length=255, verbose_name="Адреса доставки", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Місто", blank=True, null=True)

    def __str__(self):
        return f"Профіль {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


# --- КАТЕГОРІЇ ---
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категорії"


# --- ТОВАРИ ---
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    brand = models.CharField(max_length=100, verbose_name="Бренд", default="Vaporesso")
    sku = models.CharField(max_length=50, verbose_name="Артикул", blank=True)
    description = models.TextField(verbose_name="Опис", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна (грн)")
    image = models.ImageField(upload_to='products/', verbose_name="Фото товару", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="У наявності")
    
    # Зв'язки між товарами
    compatible_products = models.ManyToManyField(
        'self', 
        blank=True, 
        symmetrical=False, 
        related_name='compatible_with', 
        verbose_name="Супутні товари (картриджі тощо)"
    )
    similar_products = models.ManyToManyField(
        'self', 
        blank=True, 
        symmetrical=False, 
        related_name='similar_to', 
        verbose_name="Схожі товари"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Товари"


# --- ВАРІАНТИ (Кольори/Смаки) ---
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Назва (Колір/Смак)")
    image = models.ImageField(upload_to='products/variants/', blank=True, null=True, verbose_name="Фото варіації")

    def __str__(self):
        return f"{self.product.name} - {self.name}"


# --- ЗАМОВЛЕННЯ ---
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_label = models.CharField(max_length=255, blank=True)
    birthday_verification_required = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Нове')

    def __str__(self):
        return f"Замовлення №{self.id} від {self.first_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
