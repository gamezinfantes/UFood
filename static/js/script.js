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
	

	/**
	 *  Click del boton de paypal
	 */

	 $('form#detaill .paypal-btn').click(function(event) {
	 	$('form#detaill').append('<input type="hidden" name="pago" value="Paypal" /> '); 
	 	$('form#detaill').submit();
	 	
	 });

	/**************************************
	* Validacion del codigo postal
	***************************************/
	$('input#where').keydown(function (e) {  
	    // Permite el retoriceso, la tecla del, tablulacion y enter
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) || 
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Se asegura de que es un numero y corta el evento
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
	});


	//Formulario de la busqueda del home
	$('#form-seaarch-restaurant').submit(function(event) {
		event.preventDefault();
		var codigo_postal = $('#where').val();
		if (codigo_postal>53000 || codigo_postal<1000) {
			alert("Codigo postal erroneo");
			return false;
		}
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
	



	var ShopingCart = function () {
		this.cantidadBarra = $('#shoping-cart-btn #total-items');
		this.platos = $('#shoping-cart-btn #platos');
		this.articulos = this.cantidadBarra.text();
	};
	ShopingCart.prototype.save = function(url, jsonOb) {
		this.cantidadBarra.text(this.articulos);
		var plural = this.cantidadBarra.text() != 1 ? "platos" : "plato";
		this.platos.text(plural);
		$.get('/shoping-cart/'+url+"/?"+$.param(jsonOb), function(data){
			//cantidad en la barra menu
			//Datos del carrito
			$('#shoping-cart-list').html(data);
		});
	};

	ShopingCart.prototype.add = function(productId, cantidad) {
		this.articulos += cantidad;
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
		this.articulos--;
		this.save("remove-single", {"product_id": productId});
	}
	ShopingCart.prototype.clear = function () {
		this.articulos = 0;
		this.save("clear",{});
	};
	ShopingCart.prototype.set_quantity = function (productId, cantidad) {
		this.save("set-quantity", {"product_id": productId, "quantity": cantidad});
	};

	var carrito = new ShopingCart();


	$('.add').click(function(event) {
		event.stopPropagation();
		var platoId = $(this).data('plato');
		//var precio = $('span.add').parent().children('.price');
		carrito.add_single(platoId);

	});
	
	
	$('#shoping-cart-list').on('click', '.remove', function(){
		event.stopPropagation();
		var platoId = $(this).data('plato');
		carrito.remove_single(platoId);
	});
	
	
	
	var ToggleMenuDescription = function () {
		$('.desc', this).toggleClass('visible');
	};

	var mostarCarrito = function(event) {
		event.preventDefault();
		$('#shoping-cart').toggleClass('visible');
		$('#modal').toggleClass('visible');
	};


	function mobile() {
		// Mostrar descripcion del plato cuando hay click
		$('#menu').on('click', 'li', ToggleMenuDescription);

		//evento que despliega el carrito
		$('#shoping-cart-btn a').click(mostarCarrito);
	
	
	}
	function mobileExit() {
		$('#menu').off('click', 'li', ToggleMenuDescription);

		var modal = $('#modal');
		if(modal.hasClass('visible')) {
			$('#shoping-cart-btn a').click();
		}
		$('#shoping-cart-btn a').off('click', mostarCarrito);
	}
	function desktop () {
		if ($("section#menu").length > 0){
			var spConOffTop = $('#shoping-cart-content').offset().top;
			var $spCon = $('#shoping-cart-content');
			$(window).scroll( function(event) {
				console.log('erer');
				var winH = $(window).scrollTop();
				if (winH >spConOffTop) {
					$spCon.css({
						position: 'fixed',
						top: '1em',
						right: $(window).width() - $spCon.offset().left - $spCon.outerWidth()
					});
				}else {
					$spCon.css({
						position: 'absolute',
						right: 0,
						top: 6
					});
				}
			});

			$(window).resize(function(event) {
				if ($spCon.css('position') == 'fixed') {
					$spCon.css({
						right: $(window).width() - ($('.content').offset().left + $('.content').width())
					});
				}
			});
		}


		var PreetySlide = function () {
			var self = this;
			this.posicion = 1;

			var $image = $('#images_slider img');

			this.avanza = function () {
				var posCambio = this.posicion;
				if (this.posicion == 3) {
					posCambio = 1;
				} else {
					posCambio++;
				}
				self.cambiarImagen(posCambio);
				if (this.posicion == 3) {
					this.posicion = 1;
				} else {
					this.posicion++;
				}
				//console.log(this.posicion);
			};
			this.cambiarImagen = function (posCambio){
				var newSrc = $image.attr("src").replace("slide"+this.posicion+".jpg", "slide"+posCambio+".jpg");
				$image.attr("src", newSrc);
			};


			$('.controls #1').click(function(event) {
			 	self.cambiarImagen(1);
			 	self.posicion = 1;
			});

			$('.controls #2').click(function(event) {
			 	self.cambiarImagen(2);
			 	self.posicion = 2;
			});
			$('.controls #3').click(function(event) {
			 	self.cambiarImagen(3);
			 	self.posicion = 3;
			});
			
			setInterval(function () {
				self.avanza();
			} , 10000);
		};
		if ($("#images_slider").length > 0){
			new PreetySlide();
		}	

	}
	function desktopExit() {
		$(window).off('resize');
		$(window).off('scroll');
	}


	var _breakpoints = {
		"breakpoints": [20,1000]
	};
	$(window).setBreakpoints(_breakpoints);
	$(window).on('enterBreakpoint20', mobile);
	$(window).on('exitBreakpoint20', mobileExit);
	$(window).on('enterBreakpoint1000', desktop);
	$(window).on('exitBreakpoint1000', desktopExit);

});