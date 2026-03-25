import uuid

from django.db import migrations, models


def populate_share_tokens(apps, schema_editor):
    FloorPlan = apps.get_model("catalog", "FloorPlan")
    AvailableHome = apps.get_model("catalog", "AvailableHome")

    for plan in FloorPlan.objects.filter(share_token__isnull=True):
        plan.share_token = uuid.uuid4()
        plan.save(update_fields=["share_token"])

    for home in AvailableHome.objects.filter(share_token__isnull=True):
        home.share_token = uuid.uuid4()
        home.save(update_fields=["share_token"])


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_community_share_banner_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="floorplan",
            name="info_sections",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="floorplan",
            name="share_banner_image",
            field=models.ImageField(blank=True, null=True, upload_to="plans/share_banners/"),
        ),
        migrations.AddField(
            model_name="floorplan",
            name="share_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="floorplan",
            name="share_token",
            field=models.UUIDField(blank=True, db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="availablehome",
            name="info_sections",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="availablehome",
            name="share_banner_image",
            field=models.ImageField(blank=True, null=True, upload_to="homes/share_banners/"),
        ),
        migrations.AddField(
            model_name="availablehome",
            name="share_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="availablehome",
            name="share_token",
            field=models.UUIDField(blank=True, db_index=True, editable=False, null=True),
        ),
        migrations.RunPython(populate_share_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="floorplan",
            name="share_token",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="availablehome",
            name="share_token",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
