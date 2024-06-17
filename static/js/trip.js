function count_items(parent, action){
    let number = parent.querySelector('[name="number"]');
    if (action==='+'){number.textContent = 1 + Number(number.textContent);}
    else if (action==='-'){number.textContent = Number(number.textContent) - 1;}
    check_count_items(parent);
}

 function check_count_items(parent){
    if (parent.querySelector('[name="number"]').textContent==='0'){
        parent.querySelector('[name="plus"]').style.cssText = 'display:None;';
        parent.querySelector('[name="minus"]').style.cssText = 'display:None;';
        parent.querySelector('[name="number"]').style.cssText = 'display:None;';
        parent.querySelector('[class="btn_list_item"]').style.cssText = 'display: inline-flex;';
        parent.querySelector('[name="number"]').classList.toggle('hide', true);}
 }

 function open_tools(elem){
    const container = elem.previousElementSibling;
    if (container.classList.contains('div_tools') === true){
        container.classList.toggle('tools_show', true);
        container.classList.toggle('div_tools', false);
    } else{
        container.classList.toggle('tools_show', false);
        container.classList.toggle('div_tools', true);
    }
}

 function event_click_list_item (event){
    event.stopPropagation();
    const span = event.currentTarget;
    const item = span.parentElement.parentElement;
    if (span.classList.contains('del_element_label') === true){
        span.classList.toggle('del_element_label', false);
        item.parentElement.prepend(item);
    } else{
        span.classList.toggle('del_element_label', true);
        item.parentElement.lastElementChild.before(item);
    }
}

 function count_btns_trip_list(elem){
    elem.style.cssText = 'display:None;';
    let elements = elem.parentElement.querySelectorAll('.count');
    elements.forEach((e) => {
        e.style.cssText = 'display:inline-flex;'});
        elements[1].textContent = '1';
        elements[1].classList.toggle('hide', false);
}

function upload_data_window(card){
    console.log(1);
    let wind = document.querySelector('.actions_window');
    wind.querySelector('.day_month').textContent = card.querySelector('.day_month').textContent;
    wind.querySelector('.month').textContent = card.querySelector('.month').textContent;
    wind.querySelector('.day_week').textContent = card.querySelector('.day_week').textContent;
    service = card.querySelector('.service_span_actions').textContent;
    if (typeof service !== 'undefined'){
            if (service.length !== 0){
                data = service.split(';');
                data.forEach((action) => {
                    let action_data = JSON.parse(action);
                    let inserted_elem = `<div class="action">
        <input type="text" class="action_name input_action">
        <input type="time" class="time_start input_action"><input type="time" class="time_end input_action">
        <button class="delete_action" onclick='delete_elem(this.parentElement)'><img src='/static/css/delete.png'></button>
    </div>`;
                    const body_action = document.querySelector('.actions_body');
                    body_action.insertAdjacentHTML('beforeend', inserted_elem);
                    body_action.lastElementChild.querySelector('.action_name').value = action_data['action_name'];
                    body_action.lastElementChild.querySelector('.time_start').value = action_data['time_start'];
                    body_action.lastElementChild.querySelector('.time_end').value = action_data['time_end'];
            });
        }
    }
}

function text_to_save(body){
    let text = '';
    body.querySelectorAll('.action').forEach((action) => {
        text = text + `{"action_name":"${action.querySelector('.action_name').value}",
        "time_start":"${action.querySelector('.time_start').value}",
        "time_end":"${action.querySelector('.time_end').value}"};`;
    });
    text = text.slice(0, -1);
    return text;
}

function upload_data_to_card() {
    let body = document.querySelector('.actions_body');
    if (body.hasChildNodes()) {
        let text = text_to_save(body);
        document.querySelectorAll('.card').forEach((card) => {
            const title = document.querySelector('.actions_title');
            if (card.querySelector('.day_month').textContent === title.querySelector('.day_month').textContent &&
                card.querySelector('.month').textContent === title.querySelector('.month').textContent) {
                card.querySelector('.service_span_actions').textContent = text;
                title.querySelector('.day_month').textContent = '';
                title.querySelector('.month').textContent = '';
                title.querySelector('.day_week').textContent = '';
            }
        });
        while (body.firstChild) {
            body.removeChild(body.firstChild);};
    }
}

function save_data_to_card(){
    let body = document.querySelector('.actions_body');
    if (body.hasChildNodes()) {
        let text = text_to_save(body);
        document.querySelectorAll('.card').forEach((card) => {
            const title = document.querySelector('.actions_title');
            if (card.querySelector('.day_month').textContent === title.querySelector('.day_month').textContent &&
                card.querySelector('.month').textContent === title.querySelector('.month').textContent) {
                card.querySelector('.service_span_actions').textContent = text;
            }
        });
    }
}

function card_actions (button){
    const parent = button.currentTarget.parentElement;
    let wind = document.querySelector('.actions_window');
    if(wind.querySelector('.day_month').textContent !== ''){
        if (wind.querySelector('.day_month').textContent !== parent.querySelector('.day_month').textContent ||
            wind.querySelector('.month').textContent !== parent.querySelector('.month').textContent){
            upload_data_to_card();
        }
    }
    upload_data_window(parent);
    document.querySelector('.actions_window').style.cssText = 'display:flex';
    document.querySelector('.trip_calendar').style.cssText = 'height:60%';
}

function delete_elem(element){
    element.remove();
}

function hide_action_window(){
    parent = document.querySelector('.actions_window');
    parent.style.cssText = 'display:none;';
    parent.previousElementSibling.style.cssText = 'height:100%;';
    upload_data_to_card();
}

let saved_categoties_dict;
let index_edited_section;
let index_edited_chapter;
let status_edit_modal_window;

function edit_element(element, status){
    if (status === 'list_item'){
        status_edit_modal_window = 'list_item';
        let chapter = element.parentElement.parentElement.parentElement;
        let section = element.parentElement.parentElement;
        index_edited_element = Array.from(section.querySelectorAll('.list_item')).indexOf(element.parentElement);
        index_edited_section = Array.from(chapter.querySelectorAll('.section')).indexOf(section);
        index_edited_chapter = Array.from(chapter.parentElement.querySelectorAll('.chapter')).indexOf(chapter);
        document.querySelector('.old_name').textContent = element.parentElement.firstElementChild.lastElementChild.textContent;
    } else if (status === 'category'){
        status_edit_modal_window = 'category';
        let chapter = element.parentElement.parentElement;
        let section = element.parentElement.nextElementSibling;
        index_edited_section = Array.from(chapter.querySelectorAll('.section')).indexOf(section);
        index_edited_chapter = Array.from(chapter.parentElement.querySelectorAll('.chapter')).indexOf(chapter);
        document.querySelector('.old_name').textContent = element.previousElementSibling.textContent;
    }
    document.querySelector('.modalBackground').style.cssText = 'display:flex;';
    document.querySelector('#modal_window_edit').style.cssText = 'display:flex;';
    document.querySelector('#modal_window_edit').classList.add('modal-animation');
}

function cancel(){
    document.querySelector('#modal_window_edit').style.cssText = 'display:none;';
    document.querySelector('.modalBackground').style.cssText = 'display:none;';
    document.querySelector('#modal_window_edit').classList.remove('modal-animation');
    document.querySelector('.new_name').value = '';
    document.querySelector('.old_name').textContent = '';
    document.querySelector('.save_adress').innerHTML = '';
}

function confirm(){
    document.querySelector('#modal_window_edit').style.cssText = 'display:none;';
    document.querySelector('.modalBackground').style.cssText = 'display:none;';
    document.querySelector('#modal_window_edit').classList.remove('modal-animation');
    if (status_edit_modal_window ==='category'){
        let chapter = Array.from(document.querySelector('.list').querySelectorAll('.chapter'))[index_edited_chapter]
        let section = Array.from(chapter.querySelectorAll('.section'))[index_edited_section]
        section.previousElementSibling.firstElementChild.textContent = document.querySelector('.new_name').value;
    } else if (status_edit_modal_window === 'list_item'){
        let chapter = Array.from(document.querySelector('.list').querySelectorAll('.chapter'))[index_edited_chapter]
        let section = Array.from(chapter.querySelectorAll('.section'))[index_edited_section]
        let list_item = Array.from(section.querySelectorAll('.list_item'))[index_edited_element]
        list_item.firstElementChild.lastElementChild.textContent = document.querySelector('.new_name').value;
    }
    document.querySelector('.new_name').value = '';
    document.querySelector('.old_name').textContent = '';
}

function data_collection (){
    let trip_dict = {}
    saved_categoties_dict = {}
    document.querySelectorAll('.chapter').forEach((chapter) => {
        let chapter_name = chapter.classList[0];
        let sections_data = {};
        chapter.querySelectorAll('.section').forEach((section) => {
            let  section_items_data = Array();
            section.querySelectorAll('.list_item').forEach((item) => {
                if (item.classList.contains('new_item') === false){
                    let item_data = {};
                    name = item.firstElementChild.lastElementChild.textContent;
                    let name_status = String(item.firstElementChild.lastElementChild.classList.contains('del_element_label'));
                    if (name_status === false){ name_status='fls'}
                    else if (name_status === true) {name_status='tr'}
                    let number;
                    if (item.querySelector('.number').classList.contains('hide')){number = '0';}
                    else{number = item.querySelector('.number').textContent;}
                    item_data["name"] = name;
                    item_data["name_status"] = name_status;
                    item_data["number"] = number;
                    section_items_data.push(item_data);
                }});
            let section_name = section.classList[0];
            sections_data[section_name] = section_items_data;
            });
            let sections_dict = {};
            chapter.querySelectorAll('.list_title').forEach((label_section) => {
                let section_name = label_section.classList[2];
                let section_status = label_section.parentElement.classList.contains('title_show');
                if (section_status === false){ section_status = 'fls'}
                    else if (section_status === true) {section_status = 'tr'}
                let section_name_ru = label_section.textContent;
                sections_dict[section_name] = {"name_en": section_name, "name_ru": section_name_ru,
                    "status": section_status, "data": sections_data[section_name]};
            });
        if (chapter.classList.contains('user_categories') !== true){
            trip_dict[chapter_name] = sections_dict;
        }
        else{
             saved_categoties_dict = sections_dict
        }
    });
    let calendar_data = Array();
    let calendar = document.querySelector('.calendar_table');
    calendar.querySelectorAll('.card').forEach((card) => {
        let calendar_day = {};
        calendar_day["day"] = card.querySelector('.day_month').textContent;
        calendar_day["month"] = card.querySelector('.month').textContent;
        calendar_day["day_week"] = card.querySelector('.day_week').textContent;
        calendar_day["actions"] = card.querySelector('.service_span_actions').textContent;
        calendar_data.push(calendar_day);
    });
    document.querySelector('#trip_data').value = JSON.stringify(trip_dict);
    document.querySelector('#calendar_data').value = JSON.stringify(calendar_data);
    document.querySelector('#saved_categories').value = JSON.stringify(saved_categoties_dict);
}

function save_data(){
    data_collection();
    document.querySelector('#submit_data_trip').click();
}

function toggle_list_items(event) {
    let elem = event.currentTarget.parentElement.nextElementSibling;
    if (elem.classList.contains('list_item_ani_show') === true) {
        elem.classList.toggle('list_item_ani_show', false);
        elem.classList.toggle('list_item_ani_hide', true);
    } else if (elem.classList.contains('list_item_ani_hide') === true) {
        elem.classList.toggle('list_item_ani_show', true);
        elem.classList.toggle('list_item_ani_hide', false);
    } else if (elem.classList.contains('list_item_ani_show') === false) {
        elem.classList.toggle('list_item_ani_show', true);
    }
}

function search_elements_section(section_name){
    let section = document.querySelector(`.${section_name}`);
    let items = [];
    section.querySelectorAll('.list_item').forEach((item) => {
        items.push(item.querySelector('label>span').textContent);
    });
    return items;
}

const winter_clothes = document.querySelector('div.winter_clothes');
const clothes = document.querySelector('div.clothes');

function select_items_one_count(items){
    clothes.querySelectorAll('.list_item').forEach((elem) => {
        if (elem.classList.contains('new_item') !== true){
            let name_elem = elem.querySelector('label>span').textContent
            if (items.includes(name_elem)){
                elem.querySelector('.btn_list_item').click();
            }
        }
    })
}

function winter_spring_and_autumn_winter(){
    winter_clothes.querySelectorAll('.list_item').forEach((elem) =>{
        let clothes_winter = ['Варежки|Перчатки', 'Свитер', 'Шапка', 'Термобелье', 'Шарф', 'Куртка зимняя']
        if (elem.classList.contains('new_item') !== true){
            let name_elem = elem.querySelector('label>span').textContent
            if (clothes_winter.includes(name_elem)){
                if (name_elem === 'Термобелье' || name_elem === 'Варежки|Перчатки'){
                    elem.querySelector('.btn_list_item').click();
                    if (count_days>3){elem.querySelector('.btns_count>span').textContent = 2;}
                } else{
                    elem.querySelector('.btn_list_item').click();
                }
            }
        }
    })
    let items = ['Куртка'];
    select_items_one_count(items);
}

function middle_spring_and_middle_autumn(){
    winter_clothes.querySelectorAll('.list_item').forEach((elem) =>{
        if (elem.classList.contains('new_item') !== true){
            if (['Свитер', 'Шапка'].includes(elem.querySelector('label>span').textContent)){
                elem.querySelector('.btn_list_item').click();
            }
        }
    })
    let items = ['Жилетка', 'Куртка'];
    select_items_one_count(items);
}

async function load_lk(){
    fetch('/load_lk', {
        method: 'POST'})
        .then(response => response.text())
        .then(html => {
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
})}
async function back_lk(status){
    data_collection()
    let url;
    if (status === 'edit'){url = '/edit_trip'}
    else if (status === 'save') {url = '/save_trip'}
    await fetch (url, {
        method: 'POST', // Метод запроса (GET, POST, PUT, DELETE, PATCH и т.д.)
        headers: {
        'Content-Type': 'application/json' // Тип данных в теле запроса
        },
        body: JSON.stringify({ // Тело запроса в формате JSON
            trip_data: document.querySelector('#trip_data').value,
            calendar_data: document.querySelector('#calendar_data').value,
            saved_categories: document.querySelector('#saved_categories').value
        })
    });
await load_lk()}

window.addEventListener('load', () => {
    if (document.querySelector('.weather')){
        let international = document.querySelector('div.international')
        international.querySelectorAll('.list_item').forEach((elem) => {
            if (elem.classList.contains('new_item') !== true){
                elem.querySelector('.btn_list_item').click();}
        })
        const formal_clothes_arr = ['Пиджак', 'Рубашка', 'Брюки'];
        let formal_clothes = document.querySelector('div.formal_clothes')
        formal_clothes.querySelectorAll('.list_item').forEach((elem) => {
            if (elem.classList.contains('new_item') !== true){
                if (formal_clothes_arr.includes(elem.querySelector('label>span').textContent)){
                    elem.querySelector('.btn_list_item').click();}
            }
        })
    }
    let count_days = document.querySelectorAll('.elem_calendar').length;
    clothes.querySelectorAll('.list_item').forEach((elem) => {
        if (elem.classList.contains('new_item') !== true){
            if (elem.querySelector('label>span').textContent === 'Обувь'){
                elem.querySelector('.btn_list_item').click();
                elem.querySelector('.btns_count>span').textContent = 2;
            }
            if (elem.querySelector('label>span').textContent === 'Нижнее белье' ||
                    elem.querySelector('label>span').textContent === 'Носки' ){
                elem.querySelector('.btn_list_item').click();
                elem.querySelector('.btns_count>span').textContent = count_days;
            }
            if (elem.querySelector('label>span').textContent === 'Футболка'){
                elem.querySelector('.btn_list_item').click();
                if (count_days%2===0){
                    elem.querySelector('.btns_count>span').textContent = count_days/2;
                }else if (count_days%2===1){
                    elem.querySelector('.btns_count>span').textContent = (count_days+1)/2;
                }
            }
             if (elem.querySelector('label>span').textContent === 'Джинсы'){
                elem.querySelector('.btn_list_item').click();
            }
        }
    })
    const months = [['Декабрь', 'Январь', 'Февраль'], ['Март', 'Апрель', 'Май'],
                            ['Июнь', 'Июль', 'Август'], ['Сентябрь', 'Октябрь', 'Ноябрь']];
    let month = document.querySelector('.calendar_table div p:first-child .month').textContent;
    for (let i=0; i<4;i++){
        if (months[i].includes(month)){
            if (i===0){
                winter_clothes.querySelectorAll('.list_item').forEach((elem) =>{
                    clothes_winter = ['Варежки|Перчатки', 'Свитер', 'Шапка', 'Термобелье', 'Шарф', 'Куртка зимняя'];
                    if (elem.classList.contains('new_item') !== true){
                        let name_elem = elem.querySelector('label>span').textContent;
                        if (clothes_winter.includes(name_elem)){
                            if (name_elem === 'Термобелье' || name_elem === 'Варежки|Перчатки'){
                                elem.querySelector('.btn_list_item').click();
                                if (count_days>3){elem.querySelector('.btns_count>span').textContent = 2;}
                            } else{
                                elem.querySelector('.btn_list_item').click();
                            }
                        }
                    }
                })
            } else if (i===1){
                if (month==='Март'){
                    winter_spring_and_autumn_winter();
                }
                if (month==='Апрель'){
                    middle_spring_and_middle_autumn();
                }
                if (month==='Май'){
                    let items = ['Жилетка', 'Куртка', 'Шорты'];
                    select_items_one_count(items);
                }
            } else if (i===2){
                let items = ['Жилетка', 'Куртка', 'Шорты'];
                select_items_one_count(items);
            } else if (i===3){
                if (month==='Сентябрь'){
                    let items = ['Жилетка', 'Куртка'];
                    select_items_one_count(items);
                } if (month==='Октябрь'){
                    middle_spring_and_middle_autumn();
                } if (month==='Ноябрь'){
                    winter_spring_and_autumn_winter();
                }
            }
        }
    }
})



















