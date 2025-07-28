from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Test, Question, Option
from .forms import TestForm, QuestionForm, OptionForm
from django.forms import inlineformset_factory

# --- Variantlar formseti ---
OptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=OptionForm,
    fields=('text', 'image', 'is_correct'),
    extra=0,  # Yangi variantlar uchun bo‘sh joy
    can_delete=True
)

# --- Testlar ro‘yxati ---
@login_required
def test_list(request):
    tests = Test.objects.filter(created_by__role='teacher')
    return render(request, 'teachers/tests/test_list.html', {'tests': tests})

# --- Test yaratish ---
@login_required
def test_create(request):
    form = TestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        test = form.save(commit=False)
        test.created_by = request.user
        test.save()
        messages.success(request, "Test yaratildi.")
        return redirect('teachers:test_list')
    return render(request, 'teachers/tests/test_form.html', {'form': form})

# --- Test tahrirlash ---
@login_required
def test_update(request, pk):
    test = get_object_or_404(Test, pk=pk, created_by=request.user)
    form = TestForm(request.POST or None, instance=test)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Test yangilandi.")
        return redirect('teachers:test_list')
    return render(request, 'teachers/tests/test_form.html', {'form': form})

# --- Test o‘chirish ---
@login_required
def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk, created_by=request.user)
    if request.method == 'POST':
        test.delete()
        messages.success(request, "Test o‘chirildi.")
        return redirect('teachers:test_list')
    return render(request, 'teachers/tests/test_confirm_delete.html', {'test': test})

# --- Test detallari va savollar ---
@login_required
def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk, created_by=request.user)
    questions = test.questions.all()
    return render(request, 'teachers/tests/test_detail.html', {
        'test': test,
        'questions': questions
    })

# --- Savol qo‘shish (variantlar bilan) ---
@login_required
def add_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        warning = request.POST.get('warning')
        image = request.FILES.get('image')
        question = Question.objects.create(test=test, text=text, warning=warning, image=image)

        # Variantlarni olish
        i = 1
        while True:
            key_text = f'option_text_{i}'
            key_image = f'option_image_{i}'
            key_correct = f'option_correct_{i}'

            if key_text not in request.POST and key_image not in request.FILES:
                break  # hech bo‘lmaganda matn yoki rasm bo‘lishi kerak

            text_val = request.POST.get(key_text)
            image_val = request.FILES.get(key_image)
            is_correct = key_correct in request.POST

            Option.objects.create(
                question=question,
                text=text_val,
                image=image_val,
                is_correct=is_correct
            )
            i += 1

        return redirect('teachers:test_detail',  pk=question.test.id)

    return render(request, 'teachers/tests/question_form.html', {'test': test})

# --- Savolni tahrirlash (variantlar bilan) ---
@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk, test__created_by=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        formset = OptionFormSet(request.POST, request.FILES, instance=question)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Savol va variantlar muvaffaqiyatli yangilandi.")
            return redirect('teachers:test_detail', pk=question.test.pk)
    else:
        form = QuestionForm(instance=question)
        formset = OptionFormSet(instance=question)

    return render(request, 'teachers/tests/update_question.html', {
        'form': form,
        'formset': formset,
        'test': question.test,
        'question': question
    })
# --- Savolni o‘chirish ---
@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk, test__created_by=request.user)
    test_id = question.test.id
    question.delete()
    messages.success(request, "Savol o‘chirildi.")
    return redirect('teachers:test_detail', pk=test_id)
