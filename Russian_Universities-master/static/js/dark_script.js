// Обращение к элементам на странице с проверкой их сущестования

const toggle = document.querySelector('#themeToggle');

if (document.getElementById('card-list')) {
    window.cards = Array.from(document.getElementById('card-list').children);
};

if (document.getElementById('news-list')) {
    window.news = Array.from(document.getElementById('news-list').children);
};

if (document.getElementsByClassName('form_input')) {
    window.form_input = Array.from(document.getElementsByClassName('form_input'));
};

const searchbar_dark = document.querySelector('#searchbar');

// Проверка существования куки и изменение темы в зависимости от данных в куки

if (get_cookie('theme')) {
    if (get_cookie('theme') == 'dark'){
        if (toggle) {
            toggle.checked = true;
        }
        if (!document.body.classList.contains('dark')) {
            document.body.classList.add('dark');

            if (document.getElementById('card-list')) {
                cards.forEach(item => {
                    item.classList.add('dark');
                });
            };

            if (document.getElementById('news-list')) {
                news.forEach(item => {
                    item.classList.add('dark');
                });
            };

            if (document.getElementsByClassName('form_input')) {
                form_input.forEach(item => {
                    item.classList.add('dark');
                });
            };

            if (searchbar_dark) {
                searchbar_dark.classList.add('dark');
            };
        }
    }
    else {
        if (toggle) {
            toggle.checked = false
        }
        if (document.body.classList.contains('dark')) {
            document.body.classList.remove('dark');

            if (document.getElementById('card-list')) {
                cards.forEach(item => {
                    item.classList.remove('dark');
                });
            };

            if (document.getElementById('news-list')) {
                news.forEach(item => {
                    item.classList.remove('dark');
                });
            };

            if (document.getElementsByClassName('form_input')) {
                form_input.forEach(item => {
                    item.classList.remove('dark');
                });
            };

            if (document.getElementById('card-list')) {
                searchbar_dark.classList.remove('dark');
            };
        }
    }
}

// Обработка переключателя, создание куки, где хранится информация о включенной теме

if (toggle) {
    toggle.addEventListener('ionChange', (ev) => {
        document.body.classList.toggle('dark', ev.detail.checked);
        cards.forEach(item => {
            item.classList.toggle('dark');
        });
        if (document.getElementById('news-list')) {
            news.forEach(item => {
                item.classList.toggle('dark');
            });
        };
        searchbar_dark.classList.toggle('dark');
        if (document.body.classList.contains('dark')) {
            var cookie_date = new Date();
            cookie_date.setYear(cookie_date.getFullYear() + 1);
            document.cookie = "theme=dark;expires=" + cookie_date.toUTCString()
        }
        else {
            var cookie_date = new Date();
            cookie_date.setYear(cookie_date.getFullYear() + 1);
            document.cookie = "theme=light;expires=" + cookie_date.toUTCString()
        }
    });
};

// переключение темы в зависимости от темы браузера

const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

prefersDark.addListener((e) => checkToggle(e.matches));


function loadApp() {
    checkToggle(prefersDark.matches);
}


function checkToggle(shouldCheck) {
    if (!get_cookie('theme')) {
        toggle.checked = shouldCheck;
    }
}

// функция получения куки

function get_cookie ( cookie_name )
{
    var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );
 
    if ( results )
        return ( unescape ( results[2] ) );
    else
        return null;
}