/* Insert Documentation Here
 *
 */
input_files = ["2013_December.csv","2013_November.csv"];
//all_results = [];

/* For multiple files
function parseData(createGraph) {

    for (var k = 0; k < input_files.length; k++) {

        Papa.parse(input_files[k], {
            download: true,
            complete: function(results) {
                all_results.push(results);
                if (all_results.length == input_files.length)
                {
                    console.log("Done");
                    console.log(all_results)
                    console.log(typeof all_results)
                    //createGraph(results.all_results)
                    createGraph(all_results)
                }
            }
        });
    }
}
*/

// For single file.. will use the above multi-file code
// after it is complete
function parseData(createGraph) {

    Papa.parse(input_files[0], {
        download: true,
        complete: function(results) {
            //all_results.push(results);
            console.log("Done");
            //console.log(all_results)
            //console.log(typeof all_results)
            //createGraph(results.all_results)
            createGraph(results.data)
        }
    });
}

/* For multiple files
function createGraph(all_results) {
    //Line Plot
    start_at = 10;
    index = [];
    wind_speed = [];
    var graphish = new Array(all_results.length);
    console.log(all_results)
    console.log(typeof all_results)    
    //vertical_location = [];

    for (var j = 0; j < all_results.length; j++) {
        
        data = all_results[j];
        console.log(data);

        for (var i = start_at; i < data.length; i++) {
            
            index.push(data[i][1]);
            wind_speed.push(data[i][7]);

            // blah = math.mean()
            
            var trace = {
                x: index,
                y: wind_speed,
                type: "scatter"
            };
            
        }

        graphish[j] = trace;
        
    }

    Plotly.newPlot("chart", graphish); 
  
}
*/ 

// For single file
function createGraph(data) {
    //Line Plot
    start_at = 10;
    index = [];
    wind_speed = [];
    //vertical_location = [];

    for (var i = start_at; i < data.length; i++) {
        
        index.push(data[i][1]);
        wind_speed.push(data[i][7]);
        
        var trace = {
            x: index,
            y: wind_speed,
            type: "scatter"

        };  
    }

    data = [trace];
    Plotly.newPlot("chart", data); 

}


parseData(createGraph)
//createGraph(all_results)