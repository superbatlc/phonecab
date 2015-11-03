$('.cdr-date-filter').datepicker()

/* ==========================================================
 * PhoneCab
 * Funzione Filtra CDR
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.cdr-do-filter').on('click',function(){
                                        
    $('#cdr-table').html('<div style=\"text-align:center; height:300px;vertical-align:middle;\"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
                                        
    dict = {}
    
    if($('input[name=data_inizio]').val()){
        dict['start_date'] = $('input[name=data_inizio]').val()
        if($('input[name=ora_inizio]').val()){
            dict['start_time'] = $('input[name=ora_inizio]').val()
        }
    }
                                                                
    if($('input[name=data_fine]').val()){
        dict['end_date'] = $('input[name=data_fine]').val()
        if($('input[name=ora_fine]').val()){
            dict['end_time'] = $('input[name=ora_fine]').val()
        }
    }
                                                    
    if($('input[name=accountcode]').val()){
        dict['accountcode'] = $('input[name=accountcode]').val()
    }
                                          
    if($('input[name=dst]').val()){
        dict['dst'] = $('input[name=dst]').val()
    }
     
    
    $.ajax({
           type: 'GET',
           url: '/cdr/ajax/filter/',
           data: dict,
           success: function(data){
                $('.log-cdr').html(data)                            
           },
           error: function(xhr, ajaxOptions, thrownError){
                alert(xhr.status)
                 alert(thrownError)
            }
    })
})


/* ==========================================================
 * PhoneCab
 * Funzione Paginazione CDR
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.cdr-page').on('click',function(e){
    e.preventDefault()

    query = $(this).attr('href')
    
    $.ajax({
           type: 'GET',
           url: '/cdr/ajax/filter/'+query,
           success: function(data){
                $('.log-cdr').html(data)                            
           },
            error: function(xhr, ajaxOptions, thrownError){
                alert(xhr.status)
                 alert(thrownError)
            }
    })
})



/* ==========================================================
 * PhoneCab
 * Abilitazione / Disabilitazione Chiamate
 * ==========================================================
 * Copyright 2015 SuperbatTLC
 * ========================================================== */
$('.cdr-valid').on('click',function(e){
	
	var button = confirm("Attenzione! L\'abilitazione/disabilitazione di una chiamata influisce sul calcolo complessivo.\nSei sicuro di voler continuare?")
    
    if(button){
	
		var this_this = this
		var icon = $("i", this_this);
		var detail_id = $(this_this).attr("data-id");
		// valore attuale
		var valid = $(this_this).attr("data-valid");
		
		$.ajax({
		       type: 'POST',
		       url: '/cdr/valid/',
		       async: true,
		       data: {detail_id: detail_id, valid: valid},
		       dataType: 'json',
		       success: function(response){
		    	   if(response.err == "0"){
		    		// nuovo valore attuale
			    	   if(!response.data){
			    		   $(this_this).attr("data-valid","False");
			    		   icon.removeClass("icon-ok").addClass("icon-remove");
			    	   }else{
			    		   $(this_this).attr("data-valid","True");
			    		   icon.removeClass("icon-remove").addClass("icon-ok");
			    	   }
		    	   } else {
		    		   msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
		    	       msg += '<h4>Errore:</h4>' + response.err_msg + '<br>';
		    	       msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
		    	       $('.message').append(msg);
		    	   }
		       },
		       error: function(jqXHR, textStatus, errorThrown){
		    	   msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>';
		    	   msg += '<h4>Errore nella trasmissione del dato</h4><br>';
		    	   msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>';
		    	   $('.message').append(msg);
		       }
		    })
    } else {
    	return false;
    }
})



