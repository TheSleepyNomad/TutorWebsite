const loginForm = document.querySelector("#login-form")
console.log(loginForm)

function handleSubmit(loginForm) {
    loginForm.addEventListener("submit", e => {
        // Отключаем обновление страницы
        e.preventDefault();
        // Собираем данные с формы
        formData = new FormData(loginForm);
        fetch('', {
            method: 'POST',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData,
        })
            .then(response => {
                if (response.ok) {
                    window.location.replace(response.url);;
                }
            })
            .then(data => {
                loginForm.reset()
            });
    })
}

handleSubmit(loginForm)