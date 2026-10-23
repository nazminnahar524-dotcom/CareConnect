from django.db import migrations, models


def add_created_at_column_if_missing(apps, schema_editor):
    donor_model = apps.get_model('donors', 'Donor')
    table_name = donor_model._meta.db_table

    with schema_editor.connection.cursor() as cursor:
        columns = {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(
                cursor, table_name
            )
        }

    if 'created_at' not in columns:
        created_at_field = models.DateTimeField(auto_now_add=True)
        created_at_field.set_attributes_from_name('created_at')
        created_at_field.model = donor_model
        schema_editor.add_field(donor_model, created_at_field)


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0002_remove_donor_date_joined_remove_donor_distance_km_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    add_created_at_column_if_missing,
                    reverse_code=migrations.RunPython.noop,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='donor',
                    name='created_at',
                    field=models.DateTimeField(auto_now_add=True),
                ),
            ],
        ),
    ]
