from django.db import models
from utils.common import hash_sha256

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256,unique=True)
    password = models.CharField(max_length=512)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    def toDynamodbItem(self):
        return {
            "username" : {
                "S" : self.username
            },
            "active" : {
                "B" : self.active
            },
            "updated" : {
                "S" : self.updated.isoformat()
            }
        }
    
    def save(self,*args,**kwargs):
        self.password = hash_sha256(self.password)
        super().save()
        
    def check_password(self,plain_text_password : str) -> bool:
        return self.password == hash_sha256(plain_text_password)
        
    @staticmethod
    def getUserByUsername(username : str ) -> 'User' :
        return User.objects.filter(username=username).first()
