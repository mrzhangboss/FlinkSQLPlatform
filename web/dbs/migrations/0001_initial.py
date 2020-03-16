# Generated by Django 2.2.5 on 2019-09-27 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_name', models.CharField(max_length=128, verbose_name='唯一名称')),
                ('info', models.CharField(blank=True, max_length=1024, null=True, verbose_name='介绍')),
                ('real_path', models.CharField(max_length=2048, verbose_name='文件路径')),
                ('create_by', models.IntegerField(default=0, verbose_name='创建用户ID')),
                ('is_publish', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
                'db_table': 'file_resource',
                'unique_together': {('create_by', 'unique_name')},
                'index_together': {('create_by', 'unique_name')},
            },
        ),
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='名字')),
                ('info', models.CharField(blank=True, max_length=2048, null=True, verbose_name='介绍')),
                ('avatar', models.CharField(blank=True, max_length=2048, null=True, verbose_name='图片地址')),
                ('create_by', models.IntegerField(default=0, verbose_name='创建用户ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_publish', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
                'db_table': 'namespace',
                'unique_together': {('create_by', 'name')},
                'index_together': {('create_by', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='表名')),
                ('info', models.CharField(blank=True, max_length=2048, null=True, verbose_name='介绍')),
                ('typ', models.CharField(choices=[('sink-table', '输出表'), ('source-table', '输入表')], max_length=16, verbose_name='表类型')),
                ('yaml', models.TextField(default='', verbose_name='其他信息(yaml格式)')),
                ('create_by', models.IntegerField(default=0, verbose_name='创建用户ID')),
                ('is_available', models.BooleanField(default=True)),
                ('is_publish', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('namespace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dbs.Namespace')),
            ],
            options={
                'db_table': 'resource',
                'unique_together': {('create_by', 'name')},
                'index_together': {('create_by', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Transform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='名字')),
                ('info', models.CharField(blank=True, max_length=2048, null=True, verbose_name='介绍')),
                ('sql', models.TextField(verbose_name='SQL')),
                ('require', models.TextField(verbose_name='依赖链')),
                ('is_used_as_view', models.BooleanField(default=False)),
                ('use_self', models.BooleanField(default=False)),
                ('create_by', models.IntegerField(default=0, verbose_name='创建用户ID')),
                ('is_publish', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('namespace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dbs.Namespace')),
                ('sink', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dbs.Resource')),
            ],
            options={
                'db_table': 'transform',
                'unique_together': {('create_by', 'name')},
                'index_together': {('create_by', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Functions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='名字')),
                ('function_from', models.CharField(default='class', max_length=16, verbose_name='来源')),
                ('class_name', models.CharField(max_length=256, verbose_name='类名')),
                ('constructor_config', models.CharField(max_length=2048, verbose_name='构造器')),
                ('create_by', models.IntegerField(default=0, verbose_name='创建用户ID')),
                ('is_publish', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dbs.FileResource')),
            ],
            options={
                'db_table': 'functions',
                'unique_together': {('create_by', 'name')},
                'index_together': {('create_by', 'name')},
            },
        ),
    ]