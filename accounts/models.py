#basically define and explain the data structure , and the relation
#between different data types , used to create CRUD


from django.db import models

class Authors(models.Model):
    name=models.CharField(max_length=100,unique=True)
    details=models.TextField(max_length=2002)
    def __str__(self):
        return self.name


class Article(models.Model):
    author_name=models.ForeignKey(Authors,on_delete=models.CASCADE) #ManyToOne,(many articles mapped to one author)
    article_name=models.CharField(max_length=100)
    article_photo=models.ImageField(upload_to='uploads/')
    article_body=models.TextField(max_length=10020)
    published_at=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.article_name
    
class NewUser(models.Model):
    username=models.CharField(max_length=100,unique=True)
    email_id=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100)


class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)