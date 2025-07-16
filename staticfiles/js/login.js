
$(function () {

  $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover();

  var withRipples = [
    '.btn:not(.withoutripple)',
    '.card-image',
    '.navbar a:not(.withoutripple)',
    '.dropdown-menu a',
    '.nav-tabs a:not(.withoutripple)',
    '.withripple'
  ].join(',');

  $('body').find(withRipples).ripples();

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
