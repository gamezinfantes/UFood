$(function () {
	
	//window.scrollTo(0,1);

	/**************************************
	* Eventos botones del menu
	***************************************/
	$('.left-button').click(function(event) {
		$('header nav').toggleClass('menu-open');
	});
	$('#shoping-cart-btn a').click(function(event) {
		event.preventDefault();
		$('#shoping-cart-list').toggleClass('menu-open');
	});	


	/**************************************
	*Validacion del codigo postal
	***************************************/
	$('input#where').keydown(function (e) {  
	    // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) || 
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
	});
	//Formulario de la busqueda del home
	$('#form-seaarch-restaurant').submit(function(event) {
		event.preventDefault();
		var codigo_postal = $('#where').val();
		window.location.href = "/restaurantes/"+codigo_postal+"/";
	});


	/***********************************************
	    En esta función se hace la solicitud de geolocalización y el primer
	    control para ver si el navegador soporta el servicio
	***********************************************/
	 
	$('#geolocation').click(geoposicionar);


	function geoposicionar(){
	    if(navigator.geolocation){
	        //mostrarMensaje("obteniendo posición...");
	        navigator.geolocation.getCurrentPosition(centrarMapa,errorPosicionar);
	    }else{
	        mostrarMensaje('Tu navegador no soporta geolocalización');
	    }   
	}
	 

	function errorPosicionar(error) {
	    switch(error.code)  
	    {  
	        case error.TIMEOUT:  
	            mostrarMensaje('Request timeout');  
	        break;  
	        case error.POSITION_UNAVAILABLE:  
	            mostrarMensaje('Tu posición no está disponible');  
	        break;  
	        case error.PERMISSION_DENIED:  
	            mostrarMensaje('Tu navegador ha bloqueado la solicitud de geolocalización');  
	        break;  
	        case error.UNKNOWN_ERROR:  
	            mostrarMensaje('Error desconocido');  
	        break;  
	    }  
	}
	 
	/***********************************************
	    Esta función se ejecuta si la llamada a  navigator.geolocation.getCurrentPosition
	    tiene éxito. La latitud y la longitud vienen dentro del objeto coords. 
	***********************************************/
	function centrarMapa(pos, z){
		var codigoPostal;
		//pos.coords.latitude, pos.coords.longitude
		$.get('https://maps.googleapis.com/maps/api/geocode/json?latlng='+pos.coords.latitude+','+pos.coords.longitude+'&sensor=true', function(data) {	
	    	codigoPostal = data.results[0].address_components[6].long_name;
			$('#where').val(codigoPostal);
		});
	}
	 
	//Gestión de mensajes
	function mostrarMensaje(str){
	   alert(str);
	}
	 
	/*********************************************************
	* Boton de añadir a la cesta de la carta del restaurante
	*********************************************************/
	$('.add').click(function(event) {
		var plato = $(this).data('plato');
		
		//var nombrePlato = 
		//var precioPlato =

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
			//lo eliminamos de la vista en la cesta y comunnicamos el error
			
		})
		.always(function() {
			console.log("complete");
		});
		*/

	});

	var ShopingCart = function () {
		
	};
	ShopingCart.prototype.save = function(url, jsonOb) {
		$.get('/shoping-cart/'+url+"/", jsonOb);
	};

	ShopingCart.prototype.add = function(productId, cantidad) {
		this.save("add", {"product_id": productId, "quantity": cantidad});
	};
	ShopingCart.prototype.remove = function (productId) {
		this.save("remove", {"product_id": productId});
	};
	ShopingCart.prototype.remove_single = function (productId) {
		this.save("remove-single", {"product_id": productId});
	}
	ShopingCart.prototype.clear = function () {
		this.save("clear",{});
	};
	ShopingCart.prototype.set_quantity = function (productId, cantidad) {
		this.save("set-quantity", {"product_id": productId, "quantity": cantidad});
	};

});