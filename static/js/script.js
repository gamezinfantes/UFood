$(function () {
	
	$('.left-button').click(function(event) {
		$('header nav').toggleClass('menu-open');
	});	
	console.log("jquery");
	//Formulario de la busqueda del home
	$('#form-seaarch-restaurant').submit(function(event) {
		event.preventDefault();
		var codigo_postal = $('#where').val();
		window.location.href = "/restaurantes/"+codigo_postal+"/";
	});
		/* Act on the event */
	//Boton de añadir a la cesta de la carta del restaurante
	$('.add').click(function(event) {
		var plato = $(this).data('plato');
		
		//var nombrePlato = 
		//var precioPlato

		//lo ponemos en la cesta de la pagina

		

		//lo enviamos para que quede en la sesion del servidor
		/*$.ajax({
			url: '/path/to/file',
			type: 'POST',
			dataType: 'json',
			data: {param1: 'value1'},
		})
		.done(function() {
			console.log("success");
		})
		.fail(function() {
			alert('El plato no se pudo añadir');
			//lo eliminamos de la vista en la cesta


			
		})
		.always(function() {
			console.log("complete");
		});
		*/

	});

});