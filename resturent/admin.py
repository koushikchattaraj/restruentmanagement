from django.contrib import admin
from django.apps import apps
models = apps.all_models['resturent'].values()

for model in models:
	try:
		admclass = type(model._meta.model.__name__+'Admin', (admin.ModelAdmin,), {'list_display':tuple(map(lambda obj: obj.name,model._meta.fields))[1:]})
		admin.site.register(model,admclass)
	except admin.sites.AlreadyRegistered:
		pass
	except Exception as msg:
		print(msg)