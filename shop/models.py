from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, default='bi-droplet', help_text="Bootstrap icon name, e.g. bi-droplet")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SuitabilityTag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    badge_color = models.CharField(max_length=30, default='success', help_text="Bootstrap color class e.g. success, info, warning")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Nepalese Rupees (NPR)")
    stock = models.PositiveIntegerField(default=25)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, help_text="Fallback photo URL")
    size = models.CharField(max_length=50, blank=True, help_text="e.g. 355ml, 250g")
    
    # Ingredient transparency
    ingredients_list = models.TextField(help_text="Full INCI ingredient breakdown")
    key_actives = models.CharField(max_length=255, blank=True, help_text="e.g. Shea Butter, Jamaican Black Castor Oil, Flaxseed")
    
    # Suitability filters
    suitable_curl_types = models.CharField(
        max_length=150,
        default='2A,2B,2C,3A,3B,3C,4A,4B,4C',
        help_text="Comma-separated curl types: 2A,2B,3A,3B,3C,4A,4B,4C"
    )
    suitable_porosity = models.CharField(
        max_length=50,
        default='low,medium,high',
        help_text="Comma-separated porosity: low,medium,high"
    )
    suitability_tags = models.ManyToManyField(SuitabilityTag, blank=True, related_name='products')
    
    usage_instructions = models.TextField(blank=True, help_text="Step-by-step application method for curly hair")
    nepal_availability_note = models.CharField(
        max_length=255,
        default="Express Delivery within Kathmandu Valley (1-2 days) & Nepal-wide courier",
        help_text="Nepal availability & delivery guarantee"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.name} (NPR {self.price})"

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "/static/images/product-placeholder.jpg"

    @property
    def in_stock(self):
        return self.is_available and self.stock > 0

class HaircutGuide(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    suitable_curls = models.CharField(max_length=150, help_text="e.g. 2B to 3C waves & curls")
    face_shapes = models.CharField(max_length=150, help_text="e.g. Oval, Round, Heart, Diamond")
    description = models.TextField()
    nepal_salon_advice = models.TextField(
        help_text="Exact instructions to give your hairstylist in Nepal (e.g. avoiding thinning shears, cutting dry, shrinkage caution)"
    )
    maintenance_guide = models.TextField(help_text="How to refresh and style this haircut day-to-day")
    image_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
