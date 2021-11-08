const PAGE_SIZE = 15

var results = []
var ALL_DATA = []

var numPage = 0
var THEME_ID = 0

var MAX_ROWS = 20
var rowsScreen = 0

var subIndex = 150

var SOVA = document.getElementById("sov-container")
var PLSCHECK = document.getElementById("start-container")

var PLATFORMS = ["Vk","Reddit","Youtube"]
var filterPlatforms = ["Vk","Reddit","Youtube"]

var Searched = false


var tt = {}
try{
	
	console.log("SSS")
	if(tt["l"] == undefined){
		tt["l"] = 1
	} 
	console.log(tt["l"])
}catch(e){
	console.log("DD")
}



function return_block(row,num){
		switch(row.type){
			case "Vk":
			return  `<div class="row text-center post align-items-center pl-2 pr-3 m-2 ">
	
						<div class="col-1 my-2">
							<img src="${row.avatar}" alt="" class="post-avatar">
						</div>
						<div class="col-11  post-links">
							<div class="row ">
								<div class="col-6 text-left post-title">
									<p>${row.name}</p>

								</div>
								<div class="col text-right post-title">

									<p>${getTime(row.date)}</p>

								</div>
								<div class="col post-title text-right pr-2">

									<a href = 'https://vk.com/${row.screen_name}'>https://vk.com/${row.screen_name}</a>
								</div>
							</div>
							<div class="row pr-2">
								<div class="col-12 p-0">


									<p class="post-text" id="shortText${num}" style="display: block;"> ${row.content.length > subIndex ? row.content : (row.content.substring(0,subIndex)+"...")}</p>
									


								</div>
							</div>
						</div>
						<div class="col-12 post-text-collapse__opener text-right">

							<a align="right" data-toggle="collapse" href="#fullText${num}" role="button" aria-expanded="false" aria-controls="collapse" aria-controls="post-text-collapse" onclick="openText(1)"   style="line-height: 0px;">Открыть текст</a>




											<div class="collapse text-justify" id="fullText${num}">
												<div class="card card-body">
													<p>${row.content}</p>
												</div>
											</div>
						</div>
					</div>`	
			break

			case "Youtube":
			return `<div class="youtube-cont">
						
					<div class="row text-center post align-items-center  m-2 ">
						<div class="col-9 col-sm-10 col-xl-11 pl-4 pt-2 post-links">
							<div class="row ">
								<div class="col-4 text-left post-title">
									<p>${row.name}</p>

								</div>
								<div class="col post-title pr-2">

									<a href="#">${row.title}</a>
								</div>
							</div>
							<div class="row pr-2">
								<div class="col-12 p-0">


									<p class="post-text" id="shortText${num}" style="display: block;">${row.content}</p>
									


								</div>
							</div>
						</div>
						<div class="col-12 post-text-collapse__opener text-right">

							<a align="right" data-toggle="collapse" href="#fullText${num}" role="button" aria-expanded="false" aria-controls="collapse" aria-controls="post-text-collapse" onclick="openText(1)"   style="line-height: 0px;">Открыть видео</a>




											<div class="collapse text-justify" id="fullText${num}">
												<div class="card card-body">
													<div class="row justify-content-center">
														<div class="col-12 col-sm-10 col-md-8 ">
															<iframe width="100%" class="align-self-center" height="315" src="https://www.youtube.com/embed/${row.from_id}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
														</div>
													</div>
												</div>
											</div>
						</div>
					</div>
				</div>`
			break
		}
		return ""
				
}


function getUsersBy(themeId,button){
	if(!Searched){
	var buttons = document.getElementsByClassName("thema")

	for(var b in buttons){
		try{
		buttons[b].style.color = "black"	
		buttons[b].style.backgroundColor = "#FFFFFF"
	}catch(e){

	}
	}
	button.style.color = "white"
	button.style.backgroundColor = "#F9632D"
	Searched = true
	results = []
		try{
		document.getElementById(`exel${THEME_ID}`).src = ""	
	}
	catch(e){

	}
		THEME_ID = themeId

		PLSCHECK.style.display = "none"
		SOVA.style.display = "block"
		$.ajax({
			url:'/getTheme',
			data:{id: themeId},
			type:"POST",
			async: true,
			success:onGet})
	}
	
}

function onGet(data){
	console.log("RFJNKLSFJAFMAEFKLAFAFMKKFAL")
	var scroll = document.getElementById("posts-container")
	scroll.innerHTML = ""
	ALL_DATA = data.results.sort(sortDate) 
	results = ALL_DATA
	console.log(results[0])
	numPage = PAGE_SIZE
	console.log("Cicle")
			var u = 0 
			while(u < numPage && u < results.length){
				u++
				scroll.innerHTML += return_block(results[u],numPage+u) 
				
			
			
		}	console.log("Cicle")
	getStat()
}

function sortDate(a, b) {
	return b.date - a.date
}

function nextPage(p,container) {

		var element = document.getElementById(container)
	
		var scroll = element.scrollTop;
		var height = element.scrollHeight - element.clientHeight;
		console.log(parseInt(scroll))
		console.log(height)
		var pas = height - parseInt(scroll)
		console.log(pas) 
		if(pas <= 15 && pas >= -1){
		if(p){
			var u = numPage
			while(u < numPage + PAGE_SIZE && u < results.length){
				u++
				element.innerHTML += return_block(results[u],numPage+u)
			
			
			
		}
			console.log(`GET ALL`)
			numPage+= PAGE_SIZE
		} else{
				table = document.getElementById("tableBody")
				for(var r = rowsScreen; r < rowsScreen + MAX_ROWS; r++){
					table.innerHTML += getRow(results[r])
				}
				rowsScreen+= MAX_ROWS
		}
	
	
	
	}
}

function getTime(UnixTime){
  var a = new Date(UnixTime * 1000);
  var months = ['Января','февраля','Марта','Апреля','Мая','Июня','Июля','Августа','Сгорающевого месяца','Октября','Ноября','Декабря'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
  return time;
}

function getGrafTime(UnixTime) {
  var a = new Date(UnixTime * 1000);
  var month = a.getMonth() + 1;
  var date = a.getDate();
  var time = date + ':' + month;
  return time;
}

async function getStat() {
	var dates = {}
	var dateOne = new Date(parseInt(results[0].date) *1000)
	print("Дата отсчета",dateOne.getFullYear())
	print("Лишнее время",(dateOne.getHours() * 3600 + dateOne.getMinutes() * 60 + dateOne.getSeconds()))
	dateOne = parseInt(results[0].date) - (dateOne.getHours() * 3600 + dateOne.getMinutes() * 60 + dateOne.getSeconds())
	print("Дата отсчета",dateOne)
	dates[dateOne] = {}
	for(var i in results){
		if(parseInt(results[i].date) < dateOne){
			dateOne -= 86400
			dates[dateOne] = {}
			print("type",results[i].type)
		}
		if(dates[dateOne][results[i].type] == undefined){
			dates[dateOne][results[i].type] = 1
		}else{
			dates[dateOne][results[i].type] += 1
		}
	}
	console.log(dates)
	$.ajax({
		url:'/setStaticstic',
		data: JSON.stringify({id:THEME_ID, nums: dates}),
		contentType: 'application/json',
		type:"POST",
		async: true,
		success:onStat})
}

function onStat(data) {
		  datasets = []
		  labels = []
		  for(l in data.lables){
		  	labels.push(data.lables[l])
		  }
		  var keys = Object.keys(data.stat)
		  for(d in keys){
		  		  	datasets.push({
		              label: data.stat[keys[d]]['Title'],
		                  fill:false,
		                  lineTension:0.1,
		                  backgroundColor:data.stat[keys[d]]['Color'],
		                  borderColor:data.stat[keys[d]]['Color'],
		                  borderCapStyle:'butt', 
		                  borderDash:[],
		                  borderDashOffset:0.0,
		                  borderJoinStyle:'miter',
		                  pointBorderColor:data.stat[keys[d]]['Color'],
		                  pointBackgroundColor:data.stat[keys[d]]['Color'],
		                  pointBorderWidth:10,
		                  pointHoverRadius:5,
		                  pointHoverBackgroundColor: data.stat[keys[d]]['Color'],
		                  pointHoverBorderColor:data.stat[keys[d]]['Color'],
		                  pointHoverBorderWidth:8,
		                  pointRadius:1,
		                  pointHitRadius:10,
		                  data: data.stat[keys[d]]["Nums"],
		          })}

	var chart = new Chart(ctx2, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset

    data: {
        labels:labels ,
        datasets: datasets
    },

    // Configuration options go here
    options: {scales: {
            xAxes: [{
                stacked: true
            }],
            yAxes: [{
                stacked: false
            }]

        }}
});

new Chart(document.getElementById("myDoughnutChart"), {
    type: 'doughnut',
    data: {
      labels: data.diaL,
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: data.diaC,
          hoverBorderWidth:10,
          borderColor:"white",

          data: data.diaN
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Пример заголовка',
        fontSize:16,
      }
    }
});
	table = document.getElementById("authors")
	table.innerHTML= `<thead> 
								<tr class="text-center align-items-center">
									<th class="align-middle" scope="col">Фото</th>
									<th class="align-middle" scope="col">Имя</th>
									<th class="align-middle" scope="col">Платформа</th>
									<th class="align-middle" scope="col">Дата</th>
									<th class="align-middle text-left" scope="col">Ссылка</th>
								</tr>
							</thead>
							<tbody id = "tableBody">
							</tbody>
`
	var body = document.getElementById("tableBody")
	for(var r = 0; r < MAX_ROWS; r++){
		body.innerHTML += getRow(results[r])
	}
	rowsScreen += MAX_ROWS
	document.getElementById(`exel${THEME_ID}`).src = "../static/images/exel-icon.png"	
	SOVA.style.display = "none"
	Searched = false


		   
}



function getRow(row) {
	var result = ""
	switch(row.type){
		case "Vk":
			result = `<tr>
							<td class="align-middle"><img src="${row.avatar}" alt="" class="post-avatar"></img></td>
							<td class="align-middle">${row.name}</td>
							<td class="align-middle">${row.type}</td>
							<td class="align-middle">${getTime(row.date)}</td>
							<td class="align-middle" style="word-break: break-all;">
										<a href="#">
											https://vk.com/${row["screen_name"]}
										</a>
									</td>
							  </tr>`

	}
	return result
}

function print(comment,value) {
	console.log(`__${comment}__`)
	console.log(`\t${value}`)
	console.log("______________")
}

function downloadTable(id) {
		$.ajax({
		url:`/download/${id}`,
		type:"POST",
		async: true})
}

function filter(){
	var timePlatforms = []
	for(var p in PLATFORMS){
		if(document.getElementById(PLATFORMS[p]).checked){
			timePlatforms.push(PLATFORMS[p])
		}
	}
	filterPlatforms = timePlatforms
	results = ALL_DATA.filter(item => filterPlatforms.indexOf(item["type"]) != -1)
	print("ASDSAD",timePlatforms)
	againGenearte()
}

function againGenearte(){
	var scroll = document.getElementById("posts-container")
	scroll.innerHTML = ""
	console.log(results[0])
	numPage = PAGE_SIZE
	console.log("Cicle")
			var u = 0 
			while(u < numPage && u < results.length){
				u++
				scroll.innerHTML += return_block(results[u],numPage+u) 
				
			
			
		}	
}

