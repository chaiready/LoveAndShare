from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from mdeditor.fields import MDTextField
from LoveAndShare import settings


class UserInfo(AbstractUser):
    '''用户信息'''
    phone = models.CharField(verbose_name="电话", max_length=11)
    avatar = models.FileField(verbose_name="头像", upload_to="avatars/", default="avatars/default.png")
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    email=models.EmailField(verbose_name='邮箱')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Article(models.Model):
    """文章"""
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_STATUS = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    TYPE = (
        ('a', '文章'),
        ('p', '页面'),
    )
    title = models.CharField('标题', max_length=200)
    desc=models.TextField("文章描述",blank=True,null=True,max_length=200)
    body = MDTextField('正文')
    pub_time = models.DateTimeField('发布时间', blank=False, null=False, default=datetime.now)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    comment_status = models.CharField('评论状态', max_length=1, choices=COMMENT_STATUS, default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.ForeignKey('UserInfo', verbose_name='作者', blank=False, null=False,
                               on_delete=models.CASCADE)
    article_order = models.IntegerField('排序,数字越大越靠前', blank=False, null=False, default=0)
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    up_count = models.IntegerField(verbose_name="点赞数", default=0)
    down_count = models.IntegerField(verbose_name="踩数", default=0)
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    tags=models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=("article","tag")

    )

    def body_to_string(self):
        return self.body

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-article_order', '-pub_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'


class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名', max_length=30, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    '''文章标签'''
    title=models.CharField(max_length=16,verbose_name="标签名")

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    '''文章标签多对多'''
    article=models.ForeignKey("Article",on_delete=models.CASCADE)
    tag=models.ForeignKey("Tag",on_delete=models.CASCADE)

    class Meta:
        unique_together = (("article", "tag"),)
        verbose_name = "文章-标签"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{}-{}".format(self.article.title,self.tag.title)

class ArticleUpDown(models.Model):
    '''文章点赞'''
    user = models.ForeignKey(to="UserInfo", null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article", "user"),)
        verbose_name = "文章点赞"
        verbose_name_plural = verbose_name

class Comment(models.Model):
    """
    评论表
    """
    article = models.ForeignKey("Article",on_delete=models.CASCADE)
    user = models.ForeignKey("UserInfo",on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, blank=True,on_delete=models.CASCADE)  # blank=True 在django admin里面可以不填
    def __str__(self):
        return self.content
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class Collect(models.Model):
    '''用户收藏'''
    add_time=models.DateTimeField(default=datetime.now)
    title=models.CharField(max_length=100)
    user = models.ForeignKey(to="UserInfo", null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", null=True, on_delete=models.CASCADE)
    flag=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:

        verbose_name="用户收藏"
        verbose_name_plural=verbose_name

