// форма для отправки на сервер, появляющаяся по нажатию на кнопку

customElements.define('modal-page', class ModalContent extends HTMLElement {
    connectedCallback() {
        // изменения в форме в зависимости от цели использования (добавление/редактирование) 
        if (edit_mode == 'add') {
            var inputs = `
                        <ion-item>
                            <ion-label position="floating">Имя</ion-label>
                            <ion-input id="name" name="name" placeholder="Введите ваше имя" required></ion-input>
                        </ion-item>
                        <ion-item>
                            <ion-label position="floating">Текст</ion-label>
                            <ion-input id="opinion" name="opinion" placeholder="Введите ваше мнение об университете" required></ion-input>
                        </ion-item>
                        <ion-item>
                            <ion-label position="floating">Оценка</ion-label>
                            <ion-input id="rating" name="rating" placeholder="Введите вашу оценку" type="number" required></ion-input>
                        </ion-item>
            `;
            var but_name = 'add-submit';
        }
        else {
            var inputs = `
                        <ion-item>
                            <ion-label position="floating">Ссылка</ion-label>
                            <ion-input id="url" name="url" placeholder="Введите ссылку на новости" required></ion-input>
                        </ion-item>
                        <ion-item>
                            <ion-label position="floating">Название</ion-label>
                            <ion-input id="title" name="title" placeholder="Введите блок и класс названия" required></ion-input>
                        </ion-item>
                        <ion-item>
                            <ion-label position="floating">Ссылка</ion-label>
                            <ion-input id="news_url" name="news_url" placeholder="Введите блок и класс ссылки" required></ion-input>
                        </ion-item>
                        <ion-item>
                            <ion-label position="floating">Картинка</ion-label>
                            <ion-input id="image" name="image" placeholder="Введите блок и класс картинки" required></ion-input>
                        </ion-item>
                        <ion-item>
                            <ion-label position="floating">Текст</ion-label>
                            <ion-input id="text" name="text" placeholder="Введите блок и класс текста" required></ion-input>
                        </ion-item>
                        <ion-item>
                            <ion-label position="floating">Дата</ion-label>
                            <ion-input id="date" name="date" placeholder="Введите блок и класс даты" required></ion-input>
                        </ion-item>
            `;
            var but_name = 'edit-submit';
        }
        this.innerHTML = `
            <ion-header translucent>
                <ion-toolbar>
                    <ion-title class="modal-title">Редактирование новостей</ion-title>
                    <ion-buttons slot="end">
                        <ion-button onclick="dismissModal()">Закрыть</ion-button>
                    </ion-buttons>
                </ion-toolbar>
            </ion-header>
            <ion-content fullscreen>
                <form action="" method="post" enctype="multipart/form-data">
                    <input id="univ-id" name="univ-id" hidden />
                    <ion-list class="modal-list">
                    ${inputs}    
                    </ion-list>
                    <ion-item class="box">
                        <input type="submit" id="submit" class="input-button" name="${but_name}" />
                        <label for="submit" class="submit-button ion-activatable">
                            <ion-icon name="aperture-outline" slot="start" class="submit-icon"></ion-icon>
                            <span>Подтвердить</span>
                            <ion-ripple-effect class="submit-file-button-effect" slot="start"></ion-ripple-effect>
                        </label>
                    </ion-item>
                </form>
            </ion-content>
        `;
    }
});

var edit_mode = 'edit';
var pause = false;

let currentModal = null;

// отображение формы по нажатию на кнопку "редактировать"
const button = document.getElementsByClassName('edit-button')[0]
button.addEventListener('click', () => {
    edit_mode = 'edit';
    presentModal();
});

// отображение формы по нажатию на кнопку "добавить"
const button2 = document.getElementsByClassName('add-button')[0]
button2.addEventListener('click', () => {
    edit_mode = 'add';
    presentModal();
});

// функция отображения формы
function presentModal() {
    const modalElement = document.createElement('ion-modal');
    modalElement.component = 'modal-page';
    modalElement.cssClass = 'my-custom-class';

    currentModal = modalElement

    document.body.appendChild(modalElement);
    return modalElement.present();
}

// функция закрытия формы
function dismissModal() {
    if (currentModal) {
        currentModal.dismiss().then(() => { currentModal = null; });
        setTimeout(() => { pause = false; }, 500);
        
    }
}

document.documentElement.style.setProperty('--effect-width', '210px');
let i = setInterval(function() {

    // авто заполнение полей данными из переменных
    if (document.getElementById("title")){
        if (!pause) {
            document.getElementById("url").value = url;
            document.getElementById("title").value = title;
            document.getElementById("news_url").value = news_url;
            document.getElementById("image").value = image;
            document.getElementById("text").value = text;
            document.getElementById("date").value = date;
            pause = true;
        }
        
    }

}, 100);