var num = 0
var NAME = ""

function addPlate(event){
	console.log(event)
	if(event.keyCode == 13){
	num++
	var values = []
	inputs = document.getElementsByClassName("themeWord")
	for(var f =0 ; f<inputs.length ; f++){
		values.push(inputs[f].value)
	}
	console.log(values)
	document.getElementById("themes").innerHTML += `<input type="text" class="form-control newThemes themeWord" onfocus onkeypress="addPlate(event)">`
	for(var f =0 ; f <inputs.length - 1; f++){
		inputs[f].value = values[f]
	}
	inputs[inputs.length - 1].focus()
	}
}

function sendTheme() {
	data = {"ThemeName":String(document.getElementById("themeName").value),"Words":getData()}
	NAME = document.getElementById("themeName").value
	$.ajax({
		url:'/addTheme',
		data:JSON.stringify(data),
		type:"POST",
		contentType: "application/json",
		complete:onSend})
	document.getElementById("themeName").value = ""
	document.getElementById("themes").innerHTML = `<label for="theme_1">Ключевые слово</label>
					      				<input type="text" class="form-control newThemes themeWord" onfocus onkeypress="addPlate(event)">`
	num = 0
}
function onSend(data){
	var themes = document.getElementById("themesList")
	themes.innerHTML= ``
	themesArr = JSON.parse(data.responseText).themes
	for(var d in themesArr){
	themes.innerHTML+= `<div class="btn-group" role="group" aria-label="Basic example">
									<div onclick="getUsersBy('${themesArr[d][1]}');" class="nav-link thema d-flex mb-2 p-0 w-75" data-toggle="pill" href="#" aria-selected="true">
				    					<p class="align-self-center ml-4 my-2">${themesArr[d][0]}</p>
				    				</div>
						  			<div  class="d-flex nav-link exel-icon p-0  mb-2  w-25  align-items-center" >
						  				<a href="/download/${themesArr[d][1]}">
										<img id="exel${themesArr[d][1]}" class="w-100 
								" src="" alt="">
									</a>
									</div>
								</div>
`	
	}
	
}

function getData(){
	var words = []

	var inputs = document.getElementsByClassName("themeWord")
	for(var i = 0; i < inputs.length; i++){
	words.push(`${inputs[i].value}`)			
	}

	return words
}

function logOut() {
	$.ajax({
		url:'/logOut',
		type:"POST"})
}