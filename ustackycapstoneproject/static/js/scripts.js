async function getStates(url){
	let objects = await fetch(url);
	let states = await objects.json()
	return states;
}


window.onload = function(){
	var stateOfOrigin = document.getElementById("state");
	getStates("/static/states-localgovts.json").then(states => {
		states.forEach(state => {
			var optionStateOfOrigin = document.createElement("option");
		optionStateOfOrigin.setAttribute("value", state["state"]);
		optionStateOfOrigin.appendChild(document.createTextNode(state["state"]));
		stateOfOrigin.appendChild(optionStateOfOrigin);
		});
	}).catch(err => console.error(err));	
}
function getLG(){
	getStates("/static/states-localgovts.json").then(states => {
		var localGOfOrigin = document.getElementById('lg');
		localGOfOrigin.textContent = "";
		var optionLGOfOrigin = document.createElement("option");
		optionLGOfOrigin.setAttribute("value", "none");
		optionLGOfOrigin.appendChild(document.createTextNode("Select-Local-Government"));
		localGOfOrigin.appendChild(optionLGOfOrigin);

		console.log(localGOfOrigin.innerHTML);
		var stateOfOrigin = document.getElementById('state').value;
		states.forEach(state => {
			if(state['state'] === stateOfOrigin) {
				state['local'].forEach(lg => {
					var LGoption = document.createElement('option');
					LGoption.setAttribute('value', lg);
					LGoption.appendChild(document.createTextNode(lg));
					localGOfOrigin.appendChild(LGoption);
				});
			}
		});
	}).catch(err => console.error(err));
	
}