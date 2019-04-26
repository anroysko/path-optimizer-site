
function setHexJsonState(jsn) {
	var dts = document.getElementById("hex-grid").dataset;
	dts.hexes = JSON.stringify(jsn);
}

function getHexJsonState() {
	var dts = document.getElementById("hex-grid").dataset;
	return JSON.parse(dts.hexes);
}

function hexClick(x, y) {
	var dts = document.getElementById("hex-grid").dataset;
	const w = parseInt(dts.w);
	const h = parseInt(dts.h);
	const i = x+y*(w+1);

	var list = document.getElementById("" + x + "," + y).classList;

	var state = getHexJsonState();
	var hex_state = state[i];
	if (hex_state === undefined) {
		state[i] = "1";
		// None -> City
		list.add('hex-city')
	} else if (hex_state === "1") {
		state[i] = "2";
		// City -> Road
		list.remove('hex-city');
		list.add('hex-road');
	} else if (hex_state === "2") {
		delete state[i];
		// Road -> None
		list.remove('hex-road');
	}
	setHexJsonState(state);

	window.onbeforeunload = function() {
		return true;
	}
}

function saveChanges() {
	const base_url = window.location.href
	const req_url = base_url + "/save";

	// Post the save request
	var xhr = new XMLHttpRequest();
	xhr.open("POST", req_url, true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify(getHexJsonState()));

	// Remove warning about leaving with unsaved changes
	window.onbeforeunload = null;
}

function optimize() {
	alert("test")
}
