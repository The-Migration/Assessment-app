from django.db import migrations

def add_designations_and_categories(apps, schema_editor):
    Designation = apps.get_model('assessments', 'Designation')
    QuestionCategory = apps.get_model('assessments', 'QuestionCategory')

    designations = [
        "Executive",
        "Senior Executive",
        "Assistant Manager",
        "Deputy Manager",
        "Manager",
        "Senior Manager"
    ]
    categories = ["IQ", "Cultural"]

    for desig in designations:
        designation_obj, _ = Designation.objects.get_or_create(name=desig, defaults={"description": f"{desig} designation"})
        for cat in categories:
            QuestionCategory.objects.get_or_create(name=cat, assessment_type=designation_obj)

class Migration(migrations.Migration):
    dependencies = [
        ('assessments', '0002_assessment_allow_retake_and_more'),
    ]
    operations = [
        migrations.RunPython(add_designations_and_categories),
    ] 