from tortoise import fields, models


class User(models.Model):
    name = fields.CharField(max_length=64)
    password = fields.BinaryField()
    email = fields.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Offer(models.Model):
    user = fields.ForeignKeyField('models.User')
    title = fields.CharField(max_length=64)
    text = fields.TextField()

    def __str__(self):
        return self.title
