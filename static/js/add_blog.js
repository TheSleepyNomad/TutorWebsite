// Форма
const addBlogForm = document.querySelector("#blog-form")


// Кнопки
const addHeaderBtn = document.querySelector("#blog_form_add_header")
const addTextBtn = document.querySelector("#blog_form_add_text")
const addQuoteBtn = document.querySelector("#blog_form_add_quote")
const addImgBtn = document.querySelector("#blog_form_add_img")
const lastElForm = document.querySelector("#last_el_blog_form")
// Шаблоны
let textTemplate = `<div class="form-group"><textarea class="form-control" name="message" rows="5" placeholder="Message"></textarea></div>`
let imgTemplate = `<div class="col form-group"><input type="file" name="entry-img" class="form-control" id="entry-img" placeholder="entry-img"></div>`
let quoteTemplate = `<blockquote><p>Et vero doloremque tempore voluptatem ratione vel aut. Deleniti sunt animi aut. Aut eos aliquam doloribus minus autem quos.</p></blockquote>`

clickCount = 1

function handleHeaderBtn(btn, lastElForm, clickCount) {
    btn.addEventListener('click', e => {
        e.preventDefault()
        let headerTemplate = `<div class="col form-group mb-3"><input type="text" name="header${clickCount}" class="form-control secObj" id="header" placeholder="title"></div>`
        lastElForm.insertAdjacentHTML('beforebegin', headerTemplate)
        clickCount++


    })
}


function handleTextBtn(btn, lastElForm, clickCount) {
    btn.addEventListener('click', e => {
        e.preventDefault()
        let textTemplate = `<div class="form-group mb-3"><textarea class="form-control secObj" name="text${clickCount}" rows="5" placeholder="Message" id="text"></textarea></div>`
        lastElForm.insertAdjacentHTML('beforebegin', textTemplate)
        clickCount++


    })
}


function handleQuoteBtn(btn, lastElForm, clickCount) {
    btn.addEventListener('click', e => {
        e.preventDefault()
        let quoteTemplate = `<div class="form-group mb-3"><textarea class="form-control secObj" name="quote${clickCount}" rows="5" placeholder="Message" id="quote"></textarea></div>`
        lastElForm.insertAdjacentHTML('beforebegin', quoteTemplate)
        clickCount++


    })
}


function handleImgBtn(btn, lastElForm, clickCount) {
    btn.addEventListener('click', e => {
        e.preventDefault()
        let imgTemplate = `<div class="col form-group mb-3"><input type="file" name="gallary${clickCount}" class="form-control secObj" id="img" placeholder="entry-img"></div>`
        lastElForm.insertAdjacentHTML('beforebegin', imgTemplate)
        clickCount++
        console.log(clickCount);


    })
}

handleHeaderBtn(addHeaderBtn, lastElForm, clickCount)
handleTextBtn(addTextBtn, lastElForm, clickCount)
handleQuoteBtn(addQuoteBtn, lastElForm, clickCount)
handleImgBtn(addImgBtn, lastElForm, clickCount)

function handleSubmit(addBlogForm) {
    addBlogForm.addEventListener("submit", e => {
        // Отключаем обновление страницы
        e.preventDefault();
        let entry_img = document.querySelector("#entry-img")
        // Добавляем анимацию загрузки
        addBlogForm.querySelector('.loading').classList.add('d-block')
        // Собираем данные с формы

        let allSecondObj = document.querySelectorAll('.secObj');
        console.log(allSecondObj);
        let textDataTemplate = []
        for (let i of allSecondObj) {
            if (i.id == 'header') {
                textDataTemplate.push(`<h3>${i.value}</h3>`)
            }
            if (i.id == 'text') {
                textDataTemplate.push(`<p>${i.value}</p>`)
            }
            if (i.id == 'quote') {
                textDataTemplate.push(`<blockquote><p>${i.value}</p></blockquote>`)
            }
            if (i.id == 'img') {
                textDataTemplate.push(`<img src="/media/images/${i.files[0].name}" class="img-fluid" alt="">`)
            }
        }
        textData = `<div class="entry-content">${textDataTemplate.join('')}</div>`
        formData = new FormData(addBlogForm);
        formData.append("text", textData);










        // formData.append('entry_img', entry_img.files[0])
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
                addBlogForm.reset()
            });
    })
}

handleSubmit(addBlogForm)