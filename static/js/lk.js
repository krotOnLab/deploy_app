function toggle_list_items(event) {
    let elem = event.currentTarget.nextElementSibling;
    console.log(elem)
    console.log(elem.classList.contains('hide'))
    if (elem.classList.contains('show') === true) {
        elem.classList.toggle('show', false);
        elem.classList.toggle('hide', true);
    } else if (elem.classList.contains('hide') === true) {
        elem.classList.toggle('show', true);
        elem.classList.toggle('hide', false);
    } else if (elem.classList.contains('show') === false) {
        elem.classList.toggle('show', true);
    }
}
function delete_trip(elem){
    let trip = elem.parentElement
    trip.style.cssText = 'display:None;';
    fetch('/delete_trip', {
            method: 'POST', // Метод запроса
            headers: {
                'Content-Type': 'application/json' // Тип контента
            },
            body: JSON.stringify({id_trip: trip.querySelector('#uuid').textContent})
            // body: JSON.stringify({id_trip: trip.querySelector('#uuid').textContent}) // Преобразуем объект в строку JSON
        })
              .then(response => response.text()) // Получаем текст ответа
              .then(html => {
                // Вставляем полученный HTML в элемент на странице
                document.querySelector('html').innerHTML = html;
                document.querySelectorAll('p.materials').forEach((p) =>{
                    p.addEventListener('click', (event) => toggle_list_items(event))
                });
                document.querySelectorAll('.description_trip').forEach((trip) => {
                    trip.addEventListener('click', (event) => {
                        let t = event.currentTarget
                        text = `{"uuid":"${t.querySelector('#uuid').textContent}"}`
                        document.querySelector('.data').value = text
                        document.querySelector('.load').click()
                    } )
                });
              })
              .catch(error => {
                // Обработка ошибок
                console.error('Ошибка:', error);
              });
}
// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelectorAll('p.materials').forEach((p) =>{
//         p.addEventListener('click', (event) => toggle_list_items(event))
//     });
//     document.querySelectorAll('.description_trip').forEach((trip) => {
//         trip.addEventListener('click', (event) => {
//             let t = event.currentTarget
//             text = `{"uuid":"${t.querySelector('#uuid').textContent}"}`
//             document.querySelector('.data').value = text
//             document.querySelector('.load').click()
//         } )
//     });
// })
window.addEventListener('load', () => {
    document.querySelectorAll('p.materials').forEach((p) =>{
        p.addEventListener('click', (event) => toggle_list_items(event))
    });
    document.querySelectorAll('.description_trip').forEach((trip) => {
        trip.addEventListener('click', (event) => {
            let t = event.currentTarget
            text = `{"uuid":"${t.querySelector('#uuid').textContent}"}`
            document.querySelector('.data').value = text
            document.querySelector('.load').click()
        } )
    });
})
