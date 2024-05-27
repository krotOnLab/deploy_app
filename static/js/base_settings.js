document.querySelector('#new_trip').addEventListener('click', function () {
	document.querySelector('#submit_dates').setAttribute('value', document.querySelector('#range').textContent);
	document.querySelector('#submit_business').setAttribute('value', document.querySelector('#business').getAttribute('checked'));
	document.querySelector('#submit_vacation').setAttribute('value', document.querySelector('#vacation').getAttribute('checked'));
	document.querySelector('#submit').click();
});

function toggle_check(elem, status){elem.classList.toggle('checked', status);
									elem.setAttribute('checked', `${status}`);};
let buttons = document.querySelectorAll('.type_trip');
buttons.forEach((elem) => {
	elem.addEventListener("click", function(event) {
		let child = event.currentTarget.firstElementChild
		if (child.getAttribute('checked')!='true'){
			toggle_check(child, true)}
		else{
			toggle_check(child, false)}
	})});
