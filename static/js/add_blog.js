// * @TheSleepyNomad
// ? Скрипт для формы(CMS) написания статьи

const addBlogBtn = document.querySelector("#addBlog")
let blogFormWrapper = document.querySelector('#blogFormWrapper')
addBlogBtn.addEventListener('click', e => {
    blogFormWrapper.classList.remove('d-none')
})

// Форма
const addBlogForm = document.querySelector("#blog-form")

// Кнопки
const addHeaderBtn = document.querySelector("#blog_form_add_header")
const addTextBtn = document.querySelector("#blog_form_add_text")
const addQuoteBtn = document.querySelector("#blog_form_add_quote")
const addImgBtn = document.querySelector("#blog_form_add_img")
const lastElForm = document.querySelector("#last_el_blog_form")


clickCount = 1

// Обработчики кнопок
// При нажатии добавляет новое поле для ввода на форму
function handleHeaderBtn(btn, lastElForm, clickCount) {
    btn.addEventListener('click', e => {
        e.preventDefault()
        let headerTemplate = `<div class="col form-group mb-3"><label for="">Добавить заголовок</label><input type="text" name="header${clickCount}" class="form-control secObj" id="header" placeholder="title"></div>`
        lastElForm.insertAdjacentHTML('beforebegin', headerTemplate)
        clickCount++


    })
}


function handleTextBtn(btn, lastElForm, clickCount) {
    btn.addEventListener('click', e => {
        e.preventDefault()
        let textTemplate = `<div class="form-group mb-3"><label for="">Добавить текст</label><textarea class="form-control secObj" name="text${clickCount}" rows="5" placeholder="Message" id="text"></textarea></div>`
        lastElForm.insertAdjacentHTML('beforebegin', textTemplate)
        clickCount++


    })
}


function handleQuoteBtn(btn, lastElForm, clickCount) {
    btn.addEventListener('click', e => {
        e.preventDefault()
        let quoteTemplate = `<div class="form-group mb-3"><label for="">Добавить цитату</label><textarea class="form-control secObj" name="quote${clickCount}" rows="5" placeholder="Message" id="quote"></textarea></div>`
        lastElForm.insertAdjacentHTML('beforebegin', quoteTemplate)
        clickCount++


    })
}


function handleImgBtn(btn, lastElForm, clickCount) {
    btn.addEventListener('click', e => {
        e.preventDefault()
        let imgTemplate = `<div class="col form-group mb-3"><label for="">Добавить изображение</label><input type="file" name="gallary${clickCount}" class="form-control secObj" id="img" placeholder="entry-img"></div>`
        lastElForm.insertAdjacentHTML('beforebegin', imgTemplate)
        clickCount++
        console.log(clickCount);


    })
}


handleHeaderBtn(addHeaderBtn, lastElForm, clickCount)
handleTextBtn(addTextBtn, lastElForm, clickCount)
handleQuoteBtn(addQuoteBtn, lastElForm, clickCount)
handleImgBtn(addImgBtn, lastElForm, clickCount)


// Обработчик для формы
function handleSubmit(addBlogForm) {
    addBlogForm.addEventListener("submit", e => {
        // Отключаем обновление страницы
        e.preventDefault();
        // Добавляем анимацию загрузки
        addBlogForm.querySelector('.loading').classList.add('d-block')
        // Собираем данные с формы
        let allSecondObj = document.querySelectorAll('.secObj'); // Получаем все элементы, которые добавил пользователь
        let textDataTemplate = [] // С помощью этого массива объединим разметку и создадим html структуру статьи

        // Создаем основную разметку статьи
        let pCount = 1;
        let prevText = ''
        for (let i of allSecondObj) {
            if (i.id == 'header') {
                textDataTemplate.push(`<h3>${i.value}</h3>`)
            }
            if (i.id == 'text') {
                textDataTemplate.push(`<p>${i.value}</p>`)
                if (pCount == 1) {
                    pCount++
                    prevText = `<p>${i.value}</p>`
                }
            }
            if (i.id == 'quote') {
                textDataTemplate.push(`<blockquote><p>${i.value}</p></blockquote>`)
            }
            if (i.id == 'img') {
                textDataTemplate.push(`<img src="/media/images/${i.files[0].name}" class="img-fluid" alt="">`)
            }
        }
        textData = `<div class="entry-content">${textDataTemplate.join('')}</div>`
        // Формируем пакет данных к отправке
        formData = new FormData(addBlogForm);
        formData.append("text", textData);
        formData.append("prev_text", prevText);

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
                addBlogForm.querySelector('.loading').classList.remove('d-block')
                addBlogForm.querySelector('.sent-message').classList.add('d-block')
                location.reload()
            });
    })
}

handleSubmit(addBlogForm)