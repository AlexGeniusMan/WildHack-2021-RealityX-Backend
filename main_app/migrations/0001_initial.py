# Generated by Django 3.2.6 on 2021-11-09 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='none', max_length=50, verbose_name='Уникальный идентификатор')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='Описание')),
                ('recognition_image', models.IntegerField(blank=True, null=True, verbose_name='ID иконки')),
            ],
            options={
                'verbose_name': 'Экспонат',
                'verbose_name_plural': 'Экспонаты',
            },
        ),
        migrations.CreateModel(
            name='Exposition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='Описание')),
                ('type', models.CharField(choices=[('По билетам', 'По билетам'), ('Свободный вход', 'Свободный вход')], default='По билетам', max_length=64, verbose_name='Тип выставки')),
                ('ticket_lifetime', models.IntegerField(default=3, verbose_name='Время жизни билета (в часах)')),
                ('admin', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exposition', to=settings.AUTH_USER_MODEL, verbose_name='Администратор')),
            ],
            options={
                'verbose_name': 'Выставка',
                'verbose_name_plural': 'Выставки',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания')),
                ('token', models.CharField(default='none', max_length=5000, verbose_name='Токен')),
                ('exposition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='main_app.exposition', verbose_name='Выставка')),
            ],
            options={
                'verbose_name': 'Билет',
                'verbose_name_plural': 'Билеты',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='none', max_length=50, verbose_name='Уникальный идентификатор')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('img', models.ImageField(blank=True, upload_to='rooms/images', verbose_name='Изображение')),
                ('img_compressed_resized', models.ImageField(blank=True, upload_to='rooms/img_compressed_resized', verbose_name='Изображение')),
                ('description', models.TextField(blank=True, max_length=200, verbose_name='Описание')),
                ('recognition_image', models.IntegerField(blank=True, null=True, verbose_name='ID иконки')),
                ('connected_rooms', models.ManyToManyField(blank=True, related_name='_main_app_room_connected_rooms_+', to='main_app.Room', verbose_name='Соединенные комнаты')),
                ('exposition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='main_app.exposition', verbose_name='Выставка')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
            },
        ),
        migrations.CreateModel(
            name='MediaLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('link', models.CharField(max_length=2000, verbose_name='Ссылка')),
                ('artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='main_app.artifact', verbose_name='Экспонат')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
            },
        ),
        migrations.CreateModel(
            name='MediaImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='artifacts/images', verbose_name='Изображение')),
                ('img_compressed_resized', models.ImageField(blank=True, upload_to='artifacts/img_compressed_resized', verbose_name='Мини-Изображение')),
                ('artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main_app.artifact', verbose_name='Экспонат')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='MediaAudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('audio', models.FileField(upload_to='artifacts/audios', verbose_name='Аудиофайл')),
                ('artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audios', to='main_app.artifact', verbose_name='Экспонат')),
            ],
            options={
                'verbose_name': 'Аудиофайл',
                'verbose_name_plural': 'Аудиофайлы',
            },
        ),
        migrations.AddField(
            model_name='artifact',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artifacts', to='main_app.room', verbose_name='Комната'),
        ),
    ]
