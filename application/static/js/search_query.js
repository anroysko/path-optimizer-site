"use strict";

function toggleError(err_code) {
	document.getElementById("search-feedback-400").style.display = 'none';
	document.getElementById("search-feedback-401").style.display = 'none';
	document.getElementById("search-feedback-404").style.display = 'none';
	document.getElementById("search-feedback-" + err_code).style.display = 'block';
}

function searchMap() {
	var field = document.getElementById('search-id-field');
	const id = field.value;
	var val = parseInt(id);
	if (isNaN(val)) {
		toggleError("400");
	} else if (val <= 0) {
		toggleError("400");
	} else {
		const base_url = window.location.href.split('?')[0];
		const req_url = base_url + "map/search";
		console.log(req_url);

		// Post the search request
		var xhr = new XMLHttpRequest();
		xhr.open("POST", req_url, true);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.send(JSON.stringify({ "id": id }));
		xhr.onreadystatechange = function() {
			if (xhr.readyState == 4) {
				console.log(xhr.status);
				console.log(xhr.responseText);
				if (xhr.status == 204) {
					window.location.replace("/map/" + id);
				} else {
					toggleError("" + xhr.status);
				}
			}
		}
	}
	return false;
}
