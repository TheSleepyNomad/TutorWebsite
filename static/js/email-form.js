const emailForm = document.querySelector("#email-form")
console.log(emailForm)

function handleSubmit(emailForm) {
    emailForm.addEventListener("submit", e => {
        e.preventDefault();
        console.log(emailForm)
        formData = new FormData(emailForm);
        console.log(formData);
        fetch('', {
            method: 'POST',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData,
        })
            .then(response => response.json());
    })
}

handleSubmit(emailForm)