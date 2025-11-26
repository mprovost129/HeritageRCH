# pages/models.py
from django.db import models


class SiteSettings(models.Model):
    """
    Singleton-style model for global site content:
    phone, email, hero text, CTA text, and lead recipients.
    """

    site_name = models.CharField(
        max_length=200,
        default="Heritage Realty & Custom Homes",
        help_text="Displayed in browser titles and meta where needed.",
    )

    primary_phone = models.CharField(
        max_length=32,
        blank=True,
        help_text="Main phone number (for header / CTA). Example: 508-555-1234",
    )
    primary_phone_link = models.CharField(
        max_length=32,
        blank=True,
        help_text="Phone in tel: format. Example: 15085551234",
    )

    # Public contact email (can be shown on Contact page / footer)
    primary_email = models.EmailField(
        blank=True,
        help_text="Main contact email shown publicly (if desired).",
    )

    # Lead notification recipients (used for ALL website contact emails)
    lead_recipients = models.TextField(
        blank=True,
        help_text=(
            "One or more email addresses to receive website leads. "
            "Separate multiple addresses with commas or new lines."
        ),
    )

    # Home hero content
    hero_headline = models.CharField(
        max_length=200,
        blank=True,
        help_text="Homepage hero headline.",
    )
    hero_subheadline = models.TextField(
        blank=True,
        help_text="Homepage hero supporting text.",
    )

    # Global CTA strip content
    cta_heading = models.CharField(
        max_length=200,
        blank=True,
        help_text="CTA strip heading. Example: 'Ready to get started?'",
    )
    cta_body = models.TextField(
        blank=True,
        help_text="CTA strip short paragraph under the heading.",
    )

    cta_phone_label = models.CharField(
        max_length=50,
        blank=True,
        help_text="Label for the phone button. Example: 'Call Us'",
    )

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self) -> str:
        return "Site Settings"

    @classmethod
    def get_solo(cls):
        """
        Convenience method: always return the single settings row, or None.
        """
        return cls.objects.first()