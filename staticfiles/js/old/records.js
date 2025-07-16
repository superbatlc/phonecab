$('.records-date-filter').datepicker()

/* ==========================================================
 * PhoneCab
 * Funzione Filtra Record
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.records-do-filter').on('click',function(){
                                        
    $('#records-table').html('<div style=\"text-align:center; height:300px;vertical-align:middle;\"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
                                        
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
                                                    
    if($('input[name=pincode]').val()){
        dict['pincode'] = $('input[name=pincode]').val()
    }

    
    $.ajax({
           type: 'GET',
           url: '/records/ajax/filter/',
           data: dict,
           success: function(data){
                $('.log-records').html(data)                            
           },
           error: function(xhr, ajaxOptions, thrownError){
                alert(xhr.status)
                 alert(thrownError)
            }
    })



})

/* ==========================================================
 * PhoneCab
 * Funzione Paginazione Record
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.records-page').on('click',function(e){
    e.preventDefault()

    query = $(this).attr('href')
    
    $.ajax({
           type: 'GET',
           url: '/records/ajax/filter/'+query,
           success: function(data){
                $('.log-records').html(data)                            
           },
            error: function(xhr, ajaxOptions, thrownError){
                alert(xhr.status)
                 alert(thrownError)
            }
    })
})


/* ==========================================================
 * PhoneCab
 * Funzione Mostra finestra Conferma Eliminazione Record
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.records-confirm-remove').on('click',function(e){
	//e.preventDefault()
	do_remove = confirm("Attenzione! i file saranno cancellati definitivamente. Continuare?")

	if(!do_remove){
		return false
	}
})


/* ==========================================================
 * PhoneCab
 * Funzione Elimina Utente
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.remove-record').on('click',function(e){
    e.preventDefault()                           
    record_id = $(this).attr("data-id")
    
    $.ajax({
       type: 'POST',
       url: '/records/remove/'+record_id,
       async: true,
       success: function(e){ 
            if(e=="1"){
                msg = '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">×</button>'
                msg += '<h4>Ok!</h4>Registrazione eliminata con successo.</div>'      
            }else{
                msg = '<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">×</button>'
                msg += '<h4>Attenzione!</h4>Errore eliminazione Registrazione.</div>'
            }
            $('#myModal').modal('hide')
            $('.message').append(msg)
       }
    })  
})


$('.records-export').on('click',function(e){
        //e.preventDefault()
        $(this).addClass('hide')
        //$('.records-confirm-remove').removeClass('hide')
})
