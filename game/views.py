from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from .models import Level, UserProgress, Mineral, TestQuestion, TestAnswer, TestResult


@login_required
def home(request):
    # Получаем все уровни
    levels = Level.objects.all().order_by('number')

    # Получаем прогресс пользователя
    user_progress = {}
    for progress in UserProgress.objects.filter(user=request.user):
        user_progress[progress.level_id] = progress

    # Получаем результаты тестов
    test_results = {}
    for result in TestResult.objects.filter(user=request.user):
        test_results[result.level_id] = result

    # Добавляем статус для каждого уровня
    for level in levels:
        # Уровень 1 всегда доступен
        if level.number == 1:
            level.status = 'available'
        # Остальные уровни доступны если разблокированы
        elif level.is_unlocked:
            level.status = 'available'
        else:
            level.status = 'locked'

        # Проверяем пройден ли уровень (по тесту)
        if level.id in test_results:
            if test_results[level.id].passed:
                level.status = 'completed'

    return render(request, 'game/home.html', {'levels': levels})




def lab_level_2(request):
    """Страница лаборатории для уровня 2"""
    return render(request, 'game/lab_level_2.html')



def level_detail(request, level_number):
    try:
        level = Level.objects.get(number=level_number)

        # Проверяем доступность уровня
        if level.number > 1 and not level.is_unlocked:
            # Показываем сообщение что уровень заблокирован
            return render(request, 'game/level_locked.html', {'level': level})

        return render(request, 'game/level_detail.html', {
            'level': level,
            'minerals': Mineral.objects.filter(level=level)
        })
    except Level.DoesNotExist:
        # Если уровень не найден
        return render(request, 'game/level_not_found.html')


def level_practice(request, level_number):
    try:
        level = Level.objects.get(number=level_number)

        # Проверяем доступность уровня
        if level.number > 1 and not level.is_unlocked:
            return render(request, 'game/level_locked.html', {'level': level})

        # Для уровня 2 используем специальный шаблон практики
        if level_number == 2:
            minerals = Mineral.objects.filter(level=level)
            return render(request, 'game/level_2_practice.html', {
                'level': level,
                'minerals': minerals
            })

        # Для других уровней можно сделать общий шаблон
        return render(request, 'game/level_practice.html', {
            'level': level,
            'minerals': Mineral.objects.filter(level=level)
        })

    except Level.DoesNotExist:
        return render(request, 'game/level_not_found.html')


@csrf_exempt  # Временно отключаем CSRF для простоты тестирования
def filter_minerals(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_properties = data.get('properties', [])

            minerals = Mineral.objects.filter(level__number=2)

            for prop in selected_properties:
                # Существующие фильтры цвета
                if prop == 'color_white':
                    minerals = minerals.filter(color__icontains='белый') | minerals.filter(
                        color__icontains='бесцветный')
                elif prop == 'color_yellow':
                    minerals = minerals.filter(color__icontains='желтый') | minerals.filter(color__icontains='латунный')
                elif prop == 'color_black':
                    minerals = minerals.filter(color__icontains='черный') | minerals.filter(color__icontains='серый')

                # Фильтры блеска
                elif prop == 'luster_metallic':
                    minerals = minerals.filter(luster='metallic')
                elif prop == 'luster_glassy':
                    minerals = minerals.filter(luster='glassy')
                elif prop == 'luster_pearly':
                    minerals = minerals.filter(luster='pearly')

                # Фильтры черты
                elif prop == 'streak_white':
                    minerals = minerals.filter(streak__icontains='белая')
                elif prop == 'streak_black':
                    minerals = minerals.filter(streak__icontains='черная')
                elif prop == 'streak_red':
                    minerals = minerals.filter(streak__icontains='красная') | minerals.filter(
                        streak__icontains='вишневая')

                # Фильтры кристаллической системы
                elif prop == 'crystal_cubic':
                    minerals = minerals.filter(crystal_system='cubic')
                elif prop == 'crystal_hexagonal':
                    minerals = minerals.filter(crystal_system='hexagonal')

                # НОВЫЕ ФИЛЬТРЫ: ТВЕРДОСТЬ
                elif prop == 'hardness_very_soft':
                    minerals = minerals.filter(hardness__lte=2.5)
                elif prop == 'hardness_soft':
                    minerals = minerals.filter(hardness__gt=2.5, hardness__lte=4.0)
                elif prop == 'hardness_medium':
                    minerals = minerals.filter(hardness__gt=4.0, hardness__lte=6.0)
                elif prop == 'hardness_hard':
                    minerals = minerals.filter(hardness__gt=6.0)

                # НОВЫЕ ФИЛЬТРЫ: ПЛОТНОСТЬ
                elif prop == 'density_very_light':
                    minerals = minerals.filter(density__lte=2.5)
                elif prop == 'density_light':
                    minerals = minerals.filter(density__gt=2.5, density__lte=4.0)
                elif prop == 'density_medium':
                    minerals = minerals.filter(density__gt=4.0, density__lte=5.0)
                elif prop == 'density_heavy':
                    minerals = minerals.filter(density__gt=5.0)

                # НОВЫЕ ФИЛЬТРЫ: РЕАКЦИЯ С КИСЛОТОЙ
                elif prop == 'reaction_acid_yes':
                    minerals = minerals.filter(reaction_with_acid=True)
                elif prop == 'reaction_acid_no':
                    minerals = minerals.filter(reaction_with_acid=False)

            # Подготавливаем данные для ответа
            mineral_list = []
            for mineral in minerals:
                mineral_list.append({
                    'id': mineral.id,
                    'name': mineral.name,
                    'color': mineral.color,
                    'streak': mineral.streak,
                    'luster': mineral.get_luster_display(),
                    'hardness': float(mineral.hardness),
                    'density': float(mineral.density),
                    'reaction_with_acid': mineral.reaction_with_acid,
                    'crystal_system': mineral.get_crystal_system_display(),
                    'cleavage': mineral.cleavage
                })

            return JsonResponse({
                'success': True,
                'minerals': mineral_list,
                'count': len(mineral_list)
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False, 'error': 'Only POST method allowed'})


def level_test(request, level_number):
    try:
        level = Level.objects.get(number=level_number)

        # Проверяем доступность уровня
        if level.number > 1 and not level.is_unlocked:
            return render(request, 'game/level_locked.html', {'level': level})

        # Получаем вопросы для уровня
        questions = TestQuestion.objects.filter(level=level).prefetch_related('testanswer_set')

        # Проверяем, не прошел ли пользователь уже тест
        previous_result = TestResult.objects.filter(user=request.user, level=level).first()

        return render(request, 'game/level_test.html', {
            'level': level,
            'questions': questions,
            'previous_result': previous_result
        })

    except Level.DoesNotExist:
        return render(request, 'game/level_not_found.html')


@csrf_exempt
def submit_test(request, level_number):
    if request.method == 'POST':
        try:
            level = Level.objects.get(number=level_number)
            data = json.loads(request.body)
            user_answers = data.get('answers', {})

            # Получаем все вопросы для уровня
            questions = TestQuestion.objects.filter(level=level).prefetch_related('testanswer_set')
            total_score = 0
            max_score = 0

            # Проверяем ответы
            for question in questions:
                max_score += 1
                user_answer = user_answers.get(str(question.id))

                if question.question_type == 'single_choice':
                    # Для одиночного выбора проверяем выбранный ответ
                    if user_answer:
                        try:
                            answer = TestAnswer.objects.get(id=user_answer, question=question)
                            if answer.is_correct:
                                total_score += 1
                        except TestAnswer.DoesNotExist:
                            pass

                elif question.question_type == 'multiple_choice':
                    # Для множественного выбора проверяем все выбранные ответы
                    if user_answer and isinstance(user_answer, list):
                        correct_answers = set(
                            question.testanswer_set.filter(is_correct=True).values_list('id', flat=True))
                        user_answers_set = set(map(int, user_answer))

                        if correct_answers == user_answers_set:
                            total_score += 1

                elif question.question_type == 'true_false':
                    # Для верно/неверно
                    if user_answer:
                        try:
                            answer = TestAnswer.objects.get(id=user_answer, question=question)
                            if answer.is_correct:
                                total_score += 1
                        except TestAnswer.DoesNotExist:
                            pass

            # Рассчитываем процент и проверяем прохождение (80% для прохождения)
            percentage = (total_score / max_score) * 100 if max_score > 0 else 0
            passed = percentage >= 80

            # Сохраняем результат
            test_result, created = TestResult.objects.update_or_create(
                user=request.user,
                level=level,
                defaults={
                    'score': total_score,
                    'max_score': max_score,
                    'passed': passed
                }
            )

            # Если тест пройден, разблокируем следующий уровень
            if passed and level.number < 3:
                next_level = Level.objects.get(number=level.number + 1)
                next_level.is_unlocked = True
                next_level.save()

            return JsonResponse({
                'success': True,
                'score': total_score,
                'max_score': max_score,
                'percentage': round(percentage, 1),
                'passed': passed
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False, 'error': 'Only POST method allowed'})