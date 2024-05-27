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
								elem.setAttribute('checked', `${status}`);};

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
});
