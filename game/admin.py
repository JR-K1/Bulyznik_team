from django.contrib import admin
from .models import Level, Mineral, UserProgress
from .models import TestQuestion, TestAnswer, TestResult

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'is_unlocked')
    list_editable = ('is_unlocked',)
    ordering = ('number',)

@admin.register(Mineral)
class MineralAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'color', 'hardness', 'density')
    list_filter = ('level', 'luster', 'crystal_system')
    search_fields = ('name', 'description')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'is_completed', 'score')
    list_filter = ('level', 'is_completed')


class TestAnswerInline(admin.TabularInline):
    model = TestAnswer
    extra = 1

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'level', 'question_type', 'order')
    list_filter = ('level', 'question_type')
    inlines = [TestAnswerInline]
    ordering = ['level', 'order']

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'score', 'max_score', 'passed', 'completed_at')
    list_filter = ('level', 'passed', 'completed_at')
    readonly_fields = ('completed_at',)