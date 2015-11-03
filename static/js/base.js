var loading_path = "/static/img/loading.gif"

/* ==========================================================
 * PhoneCab
 * Impostazione CSRFToken per ogni chiamata Ajax
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});


/* ==========================================================
 * PhoneCab
 * Funzione Ricarica Anagrafica
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function reload_anagrafica(phoneuser_id){

	window.location.href = '/phoneusers/view/'+ phoneuser_id;
	/*
	$.ajax({
        type: 'POST',
        url: '/phoneusers/ajax/'+phoneuser_id,
        async: true,
        cache: false,
        success: function(data) {
            $("#anagrafica").html(data)
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert('I (reload_anagrafica) Errore nella trasmissione del dato')
           }
    })
    */
}


/* ==========================================================
 * PhoneCab
 * Funzione Apri Preferenze
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('#open-prefs').click(function(e){
    e.preventDefault()
    $('.modal-body').html('<div style="text-align:center;"><img id=\"loading\" src=\"' + loading_path + '\"></div>')

    // imposto il titolo
    $('#myModalLabel').html('Preferenze')
    $('#modal-action').html('Salva').removeClass().addClass('btn btn-primary save-prefs')

    $.ajax({
       type: 'POST',
       url: '/prefs/edit/',
       async: true,
       success: function(e){
            $('.modal-body').html(e)
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Maschera Preferenze non caricata correttamente.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })

})

/* ==========================================================
 * PhoneCab
 * Funzione Salva Preferenze
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$(".save-prefs").on('click', function(e){
    e.preventDefault()

    var prefs = new Object()

    prefs.naz_connection_charge = $('#prefs-naz-scatto').val()
    prefs.naz_fee_per_second = $('#prefs-naz-tariffa').val()

    prefs.int1_connection_charge = $('#prefs-int1-scatto').val()
    prefs.int1_fee_per_second = $('#prefs-int1-tariffa').val()
    prefs.int1_prefix_list = $('#prefs-int1-prefix').val()

    prefs.int2_connection_charge = $('#prefs-int2-scatto').val()
    prefs.int2_fee_per_second = $('#prefs-int2-tariffa').val()
    prefs.int2_prefix_list = $('#prefs-int2-prefix').val()

    prefs.int3_connection_charge = $('#prefs-int3-scatto').val()
    prefs.int3_fee_per_second = $('#prefs-int3-tariffa').val()
    prefs.int3_prefix_list = $('#prefs-int3-prefix').val()

    prefs.int4_connection_charge = $('#prefs-int4-scatto').val()
    prefs.int4_fee_per_second = $('#prefs-int4-tariffa').val()
    prefs.int4_prefix_list = $('#prefs-int4-prefix').val()

    prefs.int5_connection_charge = $('#prefs-int5-scatto').val()
    prefs.int5_fee_per_second = $('#prefs-int5-tariffa').val()
    prefs.int5_prefix_list = $('#prefs-int5-prefix').val()

    prefs.int6_connection_charge = $('#prefs-int6-scatto').val()
    prefs.int6_fee_per_second = $('#prefs-int6-tariffa').val()
    prefs.int6_prefix_list = $('#prefs-int6-prefix').val()

    prefs.int7_connection_charge = $('#prefs-int7-scatto').val()
    prefs.int7_fee_per_second = $('#prefs-int7-tariffa').val()
    prefs.int7_prefix_list = $('#prefs-int7-prefix').val()

    prefs.int8_connection_charge = $('#prefs-int8-scatto').val()
    prefs.int8_fee_per_second = $('#prefs-int8-tariffa').val()
    prefs.int8_prefix_list = $('#prefs-int8-prefix').val()

    prefs.int9_connection_charge = $('#prefs-int9-scatto').val()
    prefs.int9_fee_per_second = $('#prefs-int9-tariffa').val()
    prefs.int9_prefix_list = $('#prefs-int9-prefix').val()

    prefs.mob_connection_charge = $('#prefs-mob-scatto').val()
    prefs.mob_fee_per_second = $('#prefs-mob-tariffa').val()

    prefs.min_duration = $('#prefs-min-duration').val()
    prefs.alert_before_end = $('#prefs-alert-before-end').val()
    prefs.privacy_mode = 0
    if($("input[type=checkbox]#prefs-privacy-mode").is(':checked')){
        prefs.privacy_mode = 0
    }

    $.ajax({
       type: 'POST',
       url: '/prefs/save/',
       async: true,
       data: {data: prefs},
       success: function(e){
            if(e=="1"){
                msg = '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Ok!</h4>Preferenze modificate con successo.</div>'
            }else{
                msg = '<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Attenzione!</h4>Errore modifica Preferenze.</div>'
            }
            $('#myModal').modal('hide')
            $('.message').append(msg)
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Errore nella trasmissione dei dati Preferenze.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })
 })


/* ==========================================================
 * PhoneCab
 * Funzione Nuova Anagrafica
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('#new-ana').click(function(e){
    e.preventDefault()
    $('.modal-body').html('<div style="text-align:center;"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
    //user_id = $('#user-id').val()
    // imposto il titolo
    $('#myModalLabel').html('Crea Nuova Anagrafica')
    $('#modal-action').html('Salva').removeClass().addClass('btn btn-primary save-ana')

    $.ajax({
       type: 'POST',
       url: '/phoneusers/new/',
       async: true,
       success: function(e){
            $('.modal-body').html(e)
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Maschera Nuova Anagrafica non caricata correttamente.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })

})

/* ==========================================================
 * PhoneCab
 * Funzione Salva Anagrafica
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$(".save-ana").on('click', function(e){
    e.preventDefault()

    var new_ana = false;
    var phoneuser = new Object()

    phoneuser_id = $("#ana-phoneuser-id").val()

    if (phoneuser_id == "None" || phoneuser_id == ''){
        phoneuser.phoneuser_id = 0;
        new_ana = true;
    }else{
        phoneuser.phoneuser_id = phoneuser_id;
        new_ana = false;
    }

    ok = check_anagrafica_form(new_ana);
    if(!ok) return

    phoneuser.enabled = 0
    if($("input[type=checkbox]#ana-enabled").is(':checked')){
        phoneuser.enabled = 1
    }

    phoneuser.first_name = $("#ana-first-name").val()
    phoneuser.last_name = $("#ana-last-name").val()
    phoneuser.serial_no = $("#ana-serial-no").val()
    phoneuser.pincode = $("#ana-pincode").val()
    phoneuser.language = $("#ana-language").val()

    phoneuser.four_bis_limited = 0
    if($("input[type=checkbox]#ana-four-bis-limited").is(':checked')){
        phoneuser.four_bis_limited = 1
    }

    phoneuser.listening_enabled = 0
    if($("input[type=checkbox]#ana-listening-enabled").is(':checked')){
        phoneuser.listening_enabled = 1
    }
    phoneuser.recording_enabled = 0
    if($("input[type=checkbox]#ana-recording-enabled").is(':checked')){
        phoneuser.recording_enabled = 1
    }

    phoneuser.vipaccount = 0
    if($("input[type=checkbox]#ana-vipaccount").is(':checked')){
        phoneuser.vipaccount = 1
    }


    $.ajax({
       type: 'POST',
       url: '/phoneusers/save/',
       async: true,
       data: {data: phoneuser},
       success: function(e){
            if(e != "0"){
                msg = '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Ok!</h4>Anagrafica inserita con successo.</div>'
                // ricarichiamo la parte relativa a anagrafica
                reload_anagrafica(e)
            }else{
                msg = '<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Attenzione!</h4>Errore inserimento Anagrafica.</div>'
            }
            $('#myModal').modal('hide')
            $('.message').append(msg)



       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Errore nella trasmissione dei dati Anagrafica.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })
 })

/* ==========================================================
 * PhoneCab
 * Funzione Edita Anagrafica
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$(".edit-ana").click(function(e){
    e.preventDefault()
    phoneuser_id = $('#phoneuser-id').val()
    $('.modal-body').html('<div style="text-align:center;"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
    // imposto il titolo
    $('#myModalLabel').html('Modifica Anagrafica')
    $('#modal-action').html('Salva').removeClass().addClass('btn btn-primary save-ana')

    $.ajax({
       type: 'POST',
       url: '/phoneusers/edit/'+phoneuser_id,
       async: true,
       success: function(e){
            $('.modal-body').html(e)
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Maschera Modifica Anagrafica non caricata correttamente.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })

})


/* ==========================================================
 * PhoneCab
 * Funzione Archivia Anagrafica
 * ==========================================================
 * Copyright 2014 SuperbatTLC
 * ========================================================== */
$(".archive-ana").click(function(e){

	var button = confirm("Attenzione! L\'archiviazione elimina tutti i dati relati a questa anagrafica.\nSei sicuro di voler continuare?")

    if(button){
	    e.preventDefault();
	    phoneuser_id = $('#phoneuser-id').val();

	    $.ajax({
	       type: 'POST',
	       url: '/phoneusers/archive/'+phoneuser_id,
	       async: true,
	       success: function(e){
	    	   if (e == '1'){
	    		   window.location.href = "/phonecab/?archive=ok";
	    	   }else{
	    		   window.location.href = "/phonecab/?archive=error";
	    	   }

	       },
	       error: function(jqXHR, textStatus, errorThrown){
	    	   window.location.href = "/phonecab/?archive=error"
	       }
	    })
    }else{
    	return
    }

})


/* ==========================================================
 * PhoneCab
 * Funzione Cambia Enable
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$(".enable-ana").click(function(e){
    e.preventDefault()
    var phoneuser_id = $('#phoneuser-id').val();
    var url = '/phoneusers/disable/'+phoneuser_id;

    var enable = $(this).attr("data-action") == '1';
    if(enable){
    	url = '/phoneusers/enable/'+phoneuser_id;
    }

    $.ajax({
       type: 'POST',
       url: url,
       async: true,
       dataType: 'json',
       success: function(response){
            location.reload()
       },
       error: function(jqXHR, textStatus, errorThrown){
    	   //
       }
    })

})

/* ==========================================================
 * PhoneCab
 * Funzione Verifica Form Anagrafica
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function check_anagrafica_form(new_ana){

    var ok = true;

    ok &= clean_and_check_empty_field("#ana-first-name");
    ok &= clean_and_check_empty_field("#ana-last-name");
    ok &= clean_and_check_empty_field("#ana-serial-no");
    if(new_ana){
    	ok &= check_unique_pincode("#ana-pincode");
    }

    return ok
}



/* ==========================================================
 * PhoneCab
 * Funzione Nuovo Utente
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('#new-user').click(function(e){
    e.preventDefault()
    $('.modal-body').html('<div style="text-align:center;"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
    // imposto il titolo
    $('#myModalLabel').html('Crea Nuovo Utente')
    $('#modal-action').html('Salva').removeClass().addClass('btn btn-primary save-user')

    $.ajax({
       type: 'POST',
       url: '/phonecab/user/new',
       async: true,
       success: function(e){
            $('.modal-body').css('max-height','780px').html(e)
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Maschera Nuovo Utente non caricata correttamente.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })

})

/* ==========================================================
 * PhoneCab
 * Funzione Salva Utente
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$(".save-user").on('click', function(e){
    e.preventDefault()

    ok = check_user_form()
    if(!ok) return

    var utente = new Object()

    user_id = $("#user-id").val()

    if (user_id == "None" || user_id == ''){
        utente.user_id = 0
        user_success_msg = 'inserito'
        user_error_msg = 'inserimento'
    }else{
        utente.user_id = user_id
        user_success_msg = 'aggiornato'
        user_error_msg = 'aggiornamento'
    }

    utente.username = $(".user-username").val()
    utente.firstname = $(".user-firstname").val()
    utente.lastname = $(".user-lastname").val()
    utente.password = $(".user-password").val()

    utente.is_admin = 0
    if($("input[type=radio]#user-type-admin").is(':checked')){
        utente.is_admin = 1
    }else{
        // Recuperiamo i privilegi
        utente.priv_anagrafica = 1
        if($("input[type=checkbox]#priv-ana-write").is(':checked')){
            utente.priv_anagrafica = 3
        }
        utente.priv_whitelist = 0
        if($("input[type=checkbox]#priv-white-read").is(':checked')){
            utente.priv_whitelist = 1
        }
        if($("input[type=checkbox]#priv-white-write").is(':checked')){
            utente.priv_whitelist = 3
        }
        utente.priv_credit = 0
        if($("input[type=checkbox]#priv-credit-read").is(':checked')){
            utente.priv_credit = 1
        }
        if($("input[type=checkbox]#priv-credit-write").is(':checked')){
            utente.priv_credit = 3
        }
        utente.priv_cdr = 0
        if($("input[type=checkbox]#priv-cdr-read").is(':checked')){
            utente.priv_cdr = 1
        }
        utente.priv_record = 0
        if($("input[type=checkbox]#priv-record-read").is(':checked')){
            utente.priv_record = 1
        }
    }


    $.ajax({
       type: 'POST',
       url: '/phonecab/user/save/',
       async: true,
       data: {data: utente},
       success: function(e){
            if(e=="1"){
                msg = '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Ok!</h4>Utente '+user_success_msg+' con successo.</div>'
            }else{
                msg = '<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Attenzione!</h4>Errore '+user_error_msg+' Utente.</div>'
            }

            $('#myModal').modal('hide')
            $('.message').append(msg)
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Errore nella trasmissione dei dati Utente.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })
 })

/* ==========================================================
 * PhoneCab
 * Funzione Edita Utente
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.edit-user').click(function(e){
    e.preventDefault()
    $('.modal-body').html('<div style="text-align:center;"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
    // imposto il titolo
    $('#myModalLabel').html('Modifica Utente')
    $('#modal-action').html('Salva').removeClass().addClass('btn btn-primary save-user')

    $.ajax({
       type: 'POST',
       url: '/phonecab/user/edit/'+$(this).attr("data-id"),
       async: true,
       success: function(e){
            $('.modal-body').css('max-height','780px').html(e)
       },
       error: function(jqXHR, textStatus, errorThrown){
            $('#myModal').modal('hide')
            msg = '<div class="alert alert-warning"><button type="button" class="close" data-dismiss="alert">x</button>'
            msg += '<h4>Attenzione</h4>Maschera Modifica Utente non caricata correttamente.<br>'
            msg += 'Si prega di contattare il responsabile del software PhoneCab.</div>'
            $('.message').append(msg)
       }
    })

})

/* ==========================================================
 * PhoneCab
 * Funzione Verifica Form Utente
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function check_user_form(){
    var ok = true

    ok &= clean_and_check_empty_field(".user-firstname")
    ok &= clean_and_check_empty_field(".user-lastname")
    if ($("#user-id").val() == 'None' || $("#user-id").val() == ''){
        ok &= check_unique_username(".user-username")
    }
    ok &= check_passwords()

    return ok
}


/* ==========================================================
 * PhoneCab
 * Funzione Verifica Campi Password Utente
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function check_passwords() {
    // return false on error
    if($(".user-password").val()) {
        if($(".user-confirm-password").val()) {
            //alert("ci sono tutte e due le pass")
            if($(".user-confirm-password").val() == $(".user-password").val()) {
                $("#user-confirm-password-div").addClass('success')
                $("#user-password-div").addClass('success')
                return true
            }else{
                //alert('le pass sono diverse!')
                $("#user-confirm-password-div").addClass('error')
                $("#user-password-div").addClass('error')

            }
        }else{
            //alert("manca la pass di confirm")
            $("#user-confirm-password-div").addClass('error')
            $("#user-password-div").addClass('success')
        }
    }else{
        if($("#user-id").val() != 'None'){
            $("#user-confirm-password-div").addClass('success')
            $("#user-password-div").addClass('success')
            return true
        }

        if($(".user-confirm-password").val()) {
            //alert("manca la pass")
            $("#user-password-div").addClass('error')
            $("#user-confirm-password-div").addClass('success')
        }else{
            //alert("mancano tutte le pass")
            $("#user-confirm-password-div").addClass('error')
            $("#user-password-div").addClass('error')
        }
    }

    return false
}

/* ==========================================================
 * PhoneCab
 * Funzione Verifica Username Univoco
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function check_unique_username(){
    // return false on error
    username = $(".user-username").val()
    if(!username) {
        $("#user-username-div").addClass('error')
        return false
    }

    var ret = true;

    $.ajax({
       type: 'POST',
       url: '/phonecab/user/check/',
       async: false,
       data: {username: username},
       success: function(e){
            if(e=="0"){
                $("#user-username-div").addClass('success')
                ret = true
            }else{
                $("#user-username-div").addClass('error')
                ret = false
            }
       }
    })

    return ret
}

/* ==========================================================
 * PhoneCab
 * Funzione Verifica Pincode Univoco
 * ==========================================================
 * Copyright 2014 SuperbatTLC
 * ========================================================== */
function check_unique_pincode(pincode){
    // return false on error
    if(!$(pincode).val()) {
        $(pincode).parent().addClass('error')
        $('.pincode-check').show()
        return false
    }


    var ret = false;

    $.ajax({
       type: 'POST',
       url: '/phoneusers/check/',
       async: false,
       data: {pincode: $(pincode).val()},
       success: function(e){
    	   // ritorna il numero di occorrenze
            if(e=="0"){
            	$(pincode).parent().removeClass('error')
                $('.pincode-check').hide()
                ret = true
            }else{
            	$(pincode).parent().addClass('error')
                $('.pincode-check').show()
                ret = false
            }
       }
    })

    return ret
}






/* ==========================================================
 * PhoneCab
 * Funzione Mostra finestra Conferma Eliminazione Utente
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('#confirm-remove-user').click(function(e){
    user_id = $(this).attr("data-id")
    e.preventDefault()
    $('.modal-body').html('Si prega di confermare l\'eliminazione utente.')
    // imposto il titolo
    $('#myModalLabel').html('Elimina Utente')
    $('#modal-action').html('Elimina')
    $('#modal-action').removeClass().addClass('btn btn-danger remove-user').attr('data-id',user_id)
})

/* ==========================================================
 * PhoneCab
 * Funzione Elimina Utente
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
$('.remove-user').on('click',function(e){
    e.preventDefault()
    user_id = $(this).attr("data-id")

    $.ajax({
       type: 'POST',
       url: '/phonecab/user/remove/'+user_id,
       async: true,
       success: function(e){
            if(e=="1"){
                msg = '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Ok!</h4>Utente eliminato con successo.</div>'
            }else{
                msg = '<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">x</button>'
                msg += '<h4>Attenzione!</h4>Errore eliminazione Utente.</div>'
            }
            $('#myModal').modal('hide')
            $('.message').append(msg)
       }
    })
})



// SCHEDA NUOVO UTENTE
$("input[type=radio]#user-type-admin").on('change',function(){
            if($(this).is(':checked')){
                $('div#privileges').fadeOut("slow")
            }else{
                $('div#privileges').fadeIn("slow")
            }
})

$("input[type=radio]#user-type-op").on('change',function(){
            if($(this).is(':checked')){
                $('div#privileges').fadeIn("slow")
            }else{
                $('div#privileges').fadeOut("slow")
            }
})


/* ==========================================================
 * PhoneCab
 * Funzione Verifica Campo non Vuoto
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function clean_and_check_empty_field(selector){
    // restituisce false on error
    $(selector).removeClass('error')
    $(selector).removeClass('success')

    if($(selector).val()){
        $(selector).parent().addClass('success')
        return true
    }else{
        $(selector).parent().addClass('error')
        return false
    }
}



/* ==========================================================
 * PhoneCab
 * Funzione Apertura finestra registrazione
 * ==========================================================
 * Copyright 2012 SuperbatTLC
 * ========================================================== */
function popitup(url) {
    newwindow=window.open(url,'Registrazione','height=100,width=350');
    if (window.focus) {newwindow.focus()}
    return false;
}



$(function(){
	// timeout per il fadeout dei messaggi alert
	//setTimeout(function() { $("body").on(div.alert").fadeOut("slow") }, 5000);

	var timer = setInterval(function(){
		// controlliamo di essere nell pagina corretta
		var next_mode = $('.daynight').attr("data-next-mode");

		// vecchia gestione realtime
		//if(window.location.href.indexOf("phonecab") > -1 && next_mode == 'NOTTE'){
		//	update_realtime();
		//}

		//update_realtime();

	},10000);



})
