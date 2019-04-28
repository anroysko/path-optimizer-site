"use strict";

function buildPermBox(usr, perm) {
	var container = document.createElement("div");
	container.setAttribute("class", "col-sm-3 p-2 bd-highlight border rounded");
	container.setAttribute("id", perm + "-perm-" + usr);
	container.setAttribute("role", "alert");

	var link = document.createElement("a");
	link.setAttribute("href", "javascript:;");
	link.innerHTML = usr;

	// nothing bad can really happen here since the user has to write out the string "usr" themselves, and
	// additionally, to get here, it must be a valid username. It's not my bad if you shoot yourself in the foot.	

	var button = document.createElement("button");
	button.setAttribute("type", "button");
	button.setAttribute("class", "close");
	button.setAttribute("onclick", "removePerms('" + usr + "')");
	button.setAttribute("aria-label", "Close");
	button.innerHTML = "<span aria-hidden='true'>&times;</span>";
	
	container.appendChild(link);
	container.appendChild(button);
	return container;
}

function addViewPermBox(usr) {
	var view_row = document.getElementById("view-perm-users");
	view_row.appendChild(buildPermBox(usr, "view"));
}
function removeViewPermBox(usr) {
	var el = document.getElementById("view-perm-" + usr);
	if (el) el.remove();
}
function addEditPermBox(usr) {
	var edit_row = document.getElementById("edit-perm-users");
	edit_row.appendChild(buildPermBox(usr, "edit"));
}
function removeEditPermBox(usr) {
	var el = document.getElementById("edit-perm-" + usr);
	if (el) el.remove();
}

function updateHTML(usr, vp, ep) {
	removeViewPermBox(usr);
	removeEditPermBox(usr);

	if (vp && !ep) {
		addViewPermBox(usr);
	} else if (vp && ep) {
		addEditPermBox(usr);
	}
}

function changePerms(usr, vp, ep, delayed) {
	const base_url = window.location.href;
	const req_url = base_url + "/edit_perms";

	// Post the save request
	var xhr = new XMLHttpRequest();
	xhr.open("POST", req_url, true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify({ "user": usr, "view_perm": (vp ? "true" : "false"), "edit_perm": (ep ? "true" : "false")}));
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4) {
			if (xhr.status == 204) {
				if (delayed) {
					updateHTML(usr, vp, ep);
				}
				console.log("Successfully changed perms for user=" + usr + ", view_perm=" + vp + ", edit_perm=" + ep);
			} else {
				console.log("Failed to change perms (" + xhr.status + ") for user=" + usr + ", view_perm=" + vp + ", edit_perm=" + ep);
			}
		}
	}
}

function removePerms(usr) {
	changePerms(usr, false, false, false);
	updateHTML(usr, false, false);
}

function viewShareSubmit() {
	var field = document.getElementById('viewShareTo');
	const usr = field.value;
	field.value = "";
	
	changePerms(usr, true, false, true);
	return false;
}

function editShareSubmit() {
	var field = document.getElementById('editShareTo');
	const usr = field.value;
	field.value = "";
	
	changePerms(usr, true, true, true);
	return false;
}
