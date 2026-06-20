from django.db import models
import uuid

class KnowledgeGroup(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"

class Document(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    )
    doc_id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    file_name = models.CharField(max_length=255)
    knowledge_group = models.ForeignKey(KnowledgeGroup, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    actual_url = models.URLField(null=True, blank=True)
    ai_generated_url = models.URLField(null=True, blank=True)

class KBJob(models.Model):
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    )
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    url = models.URLField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Submitted')
