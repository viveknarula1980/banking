from django.db import migrations
from django.contrib.auth import get_user_model


def seed_initial_data(apps, schema_editor):
    User = get_user_model()
    BankAccountType = apps.get_model("accounts", "BankAccountType")

    # Create admin user (only if not exists)
    if not User.objects.filter(email="admin@bank.com").exists():
        User.objects.create_superuser(
            email="admin@bank.com",
            password="Admin@123",
        )

    # Create default bank account type
    if not BankAccountType.objects.exists():
        BankAccountType.objects.create(
            name="Savings",
            maximum_withdrawal_amount=50000,
            annual_interest_rate=5,
            interest_calculation_per_year=12,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_initial_data),
    ]
