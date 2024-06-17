let buttons = document.querySelectorAll('.button_trip, .type_trip');
buttons.forEach((elem) => {
	elem.addEventListener("click", function(event) {
		let child = event.currentTarget.firstElementChild;
		if (child.getAttribute('checked')!=='true'){
			toggle_check(child, true);}
		else{
			toggle_check(child, false);}
	})});

function toggle_check(elem, status){elem.classList.toggle('checked', status);
								elem.setAttribute('checked', `${status}`);}

function check_winter_clothes(){
	 if (document.querySelector('#winter_clothes').getAttribute('checked')!=='true'){
		toggle_check(document.querySelector('#winter_clothes'), true);
	}
}

function check_clothes(){
	if (document.querySelector('#clothes').getAttribute('checked')!=='true'){
		toggle_check(document.querySelector('#clothes'), true);
	}
}

window.addEventListener('load', () => {
	let list = [ 'essentials', 'toiletries', 'clothes', 'international', 'dinner', 'formal_clothes','work'];
	if (document.querySelector('#business').innerHTML === 'true'){
		list.forEach((elem) => toggle_check(document.querySelector(`#${elem}`), true));
	}
	if (document.getElementById('vacation').innerHTML === 'true'){
		for (let i=0; i<5;i++){
			if (document.querySelector(`#${list[i]}`).getAttribute('checked')!=="true")
			{toggle_check(document.querySelector(`#${list[i]}`),true)};
		}
	}
	check_clothes()
	if (document.querySelector('#country').textContent === 'china'){
		if (document.querySelector('#formal_clothes').getAttribute('checked')!=='true'){
			toggle_check(document.querySelector('#formal_clothes'), true);
		}
		if (document.querySelector('#international').getAttribute('checked')!=='true'){
			toggle_check(document.querySelector('#international'), true);
		}
	}
	const months = [['Декабрь', 'Январь', 'Февраль'], ['Март', 'Апрель', 'Май'], ['Июнь', 'Июль', 'Август'], ['Сентябрь', 'Октябрь', 'Ноябрь']]
	let month = document.querySelector('#month').textContent
    for (let i=0; i<4;i++){
        if (months[i].includes(month)){
            if (i===0){check_winter_clothes()
            } else if (i===1){
                if (month==='Март'){check_winter_clothes()}
                if (month==='Апрель'){check_winter_clothes()}
            } else if (i===3){
				if (month==='Ноябрь'){check_winter_clothes()}
            }
        }
    }
});
