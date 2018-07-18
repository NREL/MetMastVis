$(document).ready(function(){
  testrequest();
});

//supporting functions
testrequest = function() {
  console.log("testing");
  $.ajax({
    url: 'https://s3-us-west-2.amazonaws.com/nrel-nwtc-metmast-uni/int/dt%3D2013-05/2013_05.csv',
    dataType: 'text',
    success: function(data) {
      document.getElementById("csv_data").innerHTML += data;
    },
    error: function (e) {
      document.getElementById("csv_data").innerHTML += e;
    }
  });
}