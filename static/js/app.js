var TIMEOUT = 5000;

var Modal = {
    open : function(dict){
      console.log(dict);
        if (!dict.hasOwnProperty('title')) dict.title = 'No title';
        if (!dict.hasOwnProperty('content')) dict.content = 'No content';
        if (!dict.hasOwnProperty('onSave')) dict.onSave = null;
        if (!dict.hasOwnProperty('onRemove')) dict.onRemove = null;
                                           
        $('#myModalLabel').text(dict.title);
        $('#myModal .modal-body').html(dict.content);

        $('#myModal').modal();
        Modal.save_function = dict.onSave;
        Modal.remove_function = dict.onRemove;
    },
    save_function : null,
    save : function(){
        if (Modal.save_function) {
            if(!Modal.save_function()){
              return;
            }
        }
        $('#myModal').modal('hide');
    },
    remove_function : null,
    remove : function(){
      if (Modal.remove_function) {
            Modal.remove_function()
        }
      $('#myModal').modal('hide');
    }
}

function stopPropagation(event){
  if (event.stopPropagation){
         event.stopPropagation();
  }
  else if(window.event){
    window.event.cancelBubble=true;
  }
}

function showMessageBox(title, content, alertClass) {
      $('#messagebox .title').html(title);
      $('#messagebox .content').html(content);
      $('#messagebox > div').addClass(alertClass);
      
      $('#messagebox').removeClass("hide");
      setTimeout(function(){
        $('#messagebox').fadeOut();
      }, 5000);
}

function requestData(method,dataType,relativeUrl,data,onSuccess,onError) {
    var request = $.ajax({type: method,
                          url: relativeUrl,
                          dataType: dataType,
                          data: data,
                          timeout: TIMEOUT})

    .done(function(response,textStatus,jqXHR) {
      if (response.hasOwnProperty("err") && response.err > 0) {
        console.error("REQUEST ERROR '"+relativeUrl+"' (follows data object, and status)");
        console.log('request data: ',data);
        console.log('status: '+response.errMsg);
        if (onError) onError(response.errMsg);
      }
      else onSuccess(response);
    })

    .fail(function(jqXHR, textStatus, errorThrown) {
      console.error("REQUEST FAILED '"+relativeUrl+"' (follows data object, and status)");
      console.log('request data: ',data);
      console.log('error: ' + jqXHR.statusText);
      console.log( [jqXHR.responseText.split('\n')]);
      if (onError) onError(jqXHR.statusText);
    });

}


function requestDataDjango(method,dataType,relativeUrl,data,onSuccess,onError) {
    var request = $.ajax({type: method,
                          url: relativeUrl,
                          dataType: dataType,
                          data: data,
                          timeout: TIMEOUT})

    .done(function(response,textStatus,jqXHR) {
      onSuccess(response);
    })

    .fail(function(jqXHR, textStatus, errorThrown) {
      console.error("REQUEST FAILED '"+relativeUrl+"' (follows data object, and status)");
      console.log('request data: ',data);
      console.log('error: ' + jqXHR.statusText);
      console.log( [jqXHR.responseText.split('\n')]);
      if (onError) onError(jqXHR.statusText);
    });

}


function checkEmptyField(selector){
    // restituisce false on error
    $(selector).parent().parent().removeClass('has-error')

    if(!$(selector).val()){
        $(selector).parent().parent().addClass('has-error')
        return false
    }
    return true;
}

function checkUniquePincode(pincode_sel){
    // return false on error
    var pincode = $(pincode_sel).val();
    var parent = $(pincode_sel).parent().parent();
    if(!pincode) {
        parent.addClass('has-error');
        $('.pincode-check').show();
        return false;
    }

    requestDataDjango("POST", "text", '/phoneusers/check/', {pincode : pincode}, function(response){
      if(response == "0"){
        parent.removeClass('has-error');
        $('.pincode-check').hide();
        return true;
      }else{
        parent.addClass('has-error');
        $('.pincode-check').show();
        return false;
      }
    })
}




$(function () {

  $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover();

  $('.navbar-toggle').sideNav({ menuWidth: 260, closeOnClick: true });

  var withRipples = [
    '.btn:not(.withoutripple)',
    '.card-image',
    '.navbar a:not(.withoutripple)',
    '.dropdown-menu a',
    '.nav-tabs a:not(.withoutripple)',
    '.withripple'
  ].join(',');

  $('body').find(withRipples).ripples();

	var icons = {
			time: 'zmdi zmdi-time',
			date: 'zmdi zmdi-calendar',
			up: 'zmdi zmdi-chevron-up',
			down: 'zmdi zmdi-chevron-down',
			previous: 'zmdi zmdi-chevron-left',
			next: 'zmdi zmdi-chevron-right',
			today: 'zmdi zmdi-dot-circle-alt',
			clear: 'zmdi zmdi-delete',
			close: 'zmdi zmdi-close'
	};

	$('input.timepicker').datetimepicker({
										icons: icons,
                    format: 'HH:mm',
										locale: 'it'
                }).show();

	$('input.datepicker').datetimepicker({
										// inline: true,
										// sideBySide: true,
										icons: icons,
                    format: 'DD-MM-YYYY',
										locale: 'it'
                }).show();

  $('.form-control').each(function (){
		console.log($(this));
    // Add class filled to form-control's that have a value
    if($(this).val()){
      $(this).parent().addClass('filled');
    }

    // Animate form labels
    $(this).bind('blur', function (e) {
      input = $(e.currentTarget);
      if(input.val()){
        input.parent().addClass('filled');
      } else {
        input.parent().removeClass('filled');
      }
      input.parent().removeClass('active');
    }).bind('focus', function (e) {
      input = $(e.currentTarget);
      input.parent().addClass('active');
    });
  });

  /*  
  $(".edit-ana").click(function(e){
    e.preventDefault()
    phoneuser_id = $('#phoneuser-id').val()
    //$('.modal-body').html('<div style="text-align:center;"><img id=\"loading\" src=\"' + loading_path + '\"></div>')
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
*/

});


