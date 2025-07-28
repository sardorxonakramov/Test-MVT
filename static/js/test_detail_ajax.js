function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function updateQuestion(localId, dbId) {
    if (!dbId) return alert("Ma'lumot ID mavjud emas");

    const questionDiv = document.getElementById(localId);
    const text = questionDiv.querySelector('.question-text').value;
    const warning = questionDiv.querySelector('.question-warning').value;

    fetch(`/teachers/questions/${dbId}/update/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text, warning })
    }).then(r => r.json()).then(data => {
        if (data.success) alert("✅ Savol yangilandi!");
    });
}

function deleteQuestion(localId, dbId) {
    if (!confirm("❗Savolni o‘chirmoqchimisiz?")) return;

    fetch(`/teachers/questions/${dbId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    }).then(r => r.json()).then(data => {
        if (data.success) document.getElementById(localId).remove();
    });
}

function updateOption(button, optionId) {
    const group = button.closest('.input-group');
    const text = group.querySelector('.option-text').value;
    const isCorrect = group.querySelector('input[type="checkbox"]').checked;

    fetch(`/teachers/options/${optionId}/update/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text, is_correct: isCorrect })
    }).then(r => r.json()).then(data => {
        if (data.success) alert("✅ Variant yangilandi!");
    });
}

function deleteOption(button, optionId) {
    if (!confirm("❗Variantni o‘chirmoqchimisiz?")) return;

    fetch(`/teachers/options/${optionId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    }).then(r => r.json()).then(data => {
        if (data.success) button.closest('.input-group').remove();
    });
}
