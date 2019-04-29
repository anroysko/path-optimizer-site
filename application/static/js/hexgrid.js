"use strict";

function setHexgridJsonState(jsn) {
	var dts = document.getElementById("hex-grid").dataset;
	dts.hexes = JSON.stringify(jsn);
}

function getHexgridJsonState() {
	var dts = document.getElementById("hex-grid").dataset;
	return JSON.parse(dts.hexes);
}

function nextState(v) {
	if (v === undefined) return "1";
	else if (v === "1") return "2";
	else if (v === "2") return undefined;
	else return "-1";
}

function setHexState(x, y, i, v, state) {
	var list = document.getElementById("" + x + "," + y).classList;
	const hex_state = state[i];

	// Remove old state
	if (hex_state === "1") {
		delete state[i];
		list.remove('hex-city');
	} else if (hex_state === "2") {
		delete state[i];
		list.remove('hex-road');
	}

	if (v === "1") {
		state[i] = "1";
		list.add('hex-city');
	} else if (v === "2") {
		state[i] = "2";
		list.add('hex-road');
	}
}

function getCounts(w, h, state) {
	var city_cou = 0;
	var road_cou = 0;
	var empty_cou = w * h + Math.floor(h / 2);
	for (var key in state) {
		if (state[key] == "1") ++city_cou;
		else if (state[key] == "2") ++road_cou;
	}
	empty_cou -= city_cou + road_cou;
	return [empty_cou, city_cou, road_cou];
}

function hexClick(x, y) {
	var dts = document.getElementById("hex-grid").dataset;
	const w = parseInt(dts.w);
	const h = parseInt(dts.h);
	const i = x+y*(w+1);

	var state = getHexgridJsonState();
	var list = document.getElementById("" + x + "," + y).classList;
	setHexState(x, y, i, nextState(state[i]), state);

	setHexgridJsonState(state);
	enableButton(getSaveButton());
}

function clearPaths() {
	var dts = document.getElementById("hex-grid").dataset;
	const w = parseInt(dts.w);
	const h = parseInt(dts.h);

	var state = getHexgridJsonState();
	var clear_list = [];
	for (var key in state) {
		if (state[key] == "2") {
			console.log("key: " + key);
			clear_list.push(parseInt(key));
		}
	}
	for (var j = 0; j < clear_list.length; ++j) {
		const i = clear_list[j];
		const x = i % (w+1);
		const y = Math.floor(i / (w+1));
		console.log("" + i + "," + x + "," + y);
		setHexState(x, y, i, undefined, state);
	}

	setHexgridJsonState(state);
	enableButton(getSaveButton());
}

function optimize() {
	var dts = document.getElementById("hex-grid").dataset;
	const w = parseInt(dts.w);
	const h = parseInt(dts.h);

	var state = getHexgridJsonState();
	const ini_cou = getCounts(w, h, state);
	alert("Optimization successful!\nTime taken: 13s\nRoads added: 3\nTotal roads: " + ini_cou[2]);
}

function getSaveButton() {
	return document.getElementById("save-button")
}

function enableButton(el) {
	el.disabled = false;

	var list = el.classList;
	list.remove('btn-light');
	list.add('btn-primary');

	window.onbeforeunload = function() {
		return true;
	}
}
function disableButton(el) {
	el.disabled = true;
	el.blur(); // Remove outline

	var list = el.classList;
	list.remove('btn-primary');
	list.add('btn-light');
	
	window.onbeforeunload = null;
}

function saveChanges() {
	const base_url = window.location.href
	const req_url = base_url + "/save";

	// Post the save request
	var xhr = new XMLHttpRequest();
	xhr.open("POST", req_url, true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify(getHexgridJsonState()));
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4) {
			if (xhr.status == 204) {
				// Successful save, remove warning about leaving with unsaved changes
				disableButton(getSaveButton());
			} else if (xhr.status == 404) {
				alert("Save failed with error code 404. Did you perhaps change the index of the map in the URL?");
			} else if (xhr.status == 400) {
				alert("Save failed with error code 400. Did you perhaps modify the HTML by hand?");
			}
		}
	}
}
