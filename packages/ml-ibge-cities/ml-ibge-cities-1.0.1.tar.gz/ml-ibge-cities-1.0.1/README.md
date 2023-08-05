# ML IBGE CITIES

## Quick start

1. Add `ml_ibge_cities` in your Django `settings.py`:
```python:
    INSTALLED_APPS = [
        ...
        'ml_ibge_cities',
        ...
    ]
```

2. Add in your `admin.py` file the fallow code:
```python:
    from ml_ibge_cities.admin import MLIBGECitiesAdmin

    @admin.register(Example)
    class ExampleAdmin(MLIBGECitiesAdmin):
        pass
```

3. Add in the `forms.py` file the fallow code:
```python:    
    from ml_ibge_cities.forms import MLIBGECitiesForm
    class ExampleAdminForm(MLIBGECitiesForm):
        class Meta:
            ...
            fields = (... "state", "city", ...)
            ...
```
