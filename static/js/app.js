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

});
