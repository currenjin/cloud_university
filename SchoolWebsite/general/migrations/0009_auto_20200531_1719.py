# Generated by Django 3.0.6 on 2020-05-31 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general', '0008_remove_memberinfo_membergrades'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general.Course')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Grade')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Semester')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='MemberGrades',
        ),
    ]
