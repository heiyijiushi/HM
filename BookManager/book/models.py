from django.db import models

# Create your models here.
class BookInfo(models.Model):
    #书名
    name=models.CharField(max_length=10,verbose_name="名称")
    pub_date=models.DateField(verbose_name="发布时间",null=True)
    readcount=models.IntegerField(default=0,verbose_name="阅读量")
    commentcount=models.IntegerField(default=0,verbose_name="评论量")
    is_delete=models.BooleanField(default=False,verbose_name="逻辑删除")
    class Meta:
        db_table='bookinfo'
        verbose_name="图书"
    def __str__(self):
        '''将模型类以字符串形式输出'''
        return self.name

#人物列表信息模型类
class PeopleInfo(models.Model):
    GENDER_CHOICES=((0,'male'),(1,'female'))

    #名字
    name=models.CharField(max_length=10,verbose_name="姓名")
    #性别
    gender=models.SmallIntegerField(choices=GENDER_CHOICES,default=0,verbose_name="性别")

    #外键约束 人物属于哪本书
    book=models.ForeignKey(BookInfo,on_delete=models.CASCADE,verbose_name="图书")

    is_delete=models.BooleanField(default=False,verbose_name="逻辑删除")

    class Mete:
        db_table='peopleinfo'
        verbose_name='人物信息'

    def __str__(self):
        '''将模型类以字符串形式输出'''
        return self.name