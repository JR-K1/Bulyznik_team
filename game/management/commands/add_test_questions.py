from django.core.management.base import BaseCommand
from game.models import Level, TestQuestion, TestAnswer


class Command(BaseCommand):
    help = 'Добавляет тестовые вопросы для уровня 2'

    def handle(self, *args, **options):
        level2 = Level.objects.get(number=2)

        # Удаляем старые вопросы если есть
        TestQuestion.objects.filter(level=level2).delete()

        questions_data = [
            {
                'question_text': 'Что такое минерал?',
                'question_type': 'single_choice',
                'answers': [
                    {'text': 'Природное химически однородное вещество с упорядоченной структурой', 'correct': True},
                    {'text': 'Любой твердый природный объект', 'correct': False},
                    {'text': 'Искусственно созданное кристаллическое вещество', 'correct': False},
                    {'text': 'Смесь различных химических элементов', 'correct': False},
                ]
            },
            {
                'question_text': 'Какой блеск характерен для пирита?',
                'question_type': 'single_choice',
                'answers': [
                    {'text': 'Металлический', 'correct': True},
                    {'text': 'Стеклянный', 'correct': False},
                    {'text': 'Перламутровый', 'correct': False},
                    {'text': 'Жирный', 'correct': False},
                ]
            },
            {
                'question_text': 'Что показывает цвет черты минерала?',
                'question_type': 'single_choice',
                'answers': [
                    {'text': 'Цвет порошка минерала', 'correct': True},
                    {'text': 'Цвет поверхности минерала', 'correct': False},
                    {'text': 'Цвет при освещении ультрафиолетом', 'correct': False},
                    {'text': 'Цвет прозрачности минерала', 'correct': False},
                ]
            },
            {
                'question_text': 'Какие из перечисленных свойств относятся к макроскопическим?',
                'question_type': 'multiple_choice',
                'answers': [
                    {'text': 'Цвет', 'correct': True},
                    {'text': 'Черта', 'correct': True},
                    {'text': 'Блеск', 'correct': True},
                    {'text': 'Химическая формула', 'correct': False},
                    {'text': 'Спайность', 'correct': True},
                ]
            },
            {
                'question_text': 'Минерал с твердостью 7 царапает стекло',
                'question_type': 'true_false',
                'answers': [
                    {'text': 'Верно', 'correct': True},
                    {'text': 'Неверно', 'correct': False},
                ]
            }
        ]

        for i, q_data in enumerate(questions_data):
            question = TestQuestion.objects.create(
                level=level2,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                order=i + 1
            )

            for j, a_data in enumerate(q_data['answers']):
                TestAnswer.objects.create(
                    question=question,
                    answer_text=a_data['text'],
                    is_correct=a_data['correct'],
                    order=j + 1
                )

            self.stdout.write(self.style.SUCCESS(f'Создан вопрос: {question.question_text}'))

        self.stdout.write(self.style.SUCCESS(f'Создано {len(questions_data)} вопросов для уровня 2'))