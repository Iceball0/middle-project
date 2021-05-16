// Обращение к поисковой строке и карточкам

const searchbar = document.getElementById('searchbar');
const items = Array.from(document.getElementById('card-list').children);

// Функция, ищущая совпадения среди заголовков и подзаголовков на основе введённого в поисковую строку запроса

searchbar.addEventListener('ionInput', handleInput);

function handleInput(event) {
    const query = event.target.value.toLowerCase();
    requestAnimationFrame(() => {
        items.forEach(item => {
            const title = item.querySelector('ion-card-title');
            const subtitle = item.querySelector('ion-card-subtitle');
            const shouldShow = title.textContent.toLowerCase().indexOf(query) > -1;
            const shouldShow_2 = subtitle.textContent.toLowerCase().indexOf(query) > -1;
            
            // скрытие всех элементов не подходящих под поисковой запрос 
            item.style.display = shouldShow || shouldShow_2 ? 'block' : 'none';
        });
    });
}