$(document).ready(function(){
  // Number of days since last report to be considered active.
  var daysSinceLastViableReport = 10;
  var lastViableReportTime = new Date();
  lastViableReportTime.setDate(lastViableReportTime.getDate() - daysSinceLastViableReport);

  //WFSP main page
  if(location.pathname == "/wiki/metmastportal"){
    //define & set variables
    latestData = [];
    itemData = [];

    turbineEnergy = 0;
    turbineTotalEnergy = 0;
    turbinePower = 0;
    turbineWindSpeed = 0;

    wfspEnergy = 0;
    totalProjects = 0;
    runningProjects = 0;
    reportingProjects = 0;

    //fetch turbine data
    $.ajax({
      url: 'tbd',
      dataType: 'json',
      success: function(data) {
        itemData = data.items;
        if ($.isArray(itemData)) {
          for (var i in itemData) {
            var turbineID = parseInt(itemData[i].turbine_id);
            var turbineEnergy = parseInt(itemData[i].total_energy);
            var turbineDailyEnergy = parseInt(itemData[i].energy_today);
            var turbinePower = parseInt(itemData[i].power);
            var turbineWindSpeed = parseInt(itemData[i].wind);
            var turbineStatus = itemData[i].turbine_status.toString().replace(/,/g,'<br />');
            var systemStatus = itemData[i].system_status.toString().replace(/,/g,'<br />');
            var lastReported = new Date((itemData[i].last_reported).concat(" UTC").replace(/-/g, "/"));

            var oneMonthAgo = new Date();
            oneMonthAgo.setDate(oneMonthAgo.getDate() - 30);

            if (lastReported < lastViableReportTime) {
              var statusCode = 'unregistered statusCell';
              systemStatus = 'Not reporting';
            }

            if (lastReported > oneMonthAgo && lastReported >= lastViableReportTime) {reportingProjects += 1};

            wfspEnergy += turbineEnergy;
            if(!$.inArray("Running", systemStatus)){
              runningProjects += 1;
            }
            latestData[parseInt(turbineID)] = itemData[i];
            if(systemStatus.indexOf('Running') >= 0){
              var statusCode = "alert-success";
              runningProjects += 1;
            }
            if(systemStatus.indexOf('Not Running') >= 0){
              var statusCode = "alert-danger";
              runningProjects -= 1;
            }
            $('tr[data-id="'+turbineID+'"]').append('<td>'+turbinePower+'</td><td>'+turbineWindSpeed+'</td><td>'+turbineDailyEnergy+'</td><td>'+turbineEnergy+'</td><td>'+turbineStatus+'</td><td class="alert '+statusCode+'">'+systemStatus+'</td><td>'+String(lastReported).slice(0,21)+'</td>');
          }
          totalProjects = Object.keys(latestData).length;
          videoHrs = Math.round(((wfspEnergy*1000)/11.1)*14);
          videoYrs = Math.round(videoHrs/8766);

          $('#turbineCount').text(totalProjects);
          $('#runningCount').text(reportingProjects);
          $('#totalEnergy').text(wfspEnergy.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","));
          $('#videoPlayback').text(videoYrs.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","));
        }
        //add null cells if turbine has not been registered
        $('tr').each(function(){
          if($(this).children('td').length == 2){
            $(this).append('<td class="unregistered">-</td><td class="unregistered">-</td><td class="unregistered">-</td><td class="unregistered">-</td><td class="unregistered">Not Registered</td><td class="unregistered statusCell">Not Registered</td><td class="unregistered">-</td>');
          }
        });
      }
    });

    //add table head <thead>
    $('.turbine-table table').prepend('<thead><tr><th class="active ascending">School</th><th>Location</th><th>Power (W)</th><th>Wind (m/s)</th><th>Energy Today (kWh)</th><th>Total Energy (kWh)</th><th>Turbine Status</th><th>System Status</th><th>Last Reported</th></tr></thead>');

    //add data-index to th elements
    $('#sort-table th').each(function(){
      headerIndex = $(this).index();
      $(this).attr('data-index',headerIndex);
    });

    //render sticky table header
    constructStickyHeader();
    stickyWidth();

    //sticky header action for collapsed table
    $('.turbine-table.table-mask').scroll(function(){
      sticky = $(this).scrollTop();
      $('.stickyHeader').css('top',sticky+'px');
    });

    //expland/collapse table action
    $('.expand-tab').click(function(){
      if($('.turbine-table').hasClass('table-mask')){
        $('.expand-tab').text('Collapse Table');
        $('.turbine-table').removeClass('table-mask');
        return;
      } else {
        $('.expand-tab').text('Expand Table');
        $('.turbine-table').addClass('table-mask');
      }
    });

    //table header click action
    $('.stickyHeader th').click(function(){
      clickIndex = $(this).index();
      $('.stickyHeader th, #sort-table th').removeClass('active ascending descending');
      $(this).addClass('active');
      $('#sort-table').find('[data-index='+clickIndex+']').addClass('active').trigger('click');
      sortDirection = $('#sort-table').find('th.active').attr('aria-sort');
      $(this).addClass(sortDirection);
    });

    //fix flickering stickyHeader
    //set stickyHeader to fixed when scrolling inside table
    $('.turbine-table.table-mask').scroll(function(){
      var windowTop = $(window).scrollTop();
      var tableTop = $(this).offset().top;
      $('.stickyHeader').css({'position':'fixed','top':tableTop - windowTop});
    });
    //set stickyHeader to absolute when on scroll out of header
    $(window).scroll(function(){
      var tableTop = $('.turbine-table').scrollTop();
      $('.stickyHeader').css({'position':'absolute','top':tableTop});
    });

    //sticky header action for exapnded table
    $(window).scroll(function(){
      if(!$('.turbine-table.table-mask').is(':visible')){
        expandedSticky();
        expandedEnd();
      } else {
        $('.stickyHeader').removeClass('expanded');
      }
    });

    //check to see if table is ready for sort initialization
    activateTable = setInterval(function() {
    if ($('.stickyHeader').length) {
      initializeDataTables();
      $('#sort-table').dataTable({
        searching:false,
        paging:false
      });
      //clear activation check
      clearInterval(activateTable);
    }
  }, 100);

  } else {
    //School pages
    //define & set variables
    latestData = [];
    itemData = [];

    turbineID = $('#wfspID').text();

    turbineEnergy = 0;
    turbineDailyEnergy = 0;
    turbinePower = 0;
    turbineVolts = 0;
    turbineRPM = 0;
    turbineWindSpeed = 0;

    //fetch turbine data
    $.ajax({
      url: '/services/api/3/WFS/?latest=true&turbineid='+turbineID,
      dataType: 'json',
      success: function(data) {
        itemData = data.items;
        if ($.isArray(itemData)) {
          for (var i in itemData) {
            var turbineEnergy = parseInt(itemData[i].total_energy);
            var turbineDailyEnergy = parseInt(itemData[i].energy_today);
            //var turbinePower = parseInt(itemData[i].power);
            var turbinePower = itemData[i].power;
            var turbineVolts = parseInt(itemData[i].volts);
            var turbineRPM = parseInt(itemData[i].rpm);
            var turbineWindSpeed = parseInt(itemData[i].wind);
            var turbineStatus = itemData[i].turbine_status.toString().replace(/,/g,'<br />');
            var systemStatus = itemData[i].system_status.toString().replace(/,/g,'<br />');
            var lastReported = new Date((itemData[i].last_reported).concat(" UTC").replace(/-/g, "/"));

            if (lastReported < lastViableReportTime) {
              systemStatus = 'Not reporting';
            }
            lastReported = String(lastReported).slice(0,21);

            $('.watts').text(turbinePower.toFixed(2)*1000);
            $('.volts').text(turbineVolts);
            $('.rpm').text(turbineRPM);
            $('.speed').text(turbineWindSpeed+' m/s');
            $('.turbineHealth').html(turbineStatus);
            $('.systemHealth').html(systemStatus);
            $('.timestamp').text(lastReported);
            $('.dailyEnergy').text(turbineDailyEnergy+' kWh');
            $('.lifeEnergy').text(turbineEnergy+' kWh');

            //remove div elements if there is no chart to display
            if(lastReported == "1969-12-31 23:00:00"){
              $('.mm-dashboard-cluster').addClass('not-registered');
              $('#div_graphs, #div_preset_btns').hide();
            }

            //the wiki places a successful {{#show}} query outside of the intended HTML - if there is an installed capacity value, move it to the proper parent element
            $('.installedCapacity').detach().appendTo($('.mm-dashboard-gauge.power .mm-dashboard-data'));
          }
        }
      }
    });
  }
});

//supporting functions
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