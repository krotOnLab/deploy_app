let startDate = null;
let endDate = null;
let selectedDates = [];
let saved_dates = document.querySelector('#dates_for_script').getAttribute('data-for-script')

function renderCalendar(year, month) {
    const monthYearElement = document.getElementById('monthYear');
    const calendarDaysElement = document.querySelector('.calendar-days');
    calendarDaysElement.innerHTML = '';
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDay = new Date(year, month, 1).getDay();
    monthYearElement.textContent = new Date(year, month).toLocaleString('default', { month: 'long', year: 'numeric' });
    for (let i = 0; i < firstDay; i++) {
        const dayElement = document.createElement('div');
        dayElement.classList.add('day', 'prev-month');
        dayElement.textContent = '';
        calendarDaysElement.appendChild(dayElement);
    }
    for (let i = 1; i <= daysInMonth; i++) {
        const dayElement = document.createElement('div');
        dayElement.classList.add('day');
        dayElement.textContent = i;
        dayElement.addEventListener('click', () => selectDate(year, month, i));
        calendarDaysElement.appendChild(dayElement);
    }
    // Отображение выбранных дат в соседних месяцах
    selectedDates.forEach(date => {
        const selectedYear = date.getFullYear();
        const selectedMonth = date.getMonth();
        if (selectedYear === year && selectedMonth === month) {
            const day = date.getDate();
            const days = document.querySelectorAll('.day');
            days[day + firstDay - 1].classList.add('selected');
        }
    });
}

function selectDate(year, month, day) {
    const currentDate = new Date(year, month, day);

    if (!startDate || (startDate && endDate)) {
        startDate = currentDate;
        endDate = null;
    } else if (currentDate < startDate) {
        endDate = startDate;
        startDate = currentDate;
    } else {
        endDate = currentDate;
    }
    let rangeDates = Array()
    selectedDates = getDatesRange(startDate, endDate)
    selectedDates.forEach((date) => rangeDates.push(new Intl.DateTimeFormat('ru').format(date)));
    renderCalendar(year, month);
	document.getElementById('range').textContent = `${rangeDates[0]},${rangeDates[rangeDates.length-1]}`
}

function getDatesRange(startDate, endDate) {
    const datesRange = [];
    let currentDate = new Date(startDate);
    while (currentDate <= endDate) {
        datesRange.push(new Date(currentDate));
        currentDate.setDate(currentDate.getDate() + 1);
    }
    return datesRange;
}

function clearSelection() {
    startDate = null;
    endDate = null;
    selectedDates = [];
    renderCalendar(new Date().getFullYear(), new Date().getMonth());
}

const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

prevBtn.addEventListener('click', () => {
    selectedDates = [];
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    const prevMonth = currentMonth === 0 ? 11 : currentMonth - 1;
    const prevYear = currentMonth === 0 ? currentYear - 1 : currentYear;
    renderCalendar(prevYear, prevMonth);
});

nextBtn.addEventListener('click', () => {
    selectedDates = [];
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    const nextMonth = currentMonth === 11 ? 0 : currentMonth + 1;
    const nextYear = currentMonth === 11 ? currentYear + 1 : currentYear;
    renderCalendar(nextYear, nextMonth);
});

let clicks = 0;

function count_clicks(){
	clicks = clicks + 1;
	if (clicks === 3){ clearSelection();  clicks = 0;console.log(clicks);}
}

document.querySelectorAll('.day').forEach((day) => {
	day.addEventListener('click', ()=> count_clicks() );
});

document.querySelector('.calendar-days').addEventListener('click', () => count_clicks() );

clearSelection();
set_dates();


function set_dates(){
    if (saved_dates !== ''){
        let dates = saved_dates.split(',')
        document.querySelectorAll('.day').forEach((elem) => {
            dates = [dates[0].split('.')[0].replace('0', ''), dates[1].split('.')[0].replace('0', '')]
            console.log(elem.textContent)
            console.log(dates[0], dates[1], typeof dates[0])
            console.log(elem.textContent == dates[0] || elem.textContent == dates[1])
            if (elem.textContent == dates[0] || elem.textContent == dates[1]){
                elem.click();
            }
        })
    }

}