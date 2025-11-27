from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée des utilisateurs de test par défaut pour tous les rôles'

    def handle(self, *args, **options):
        test_users = [
            {
                'username': 'admin_user',
                'email': 'admin@test.com',
                'password': 'Admin@123',
                'first_name': 'Admin',
                'last_name': 'System',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'encadreur1',
                'email': 'encadreur1@test.com',
                'password': 'Encadreur@123',
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'role': 'encadreur',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'encadreur2',
                'email': 'encadreur2@test.com',
                'password': 'Encadreur@123',
                'first_name': 'Marie',
                'last_name': 'Martin',
                'role': 'encadreur',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'etudiant1',
                'email': 'etudiant1@test.com',
                'password': 'Etudiant@123',
                'first_name': 'Pierre',
                'last_name': 'Bernard',
                'role': 'etudiant',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'etudiant2',
                'email': 'etudiant2@test.com',
                'password': 'Etudiant@123',
                'first_name': 'Sophie',
                'last_name': 'Leclerc',
                'role': 'etudiant',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'jury1',
                'email': 'jury1@test.com',
                'password': 'Jury@123',
                'first_name': 'Dr.',
                'last_name': 'Rousseau',
                'role': 'jury',
                'is_staff': False,
                'is_superuser': False,
            },
        ]

        created_count = 0
        skipped_count = 0

        for user_data in test_users:
            if not User.objects.filter(email=user_data['email']).exists():
                User.objects.create_user(**user_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Utilisateur '{user_data['username']}' créé")
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"⊘ Utilisateur '{user_data['email']}' existe déjà")
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ {created_count} utilisateur(s) créé(s), {skipped_count} déjà existant(s)')
        )
