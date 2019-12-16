# Generated by Django 2.2.5 on 2019-12-03 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoAPI', '0006_existingroledisposedbyproject'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinedRoleAssetView',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('role_number', models.TextField(null=True)),
                ('role_name', models.TextField(null=True)),
                ('parent', models.IntegerField(null=True)),
                ('project_id', models.IntegerField(null=True)),
                ('role_exists', models.BooleanField(null=True)),
                ('role_missing_from_registry', models.BooleanField(null=True)),
                ('full_path', models.TextField(null=True)),
                ('parent_changed', models.BooleanField(null=True)),
                ('approved', models.BooleanField(null=True)),
                ('role_new', models.BooleanField(null=True)),
                ('role_disposed', models.BooleanField(null=True)),
                ('asset_id', models.IntegerField(null=True)),
                ('asset_serial_number', models.TextField(null=True)),
                ('designer_planned_action_type_tbl_id', models.TextField(null=True)),
                ('role_changed', models.BooleanField(null=True)),
                ('role_link', models.IntegerField(null=True)),
                ('asset_new', models.BooleanField(null=True)),
                ('asset_exists', models.BooleanField(null=True)),
                ('asset_missing_from_registry', models.BooleanField(null=True)),
            ],
            options={
                'db_table': 'joined_role_asset',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='reconciliationview',
            table='reconciliation_view',
        ),
    ]
