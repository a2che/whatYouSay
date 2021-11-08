var realState = 0
var clases = ['posts-container','authors-container','lineChart-container','doughnutChart-container']

function changeScreen(id, button) {
	document.getElementById(clases[realState]).style.display = "none"
	realState = id
	document.getElementById(clases[realState]).style.display = "block"

	var buttonColor = document.getElementsByClassName('tabbar-button')
	for(var c = 0; c < buttonColor.length; c++){
		buttonColor[c].style.backgroundColor ='#E7E7E7'
	}
	button.style.backgroundColor ='#D0D0D0'
}
