# Generated manually to safely add unique UUID tokens for existing rows.
import uuid

from django.db import migrations, models


def populate_share_tokens(apps, schema_editor):
    Community = apps.get_model("catalog", "Community")
    for community in Community.objects.filter(share_token__isnull=True):
        community.share_token = uuid.uuid4()
        community.save(update_fields=["share_token"])


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_community_info_sections"),
    ]

    operations = [
        migrations.AddField(
            model_name="community",
            name="share_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="community",
            name="share_token",
            field=models.UUIDField(blank=True, db_index=True, editable=False, null=True),
        ),
        migrations.RunPython(populate_share_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="community",
            name="share_token",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
