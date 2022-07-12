const emailForm = document.querySelector("#email-form")
console.log(emailForm)

function handleSubmit(emailForm) {
    emailForm.addEventListener("submit", e => {
        // Отключаем обновление страницы
        e.preventDefault();
        // Добавляем анимацию загрузки
        emailForm.querySelector('.loading').classList.add('d-block')
        // Собираем данные с формы
        formData = new FormData(emailForm);
        fetch('', {
            method: 'POST',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData,
        })
            .then(response => {
                if (response.ok) {
                    console.log(response);
                }
            })
            .then(data => {
                emailForm.querySelector('.loading').classList.remove('d-block')
                emailForm.querySelector('.sent-message').classList.add('d-block')
                emailForm.reset()
            });
    })
}

handleSubmit(emailForm)