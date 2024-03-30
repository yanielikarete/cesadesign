$(document).ready(function(){
        var options = {
          nextButton: true,
          prevButton: true,
          animateStartingFrameIn: true,
          autoPlay: true,
          autoPlayDelay: 3000,
        }
        var sequence = $("#sequence").sequence(options).data("sequence");
});