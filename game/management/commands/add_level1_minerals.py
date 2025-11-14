from django.core.management.base import BaseCommand
from game.models import Level, Mineral


class Command(BaseCommand):
    help = 'Добавляет учебные минералы для уровня 1'

    def handle(self, *args, **options):
        level1 = Level.objects.get(number=1)

        minerals_data = [
            {
                'name': 'Образец А',
                'level': level1,
                'color': 'Серый',
                'streak': 'Белая',
                'luster': 'glassy',
                'crystal_system': 'cubic',
                'cleavage': 'Отсутствует',
                'fracture': 'Раковистый',
                'hardness': 5.0,
                'density': 2.50,
                'reaction_with_acid': False,
                'description': 'Учебный образец для знакомства с основами минералогии'
            },
            {
                'name': 'Образец Б',
                'level': level1,
                'color': 'Черный',
                'streak': 'Черная',
                'luster': 'metallic',
                'crystal_system': 'hexagonal',
                'cleavage': 'Совершенная',
                'fracture': 'Неровный',
                'hardness': 4.0,
                'density': 3.20,
                'reaction_with_acid': False,
                'description': 'Второй учебный образец для тренировки'
            }
        ]

        for mineral_data in minerals_data:
            mineral, created = Mineral.objects.get_or_create(
                name=mineral_data['name'],
                level=mineral_data['level'],
                defaults=mineral_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан минерал: {mineral.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Минерал уже существует: {mineral.name}'))

        self.stdout.write(self.style.SUCCESS('Учебные минералы для уровня 1 добавлены!'))