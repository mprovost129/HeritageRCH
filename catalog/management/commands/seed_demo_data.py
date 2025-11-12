# ──────────────────────────────────────────────────────────────────────────────
# scripts/seed_demo_data.py (quick seed for admin testing)
# ──────────────────────────────────────────────────────────────────────────────
from django.core.management.base import BaseCommand
from catalog.models import Amenity, Community, FloorPlan, AvailableHome, CommunityStatus

class Command(BaseCommand):
    help = "Seed a few demo records for Heritage RCH"

    def handle(self, *args, **opts):
        # Amenities
        a_names = ["Walking Trails", "Playground", "Sidewalks", "Open Space"]
        amenities = [Amenity.objects.get_or_create(name=n)[0] for n in a_names]

        c, _ = Community.objects.get_or_create(
            slug="eastwood-estates",
            defaults=dict(
                name="Eastwood Estates",
                city="Attleboro",
                state="MA",
                status=CommunityStatus.ACTIVE,
                description="A charming community near local amenities.",
            ),
        )
        c.amenities.set(amenities)

        p, _ = FloorPlan.objects.get_or_create(
            slug="harborview",
            defaults=dict(name="Harborview", beds=3, baths=2.5, sq_ft_min=1800, sq_ft_max=2200),
        )
        p.available_in.add(c)

        h, _ = AvailableHome.objects.get_or_create(
            slug="lot-12-eastwood",
            defaults=dict(
                community=c,
                plan=p,
                address_1="12 Eastwood Way",
                city="Attleboro",
                state="MA",
                postal_code="02703",
                beds=3,
                baths=2.5,
                sq_ft=1950,
                price=689000,
                description="Under construction, ready soon.",
            ),
        )
        self.stdout.write(self.style.SUCCESS("Seeded demo data."))