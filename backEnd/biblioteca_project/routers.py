
APPS_NEGOCIO = {"biblioteca"}


class NegocioRouter:

    def db_for_read(self, model, **hints):
        return "negocio" if model._meta.app_label in APPS_NEGOCIO else "default"

    def db_for_write(self, model, **hints):
        return "negocio" if model._meta.app_label in APPS_NEGOCIO else "default"

    def allow_relation(self, obj1, obj2, **hints):
        db1 = self.db_for_read(type(obj1))
        db2 = self.db_for_read(type(obj2))
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # No permitir migraciones en Oracle.
        if db == "negocio":
            return False

        # Los modelos de biblioteca no se crean mediante migraciones.
        return app_label not in APPS_NEGOCIO
    