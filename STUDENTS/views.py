from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from TEACHERS.models import Test, Question, Option
from .models import StudentTest, StudentAnswer
from .forms import TestCodeForm


@login_required
def enter_test_code(request):
    error = None
    form = TestCodeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        code = form.cleaned_data['code']
        try:
            test = Test.objects.get(code=code)
        except Test.DoesNotExist:
            error = "Bunday kodli test topilmadi."
            return render(request, 'students/enter_test_code.html', {'form': form, 'error': error})

        # Urinishlar soni
        attempts = StudentTest.objects.filter(student=request.user, test=test).count()
        if attempts >= 3:
            error = "Siz ushbu testni 3 martadan ko‘p topshira olmaysiz."
            return render(request, 'students/enter_test_code.html', {'form': form, 'error': error})

        # Yangi urinish yaratish
        student_test = StudentTest.objects.create(
            student=request.user,
            test=test,
            attempt_number=attempts + 1
        )
        return redirect('students:start_test', test_id=test.id, attempt_number=student_test.attempt_number)

    return render(request, 'students/enter_test_code.html', {'form': form, 'error': error})


@login_required
def start_test(request, test_id, attempt_number):
    test = get_object_or_404(Test, id=test_id)
    student_test = get_object_or_404(StudentTest, student=request.user, test=test, attempt_number=attempt_number)

    if student_test.completed:
        return redirect('students:test_result', test_id=test.id, attempt_number=attempt_number)

    answered_questions = StudentAnswer.objects.filter(student_test=student_test).values_list('question_id', flat=True)
    next_question = test.questions.exclude(id__in=answered_questions).first()

    if not next_question:
        # Test tugagan
        student_test.completed = True
        student_test.score = StudentAnswer.objects.filter(student_test=student_test, is_correct=True).count()
        student_test.save()
        return redirect('students:test_result', test_id=test.id, attempt_number=attempt_number)

    if request.method == 'POST':
        selected_option_id = request.POST.get('option')
        if selected_option_id:
            selected_option = get_object_or_404(Option, id=selected_option_id)
            StudentAnswer.objects.create(
                student_test=student_test,
                question=next_question,
                selected_option=selected_option,
                is_correct=selected_option.is_correct
            )
            return redirect('students:start_test', test_id=test.id, attempt_number=attempt_number)

    return render(request, 'students/start_test.html', {
        'test': test,
        'question': next_question,
        'options': next_question.options.all()
    })


@login_required
def test_result(request, test_id, attempt_number):
    test = get_object_or_404(Test, id=test_id)
    student_test = get_object_or_404(StudentTest, test=test, student=request.user, attempt_number=attempt_number)
    answers = StudentAnswer.objects.filter(student_test=student_test)

    return render(request, 'students/test_result.html', {
        'test': test,
        'student_test': student_test,
        'answers': answers
    })
