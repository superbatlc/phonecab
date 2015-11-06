/* ==========================================================
 * PhoneCab
 * Funzione recupero tabella Whitelist
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function reload_whitelists(phoneuser_id){
	$.ajax({
        type: 'POST',
        url: '/whitelist/ajax_list/'+phoneuser_id,
        async: true,
        cache: false,
        success: function(data) {
            $("#whitelist").html(data)
        },
        error: function(jqXHR, textStatus, errorThrown){
        	msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
            msg += '<h4>Attenzione</h4>Errore nella trasmissione dei dati Whitelist.<br>';
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
            $('.message').append(msg);
        }
    })
}


/* ==========================================================
 * PhoneCab
 * Funzione recupero tabella Credito
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function reload_credits(phoneuser_id){
	$.ajax({
        type: 'POST',
        url: '/credit/ajax_list/'+phoneuser_id,
        async: true,
        cache: false,
        success: function(data) {
            $("#ricariche").html(data)
        },
        error: function(jqXHR, textStatus, errorThrown){
        	msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
            msg += '<h4>Attenzione</h4>Errore recupero lista crediti.<br>';
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
            $('.message').append(msg);
        }
    })
}


/* ==========================================================
 * PhoneCab
 * Funzione Mostra finestra Nuova Whitelist
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.show-whitelist-modal').on('click',function(e){
    e.preventDefault()
    
    
    var phoneuser_id = $('#phoneuser-id').val()
    
    if (phoneuser_id == '' || phoneuser_id == 'None'){
		// siamo nella schermata di ricerca per cui 
    	// il phoneuser dipende dal pulsante che abbiamo premuto
    	phoneuser_id = $(this).attr('action-phoneuser-id')
	} 
    
    var whitelist_id = $(this).attr('data-id')
	var label = 'Crea Numero Autorizzato'
	var ajax_url = '/whitelist/edit/'
	
	if (whitelist_id != '' && whitelist_id != 'None'){
		label = 'Modifica Numero Autorizzato'
		ajax_url += whitelist_id
	}
                             
    $('.modal-body').html('<div style="text-align:center;"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
    // imposto il titolo
    $('#myModalLabel').html(label)
    $('#modal-action').html('Salva').removeClass().addClass('btn btn-primary save-whitelist')

    $.ajax({
       type: 'POST',
       url: ajax_url,
       async: true,
       data: {phoneuser_id: phoneuser_id},
       success: function(e){ 
            $('.modal-body').html(e)
       },
       error: function(jqXHR, textStatus, errorThrown){
    	   msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
           msg += '<h4>Attenzione</h4>Errore apertura finestra Whitelist.<br>';
           msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
           $('.message').append(msg);
       }
    })
    
})


/* ==========================================================
 * PhoneCab
 * Abilitazione / Disabilitazione Campi in funzione
 * della frequenza
 * ==========================================================
 * Copyright 2013 SuperbatTLC
 * ========================================================== */
$('#whitelist-frequency').on('change',function(e){
	var value = $(this).val();
	
	if(value == '0' || value == '1'){
		$('#whitelist-real-mobile-div').hide();
	}else{
		$('#whitelist-real-mobile-div').show();
	}
	
})


/* ==========================================================
 * PhoneCab
 * Funzione Salva Whitelist
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$(".save-whitelist").on('click', function(e){
    e.preventDefault()
                                    
    var ok = check_whitelist_form()
    if(!ok) return
                                    
    var whitelist = new Object()
    
    var phoneuser_id = $("#whitelist-phoneuser-id").val()
    var whitelist_id = $("#whitelist-id").val()
    
    whitelist.phoneuser_id = phoneuser_id
    
    if (whitelist_id == "None" || whitelist_id == ''){
        whitelist.whitelist_id = 0
        whitelist_success_msg = 'inserito'
        whitelist_error_msg = 'inserimento'
    }else{
    	whitelist.whitelist_id = whitelist_id
        whitelist_success_msg = 'aggiornato'
        whitelist_error_msg = 'aggiornamento'
    }
    
    whitelist.label = $("#whitelist-label").val()
    whitelist.phonenumber = $("#whitelist-phonenumber").val()
    whitelist.duration = $("#whitelist-duration").val()
	whitelist.frequency = $("#whitelist-frequency").val()
	
	whitelist.real_mobile = 0
	if($("input[type=checkbox]#whitelist-real-mobile").is(':checked')){
        whitelist.real_mobile = 1
    }
    
    $.ajax({
       type: 'POST',
       url: '/whitelist/save/',
       async: true,
       data: {data: whitelist},
       success: function(e){ 
            if(e=="1"){
                msg = '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Ok!</h4>Numero Autorizzato '+whitelist_success_msg+' con successo.</div>'
                // ricarichiamo la tabelle delle whitelist
                reload_whitelists($("#phoneuser-id").val())
            }else{
                msg = '<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Attenzione!</h4>Errore '+whitelist_error_msg+' Numero Autorizzato.</div>'
            }
                            
            $('#myModal').modal('hide');
            $('.message').append(msg);
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">√ó</button>'
            msg += '<h4>Attenzione</h4>Errore nella trasmissione dei dati Numero Autorizzato.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })
    
    return false
 })
 
 /* ==========================================================
 * PhoneCab
 * Funzione Elimina Whitelist
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.remove-whitelist').on('click',function(e){
    e.preventDefault()
    
    var button = confirm("Sei sicuro di voler eliminare il Numero Autorizzato?")
    
    if(button){
    	var whitelist_id = $(this).attr('data-id');
    	var msg = '';
    	$.ajax({
    		type: 'POST',
    		url: '/whitelist/remove/',
    		async: true,
    		data: {whitelist_id: whitelist_id},
    		success: function(e){ 
	            if(e=="1"){
	                msg = '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">x</button>'
	                msg += '<h4>Ok!</h4>Numero Autorizzato eliminato con successo.</div>'
	                // ricarichiamo la tabelle delle whitelist
	                reload_whitelists($("#phoneuser-id").val())
	            }else{
	                msg = '<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">x</button>'
	                msg += '<h4>Attenzione!</h4>Errore eliminazione Numero Autorizzato.</div>'
	            }
	                            
	            $('#myModal').modal('hide')
	            $('.message').append(msg)       
    		},
    		error: function(jqXHR, textStatus, errorThrown){
	            $('#myModal').modal('hide')
	            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
	            msg += '<h4>Attenzione</h4>Errore nella trasmissione dei dati Numero Autorizzato.<br>'
	            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
	            $('.message').append(msg)
    		}
    	})
    }else{
    	return
    } 
})


/* ==========================================================
 * PhoneCab
 * Abilitazione / Disabilitazione Whitelist
 * ==========================================================
 * Copyright 2013 SuperbatTLC
 * ========================================================== */
$('.enable-whitelist').on('click',function(e){
	
	var button = $(this);
	var icon = $("i", this);
	
	var whitelist_id = button.attr("data-id");
	var value = button.hasClass("btn-success");
	
	$.ajax({
	       type: 'POST',
	       url: '/whitelist/changestatus/',
	       async: true,
	       data: {whitelist_id: whitelist_id, value: value},
	       success: function(e){
	    	   if(e == '1'){
	    		   if(value){
		    		   button.removeClass("btn-success").addClass("btn-danger");
	    			   icon.removeClass("icon-ok").addClass("icon-remove");
	    			   
		    	   }else{
		    		   button.removeClass("btn-danger").addClass("btn-success")
		    		   icon.removeClass("icon-remove").addClass("icon-ok");
		    	   }
	    	   }
	    	   
	       },
	       error: function(jqXHR, textStatus, errorThrown){
	    	   msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
	            msg += '<h4>Attenzione</h4>Errore abilitazione/disabilitazione Whitelist.<br>';
	            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
	            $('.message').append(msg);
	       }
	    })
})

/* ==========================================================
 * PhoneCab
 * Ordinaria / Straordinaria Whitelist
 * ==========================================================
 * Copyright 2013 SuperbatTLC
 * ========================================================== */
$('.extra-whitelist').on('click',function(e){
	
	var button = $(this);
	var icon = $("i", this);
	
	var whitelist_id = button.attr("data-id");
	var value = button.hasClass("btn-success");
	
	// quando abilitiamo la whitelist diamo all'utente
	// un feedback su quante volte nel periodo precedente
	// (settimana/mese) siano state effettuate chiamate
	if(!value){
		
		$.ajax({
		       type: 'POST',
		       url: '/whitelist/checkextra/',
		       async: true,
		       data: {whitelist_id: whitelist_id} ,
		       dataType: 'json',
		       success: function(response){
		    	     var msg = "Chiamate straordinarie gi\xE0 effettuate:\n";
		    	     msg += '- nella settimana: '+ response.data.weekcalls+'\n';
		    	     msg += '- nel mese: '+ response.data.monthcalls+'\n';
		    	     msg += 'Confermare l\'autorizzazione strordinaria?';
		    	     
		    	     ok = confirm(msg)
		    	     
		    	     if(ok){
		    	    	 $.ajax({
		    			       type: 'POST',
		    			       url: '/whitelist/changeordinary/',
		    			       async: true,
		    			       data: {whitelist_id: whitelist_id, value: value},
		    			       success: function(e){
		    			    	   if(e == '1'){
		    			    		   if(value){
		    				    		   button.removeClass("btn-success").addClass("btn-danger");
		    			    			   icon.removeClass("icon-ok").addClass("icon-remove");
		    			    			   
		    				    	   }else{
		    				    		   button.removeClass("btn-danger").addClass("btn-success")
		    				    		   icon.removeClass("icon-remove").addClass("icon-ok");
		    				    	   }
		    			    	   }
		    			    	   
		    			       },
		    			       error: function(jqXHR, textStatus, errorThrown){
		    			    	   msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
		    			            msg += '<h4>Attenzione</h4>Errore abilitazione straordinaria Whitelist.<br>';
		    			            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
		    			            $('.message').append(msg);
		    			       }
		    			    })
		    	     }
		       },
		       error: function(jqXHR, textStatus, errorThrown){
		    	   msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
		            msg += '<h4>Attenzione</h4>Errore recupero statistiche Whitelist.<br>';
		            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
		            $('.message').append(msg);
		       }
		    })
	}else{
	
		$.ajax({
		       type: 'POST',
		       url: '/whitelist/changeordinary/',
		       async: true,
		       data: {whitelist_id: whitelist_id, value: value},
		       success: function(e){
		    	   if(e == '1'){
		    		   if(value){
			    		   button.removeClass("btn-success").addClass("btn-danger");
		    			   icon.removeClass("icon-ok").addClass("icon-remove");
		    			   
			    	   }else{
			    		   button.removeClass("btn-danger").addClass("btn-success")
			    		   icon.removeClass("icon-remove").addClass("icon-ok");
			    	   }
		    	   }
		    	   
		       },
		       error: function(jqXHR, textStatus, errorThrown){
		    	   msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
		            msg += '<h4>Attenzione</h4>Errore disabilitazione straordinaria Whitelist.<br>';
		            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
		            $('.message').append(msg);
		       }
		    })
	}
})



/* ==========================================================
 * PhoneCab
 * Funzione Mostra finestra Nuova Ricarica
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.new-credit').on('click',function(e){
    e.preventDefault()
    phoneuser_id = $('#phoneuser-id').val() //$(this).attr('data-id')                           
    $('.modal-body').html('<div style="text-align:center;"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
    // imposto il titolo
    $('#myModalLabel').html('Crea Nuova Ricarica')
    $('#modal-action').html('Salva').removeClass().addClass('btn btn-primary save-credit')

    $.ajax({
       type: 'POST',
       url: '/credit/new/',
       async: true,
       data: {phoneuser_id: phoneuser_id},
       success: function(e){ 
            $('.modal-body').html(e)
       },
       error: function(jqXHR, textStatus, errorThrown){
    	   msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
           msg += '<h4>Attenzione</h4>Errore apertura finestra Credit.<br>';
           msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
           $('.message').append(msg);
       }
    })
    
})


/* ==========================================================
 * PhoneCab
 * Funzione Salva Ricarica
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$(".save-credit").on('click', function(e){
    e.preventDefault()
                                    
    ok = check_credit_form()
    if(!ok) return
                                    
    var credit = new Object()

    credit.phoneuser_id = $("#credit-phoneuser-id").val()
    credit.recharge = $("#credit-recharge").val()
    credit.reason = $("#credit-reason").val()
    
    $.ajax({
       type: 'POST',
       url: '/credit/save/',
       async: true,
       data: {data: credit},
       success: function(e){ 
            if(e=="1"){
                msg = '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Ok!</h4>Ricarica inserita con successo.</div>' 
                reload_credits($("#credit-phoneuser-id").val())
            }else{
                msg = '<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Attenzione!</h4>Errore inserimento Ricarica.</div>'
            }
                            
            $('#myModal').modal('hide')
            $('.message').append(msg)       
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Errore nella trasmissione dei dati Ricarica.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })
    
    return false
 })
 
 
/* ==========================================================
 * PhoneCab
 * Funzione Verifica Form Ricarica
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */ 
function check_credit_form(){
	//return false on error
   return clean_and_check_empty_field("#credit-recharge")                                                  
}



/* ==========================================================
 * PhoneCab
 * Funzione Verifica Esistenza Prefisso
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */ 
function check_prefix_existence(selector){
	
    dummy = clean_and_check_empty_field(selector)
    if(!dummy){
    	return false
    }
    
    $(selector).parent().removeClass('error')
    $(selector).parent().removeClass('success')
    phonenumber = $(selector).val()
	
	$.ajax({
	       type: 'POST',
	       url: '/whitelist/check/prefix/',
	       async: true,
	       data: {phonenumber: phonenumber},
	       success: function(e){
	    	   if(e=="1"){
	    		   $('.whitelist-prefix-zone').text('')
	    		   $(selector).parent().addClass('success')
	    		   return true
	    	   }
	    	   if(e=="0"){
	    		   $('.whitelist-prefix-zone').text('Prefisso Assente')
	    		   $(selector).parent().addClass('error')
	    		   return false
	    	   }        
	       },
	       error: function(jqXHR, textStatus, errorThrown){
	            $('#myModal').modal('hide')
	            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
	            msg += '<h4>Attenzione</h4>Errore nella trasmissione dei dati Ricarica.<br>'
	            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
	            $('.message').append(msg)
	            
	            return false
	       }
	    })
}


/* ==========================================================
 * PhoneCab
 * Funzione Verifica Form Whitelist
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */ 
function check_whitelist_form(){
    var ok = true
    
    ok &= clean_and_check_empty_field("#whitelist-label")
	ok &= clean_and_check_empty_field("#whitelist-phonenumber")
    //ok &= check_prefix_existence('#whitelist-phonenumber')
    ok &= clean_and_check_empty_field("#whitelist-duration")
    
    return ok
}




/* ==========================================================
 * PhoneCab
 * Funzione Mostra Registrazioni 
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */ 
$('.show-record').click(function(e){
    e.preventDefault()
    window.location.href="/records/?accountcode="+$(this).attr('data-id') 
})



$('.phoneuser-export-cdr').on('click',function(e){

	accountcode = $('.phoneuser-pincode').text()

	window.location = '/phoneusers/export/'+accountcode

})


$(function(){
	setTimeout(function(){$('.alert').fadeOut("slow"), 2000});
})
 
