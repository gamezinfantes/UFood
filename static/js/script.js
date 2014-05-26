$(function () {

	var Menu = function () {};
	Menu.cerrar = function() {
		$('header nav').removeClass('menu-open');
		$("html").unbind("click");
	};
	Menu.abrir = function () {
		$('header nav').addClass('menu-open');		
		$('html').bind('click', function(event) {
			$('header nav').removeClass('menu-open');		
		});
	};

	/**************************************
	* Eventos botones del menu
	***************************************/
	$('.left-button').click(function(event) {
		event.stopPropagation()
		if ($('header nav').hasClass('menu-open')) {
			Menu.cerrar();
		} else {
			Menu.abrir();	
		}
	});
	//evento que despliega el carrito
	$('#shoping-cart-btn a').click(function(event) {
		event.preventDefault();
		$('#shoping-cart').toggleClass('visible');
	});
	


	/**************************************
	* Validacion del codigo postal
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
		var tipoComida = $('#what').val();
		var url = "/restaurantes/"+codigo_postal+"/";
		if (tipoComida != 0) {
			url += tipoComida+"/";
		}

		window.location.href = url;


	});


	/***********************************************
	    En esta función se hace la solicitud de geolocalización y el primer
	    control para ver si el navegador soporta el servicio
	***********************************************/
	 
	$('#geolocation').click(geoposicionar);

	window.geo= geoposicionar;
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
	
	var carrito = new ShopingCart();
	$('.add').click(function() {
		var plato = $(this).data('plato');
		//var precio = $('span.add').parent().children('.price');

		carrito.add_single(plato);

		//var nombrePlato = 
		//var precioPlato =

		//lo ponemos en la cesta de la pagina
	});



	var ShopingCart = function () {
		this.articulos = 0;
		var cantidadBarra;
	};
	ShopingCart.prototype.save = function(url, jsonOb) {
		$.get('/shoping-cart/'+url+"/?"+$.param(jsonOb), function(data){
			//cantidad en la barra menu
			cantidadBarra.html(this.articulos);
			//Datos del carrito
			$('#shoping-cart-list').html(data);
		});
	};

	ShopingCart.prototype.add = function(productId, cantidad) {
		this.save("add", {"product_id": productId, "quantity": cantidad});
	};
	ShopingCart.prototype.add_single = function(productId) {
		this.articulos++;
		this.save("add-single", {"product_id": productId});
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




	$('#shoping-cart-list').on('click', 'li', function(){
		console.log('hemos hecho click')
	});

});
