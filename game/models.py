from django.db import models
from django.contrib.auth.models import User


class Level(models.Model):
    LEVEL_STATUS = [
        ('locked', 'Заблокирован'),
        ('unlocked', 'Доступен'),
        ('completed', 'Пройден'),
    ]

    number = models.IntegerField(unique=True, verbose_name="Номер уровня")
    title = models.CharField(max_length=200, verbose_name="Название уровня")
    theory_text = models.TextField(verbose_name="Теоретический материал")
    skills = models.TextField(verbose_name="Навыки после уровня")
    materials = models.TextField(verbose_name="Материалы уровня")
    is_unlocked = models.BooleanField(default=False, verbose_name="Доступен")

    def __str__(self):
        return f"Уровень {self.number}: {self.title}"

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"


class Mineral(models.Model):
    # Основные свойства
    LUSTER_TYPES = [
        ('metallic', 'Металлический'),
        ('glassy', 'Стеклянный'),
        ('pearly', 'Перламутровый'),
        ('greasy', 'Жирный'),
        ('dull', 'Тусклый'),
    ]

    CRYSTAL_SYSTEMS = [
        ('cubic', 'Кубическая'),
        ('tetragonal', 'Тетрагональная'),
        ('hexagonal', 'Гексагональная'),
        ('orthorhombic', 'Ромбическая'),
        ('monoclinic', 'Моноклинная'),
        ('triclinic', 'Триклинная'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название минерала")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='minerals/', verbose_name="Изображение", null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Уровень")

    # Макроскопические свойства
    color = models.CharField(max_length=100, verbose_name="Цвет")
    streak = models.CharField(max_length=100, verbose_name="Цвет черты")
    luster = models.CharField(max_length=20, choices=LUSTER_TYPES, verbose_name="Блеск")
    crystal_system = models.CharField(max_length=20, choices=CRYSTAL_SYSTEMS, verbose_name="Кристаллическая система")
    cleavage = models.CharField(max_length=100, verbose_name="Спайность")
    fracture = models.CharField(max_length=100, verbose_name="Излом")

    # Количественные свойства
    hardness = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Твердость по Моосу")
    density = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Плотность")
    reaction_with_acid = models.BooleanField(default=False, verbose_name="Реакция с HCl")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Минерал"
        verbose_name_plural = "Минералы"

    def hardness_range(self):
        """Возвращает диапазон твердости для фильтрации"""
        hardness = float(self.hardness)
        if hardness <= 2.5:
            return 'very_soft'
        elif hardness <= 4:
            return 'soft'
        elif hardness <= 6:
            return 'medium'
        else:
            return 'hard'

    def density_range(self):
        """Возвращает диапазон плотности для фильтрации"""
        density = float(self.density)
        if density <= 2.5:
            return 'very_light'
        elif density <= 4:
            return 'light'
        elif density <= 5:
            return 'medium'
        else:
            return 'heavy'


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Уровень")
    is_completed = models.BooleanField(default=False, verbose_name="Пройден")
    score = models.IntegerField(default=0, verbose_name="Баллы")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата прохождения")

    class Meta:
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогресс пользователей"
        unique_together = ['user', 'level']


class TestQuestion(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Множественный выбор'),
        ('single_choice', 'Одиночный выбор'),
        ('true_false', 'Верно/Неверно'),
    ]

    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Уровень")
    question_text = models.TextField(verbose_name="Текст вопроса")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="Тип вопроса")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return f"Вопрос {self.order}: {self.question_text[:50]}..."

    class Meta:
        verbose_name = "Вопрос теста"
        verbose_name_plural = "Вопросы теста"
        ordering = ['level', 'order']


class TestAnswer(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer_text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return f"{self.answer_text[:30]}... ({'✓' if self.is_correct else '✗'})"

    class Meta:
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"
        ordering = ['question', 'order']


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Уровень")
    score = models.IntegerField(default=0, verbose_name="Баллы")
    max_score = models.IntegerField(default=0, verbose_name="Максимальный балл")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата прохождения")
    passed = models.BooleanField(default=False, verbose_name="Тест пройден")

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"
        unique_together = ['user', 'level']