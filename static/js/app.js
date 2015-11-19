var TIMEOUT = 5000;

var Modal = {
  open: function(dict) {
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
  save_function: null,
  save: function() {
    var callback = function(data) {
      //console.log(data);
      if (data.success) $('#myModal').modal('hide');
    }
    if (Modal.save_function) {
      Modal.save_function(callback);
    } else {
      callback({
        success: true
      });
    }
  },
  remove_function: null,
  remove: function() {
    if (Modal.remove_function) {
      Modal.remove_function()
    }
    $('#myModal').modal('hide');
  }
}

function stopPropagation(event) {
  if (event.stopPropagation) {
    event.stopPropagation();
  } else if (window.event) {
    window.event.cancelBubble = true;
  }
}

function showMessageBox(title, content, alertClass) {
  $('#messagebox .title').html(title);
  $('#messagebox .content').html(content);
  $('#messagebox > div').addClass(alertClass);

  $('#messagebox').fadeIn();
  $('#messagebox').removeClass("hide");

  setTimeout(function() {
    $('#messagebox').fadeOut();
  }, 5000);
}

function requestData(method, dataType, relativeUrl, data, onSuccess, onError) {
  var request = $.ajax({
    type: method,
    url: relativeUrl,
    dataType: dataType,
    data: data,
    timeout: TIMEOUT
  })

  .done(function(response, textStatus, jqXHR) {
    if (response.hasOwnProperty("err") && response.err > 0) {
      console.error("REQUEST ERROR '" + relativeUrl + "' (follows data object, and status)");
      console.log('request data: ', data);
      console.log('status: ' + response.errMsg);
      if (onError) onError(response.errMsg);
    } else onSuccess(response);
  })

  .fail(function(jqXHR, textStatus, errorThrown) {
    console.error("REQUEST FAILED '" + relativeUrl + "' (follows data object, and status)");
    console.log('request data: ', data);
    console.log('error: ' + jqXHR.statusText);
    console.log([jqXHR.responseText.split('\n')]);
    if (onError) onError(jqXHR);
  });

}

function requestDataDjango(method, dataType, relativeUrl, data, onSuccess, onError) {
  var request = $.ajax({
    type: method,
    url: relativeUrl,
    dataType: dataType,
    data: data,
    timeout: TIMEOUT
  })

  .done(function(response, textStatus, jqXHR) {
    onSuccess(response);
  })

  .fail(function(jqXHR, textStatus, errorThrown) {
    console.error("REQUEST FAILED '" + relativeUrl + "' (follows data object, and status)");
    console.log('request data: ', data);
    console.log('error: ' + jqXHR.statusText);
    console.log([jqXHR.responseText.split('\n')]);
    if (onError) onError(jqXHR.statusText);
  });

}

function checkEmptyField(selector) {
  // restituisce false on error
  $(selector).parent().parent().removeClass('has-error')

  if (!$(selector).val()) {
    $(selector).parent().parent().addClass('has-error')
    return false
  }
  return true;
}

function checkUniquePincode(pincode_sel, callback) {
  // async check
  // chiama il callback con {success:bool} al termine
  var pincode = $(pincode_sel).val();
  var parent = $(pincode_sel).parent().parent();
  if (!pincode) {
    parent.addClass('has-error');
    $('.pincode-check').show();
    callback({
      success: false
    });
    return;
  }

  requestDataDjango("POST", "text", '/phoneusers/check/', {
    pincode: pincode
  }, function(response) {
    if (response == "0") {
      parent.removeClass('has-error');
      $('.pincode-check').hide();
      callback({
        success: true
      });
      return;
    } else {
      parent.addClass('has-error');
      $('.pincode-check').removeClass('hide');
      callback({
        success: false
      });
      return;
    }
  })
}

function checkUniqueUsername(username_sel, callback) {
  // async check
  // chiama il callback con {success:bool} al termine
  var username = $(username_sel).val();
  var parent = $(username_sel).parent().parent();
  if (!username) {
    parent.addClass('has-error');
    $('.username-check').show();
    callback({
      success: false
    });
    return;
  }

  requestDataDjango("POST", "text", '/profiles/check/', {
    username: username
  }, function(response) {
    if (response == "0") {
      parent.removeClass('has-error');
      $('.username-check').hide();
      callback({
        success: true
      });
      return;
    } else {
      parent.addClass('has-error');
      $('.username-check').removeClass('hide');
      callback({
        success: false
      });
      return;
    }
  })
}

function updateDOM(selector, content) {
  $(selector).html(content);
}


function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    return '';
}



$(function() {

  $("body").find(".btn-flip, .card-image").on("click",
    function(el) {
      $(el.currentTarget).parents(".card").find(".card-reveal").toggleClass("active")
    })


  $('[data-role="jquerytagsinput"]').tagsinput({
    confirmKeys: [13, 44],
    trimValue: true,
    cancelConfirmKeysOnEmpty: true,
  });
  $('[data-role="jquerytagsinput"]').on('itemAdded itemRemoved', function(el) {
    $(el.target).attr('value',$(el.target).val());
  });
  $('.bootstrap-tagsinput input').attr('tabindex','-1'); //avoid TAB on tagsinput inputs


  $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover();


  $('.navbar-toggle').sideNav({
    menuWidth: 200,
    closeOnClick: true
  });

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

  $('.form-control').each(function() {
    // Add class filled to form-control's that have a value
    if ($(this).val()) {
      $(this).parent().addClass('filled');
    }

    // Animate form labels
    $(this).bind('blur', function(e) {
      input = $(e.currentTarget);
      if (input.val()) {
        input.parent().addClass('filled');
      } else {
        input.parent().removeClass('filled');
      }
      input.parent().removeClass('active');
    }).bind('focus', function(e) {
      input = $(e.currentTarget);
      input.parent().addClass('active');
    });
  });

  // evidenziazione menu attivo
  var path_elements = window.location.pathname.split("/");
  var element = 1;
  if(path_elements[1] == 'archives'){
    element = 2;
  }
  $('.sidebar li a[data-menu=' + window.location.pathname.split("/")[element] + ']').addClass("active");
  

  // gestione errori e notifiche da url
  var err = getQueryVariable('err') != '';
  if(err){
    var err_msg = getQueryVariable('err_msg');
    showMessageBox("Errore", err_msg, "alert-danger");
  } 
  var ok = getQueryVariable('ok') != '';
  if(ok) {
    var msg = getQueryVariable('msg');
    showMessageBox("Conferma", msg, "green");
  }

});
