
import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='电话')),
                ('avatar', models.FileField(default='avatars/default.png', upload_to='avatars/', verbose_name='头像')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('desc', models.TextField(blank=True, max_length=200, null=True, verbose_name='文章描述')),
                ('body', mdeditor.fields.MDTextField(verbose_name='正文')),
                ('pub_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发布时间')),
                ('status', models.CharField(choices=[('d', '草稿'), ('p', '发表')], default='p', max_length=1, verbose_name='文章状态')),
                ('comment_status', models.CharField(choices=[('o', '打开'), ('c', '关闭')], default='o', max_length=1, verbose_name='评论状态')),
                ('type', models.CharField(choices=[('a', '文章'), ('p', '页面')], default='a', max_length=1, verbose_name='类型')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览量')),
                ('article_order', models.IntegerField(default=0, verbose_name='排序,数字越大越靠前')),
                ('up_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('down_count', models.IntegerField(default=0, verbose_name='踩数')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-article_order', '-pub_time'],
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.Article')),
            ],
            options={
                'verbose_name': '文章-标签',
                'verbose_name_plural': '文章-标签',
            },
        ),
        migrations.CreateModel(
            name='ArticleUpDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_up', models.BooleanField(default=True)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userinfo.Article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '文章点赞',
                'verbose_name_plural': '文章点赞',
            },
        ),
        migrations.CreateModel(
            name='BlogSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitename', models.CharField(default='', max_length=200, verbose_name='网站名称')),
                ('site_description', models.TextField(default='', max_length=1000, verbose_name='网站描述')),
                ('site_seo_description', models.TextField(default='', max_length=1000, verbose_name='网站SEO描述')),
                ('site_keywords', models.TextField(default='', max_length=1000, verbose_name='网站关键字')),
                ('article_sub_length', models.IntegerField(default=300, verbose_name='文章摘要长度')),
                ('sidebar_article_count', models.IntegerField(default=10, verbose_name='侧边栏文章数目')),
                ('sidebar_comment_count', models.IntegerField(default=5, verbose_name='侧边栏评论数目')),
                ('show_google_adsense', models.BooleanField(default=False, verbose_name='是否显示谷歌广告')),
                ('google_adsense_codes', models.TextField(blank=True, default='', max_length=2000, null=True, verbose_name='广告内容')),
                ('open_site_comment', models.BooleanField(default=True, verbose_name='是否打开网站评论功能')),
                ('beiancode', models.CharField(blank=True, default='', max_length=2000, null=True, verbose_name='备案号')),
                ('analyticscode', models.TextField(default='', max_length=1000, verbose_name='网站统计代码')),
                ('show_gongan_code', models.BooleanField(default=False, verbose_name='是否显示公安备案号')),
                ('gongan_beiancode', models.TextField(blank=True, default='', max_length=2000, null=True, verbose_name='公安备案号')),
                ('resource_path', models.CharField(default='/var/www/resource/', max_length=300, verbose_name='静态文件保存地址')),
            ],
            options={
                'verbose_name': '网站配置',
                'verbose_name_plural': '网站配置',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='分类名')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.Article')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userinfo.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='SideBar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('sequence', models.IntegerField(unique=True, verbose_name='排序')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '侧边栏',
                'verbose_name_plural': '侧边栏',
                'ordering': ['sequence'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, verbose_name='标签名')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.Category', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='userinfo.Article2Tag', to='userinfo.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='articleupdown',
            unique_together={('article', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together={('article', 'tag')},
        ),
    ]
