document.getElementById('create_trip').addEventListener('click', () => {
        let text = '{';
        document.querySelectorAll('.check_type').forEach((elem) => {
            text = text + `"${elem.getAttribute('id')}":"${elem.getAttribute('checked')}", `
        });
        text = text.slice(0, -2);
        text = text + '}';
        document.querySelector('#text').setAttribute('value', text);
		document.getElementById('submit_btn').click();});