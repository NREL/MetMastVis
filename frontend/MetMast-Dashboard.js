$(document).ready(function(){
  testrequest();
});

//supporting functions
testrequest = function() {
  console.log("testing");
  $.ajax({
    url: 'https://s3-us-west-2.amazonaws.com/nrel-nwtc-metmast-uni/int/dt%3D2013-05/2013_05.csv',
    dataType: 'text',
    success: function (data) {
      console.log("raf - success");
    },
    error: function (e) {
      console.log("raf - error");
    }
  });
}
constructStickyHeader = function(){
  $('.turbine-table').prepend('<table class="stickyHeader" data-sortable></table>');
  $('.stickyHeader').prepend($('.turbine-table thead').html());
  tableTop = $('.stickyHeader').offset().top;
}
stickyWidth = function(){
  //get widths from "real" header
  thWidths = [];
  $('.turbine-table thead th').each(function(){
    thWidths.push($(this).width());
  });
  //apply widths to sticky header
  for (i = 0; i < $('.turbine-table thead th').length; i++) {
    cellWidth = thWidths[i];
    thChild = i+1;
    $('.stickyHeader th:nth-child('+thChild+')').css('width',cellWidth+16+'px');
  }
}
expandedSticky = function(){
  scrollTop = $(window).scrollTop();
  if(scrollTop > tableTop){
    //expanded table sticky scroll
    $('.stickyHeader').addClass('expanded');
  } else {
    $('.stickyHeader').removeClass('expanded');
  }
};
expandedEnd = function(){
  lastRow = $('.turbine-table tr:last').offset().top;
  headerHeight = $('.stickyHeader.expanded').outerHeight();
  expandedEndHeight = lastRow - tableTop - headerHeight;
  if(lastRow - headerHeight - scrollTop <= 0){
    $('.stickyHeader').removeClass('expanded').css({'top':expandedEndHeight});
  }
}
//wait for DOM to complete to set stickyHeader widths
$(window).load(function(){
  stickyWidth();
})
//resize stickyHeader on window resize
$(window).resize(function(){
  tableTop = $('.stickyHeader').offset().top;
  stickyWidth();
});