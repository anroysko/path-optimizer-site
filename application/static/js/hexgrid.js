"use strict";

function setHexgridJsonState(jsn) {
	var dts = document.getElementById("hex-grid").dataset;
	dts.hexes = JSON.stringify(jsn);
}

function getHexgridJsonState() {
	var dts = document.getElementById("hex-grid").dataset;
	return JSON.parse(dts.hexes);
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
			clear_list.push(parseInt(key));
		}
	}
	for (var j = 0; j < clear_list.length; ++j) {
		const i = clear_list[j];
		const x = i % (w+1);
		const y = Math.floor(i / (w+1));
		setHexState(x, y, i, undefined, state);
	}

	setHexgridJsonState(state);
	enableButton(getSaveButton());
}

function buildEdges(w, h) {
	var edges = []
	for (var y = 0; y < h; ++y) {
		for (var x = 0; x <= w; ++x) {
			const i = x + y * (w+1);

			var targets = [];
			if ((y % 2 == 1) || (x < w)) {
				if (y % 2 == 0) {
					if (x > 0) {
						targets.push(i-1); // left
					}
					if (y > 0) {
						targets.push(i - (w+1)); // up-left
						targets.push(i - (w+1) + 1); // up-right
					}
					if (x+1 < w) {
						targets.push(i + 1); // right
					}
					if (y+1 < h) {
						targets.push(i + (w+1) + 1); // down-right
						targets.push(i + (w+1)); // down-left
					}
				} else {
					if (x > 0) {
						targets.push(i-1); // left
					}
					if (y > 0) {
						if (x > 0) {
							targets.push(i - (w+1) - 1); // up-left
						}
						if (x < w) {
							targets.push(i - (w+1)); // up-right
						}
					}
					if (x+1 < w+1) {
						targets.push(i + 1); // right
					}
					if (y+1 < h) {
						if (x < w) {
							targets.push(i + (w+1)); // down-right
						}
						if (x > 0) {
							targets.push(i + (w+1) - 1); // down-left
						}
					}
				}
			}
			edges.push(targets);
		}
	}
	return edges;
}

// Builds path from the given node to any position where the mask tree breaks
// Returns true if it made any progress. This is to prevent going back-and-forth in a road piece
function buildPaths(i, mask, visited, edges, data_array, dp) {
	visited[mask][i] = true;
	if (dp[mask][i] == 0) return true; // base case

	// Test if we can split here
	const node_cost = (data_array[i] == 0 ? 1 : 0);
	var splitmask = -1;
	for (var submask = mask; submask != 0; submask = (submask - 1) & mask) {
		const invmask = mask ^ submask;
		if (invmask == 0) {
			continue;
		}
		if (dp[submask][i] + dp[invmask][i] - node_cost == dp[mask][i]) {
			splitmask = submask;
		}
	}
	if (splitmask != -1) {
		// Split into multiple subtrees
		const submask = splitmask;
		const invmask = mask ^ submask;

		buildPaths(i, submask, visited, edges, data_array, dp);
		buildPaths(i, invmask, visited, edges, data_array, dp);
		return true;
	} else {
		// Find next node on the path
		var nxt = -1;
		for (var ti = 0; ti < edges[i].length; ++ti) {
			const t = edges[i][ti];
			if (visited[mask][t]) {
				continue;
			}
			if (dp[mask][t] + node_cost == dp[mask][i]) {
				const ret = buildPaths(t, mask, visited, edges, data_array, dp);
				if (ret) {
					return true;
				}
			}
		}
		return false; // Can no longer reach anywhere
	}
}

function solve(w, h, data_array) {
	// Let k be the number of cities, and n=w*h Then this is O(3^k n + 2^k n^2)
	var k = 0;
	var city_xs = [];
	var city_ys = [];
	var city_is = [];
	for (var y = 0; y < h; ++y) {
		for (var x = 0; x <= w; ++x) {
			const i = x + y * (w+1);
			if (data_array[i] == 1) {
				++k;
				city_xs.push(x);
				city_ys.push(y);
				city_is.push(i);
			}
		}
	}
	if (k == 1) return data_array; // No changes required

	var edges = buildEdges(w, h);

	const mm = 1 << (k-1);
	const mi = (w+1)*h;
	const inf = 1000000000;

	var dp = [[]]; // dummy unused first dimension
	for (var mask = 1; mask < mm; ++mask) {
		// O(3^k n) part
		var dists = []
		for (var y = 0; y < h; ++y) {
			for (var x = 0; x <= w; ++x) {
				const i = x + y * (w+1);
				var d = inf;
				for (var submask = mask; submask != 0; submask = (submask - 1) & mask) {
					const invmask = mask ^ submask;
					if (invmask == 0) {
						continue;
					}
					d = Math.min(d, dp[submask][i] + dp[invmask][i]);
				}
				if ((data_array[i] == 0) && (d != inf)) {
					d -= 1; // Refund one payment of the node
				}
				dists.push(d);
			}
		}
		
		if ((mask & (mask - 1)) == 0) {
			for (var j = 0; j < k-1; ++j) {
				if (mask & (1 << j)) {
					dists[city_is[j]] = 0;
				}
			}
		}

		// O(2^k n^2) part
		var que = [];
		for (var d = 0; d <= mi; ++d) {
			que.push([]);
		}
		for (var i = 0; i <= mi; ++i) {
			if (dists[i] <= mi) {
				que[dists[i]].push(i);
			}
		}
		for (var d = 0; d <= mi; ++d) {
			for (var j = 0; j < que[d].length; ++j) {
				// Check if we have already handled this
				const i = que[d][j];
				if (dists[i] < d) {
					continue;
				}

				// Update distances
				for (var ti = 0; ti < edges[i].length; ++ti) {
					const t = edges[i][ti];
					const c = d + (data_array[t] == 0 ? 1 : 0);
					if (dists[t] > c) {
						dists[t] = c;
						que[c].push(t);
					}
				}
			}
		}

		// Save the DP and continue
		dp.push(dists);
	}

	// Construct solution from the DP
	var visited = [];
	for (var mask = 0; mask < mm; ++mask) {
		var row = [];
		for (var i = 0; i < mi; ++i) {
			row.push(false);
		}
		visited.push(row);
	}

	const start_ind = city_is[k-1];
	buildPaths(start_ind, mm-1, visited, edges, data_array, dp);

	var best = [];
	for (var i = 0; i < mi; ++i) {
		if (data_array[i] == 0) {
			var check = false;
			for (var mask = 0; mask < mm; ++mask) {
				if (visited[mask][i]) {
					check = true;
				}
			}
			if (check) {
				best.push(2);
			} else {
				best.push(0);
			}
		} else {
			best.push(data_array[i]);
		}
	}
	return best;
}

function optimize() {
	var dts = document.getElementById("hex-grid").dataset;
	const w = parseInt(dts.w);
	const h = parseInt(dts.h);

	var state = getHexgridJsonState();
	var data_array = []

	var city_cou = 0;

	for (var y = 0; y < h; ++y) {
		for (var x = 0; x <= w; ++x) {
			var i = x + y * (w+1);
			if (state[i] === "1") {
				data_array.push(1); // City
				++city_cou;
			} else if (state[i] === "2") {
				data_array.push(2); // Road
			} else {
				data_array.push(0); // Empty
			}
		}
	}
	if (city_cou < 2) return;

	// Find the optimal steiner tree
	var best = solve(w, h, data_array);

	// Change into the best state
	for (var y = 0; y < h; ++y) {
		for (var x = 0; x <= w; ++x) {
			var i = x + y * (w+1);
			if (best[i] != data_array[i]) {
				if (best[i] == 0) {
					setHexState(x, y, i, undefined, state);
				} else if (best[i] == 1) {
					setHexState(x, y, i, "1", state);
				} else if (best[i] == 2) {
					setHexState(x, y, i, "2", state);
				}
			}
		}
	}

	setHexgridJsonState(state);
	enableButton(getSaveButton());
}


function saveChanges() {
	const base_url = window.location.href.split('?')[0];
	const req_url = base_url + "/save";

	console.log(base_url);

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
