$(window).on("load",function(){
	getNote();
})
//En funksjon spør om å oppdaterer notaet i databasen. 
function update() {
	//Den henter det som er blitt skrevet inn
	title = $("#title").val();
	content = $("#content").val();
	id = window.location.href.split("#")[1];
//Sender det som ble hentet over og oppdaerer'
//api=application programing interface= for å kommunisere med serveren
	$.ajax({
		//"type" sier hva det spør om. For eksempel "GET" sier at den skal hente en side. 
		type: "PATCH",
		//hvordan urlen skal være
		url: "/api/notes/UpdateNote/" +id,
		//Det som skal oppdateres
		data: {
			title: title,
			content: content
		},
		success: function(data){
			console.log(data.status);
		}
	})
}
//Lager en ny fil til databasen
function create() {
	$.ajax({
		type: "POST",
		url: "/api/notes/CreateNote",
		success: function(response){
			console.log(response)
			window.location = "#"+response.id;
			getNote()
		}	
	})
}
function getNote() {
	var id = window.location.href.split("#")[1];
	$.ajax({
		type: "GET",
		url: "/api/notes/GetNote/"+ id,
		success: function(json){
			const res = JSON.parse(json)
			const note = res.data
			console.log(res);
			if (!note) {
				return
			}
			$("#title").val(note.title);
			$("#content").val(note.content);
		}
	})
}