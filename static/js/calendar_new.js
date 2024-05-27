let startDate = null;
let endDate = null;
let selectedDates = [];

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
    // const prevMonth = currentMonth === 0 ? 11 : ;
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
	console.log(clicks);
	if (clicks === 3){ clearSelection();  clicks = 0;console.log(clicks);}
}

document.querySelectorAll('.day').forEach((day) => {
	day.addEventListener('click', ()=> count_clicks() );
});

document.querySelector('.calendar-days').addEventListener('click', () => count_clicks() );

clearSelection();