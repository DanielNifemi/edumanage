from django.db import migrations, models

def cleanup_teacher_data(apps, schema_editor):
    Teacher = apps.get_model('teachers', 'Teacher')
    # Delete any teacher records that don't have an associated user
    Teacher.objects.filter(user__isnull=True).delete()

def reverse_cleanup(apps, schema_editor):
    # No reverse operation needed
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('teachers', '0004_alter_teacher_user'),
    ]

    operations = [
        migrations.RunPython(cleanup_teacher_data, reverse_cleanup),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(to='auth.user', on_delete=models.deletion.CASCADE),
        ),
    ]
