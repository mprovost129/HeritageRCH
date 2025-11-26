from django.db import models


class SiteSettings(models.Model):
    """
    Singleton-style model for global site content:
    phone, email, hero text, CTA text, lead recipients, office address,
    and marketing blurbs for key pages.
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

    # Office address (shown on Contact page / footer)
    address_line1 = models.CharField(
        max_length=255,
        blank=True,
        help_text="Office street address line 1.",
    )
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        help_text="Office street address line 2 (optional).",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="Office city.",
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        help_text="Office state.",
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="Office ZIP / postal code.",
    )

    # Home hero content
    hero_background = models.ImageField(
        upload_to="site/hero/",
        blank=True,
        null=True,
        help_text="Homepage hero background image.",
    )
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

    # Page intro blurbs (list pages)
    communities_intro = models.TextField(
        blank=True,
        help_text="Intro text shown at the top of the Communities page.",
    )
    plans_intro = models.TextField(
        blank=True,
        help_text="Intro text shown at the top of the Floor Plans page.",
    )
    homes_intro = models.TextField(
        blank=True,
        help_text="Intro text shown at the top of the Available Homes page.",
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


class Announcement(models.Model):
    """
    Sitewide announcement / promo bar that can be toggled on/off from admin.
    Example: 'Open House this Sunday at Eastwood Estates from 12–2pm!'
    """

    title = models.CharField(
        max_length=200,
        help_text="Short label for the announcement (internal or small heading).",
    )
    message = models.TextField(
        help_text="Main announcement text shown in the bar.",
    )
    button_label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional button label. Example: 'Learn More' or 'View Details'.",
    )
    button_url = models.URLField(
        blank=True,
        help_text="Optional URL for the button. Can be an internal or external link.",
    )

    is_active = models.BooleanField(
        default=False,
        help_text="If checked, this announcement may be shown on the site.",
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated",)
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self) -> str:
        return self.title
