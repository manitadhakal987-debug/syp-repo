from django.db import models

class CurlCareRule(models.Model):
    RULE_TYPE_CHOICES = [
        ('porosity', 'Hair Porosity Rule'),
        ('curl_type', 'Curl Pattern Rule'),
        ('density', 'Strand Thickness / Density Rule'),
        ('scalp', 'Scalp Type Rule'),
        ('concern', 'Hair Concern Rule'),
    ]

    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    rule_key = models.CharField(max_length=50, help_text="e.g. 'low', 'high', '3B', 'fine', 'frizz'")
    title = models.CharField(max_length=200)
    summary = models.TextField()
    cleansing_advice = models.TextField(blank=True)
    conditioning_advice = models.TextField(blank=True)
    styling_advice = models.TextField(blank=True)
    ingredients_recommended = models.CharField(max_length=255, blank=True, help_text="Comma-separated ingredients to seek")
    ingredients_to_avoid = models.CharField(max_length=255, blank=True, help_text="Comma-separated ingredients to avoid")
    priority = models.IntegerField(default=10)

    class Meta:
        ordering = ['priority', 'rule_type']

    def __str__(self):
        return f"[{self.get_rule_type_display()}] {self.title}"
