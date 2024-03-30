$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
    $(this).toggleClass('active');
    if($.cookie("offcanvas") == 'false'){
    	$.cookie("offcanvas",true);
    }else{
    	$.cookie("offcanvas",false);
    }
  });

  if($.cookie("offcanvas") == 'false'){
   $('[data-toggle=offcanvas]').removeClass('active');
   $('.row-offcanvas').removeClass('active');
  }

  if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    $('.row-offcanvas').removeClass('active');
  }
});