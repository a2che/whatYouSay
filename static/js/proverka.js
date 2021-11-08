var run = true
function registration() {
	run = true
	if(document.getElementById("passwordForm").value.length <= 6 ){
		run = false
		document.getElementById("passwordFormLabel").style.display = "block"
	} else{
		document.getElementById("passwordFormLabel").style.display = "none"
	}
	if(document.getElementById("mailForm").value.indexOf('@') == -1){
		run = false
		document.getElementById("mailFormLabel").innerHTML = 'Не соотвествует формату'

	}else{
		$.ajax({
			url:'/checkMail',
			data:{mail: document.getElementById("mailForm").value},
			type:"POST",
			success:onGet})
	}
	if(document.getElementById("loginForm").value == ""){
		document.getElementById("loginFormLabel").style.display = "block"
		run = false
	}else{
		document.getElementById("loginFormLabel").style.display = "none"
	}

	if(run){
		document.getElementById("REGFORM").submit()
	}
}



function onGet(data) {
	if(data == "no"){
		document.getElementById("mailFormLabel").innerHTML = "Почта уже зарегестрированна"
		run = false
	}else{
		document.getElementById("mailFormLabel").innerHTML = ""
	}
}

function recoveryPassword(){
			$.ajax({
			url:'/recoveryPassword',
			data:{mail: document.getElementById("recoveryPasswordMail").value},
			type:"POST",
			success:onRecovery})
}

function onRecovery(data) {
	if(data == "ok"){
		document.getElementById("mailRec").style.display = "none"
		document.getElementById("forgPassForm").style.display = "none"
		document.getElementById("forgPassFormMessage").style.display = "block"

	}else{
		document.getElementById("mailRec").style.display = "block"
	}
}