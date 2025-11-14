from django.core.management.base import BaseCommand
from game.models import Level, Mineral

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми уровнями и минералами'

    def handle(self, *args, **options):
        # Создаем уровни
        level1, created = Level.objects.get_or_create(
            number=1,
            defaults={
                'title': 'Введение (ознакомительный)',
                'theory_text': 'Изучение основ минералогии: что такое минерал, порода, основные макроскопические признаки.',
                'skills': 'Навигация по интерфейсу, понимание структуры курса',
                'materials': 'Описание курса, оглавление, краткие выдержки из Соколовского',
                'is_unlocked': True
            }
        )

        level2, created = Level.objects.get_or_create(
            number=2,
            defaults={
                'title': 'Базовые понятия минералогии и макроскопическое исследование',
                'theory_text': 'Изучение макроскопических признаков минералов: цвет, черта, блеск, излом, спайность.',
                'skills': 'Отличать блеск, черту, базовые формы кристаллических систем',
                'materials': 'Соколовский (макроскопическое изучение)',
                'is_unlocked': False
            }
        )

        level3, created = Level.objects.get_or_create(
            number=3,
            defaults={
                'title': 'Твердость, плотность и реакция с кислотой',
                'theory_text': 'Количественные методы определения минералов: шкала Мооса, плотность, реакция с HCl.',
                'skills': 'Правильное проведение теста по Моосу, вычисление плотности',
                'materials': 'Лабораторные работы по количественным методам',
                'is_unlocked': False
            }
        )

        # Минералы для уровня 2
        minerals_data = [
            # Уровень 2 минералы
            {
                'name': 'Кварц',
                'level': level2,
                'color': 'Бесцветный, белый, фиолетовый',
                'streak': 'Белая',
                'luster': 'glassy',
                'crystal_system': 'hexagonal',
                'cleavage': 'Отсутствует',
                'fracture': 'Раковистый',
                'hardness': 7.0,
                'density': 2.65,
                'reaction_with_acid': False,
                'description': 'Один из самых распространенных минералов'
            },
            {
                'name': 'Пирит',
                'level': level2,
                'color': 'Латунно-желтый',
                'streak': 'Черная',
                'luster': 'metallic',
                'crystal_system': 'cubic',
                'cleavage': 'Несовершенная',
                'fracture': 'Неровный',
                'hardness': 6.5,
                'density': 5.02,
                'reaction_with_acid': False,
                'description': 'Сульфид железа, известен как "золото дураков"'
            },
            {
                'name': 'Кальцит',
                'level': level3,
                'color': 'Бесцветный, белый',
                'streak': 'Белая',
                'luster': 'glassy',
                'crystal_system': 'hexagonal',
                'cleavage': 'Совершенная',
                'fracture': 'Ступенчатый',
                'hardness': 3.0,
                'density': 2.71,
                'reaction_with_acid': True,
                'description': 'Карбонат кальция, реагирует с соляной кислотой'
            },
            {
                'name': 'Галит',
                'level': level2,
                'color': 'Бесцветный, белый',
                'streak': 'Белая',
                'luster': 'glassy',
                'crystal_system': 'cubic',
                'cleavage': 'Совершенная',
                'fracture': 'Раковистый',
                'hardness': 2.5,
                'density': 2.16,
                'reaction_with_acid': False,
                'description': 'Каменная соль'
            },
            {
                'name': 'Гематит',
                'level': level2,
                'color': 'Черный, стально-серый',
                'streak': 'Вишнево-красная',
                'luster': 'metallic',
                'crystal_system': 'hexagonal',
                'cleavage': 'Отсутствует',
                'fracture': 'Неровный',
                'hardness': 6.0,
                'density': 5.26,
                'reaction_with_acid': False,
                'description': 'Оксид железа, важная железная руда'
            }
        ]

        for mineral_data in minerals_data:
            mineral, created = Mineral.objects.get_or_create(
                name=mineral_data['name'],
                defaults=mineral_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан минерал: {mineral.name}'))

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена тестовыми данными!'))