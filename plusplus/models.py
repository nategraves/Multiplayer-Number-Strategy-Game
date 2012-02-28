import datetime

from django.db import models

class ManagerBase(models.Manager):
        def get_query_set(self):
                """Only return objects that have not been deleted."""
                return super(ManagerBase, self).get_query_set().filter(time_deleted=None)

class ModelBase(models.Model):
        time_created = models.DateTimeField(auto_now_add=True)
        time_updated = models.DateTimeField(auto_now=True)
        time_deleted = models.DateTimeField(blank=True, null=True)

        active_objects = ManagerBase()
        objects = models.Manager()

        class Meta(object):
                abstract = True

        def delete(self, *args, **kwargs):
                """Set time_deleted on model.

                force_delete - Actually deletes the object from the DB.
                """
                force_delete = kwargs.pop('force_delete', False)
                if force_delete:
                        return super(ModelBase, self).delete(*args, **kwargs)

                self.time_deleted = datetime.datetime.now()