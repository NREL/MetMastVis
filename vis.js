//import "convert-csv-to-json";

// Insert Documentation Here
// test1
// 
//input_files = ["2013_January.csv","2013_February.csv","2013_March.csv","2013_April.csv","2013_May.csv","2013_June.csv","2013_July.csv","2013_August.csv","2013_September.csv","2013_October.csv","2013_November.csv","2013_December.csv"];
//input_files = ["2013_December.csv","2013_November.csv","2013_October.csv","2013_September.csv","2013_August.csv"];
//input_files = ["2013_December.csv","2013_November.csv"];
//input_files = ["2013_June.csv"];
//input_files = ["2017_January.csv"];

// input_files = [];
// year = 2017;
// for(var get_f = 0; get_f < monthnames().length; get_f++) {
//     input_files.push(year + "_" + monthnames()[get_f] + ".csv");
// }

// For multiple files (works for single also)
function parseData(createGraph, plot_type, month_list, basecolor, {category, abscissa, group_by, vertloc, range_length, format, row_select, col_select, curvefit, bins, nsector, bin_arrange} = {}) {

    var all_results = [];
    load.innerText = "Loading...";

    //for (var k = 0; k < input_files.length; k++) {
    for (var k = 0; k < month_list.length; k++) {
        Papa.parse(month_list[k], {
            download: true,

            complete: function(results) {
                all_results.push(results);

                if (all_results.length == month_list.length) {
                    createGraph(all_results, plot_type, month_list, basecolor, {category: category, abscissa: abscissa, group_by: group_by, vertloc: vertloc, range_length: range_length, format: format, rows: row_select, cols: col_select, curvefit: curvefit, nbins: bins, nsector: nsector, bin_arrange: bin_arrange})
                }

            }
        });   
    }

}

// Another method (probably quicker with no weird packages, but need a URL first)
// Plotly.d3.csv(rawDataURL, function(error, rawData))

// Calculate the domains of plot
function calcDomain_x(index, N) {

    var pad = 0.02;
    var width = 1 / N;
    
    return [
        index * (width) + pad / 2,
        (index + 1) * (width) - pad / 2
    ];

}

function calcDomain_y(index, N) {

    var pad = 0.02;
    var width = 1 / N;
    
    return [
        1 - ((index + 1) * (width) - pad / 2),
        1 - (index * (width) + pad / 2)
    ];

}

// Get cardinal directions for Wind Rose
function getCardinal(angle, nsector) {
    //easy to customize by changing the number of directions you have 
    
    var directions = 32;//nsector;
    
    var degree = 360 / directions;
    angle = angle + degree/2;
    
    if (angle >= 0 * degree && angle < 1 * degree)
        return "N";
    if (angle >= 1 * degree && angle < 2 * degree)
        return "NbE";
    if (angle >= 2 * degree && angle < 3 * degree)
        return "NNE";
    if (angle >= 3 * degree && angle < 4 * degree)
        return "NEbN";
    if (angle >= 4 * degree && angle < 5 * degree)
        return "NE";
    if (angle >= 5 * degree && angle < 6 * degree)
        return "NEbE";
    if (angle >= 6 * degree && angle < 7 * degree)
        return "ENE";
    if (angle >= 7 * degree && angle < 8 * degree)
        return "EbN";
    if (angle >= 8 * degree && angle < 9 * degree)
        return "E";
    if (angle >= 9 * degree && angle < 10 * degree)
        return "EbS";
    if (angle >= 10 * degree && angle < 11 * degree)
        return "ESE";
    if (angle >= 11 * degree && angle < 12 * degree)
        return "SEbE";
    if (angle >= 12 * degree && angle < 13 * degree)
        return "SE";
    if (angle >= 13 * degree && angle < 14 * degree)
        return "SEbS";
    if (angle >= 14 * degree && angle < 15 * degree)
        return "SSE";
    if (angle >= 15 * degree && angle < 16 * degree)
        return "SbE";
    if (angle >= 16 * degree && angle < 17 * degree)
        return "S";
    if (angle >= 17 * degree && angle < 18 * degree)
        return "SbW";
    if (angle >= 18 * degree && angle < 19 * degree)
        return "SSW";
    if (angle >= 19 * degree && angle < 20 * degree)
        return "SWbS";
    if (angle >= 20 * degree && angle < 21 * degree)
        return "SW";
    if (angle >= 21 * degree && angle < 22 * degree)
        return "SWbW";
    if (angle >= 22 * degree && angle < 23 * degree)
        return "WSW";
    if (angle >= 23 * degree && angle < 24 * degree)
        return "WbS";
    if (angle >= 24 * degree && angle < 25 * degree)
        return "W";
    if (angle >= 25 * degree && angle < 26 * degree)
        return "WbN";
    if (angle >= 26 * degree && angle < 27 * degree)
        return "WNW";
    if (angle >= 27 * degree && angle < 28 * degree)
        return "NWbW";
    if (angle >= 28 * degree && angle < 29 * degree)
        return "NW";
    if (angle >= 29 * degree && angle < 30 * degree)
        return "NWbN";
    if (angle >= 30 * degree && angle < 31 * degree)
        return "NNW";
    if (angle >= 31 * degree && angle < 32 * degree)
        return "NbW";
    
    return "N";
}

function titleCase(str) {

    return str.toLowerCase().split(' ').map(function(word) {
      return word.replace(word[0], word[0].toUpperCase());
    }).join(' ');

}

function plot_types() {

    var plot_type = ["Cumulative Profile", "Stability Profile", "Hourly", "Rose Figure", "Wind Direction Scatter", "Stability Wind Direction Scatter",
                     "Grouped Wind Direction Scatter", "Histogram", "Histogram by Stability", "Stacked Histogram by Stability",
                     "Monthly Stacked Histogram by Stability", "Normalized Histogram by Stability"];    

    return plot_type;

}

function vertloc_plots() {

    var vertloc_plots = ["Stability Profile", "Rose Figure", "Wind Direction Scatter", "Stability Wind Direction Scatter",
                         "Grouped Wind Direction Scatter", "Histogram", "Histogram by Stability", "Stacked Histogram by Stability",
                         "Normalized Histogram by Stability"];

    return vertloc_plots;

}

function one_month_plots() {

    var one_month_plots = ["Rose Figure", "Stability Wind Direction Scatter", "Histogram by Stability"];

    return one_month_plots;

}

function bin_plots() {

    var bin_plots = ["Rose Figure", "Grouped Wind Direction Scatter", "Histogram"];

    return bin_plots;

}    



function load_file(inputFiles) {

    // inputFiles.onchange = function(){
    //     var data = [];      // The results
    //     var pending = 0;    // How many outstanding operations we have
    
    //     Array.prototype.forEach.call(inputFiles.files, function(file, index) {

    //         var fr = new FileReader();
    //         fr.onload = function() {
    //             data[index] = fr.result;
    //             --pending;
    //             if (pending == 0) {
    //                 console.log(data);
    //                 // All requests are complete, you're done
    //             }
    //         }
    //         fr.readAsText(file);
    //         ++pending;
    //     });
    // }


    // function read_text(file_to_read) {

    //     return new Promise((resolve, reject) => {
    //         var fr = new FileReader();  
    //         fr.onload = resolve;  // CHANGE to whatever function you want which would eventually call resolve
    //         fr.readAsText(file_to_read);
    //     });

        // const readUploadedFileAsText = (file_to_read) => {
        //     const temporaryFileReader = new FileReader();
          
        //     return new Promise((resolve, reject) => {
        //         temporaryFileReader.onerror = () => {
        //             temporaryFileReader.abort();
        //                 reject(new DOMException("Problem parsing input file."));
        //         };
          
        //         temporaryFileReader.onload = () => {
        //             resolve(temporaryFileReader.result);
        //         };
        //         temporaryFileReader.readAsText(file_to_read);
        //     });
        // };

        // return readUploadedFileAsText();

        // fr.readAsText(file_to_read);

        // return function out() {
            
        //     return fr;

        // };

        // return out;

    // }

    //var fr = new FileReader();        
    //fr.onload = receivedText;
    // file.onchange = function(){
    //     var promise = Promise.resolve();
    //     file.files.map( file0 => promise.then(()=> read_text(file0)));
    //     promise.then(() => console.log(file0));
    // }
    //var test_this = read_text(file);

    // function receivedText() {

    // }

    //console.log(test_this);

    //return test_this;
    
}

function element_select() {

    var pre_data = document.getElementById("pre_select").value;

    if (pre_data === "yes") {

        document.getElementById("files_select_label").style.display = "inline";    
        document.getElementById("files_select").style.display = "inline";         

        var user_files = document.getElementsByTagName("input")[0]; 

        user_files.onchange = function(){

            var data = [];      
            var pending = 0;   
        
            Array.prototype.forEach.call(user_files.files, function(file, index) {

                var fr = new FileReader();
                fr.onload = function() {
                    data[index] = fr.result;
                    --pending;
                    if (pending == 0) {
   
                        load.innerText = "Loading...";

                        for (var streams = 0; streams < data.length; streams++) {
                            if (data[streams].charAt(0) === "[") {
                                graphish_data = data[streams];
                            } else {
                                layout_data = data[streams];
                            }
                        }

                        var graphish = JSON.parse(graphish_data);
                        var layout = JSON.parse(layout_data);

                        Plotly.newPlot("chart", graphish, layout)

                        load.innerText += "Done!";

                    }
                }
                fr.readAsText(file);
                ++pending;
            });

        }

    } else if (pre_data === "no") {

        var category, abscissa, group_by, vertloc, range_length, format, row_select, col_select, curvefit, bins, nsector, bin_arrange;
        category = abscissa = group_by = range_length = format = row_select = col_select = curvefit = nsector = bin_arrange = 0;    
        vertloc = bins = "";

        document.getElementById("plot_select").style.display = "inline"; 
        var plot_list = document.getElementById("plot_select");

        if (plot_list.options.length <= plot_types().length) {

            for (var plot = 0; plot < plot_types().length; plot++) {
                plot_list.options[plot_list.options.length] = new Option(plot_types()[plot],plot_types()[plot]);         
            }

        }  

        var plot_type = document.getElementById("plot_select").value;

        if (plot_type != 0) {

            if ((plot_type === "Normalized Histogram by Stability") | (plot_type === "Monthly Normalized Histogram by Stability")) {
    
                var category = 999;
    
            } else {
    
                document.getElementById("cat_select").style.display = "inline"; 
                var cat_list = document.getElementById("cat_select");
    
                if (cat_list.options.length <= categories_to_keep().length) {
    
                    for (var cat = 0; cat < categories_to_keep().length; cat++) {
                        cat_list.options[cat_list.options.length] = new Option(categories_to_keep()[cat],categories_to_keep()[cat]);         
                    }
    
                }  
    
                var category = document.getElementById("cat_select").value;
    
            }
    
            if (category != 0) {
    
                if (plot_type === "Grouped Wind Direction Scatter") {
                    
                    document.getElementById("abscissa_select").style.display = "inline"; 
                    var abscissa_list = document.getElementById("abscissa_select");
    
                    if (abscissa_list.options.length <= categories_to_keep().length) {
    
                        for (var cat = 0; cat < categories_to_keep().length; cat++) {
                            abscissa_list.options[abscissa_list.options.length] = new Option(categories_to_keep()[cat],categories_to_keep()[cat]);         
                        }
        
                    }  
        
                    var abscissa = document.getElementById("abscissa_select").value;
    
                    if (abscissa != 0) {
    
                        document.getElementById("group-by_select").style.display = "inline"; 
                        var group_by_list = document.getElementById("group-by_select");
    
                        if (group_by_list.options.length <= categories_to_keep().length) {
    
                            for (var cat = 0; cat < categories_to_keep().length; cat++) {
                                group_by_list.options[group_by_list.options.length] = new Option(categories_to_keep()[cat],categories_to_keep()[cat]);         
                            }
            
                        }  
            
                        var group_by = document.getElementById("group-by_select").value;
    
                    }
    
                }
    
                if (((plot_type === "Grouped Wind Direction Scatter") && (abscissa != 0) && (group_by != 0)) | (plot_type != "Grouped Wind Direction Scatter")) {
    
                    if (vertloc_plots().indexOf(plot_type) === -1) {
    
                        vertloc = 999;
                    
                    } else {
    
                        document.getElementById("vertloc_select").style.display = "inline"; 
                        var vertloc = document.getElementById("vertloc_select").value;
        
                    }
    
                    if (vertloc != "") {
    
                        if (one_month_plots().indexOf(plot_type) === -1) {
    
                            document.getElementById("range_length_select").style.display = "inline"; 
                            var range_length = document.getElementById("range_length_select").value;
    
                        } else {
                            
                            range_length = "one_month";
    
                        }
    
                        if (range_length === "one_month") {
    
                            document.getElementById("month_select").style.display = "inline";
                            var select_month = document.getElementById("month_select");
    
                            if (select_month.options.length <= monthnames().length) {
    
                                for (var mon = 0; mon < monthnames().length; mon++) {
                                    select_month.options[select_month.options.length] = new Option(monthnames()[mon],monthnames()[mon]);         
                                }
    
                            }          

                            if (select_month.value != 0) {

                                // if (plot_type != "Histogram") {

                                // } else {

                                // }

                                document.getElementById("year_select").style.display = "inline";

                            }
                                
                            var month_final = document.getElementById("month_select").value;
                            var year_final = document.getElementById("year_select").value;
    
                            if ((month_final != 0) && (year_final != 0)) {
    
                                var input_file_string = year_final + "_" + month_final + ".csv";
                                var input_file_list = [];
                                input_file_list.push(input_file_string);
    
                                if (plot_type === "Histogram") {
    
                                    document.getElementById("fit_select").style.display = "inline";
                                    var curvefit = document.getElementById("fit_select").value;
    
                                    if (curvefit != 0) {
    
                                        document.getElementById("bin_select").style.display = "inline";
                                        var bins = document.getElementById("bin_select").value;
    
                                        if (bins != "") {
    
                                            document.getElementById("color_select").style.display = "inline";
                                            
                                            // Histogram can't take certain colors for single month
                                            var rm  = document.getElementById("color_select");
    
                                            if (rm.length > 1 + Object.keys(get_nrelcolors()).length) {
    
                                                rm.remove(rm.length-1);
    
                                            }
    
                                            document.getElementById("start").style.display = "inline"; 
                                            document.getElementById("next").style.display = "none";
                                            var basecolor = document.getElementById("color_select").value;
    
                                            if (basecolor != 0) {
    
                                                parseData(createGraph, plot_type, input_file_list, basecolor, {category: category, abscissa: abscissa, group_by: group_by, vertloc: vertloc, range_length: range_length, format: format, row_select: row_select, col_select: col_select, curvefit: curvefit, bins: bins, nsector: nsector, bin_arrange: bin_arrange});
    
                                            }
    
                                        }
    
                                    }
                                
                                } else {
    
                                    if (bin_plots().indexOf(plot_type) != -1) {

                                        document.getElementById("bin_select").style.display = "inline";
                                        var bins = document.getElementById("bin_select").value;
                                    
                                        if (bins != "") {
                                    
                                            if (plot_type === "Rose Figure") {
                                    
                                                document.getElementById("sector_select").style.display = "inline";
                                                var nsector = document.getElementById("sector_select").value;
                                    
                                                if (nsector != 0) {
                                    
                                                    document.getElementById("bin-arrange_select").style.display = "inline";
                                                    var bin_arrange = document.getElementById("bin-arrange_select").value;
                                    
                                                }
                                    
                                            }
                                    
                                        }
                                    
                                    }
                                    
                                    if (((plot_type === "Rose Figure") && (bin_arrange != 0)) | (bin_plots().indexOf(plot_type) === -1) | ((bin_plots().indexOf(plot_type) != -1) && (bins != ""))) {
                                    
                                        document.getElementById("color_select").style.display = "inline";
                                        document.getElementById("start").style.display = "inline"; 
                                        document.getElementById("next").style.display = "none";
                                        var basecolor = document.getElementById("color_select").value;
                                    
                                        if (basecolor != 0) {  
                                    
                                            parseData(createGraph, plot_type, input_file_list, basecolor, {category: category, abscissa: abscissa, group_by: group_by, vertloc: vertloc, range_length: range_length, format: format, row_select: row_select, col_select: col_select, curvefit: curvefit, bins: bins, nsector: nsector, bin_arrange: bin_arrange});
                                    
                                        }
    
                                    }
    
                                }
    
                            }
    
                        }
    
                        if (range_length === "multiple") {

                            document.getElementById("start_month_select").style.display = "inline"; 

                            if (document.getElementById("start_month_select").value != 0) {
                            
                                document.getElementById("start_year_select").style.display = "inline"; 
                            
                            }
                            
                            if (document.getElementById("start_year_select").value != 0) {
                            
                                document.getElementById("end_month_select").style.display = "inline"; 
                            
                            }
                                
                            if (document.getElementById("end_month_select").value != 0) {
                            
                                document.getElementById("end_year_select").style.display = "inline"; 
                            
                            }
                            
                            var select_start_month = document.getElementById("start_month_select");
                            var select_end_month = document.getElementById("end_month_select");
                            
                            if ((select_start_month.options.length <= monthnames().length) && (select_end_month.options.length <= monthnames().length)) {
                            
                                for (var mon = 0; mon < monthnames().length; mon++) {
                                    select_start_month.options[select_start_month.options.length] = new Option(monthnames()[mon],monthnames()[mon]);
                                    select_end_month.options[select_end_month.options.length] = new Option(monthnames()[mon],monthnames()[mon]);            
                                }
                            
                            }
                            
                            var start_month = document.getElementById("start_month_select").value;
                            var start_year = document.getElementById("start_year_select").value;
                            var end_month = document.getElementById("end_month_select").value;
                            var end_year = document.getElementById("end_year_select").value;
                            
                            if ((start_month != 0) && (start_year != 0) && (end_month != 0) && (end_year != 0)) {
                            
                                var month_list = get_file_range(String(start_month), parseInt(start_year), String(end_month), parseInt(end_year));
                                console.log(month_list);
                            
                                if (plot_type === "Cumulative Profile") {

                                    document.getElementById("color_select").style.display = "inline";
                                    document.getElementById("start").style.display = "inline"; 
                                    document.getElementById("next").style.display = "none";
                                    var basecolor = document.getElementById("color_select").value;
                            
                                    if (basecolor != 0) {
                            
                                        parseData(createGraph, plot_type, month_list, basecolor, {category: category, abscissa: abscissa, group_by: group_by, vertloc: vertloc, range_length: range_length, format: format, row_select: row_select, col_select: col_select, curvefit: curvefit, bins: bins, nsector: nsector, bin_arrange: bin_arrange});
                            
                                    }
                            
                                } else {
                            
                                    document.getElementById("format_select").style.display = "inline";
                                    var format = document.getElementById("format_select").value;
                                
                                    // Re-emerge everything
                                    if (format != 0) {
                            
                                        // everything else here
                                        if (format === "grid") {

                                            document.getElementById("row_select").style.display = "inline";
                   
                                            var combos = get_grid_format(month_list.length);
                                            var select_row = document.getElementById("row_select");
                                            var select_col = document.getElementById("col_select");
                                            
                                            var combo_list = [];
                                            for (var c = 0; c < Object.keys(combos).length; c++) {
                                                combo_list.push(combos[Object.keys(combos)[c]][0]);
                                            }
        
                                            if ((select_row.options.length <= Object.keys(combos).length) && (select_col.options.length <= Object.keys(combos).length)) {
                                                
                                                for (var c = 0; c < Object.keys(combos).length; c++) {
                                                    select_row.options[select_row.options.length] = new Option("" + combos[Object.keys(combos)[c]][0], combos[Object.keys(combos)[c]][0]);
                                                }
        
                                            }
                                            
                                            n1r = document.getElementsByName("row_select");
                                            n2r = Array.prototype.slice.call(n1r);
                                            n3r = n2r[0].childNodes.length;
        
                                            n1c = document.getElementsByName("col_select");
                                            n2c = Array.prototype.slice.call(n1c);
                                            n3c = n2c[0].childNodes.length;
        
                                            if ((parseInt(select_row.value) != 0) && (n3r <= (3 + combo_list.length)) && (n3c <= 3)) {
        
                                                var group_in = 0;
                                                for (var gi = 0; gi < Object.keys(combos).length; gi++) {
        
                                                    if (combos[Object.keys(combos)[gi]][0] === parseInt(select_row.value)) {
                                                        group_in = gi;
                                                        select_col.options[select_col.options.length] = new Option("" + combos[""+group_in][1], combos[""+group_in][1]);
                                                    }
        
                                                }
                                                
                                            }

                                            var row_select = document.getElementById("row_select").value;

                                            if (row_select != 0) {

                                                document.getElementById("col_select").style.display = "inline";
                                                var col_select = document.getElementById("col_select").value;

                                                if (col_select != 0) {

                                                    if (bin_plots().indexOf(plot_type) === -1) {
            
                                                        var bins = 999;
    
                                                    } else {
    
                                                        document.getElementById("bin_select").style.display = "inline";
                                                        var bins = document.getElementById("bin_select").value;
    
                                                    }
    
                                                    if (bins != "") {
                
                                                        document.getElementById("color_select").style.display = "inline";
                                                        document.getElementById("start").style.display = "inline"; 
                                                        document.getElementById("next").style.display = "none";
                                                        var basecolor = document.getElementById("color_select").value;
    
                                                        if (basecolor != 0) {
                    
                                                            parseData(createGraph, plot_type, month_list, basecolor, {category: category, abscissa: abscissa, group_by: group_by, vertloc: vertloc, range_length: range_length, format: format, row_select: row_select, col_select: col_select, curvefit: curvefit, bins: bins, nsector: nsector, bin_arrange: bin_arrange});
                                                        }
    
                                                    }

                                                }

                                            }
                                            
                                        } else {

                                            if (bin_plots().indexOf(plot_type) === -1) {
        
                                                var bins = 999;
        
                                            } else {
        
                                                document.getElementById("bin_select").style.display = "inline";
                                                var bins = document.getElementById("bin_select").value;
                
                                            }

                                            if (bins != "") {
        
                                                document.getElementById("color_select").style.display = "inline";
                                                document.getElementById("start").style.display = "inline"; 
                                                document.getElementById("next").style.display = "none";
                                                var basecolor = document.getElementById("color_select").value;
          
                                                if (basecolor != 0) {
                
                                                    parseData(createGraph, plot_type, month_list, basecolor, {category: category, abscissa: abscissa, group_by: group_by, vertloc: vertloc, range_length: range_length, format: format, row_select: row_select, col_select: col_select, curvefit: curvefit, bins: bins, nsector: nsector, bin_arrange: bin_arrange});
        
                                                }

                                            }
                        
                                        }

                                    }
                                            
                                }
        
                            }
        
                        }

                    }
    
                }
    
            }
    
        }
    
    }

}

function get_file_range(start_month, start_year, end_month, end_year) {

    var file_list = [];
    var mn = monthnames();

    var start_ind = mn.indexOf(start_month);
    var end_ind = mn.indexOf(end_month);
    var total_months = ((end_year - start_year) * 12) + (end_ind - start_ind);
    
    var year_ind = start_year;
    var month = start_month;
    
    var month_ind = mn.indexOf(start_month);

    for (var im = 0; im < total_months; im++) {
        month_ind = month_ind % 12;
        
        if ((month_ind === 0) && (im != 0)) {
            year_ind += 1;
        }

        file_list.push(year_ind + "_" + mn[month_ind] + ".csv");
        month_ind += 1;
    }
    
    file_list.push(end_year + "_" + end_month + ".csv");

    return file_list;

}

function get_grid_format(graph_total) {

    var factors = [];
    var quotient = 0;
  
    for (var i = 1; i <= graph_total; i++){
        quotient = graph_total/i;
  
        if (quotient === Math.floor(quotient)){
            factors.push(i); 
        }

    }

    if ((factors.length === 2) && (graph_total > 3)) {

        var quotient = 0;
      
        for (var i = 1; i <= (graph_total+1); i++){
            quotient = (graph_total+1)/i;
      
            if (quotient === Math.floor(quotient) && (i != 1) & (i != graph_total+1)) {
                factors.push(i); 
            }
    
        }

    }

    var factor_dict = {};
    factors.sort(function(a, b) {return a - b;});

    for (var f = 0; f < factors.length/2; f++) {
        factor_dict[""+(f*2)] = [factors[f],factors[factors.length-f-1]];
        factor_dict[""+((f*2)+1)] = [factors[f],factors[factors.length-f-1]].reverse();
    }

    return factor_dict;

}

// For multiple files (works for single also) 
function createGraph(all_results, plot_type, new_files, basecolor, {category, abscissa, group_by, vertloc, range_length, format, rows, cols, curvefit, nbins, nsector, bin_arrange} = {}) { 

    var rows = parseInt(rows);
    var cols = parseInt(cols);
    var nbins = parseInt(nbins);
    var nsector = parseInt(nsector);

    var graphish, layout;

    if (plot_type === "Cumulative Profile") {

        [graphish, layout] = cumulative_prof(all_results, new_files, category, basecolor);

    }

    if (plot_type === "Stability Profile") {

        if (range_length === "one_month") {
            [graphish, layout] = stab_prof(all_results, new_files, category, vertloc, basecolor);
        }
        if (range_length === "multiple") {
            [graphish, layout] = monthly_stab_prof(all_results, new_files, category, vertloc, basecolor, format, {rows: rows, cols: cols});
        }

    }

    if (plot_type === "Hourly") {

        if (range_length === "one_month") {
            [graphish, layout] = hourly(all_results, new_files, category, basecolor);
        }
        if (range_length === "multiple") {
            [graphish, layout] = monthly_hourly(all_results, new_files, category, basecolor, format, rows, cols);
        }

    }

    if (plot_type === "Rose Figure") {

        [graphish, layout] = rose_fig(all_results, new_files, category, vertloc, basecolor, nbins, bin_arrange, nsector);

    }

    if (plot_type === "Wind Direction Scatter") {

        if (range_length === "one_month") {
            [graphish, layout] = winddir_scatter(all_results, new_files, category, vertloc, basecolor);
        }
        if (range_length === "multiple") {
            [graphish, layout] = monthly_winddir_scatter(all_results, new_files, category, vertloc, basecolor, format, rows, cols);
        }

    }

    if (plot_type === "Stability Wind Direction Scatter") {

        [graphish, layout] = stab_winddir_scatter(all_results, new_files, category, vertloc, basecolor);        

    }

    if (plot_type === "Grouped Wind Direction Scatter") {

        if (range_length === "one_month") {
            [graphish, layout] = groupby_winddir_scatter(all_results, new_files, category, abscissa, group_by, vertloc, basecolor, nbins);
        }
        if (range_length === "multiple") {
            [graphish, layout] = monthly_groupby_winddir_scatter(all_results, new_files, category, abscissa, group_by, vertloc, basecolor, nbins, format, rows, cols);
        }

    }

    if (plot_type === "Histogram") {

        if (range_length === "one_month") {
            [graphish, layout] = hist(all_results, new_files, category, vertloc, basecolor, nbins, curvefit);
        }
        if (range_length === "multiple") {
            [graphish, layout] = monthly_hist(all_results, new_files, category, vertloc, basecolor, nbins, format, rows, cols);
        }

    }

    if (plot_type === "Histogram by Stability") {
        
        [graphish, layout] = hist_by_stab(all_results, new_files, category, vertloc, basecolor, nbins);

    }

    if (plot_type === "Stacked Histogram by Stability") {

        if (range_length === "one_month") {

            [graphish, layout] = stacked_hist_by_stab(all_results, new_files, category, vertloc, basecolor);
        }
        if (range_length === "multiple") {
            [graphish, layout] = monthly_stacked_hist_by_stab(all_results, new_files, category, vertloc, basecolor, format, rows, cols);
        }

    }

    if (plot_type === "Normalized Histogram by Stability") {

        if (range_length === "one_month") {
            [graphish, layout] = norm_hist_by_stab(all_results, new_files, vertloc, basecolor);
        }

        if (range_length === "multiple") {
            [graphish, layout] = monthly_norm_hist_by_stab(all_results, new_files, vertloc, basecolor, format, rows, cols);
        }

    }

    // console.log(graphish);
    // console.log(layout);

    Plotly.newPlot("chart", graphish, layout)
    load.innerText += "Done!";

    document.getElementById("save").style.display = "inline";
    state_saver.changeState([graphish,layout]);

}
    
// Reload the page if required
function reloadPage() {

    location.reload();

}

// Save state 

var state_saver = (function () {
    var state; 

    var pub = {};

    pub.changeState = function (newstate) {
        state = newstate;
    };

    pub.getState = function() {
        return state;
    }

    return pub; 
}());

function download(filename, text) {

    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);

}

function save_state() {

    var plotly_info = state_saver.getState();
    var graphish = plotly_info[0];
    var layout = plotly_info[1]

    console.log(graphish);
    console.log(layout);

    var json_graphish = JSON.stringify(graphish);
    var json_layout = JSON.stringify(layout);

    var date_obj = new Date();
    var time_info = date_obj.getTime();

    var name_graphish = "graphish_" + time_info + ".json";
    var name_layout = "layout_" + time_info + ".json";

    // Harder and less dynamic
    // var fs = require("fs");
    // fs.writeFile("graphish_"+time_info+".json", json_graphish, "utf8", callback);
    // fs.writeFile("layout_"+time_info+".json", json_layout, "utf8", callback);

    download(name_graphish, json_graphish);
    download(name_layout, json_layout);

}

//parseData(createGraph,input_files)

///////////////////////////////////////////////////////////////

function process_data(all_results, j) {

    // Convert CSV to JSON ... need to create dynamic labels in
    // place of 7 and 10
    var arrays = all_results[j].data;
    var keys = arrays[7];
    var values = arrays.slice(10);

    // To display the data columns and values
    // console.log(keys);
    // console.log(values);

    var object1 = new Object();
    // remove -1 in code with QC data
    for (k = 0; k < (keys.length-1); k++) {
        var new_values = [];
        for (v = 0; v < values.length; v++) {
            new_values.push(values[v][k]);
        }
        if (Object.keys(object1).indexOf(keys[k]) == -1) {
            object1[keys[k]] = new_values;
        } else {
            object1[keys[k]+"_adv"] = new_values;
        }
    }  
    
    return object1;

}

// Cumulative and Monthly Profile
// Any-month

function cumulative_prof(all_results, input_files, category, basecolor) {
    // default: -,-,-,span

    // Set up data
    var graphish = []; 
    var max_x = -Infinity;
    var min_x = Infinity;
    var margin = 0.25;
    
    for (var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j);
        var object2 = edit_met_data(object1);
        var cate_info = get_catinfo(object2);

        var colnames, vertlocs, ind;
        [colnames, vertlocs, ind] = get_vertical_locations(cate_info["columns"][category]) 

        var plotdat = [];
        for (var height = 0; height < colnames.length; height++) {

            var array_temp = [];
            array_temp = object2[colnames[height]];
            var total = 0;
            var test_mat = [];
            for (var i = 0; i < array_temp.length; i += 1) {
                // until there is a faster way to remove these
                if ((parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null)) {
                    test_mat.push(array_temp[i]);
                    total += parseFloat(array_temp[i]);
                }
            }
            plotdat.push(total / (test_mat.length));  

        }
        var maxdat = plotdat.filter(Boolean);

        if (Math.max(...maxdat) > max_x) {
            max_x = Math.max(...maxdat);
        }

        if (Math.min(...maxdat) < min_x) {
            min_x = Math.min(...maxdat);
        }

        if (input_files.length > 1) {

            var colors = get_colors(input_files.length, {basecolor: basecolor});

        } else {

            var colors = get_nrelcolors()[basecolor];

        }

        var trace = {
            x: plotdat,
            y: vertlocs,
            type: "scatter",
            name: input_files[j].split("_")[1].split(".")[0],
            connectgaps: true,
            line: {
                color: colors[j]
            }
        };

        graphish[j] = trace;
    }

    // Set the string labels
    var xstring = "$$" + cate_info["labels"][category] + "$$";
    var ystring = "$$ \\text{Probe Height} [m] $$";
    // need to add $$ for LaTeX to process
    var title_string = "$$ \\text{" + titleCase(category) + " vs. } " + ystring.replace("$$","") + " $$"; 

    var diff = max_x - min_x;

    var layout = {
        font: {
            size: 15
        },
        title: title_string,
        yaxis: {
            title: ystring
        },
        xaxis: {
            title: xstring,
            range: [min_x-margin*diff, max_x+margin*diff]
        },
        hovermode: "closest"
    };

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Stability Profile
// 1-month

function stab_prof(all_results, input_files, category, vertloc, basecolor) {
    // default: -,-,-,80,red

    // Set up data
    var graphish = []; 
    var max_x = -Infinity;
    var min_x = Infinity;
    var margin = 0.25;

    for (var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j);
        var object2 = edit_met_data(object1);

        [stab_conds, stab_cats, metdat] = flag_stability(object2);
        var cate_info = get_catinfo(metdat);
        console.log(cate_info["columns"]);
        console.log(Object.keys(cate_info["columns"]));

        var stab, stabloc, ind;
        [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
        var stabconds = get_stabconds();
        var colors = get_colors(stabconds.length, {basecolor: basecolor});

        // Extract vertical locations of data from variable names
        var a, vertlocs, iax;
        [a, vertlocs, iax] = get_vertical_locations(cate_info["columns"][category]);
        
        for (var cond = 0; cond < stabconds.length; cond++) {

            var plotdat = [];
            for (var ii = 0; ii < cate_info["columns"][category].length; ii++) {
                
                var array_temp = [];
                array_temp = metdat[cate_info["columns"][category][ii]];
                var total = 0;
                var empty = 0;
                var test_mat = [];
                
                for (var i = 0; i < array_temp.length; i += 1) {
                    // until there is a faster way to remove these                        
                    if ((metdat[stab][i] === stabconds[cond]) && (parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null)) {
                        empty += 1;
                        test_mat.push(array_temp[i]);
                        total += parseFloat(array_temp[i]);
                    }
                }
                plotdat.push(total / (test_mat.length));  

            }
            var maxdat = plotdat.filter(Boolean);

            if (Math.max(...maxdat) > max_x) {
                max_x = Math.max(...maxdat);
            }

            if (Math.min(...maxdat) < min_x) {
                min_x = Math.min(...maxdat);
            }

            var trace = {
                x: plotdat,
                y: vertlocs,
                mode: "lines+markers",
                marker: {
                    color: colors[cond]
                },
                type: "scatter",
                connectgaps: true,
                name: stabconds[cond],
            };
            graphish = graphish.concat(trace);

        }

    }

    // set the string labels
    xstring = "$$" + cate_info["labels"][category] + "$$";
    ystring = "$$ \\text{Probe Height} [m] $$";
    // need to add $$ for LaTeX to process
    title_string = "$$ \\text{" + titleCase(category) + " vs. } " + ystring.replace("$$","") + " $$"; 

    var diff = max_x - min_x;

    var layout = {
        font: {
            size: 15
        },
        title: title_string,
        yaxis: {
            title: ystring
        },
        xaxis: {
            title: xstring, 
            range: [min_x-margin*diff, max_x+margin*diff]
        },
        hovermode: "closest"
    };

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Monthly Stability Profile
// Any-month

function monthly_stab_prof(all_results, input_files, category, vertloc, basecolor, format, {rows, cols} = {}) {
    // default: -,-,-,80,red,-,-,-

    // Set up data
    var graphish = []; 
    var max_x = -Infinity;
    var min_x = Infinity;
    var layout = {annotations: []};
    var margin = 0.25;

    for (var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j);
        var object2 = edit_met_data(object1);

        var stab_conds, stab_cats, metdat;
        [stab_conds, stab_cats, metdat] = flag_stability(object2);
        var cate_info = get_catinfo(metdat);

        var stab, stabloc, ind;
        [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
        var stabconds = get_stabconds();
        var colors = get_colors(stabconds.length, {basecolor: basecolor});

        // Extract vertical locations of data from variable names
        var a, vertlocs, iax;
        [a, vertlocs, iax] = get_vertical_locations(cate_info["columns"][category]);
        
        for (var cond = 0; cond < stabconds.length; cond++) {

            var plotdat = [];
            for (var ii = 0; ii < cate_info["columns"][category].length; ii++) {
                
                var array_temp = [];
                array_temp = metdat[cate_info["columns"][category][ii]];
                var total = 0;
                var empty = 0;
                var test_mat = [];
                
                for (var i = 0; i < array_temp.length; i += 1) {
                    // until there is a faster way to remove these                        
                    if ((metdat[stab][i] === stabconds[cond]) && (parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null)) {
                        empty += 1;
                        test_mat.push(array_temp[i]);
                        total += parseFloat(array_temp[i]);
                    }
                }
                plotdat.push(total / (test_mat.length));  

            }
            var maxdat = plotdat.filter(Boolean);

            if (Math.max(...maxdat) > max_x) {
                max_x = Math.max(...maxdat);
            }

            if (Math.min(...maxdat) < min_x) {
                min_x = Math.min(...maxdat);
            }

            if ((format === "dropdown") | (format === "slider")) {

                var trace = {
                    x: plotdat,
                    y: vertlocs,
                    mode: "lines+markers",
                    marker: {
                        color: colors[cond]
                    },
                    type: "scatter",
                    connectgaps: true,
                    name: stabconds[cond],
                    visible: j === 0
                };
                graphish = graphish.concat(trace);

            }

            if (format === "grid") {

                var trace = {
                    x: plotdat,
                    y: vertlocs,
                    xaxis: "x" + (j+2),
                    yaxis: "y" + (j+2),
                    mode: "lines+markers",
                    marker: {
                        color: colors[cond]
                    },
                    type: "scatter",
                    connectgaps: true,
                    name: stabconds[cond],
                    showlegend: j ===0
                };
                graphish = graphish.concat(trace);

            }
        }

        if (format === "grid") {

            layout["yaxis" + (j+2)] = {
                domain: calcDomain_y(Math.floor(j/cols),rows)
            };

            layout["xaxis" + (j+2)] = {
                domain: calcDomain_x(j%cols,cols)
            };

        }

    }

    if ((format === "dropdown") | (format === "slider")) {

        buttons = [];
        for (var j = 0; j < input_files.length; j++){
            // This array decides when to display a certain trace
            false_array = [];
            for(var i = 0; i < input_files.length; i++) {
                if (i == j) {
                    for(var sc1 = 0; sc1 < stabconds.length; sc1++) {
                        false_array.push(true);
                    }    
                } else {
                    for(var sc2 = 0; sc2 < stabconds.length; sc2++) {
                        false_array.push(false);
                    }
                }  
            }
            buttons.push({method: 'restyle', args: ['visible', false_array], label: input_files[j].replace(/_|.csv/g," ")});
        }
    }

    if (format === "slider") {

        steps = buttons;

    }

    // set the string labels
    xstring = "$$" + cate_info["labels"][category] + "$$";
    ystring = "$$ \\text{Probe Height} [m] $$";
    // need to add $$ for LaTeX to process
    title_string = "$$ \\text{" + titleCase(category) + " vs. } " + ystring.replace("$$","") + " $$"; 

    var diff = max_x - min_x;

    if (format === "slider") {
        
        var layout = {
            font: {
                size: 15
            },
            sliders: [{
                pad: {t: 30},
                len: ((input_files.length)/12),
                steps: steps
            }],
            title: title_string,
            yaxis: {
                title: ystring
            },
            xaxis: {
                title: xstring, 
                range: [min_x-margin*diff, max_x+margin*diff]
            },
            hovermode: "closest"
        };

    }

    if (format === "grid") {

        layout["font"] = {size: 15};
        layout["title"] = title_string;
        layout["hovermode"] = "closest";

        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [min_x-margin*diff, max_x+margin*diff];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 15}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 15}}); 

        layout["xaxis"] = {title: xstring, range: [0, 1.1*max_x]};

    }

    if (format === "dropdown") {

        var layout = {
            font: {
                size: 15
            },
            title: title_string,
            yaxis: {
                title: ystring
            },
            xaxis: {
                title: xstring, 
                range: [min_x-margin*diff, max_x+margin*diff]
            },
            updatemenus: [{
                y: 1, 
                yanchor: "top", 
                buttons: buttons
            }],
            hovermode: "closest"
        }

    }

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Hourly Plot
// 1-month

function hourly(all_results, input_files, category, basecolor) {
    // default: -,-,-,80,span

    // Set up data
    var graphish = []; 
    var max_y = -Infinity;
    var min_y = Infinity;
    var layout = {annotations: []};
    var margin = 0.25;

    for (var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j);
        var object2 = edit_met_data(object1);

        var stab_conds, stab_cats, metdat;
        [stab_conds, stab_cats, metdat] = flag_stability(object2);

        var cate_info = get_catinfo(metdat);
        var heights = cate_info["columns"][category].reverse();
        var colors = get_colors(heights.length, {basecolor: basecolor, reverse: true});

        var colnames, vertlocs, ind;
        [colnames, vertlocs, ind] = get_vertical_locations(heights, {reverse: true});

        for (var ii = 0; ii < heights.length; ii++) {

            var plotdat = [];
            for (var hour = 0; hour < 24; hour++) {

                var array_temp = [];
                array_temp = metdat[heights[ii]];
                var total = 0;
                var test_mat = [];
                
                for (var i = 0; i < array_temp.length; i += 1) {
                    // until there is a faster way to remove these                        
                    if ((parseInt(metdat["Date"][i].split(" ")[1].split(":")[0]) === hour) && (parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null)) {
                        test_mat.push(array_temp[i]);
                        total += parseFloat(array_temp[i]);
                    }
                }
                plotdat.push(total / (test_mat.length));  

                var maxdat = plotdat.filter(Boolean);

                if (Math.max(...maxdat) > max_y) {
                    max_y = Math.max(...maxdat);
                }

                if (Math.min(...maxdat) < min_y) {
                    min_y = Math.min(...maxdat);
                }

            }

            var trace = {
                x: [...Array(24).keys()],
                y: plotdat,
                mode: "lines+markers",
                marker: {
                    color: colors[ii]
                },
                type: "scatter",
                connectgaps: true,
                name: vertlocs[ii] + "m",
            };
            graphish = graphish.concat(trace);

        }
    }
    // set the string labels
    xstring = "$$ \\text{Time} [hour] $$";
    ystring = "$$" + cate_info["labels"][category] + "$$";
    // need to add $$ for LaTeX to process
    title_string = "$$ " + " \\text{Time[hour] vs. "+ titleCase(category) + "} $$";
        
    var diff = max_y - min_y;

    var layout = {
        font: {
            size: 15
        },
        title: title_string,
        yaxis: {
            title: ystring,
            range: [min_y-margin*diff, max_y+margin*diff]
        },
        xaxis: {
            title: xstring, 
            range: [0, 24]
        }
    };

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Monthly Hourly Plot
// Any-month

function monthly_hourly(all_results, input_files, category, basecolor, format, rows, cols) {
    // default: -,-,-,80,span,-,-,-

    // Set up data
    var graphish = []; 
    var max_y = -Infinity;
    var min_y = Infinity;
    var layout = {annotations: []};
    var margin = 0.25;

    for (var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j);
        var object2 = edit_met_data(object1);

        var stab_conds, stab_cats, metdat;
        [stab_conds, stab_cats, metdat] = flag_stability(object2);

        var cate_info = get_catinfo(metdat);
        var heights = cate_info["columns"][category].reverse();
        var colors = get_colors(heights.length, {basecolor: basecolor, reverse: true});

        var colnames, vertlocs, ind;
        [colnames, vertlocs, ind] = get_vertical_locations(heights, {reverse: true});

        for (var ii = 0; ii < heights.length; ii++) {

            var plotdat = [];
            for (var hour = 0; hour < 24; hour++) {

                var array_temp = [];
                array_temp = metdat[heights[ii]];
                var total = 0;
                var test_mat = [];
                
                for (var i = 0; i < array_temp.length; i += 1) {
                    // until there is a faster way to remove these                        
                    if ((parseInt(metdat["Date"][i].split(" ")[1].split(":")[0]) === hour) && (parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null)) {
                        test_mat.push(array_temp[i]);
                        total += parseFloat(array_temp[i]);
                    }
                }
                plotdat.push(total / (test_mat.length));  

                var maxdat = plotdat.filter(Boolean);

                if (Math.max(...maxdat) > max_y) {
                    max_y = Math.max(...maxdat);
                }

                if (Math.min(...maxdat) < min_y) {
                    min_y = Math.min(...maxdat);
                }

            }

            if ((format === "dropdown") | (format === "slider")) {

                var trace = {
                    x: [...Array(24).keys()],
                    y: plotdat,
                    mode: "lines+markers",
                    marker: {
                        color: colors[ii]
                    },
                    type: "scatter",
                    connectgaps: true,
                    name: vertlocs[ii] + "m",
                    visible: j === 0
                };
                graphish = graphish.concat(trace);

            }

            if (format === "grid") {

                var trace = {
                    x: [...Array(24).keys()],
                    y: plotdat,
                    xaxis: "x" + (j+2),
                    yaxis: "y" + (j+2),
                    mode: "lines+markers",
                    marker: {
                        color: colors[ii]
                    },
                    type: "scatter",
                    connectgaps: true,
                    name: vertlocs[ii] + "m",
                    showlegend: j ===0
                };
                graphish = graphish.concat(trace);

            }
        }

        if (format === "grid") {

            layout["yaxis" + (j+2)] = {
                domain: calcDomain_y(Math.floor(j/cols),rows)
            };

            layout["xaxis" + (j+2)] = {
                domain: calcDomain_x(j%cols,cols)
            };

        }

    }

    if ((format === "dropdown") | (format === "slider")) {

        buttons = [];
        for (var j = 0; j < input_files.length; j++){
            // This array decides when to display a certain trace
            false_array = [];
            for(var i = 0; i < input_files.length; i++) {
                if (i == j) {
                    for(var sc1 = 0; sc1 < heights.length; sc1++) {
                        false_array.push(true);
                    }    
                } else {
                    for(var sc2 = 0; sc2 < heights.length; sc2++) {
                        false_array.push(false);
                    }
                }  
            }
            buttons.push({method: 'restyle', args: ['visible', false_array], label: input_files[j].replace(/_|.csv/g," ")});
        }
    }

    if (format === "slider") {

        steps = buttons;

    }

    // set the string labels
    xstring = "$$ Time [hour] $$";
    ystring = "$$" + cate_info["labels"][category] + "$$";
    // need to add $$ for LaTeX to process
    title_string = "$$ " + " \\text{Time[hour] vs. "+ titleCase(category) + "} $$";

    var diff = max_y - min_y;

    if (format === "slider") {
        
        var layout = {
            font: {
                size: 15
            },
            sliders: [{
                pad: {t: 30},
                len: ((input_files.length)/12),
                steps: steps
            }],
            title: title_string,
            yaxis: {
                title: ystring,
                range: [min_y-margin*diff, max_y+margin*diff]
            },
            xaxis: {
                title: xstring, 
                range: [0, 24]
            }
        };

    }

    if (format === "grid") {

        layout["font"] = {size: 15};
        layout["title"] = title_string;
        
        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [0, 24];
            layout["yaxis"+(i+2)]["range"] = [min_y-margin*diff, max_y+margin*diff];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 15}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 15}}); 

    }

    if (format === "dropdown") {

        var layout = {
            font: {
                size: 15
            },
            title: title_string,
            yaxis: {
                title: ystring,
                range: [min_y-margin*diff, max_y+margin*diff]
            },
            xaxis: {
                title: xstring, 
                range: [0, 24]
            },
            updatemenus: [{
                y: 1, 
                yanchor: "top", 
                buttons: buttons
            }]
        }

    }

    return [graphish, layout];

}
// ///////////////////////////////////////////////////////////////

// Rose Fig

function rose_fig(all_results, input_files, category, vertloc, basecolor, bins, bin_arrange, nsector) {
    
    // Set up data
    var graphish = []; 
    var margin = 0.25;

    var object1 = process_data(all_results, 0);
    var object2 = edit_met_data(object1);
    var cate_info = get_catinfo(object2);
    var metdat = object2;

    [dircol, a, b] = get_vertical_locations(cate_info["columns"]["direction"], {location: vertloc});
    [varcol, vertlocs, c] = get_vertical_locations(cate_info["columns"][category], {location:vertloc});

    winddir = metdat[dircol].filter(Boolean);
    vari = metdat[varcol].filter(Boolean);

    colors = get_colors(bins-1, {basecolor: basecolor});
    colors.push("#3A4246");

    dir_card = [];
    for (var dir = 0; dir < winddir.length; dir++) {
        dir_card.push(getCardinal(parseFloat(winddir[dir]),nsector));
    }

    dir_obj = {};
    for (var dir = 0; dir < dir_card.length; dir++) {
        if (dir_obj[dir_card[dir]] == null) {
            dir_obj[dir_card[dir]] = [];
        }
        dir_obj[dir_card[dir]].push(vari[dir]);
    }

    var bin_mags = [];
    var startValue = 0;
    var stopValue = Math.max(...vari);

    if (bin_arrange === "linear") {

        var step = (stopValue - startValue) / (bins);

        for (var i = 0; i < bins; i++) {
            bin_mags.push(startValue + (step * i));
        }
    }

    if (bin_arrange === "inverse-log") {

        var range = stopValue - startValue;
        bin_mags.push(0);

        for (var i = 0; i < (bins-1); i++) {
            bin_mags.push(startValue + ( range / ( Math.pow( 2,(bins-i-1) ) ) ));
        }

    }

    bin_mags.push(Infinity);

    count = {};
    for (var key = 0; key < Object.keys(dir_obj).length; key++) {
        for (var itter = 0; itter < (bin_mags.length-1); itter++) {
            
            var numb = 0;
            for (var indy = 0; indy < dir_obj[Object.keys(dir_obj)[key]].length; indy++) {

                if ((parseFloat(dir_obj[Object.keys(dir_obj)[key]][indy]) >= bin_mags[itter]) & (parseFloat(dir_obj[Object.keys(dir_obj)[key]][indy]) < bin_mags[itter+1])) {
                    numb += 1;
                }

            }

            if (count[Object.keys(dir_obj)[key]] == null) {
                count[Object.keys(dir_obj)[key]] = [];
            }

            if (count[Object.keys(dir_obj)[key]].length != 0) {
                add_to = count[Object.keys(dir_obj)[key]][count[Object.keys(dir_obj)[key]].length-1];
                count[Object.keys(dir_obj)[key]].push(add_to + (numb/vari.length));
            } else {
                count[Object.keys(dir_obj)[key]].push(numb/vari.length);
            }
        }
    }

    t_mat = [];
    for (var cd = 0; cd < nsector; cd++) {
        t_mat.push(getCardinal(cd*(360/nsector)+1,nsector));
    }   


    for (var bi = 0; bi < bins; bi++) {
        r_mat = [];
        for (var sect = 0; sect < nsector; sect++) {
            r_mat.push(count[t_mat[sect]][bi]);
        }

        var trace = {
            r: r_mat,
            t: t_mat,
            name: "[" + parseFloat(bin_mags[bi]).toFixed(2) + ":" + parseFloat(bin_mags[bi+1]).toFixed(2) + ")",
            marker: {
                color: colors[bi]
            },
            type: "area",
        };

        graphish = graphish.concat(trace);

    }

    var layout = {
        title: "$$" + cate_info["labels"][category] + "\\text{ Distribution for " + input_files[0].replace("_"," ").replace(".csv","") + "} $$",
        orientation: 270,
        annotations: [{text: "Wind Speed", xref: "paper", yref: "paper",
                    x: 0, y: 0, showarrow: false, font: {size: 15}}]
    }

    graphish = graphish.reverse();

    return [graphish, layout];

}


// ///////////////////////////////////////////////////////////////

// // Monthly Rose Fig

// // Set up data
// var vertloc = 87;
// var margin = 0.25;
// var category = "speed";
// var bins = 6;
// var nsector = 32;
// var graphish = []; 
// var basecolor = "span";
// var format = "grid";
// var bin_arrange = "linear";
// var layout = {annotations: []};

// for (var j = 0; j < input_files.length; j++) {
//     // Convert CSV to JSON ... need to create dynamic labels in
//     // place of 7 and 10
//     var arrays = all_results[j].data;
//     var keys = arrays[7];
//     var values = arrays.slice(10);

//     var object1 = new Object();
//     // remove -1 in code with QC data
//     for (k = 0; k < (keys.length-1); k++) {
//         var new_values = [];
//         for (v = 0; v < values.length; v++) {
//             new_values.push(values[v][k]);
//         }
//         if (Object.keys(object1).indexOf(keys[k]) == -1) {
//             object1[keys[k]] = new_values;
//         } else {
//             object1[keys[k]+"_adv"] = new_values;
//         }
//     }       

//     var object2 = edit_met_data(object1);
//     var cate_info = get_catinfo(object2);
//     var metdat = object2;

//     [dircol, a, b] = get_vertical_locations(cate_info["columns"]["direction"], {location: vertloc});
//     [varcol, vertlocs, c] = get_vertical_locations(cate_info["columns"][category], {location:vertloc});
    
//     winddir = metdat[dircol].filter(Boolean);
//     vari = metdat[varcol].filter(Boolean);
    
//     colors = get_colors(bins-1, {basecolor: basecolor});
//     colors.push("#3A4246");

//     dir_card = [];
//     for (var dir = 0; dir < winddir.length; dir++) {
//         dir_card.push(getCardinal(parseFloat(winddir[dir]),nsector));
//     }

//     dir_obj = {};
//     for (var dir = 0; dir < dir_card.length; dir++) {
//         if (dir_obj[dir_card[dir]] == null) {
//             dir_obj[dir_card[dir]] = [];
//         }
//         dir_obj[dir_card[dir]].push(vari[dir]);
//     }

//     var bin_mags = [];
//     var startValue = 0;
//     var stopValue = Math.max(...vari);

//     if (bin_arrange === "linear") {

//         var step = (stopValue - startValue) / (bins);

//         for (var i = 0; i < bins; i++) {
//             bin_mags.push(startValue + (step * i));
//         }
//     }

//     if (bin_arrange === "inverse-log") {

//         var range = stopValue - startValue;
//         bin_mags.push(0);

//         for (var i = 0; i < (bins-1); i++) {
//             bin_mags.push(startValue + ( range / ( Math.pow( 2,(bins-i-1) ) ) ));
//         }

//     }

//     bin_mags.push(Infinity);

//     count = {};
//     for (var key = 0; key < Object.keys(dir_obj).length; key++) {
//         for (var itter = 0; itter < (bin_mags.length-1); itter++) {
//             var numb = 0;
//             for (var indy = 0; indy < dir_obj[Object.keys(dir_obj)[key]].length; indy++) {

//                 if ((parseFloat(dir_obj[Object.keys(dir_obj)[key]][indy]) >= bin_mags[itter]) & (parseFloat(dir_obj[Object.keys(dir_obj)[key]][indy]) < bin_mags[itter+1])) {
//                     numb += 1;
//                 }
//             }
//             if (count[Object.keys(dir_obj)[key]] == null) {
//                 count[Object.keys(dir_obj)[key]] = [];
//             }
//             if (count[Object.keys(dir_obj)[key]].length != 0) {
//                 add_to = count[Object.keys(dir_obj)[key]][count[Object.keys(dir_obj)[key]].length-1];
//                 count[Object.keys(dir_obj)[key]].push(add_to + (numb/vari.length));
//             } else {
//                 count[Object.keys(dir_obj)[key]].push(numb/vari.length);
//             }
//         }
//     }

//     t_mat = [];
//     for (var cd = 0; cd < nsector; cd++) {
//         t_mat.push(getCardinal(cd*(360/nsector)+1,nsector));
//     }   

//     for (var bi = 0; bi < bins; bi++) {
//         r_mat = [];
//         for (var sect = 0; sect < nsector; sect++) {
//             r_mat.push(count[t_mat[sect]][bi]);
//         }

//         if ((format === "dropdown") | (format === "slider")) {
//             var trace = {
//                 r: r_mat,
//                 t: t_mat,
//                 name: "[" + parseFloat(bin_mags[bi]).toFixed(2) + ":" + parseFloat(bin_mags[bi+1]).toFixed(2) + ")",
//                 marker: {
//                     color: colors[bi]
//                 },
//                 type: "area",
//                 visible: j === 0
//             };

//             graphish = graphish.concat(trace);
//         }

//         if (format === "grid") {
//             var trace = {
//                 r: r_mat,
//                 t: t_mat,
//                 xaxis: "x"+(j+2),
//                 yaxis: "y"+(j+2),
//                 name: "[" + parseFloat(bin_mags[bi]).toFixed(2) + ":" + parseFloat(bin_mags[bi+1]).toFixed(2) + ")",
//                 marker: {
//                     color: colors[bi]
//                 },
//                 type: "area",
//             };

//             graphish = graphish.concat(trace);
//         }
//     }

// }

// if ((format === "dropdown") | (format === "slider")) {

//     buttons = [];
//     for (var j = 0; j < input_files.length; j++){
//         // This array decides when to display a certain trace
//         false_array = [];
//         for(var i = 0; i < input_files.length; i++) {
//             if (i == j) {
//                 for(var sc1 = 0; sc1 < bins.length; sc1++) {
//                     false_array.push(true);
//                 }    
//             } else {
//                 for(var sc2 = 0; sc2 < bins.length; sc2++) {
//                     false_array.push(false);
//                 }
//             }  
//         }
//         buttons.push({method: 'restyle', args: ['visible', false_array], label: input_files[j].replace(/_|.csv/g," ")});
//     }
// }

// if (format === "slider") {

//     steps = buttons;

// }

// var title_string = "Wind Speed Distribution for " + input_files[0].replace("_"," ").replace(".csv","") + "-" + input_files[input_files.length-1].replace("_"," ").replace(".csv","");

// if (format === "slider") {
//     var layout = {
//         sliders: [{
//             pad: {t: 30},
//             len: ((input_files.length)/12),
//             steps: steps
//         }],
//         title: title_string,
//         orientation: 270
//     };
// }

// if (format === "dropdown") {

//     var layout = {
//         title: title_string,
//         updatemenus: [{
//             y: 1, 
//             yanchor: "top", 
//             buttons: buttons
//         }],
//         orientation: 270
//     }

// }

// if (format === "grid") {

//     layout["title"] = title_string;
//     layout["orientation"] = 270;
    
//     for(var i = 0; i < input_files.length; i++) {
//         // layout["xaxis"+(i+2)]["range"] = [0, 24];
//         // layout["yaxis"+(i+2)]["range"] = [0, 1.1*max_y];
//         layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
//                                 x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
//                                 showarrow: true, arrowhead: 0, ax: 0, ay: 0});
//     }
//     layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
//                             x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
//                             showarrow: false, font: {size: 15}});
//     layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
//                             x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
//                             showarrow: false, font: {size: 15}}); 

// }

// // var layout = {
// //     title: "Wind Speed Distribution for " + input_files[0].replace("_"," ").replace(".csv","") + "-" + input_files[input_files.length-1].replace("_"," ").replace(".csv",""),
// //     orientation: 270
// // }
// graphish = graphish.reverse();
// //console.log(graphish.slice(0,4));

// Plotly.newPlot("chart", graphish, layout)

// ///////////////////////////////////////////////////////////////

// Winddir Scatter   

function winddir_scatter(all_results, input_files, category, vertloc, basecolor) {
    
    // Set up data
    var graphish = []; 
    var margin = 0.25;
    var exclude_angles = [46,228];

    for (var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j)  
        var object2 = edit_met_data(object1);
        var cate_info = get_catinfo(object2);

        var dircol, varcol, vertlocs, a, b, c;
        [dircol, a, b] = get_vertical_locations(cate_info["columns"]["direction"], {location: vertloc});
        [varcol, vertlocs, c] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

        var other_colors = get_nrelcolors(input_files.length);

        var trace = {
            x: object2[dircol],
            y: object2[varcol],
            mode: "markers",
            marker: {
                color: other_colors[basecolor][j]
            },
            type: "scatter",
            name: input_files[j].split("_")[1].split(".")[0],
            //visible: j === 0
        };
        graphish[j] = trace;

    }

    var buttons = [];
    var shapes = [];
    var colors = get_nrelcolors();

    // Create shape to exclude angles, only takes in one set
    // of a range of excluded angles
    shapes.push({type: "rect", xref: "paper", yref: "paper", 
                x0: (exclude_angles[0]/360), y0: 0, 
                x1: (exclude_angles[1]/360), y1: 1, 
                fillcolor: colors["red"][0], 
                opacity: 0.2, 
                line: {width: 0}
                });

    var xstring = "$$ Wind Direction [^\\circ] $$";
    var ystring = "$$" + cate_info["labels"][category] + "$$";
    var title_string = "$$ \\text{Wind Direction vs. }" + ystring.replace("$$","") + " $$";

    var layout = {
        font: {
            size: 15
        },
        title: title_string,
        shapes: shapes,
        xaxis: {title: xstring},
        yaxis: {title: ystring},
        hovermode: "closest"
    };

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Monthly Winddir Scatter 

function monthly_winddir_scatter(all_results, input_files, category, vertloc, basecolor, format, rows, cols) {
    
    // Set up data
    var graphish = []; 
    var layout = {annotations: []};
    var exclude_angles = [46,228];
    var max_y = -Infinity;
    var min_y = Infinity;
    var margin = 0.25;

    for (var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j)   
        var object2 = edit_met_data(object1);
        var cate_info = get_catinfo(object2);

        var dircol, varcol, vertlocs, a, b, c;
        [dircol, a, b] = get_vertical_locations(cate_info["columns"]["direction"], {location: vertloc});
        [varcol, vertlocs, c] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

        var other_colors = get_colors(input_files.length, {basecolor: basecolor});

        if (Math.max(...object2[varcol].filter(Boolean)) > max_y) {
            max_y = Math.max(...object2[varcol].filter(Boolean));
        }

        if (Math.min(...object2[varcol].filter(Boolean)) < min_y) {
            min_y = Math.min(...object2[varcol].filter(Boolean));
        }

        if ((format === "dropdown") | (format === "slider")) {

            var trace = {
                x: object2[dircol],
                y: object2[varcol],
                mode: "markers",
                marker: {
                    color: other_colors[j]
                },
                type: "scatter",
                name: input_files[j].split("_")[1].split(".")[0],
                visible: j === 0
            };
            graphish = graphish.concat(trace);

        }

        if (format === "grid") {

            var trace = {
                x: object2[dircol],
                y: object2[varcol],
                xaxis: "x" + (j+2),
                yaxis: "y" + (j+2),
                mode: "markers",
                marker: {
                    color: other_colors[j]
                },
                type: "scatter",
                name: input_files[j].split("_")[1].split(".")[0],
                showlegend: j ===0
            };
            graphish = graphish.concat(trace);

        }

        if (format === "grid") {

            layout["yaxis" + (j+2)] = {
                domain: calcDomain_y(Math.floor(j/cols),rows)
            };

            layout["xaxis" + (j+2)] = {
                domain: calcDomain_x(j%cols,cols)
            };

        }

    }

    var buttons = [];
    var shapes = [];
    var colors = get_nrelcolors();

    var diff = max_y - min_y;

    if ((format === "dropdown") | (format === "slider")) {

        for (var j = 0; j < input_files.length; j++){
            // This array decides when to display a certain trace
            false_array = [];

            for(var i = 0; i < input_files.length; i++) {
                if (i == j) {
                    false_array.push(true);
                } else {
                    false_array.push(false);
                }  
            }

            buttons.push({method: 'restyle', args: ['visible', false_array], 
                        label: input_files[j].replace(/_|.csv/g," ")
                        });
            shapes.push({type: "rect", xref: "x"+(j+2), yref: "y"+(j+2), 
                        x0: exclude_angles[0], y0: min_y-margin*diff, 
                        x1: exclude_angles[1], y1: max_y+margin*diff, 
                        fillcolor: colors["red"][0], 
                        opacity: 0.2, 
                        line: {width: 0}
                        });
        }

    }

    if (format === "slider") {

        steps = buttons;

    }

    if (format === "grid") {

        for (var j = 0; j < input_files.length; j++){

            shapes.push({type: "rect", xref: "x"+(j+2), yref: "y"+(j+2), 
                        x0: exclude_angles[0], y0: min_y-margin*diff, 
                        x1: exclude_angles[1], y1: max_y+margin*diff, 
                        fillcolor: colors["red"][0], 
                        opacity: 0.2, 
                        line: {width: 0}
                        });
        }

    }

    var xstring = "$$ \\text{Wind Direction}[^\\circ] $$";
    var ystring = "$$" + cate_info["labels"][category] + "$$";
    var title_string = "$$ \\text{Wind Direction vs. }" + ystring.replace("$$","") + " $$";

    var diff = max_y - min_y;

    if (format === "slider") {
        
        var layout = {
            font: {
                size: 15
            },
            sliders: [{
                pad: {t: 30},
                len: ((input_files.length)/12),
                steps: steps
            }],
            shapes: shapes,
            hovermode: "closest",
            showlegend: false,
            title: title_string,
            yaxis: {
                title: ystring,
                range: [min_y-margin*diff, max_y+margin*diff]
            },
            xaxis: {
                title: xstring, 
                range: [0, 360]
            }
        };

    }

    if (format === "grid") {

        layout["font"] = {size: 15};
        layout["title"] = title_string;
        layout["shapes"] = shapes;
        layout["hovermode"] = "closest";
        layout["showlegend"] = false;
        
        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [0, 360];
            layout["yaxis"+(i+2)]["range"] = [min_y-margin*diff, max_y+margin*diff];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 15}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 15}}); 

    }

    if (format === "dropdown") {

        var layout = {
            font: {
                size: 15
            },
            title: title_string,
            hovermode: "closest",
            showlegend: false,
            yaxis: {
                title: ystring,
                range: [min_y-margin*diff, max_y+margin*diff]
            },
            xaxis: {
                title: xstring, 
                range: [0, 360]
            },
            updatemenus: [{
                y: 1, 
                yanchor: "top", 
                buttons: buttons
            }],
            shapes: shapes
        }

    }

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Stability Winddir Scatter 

// *** Only used for one month data

function stab_winddir_scatter(all_results, input_files, category, vertloc, basecolor) {

    // Set up data
    var exclude_angles = [46,228];
    var graphish = []; 
    var max_y = -Infinity;
    var min_y = Infinity;
    var margin = 0.25;

    // User input
    var one_plot = true;

    var object1 = process_data(all_results, 0);  
    var object2 = edit_met_data(object1);

    var stab_conds, stab_cats, metdat;
    [stab_conds, stab_cats, metdat] = flag_stability(object2);
    cate_info = get_catinfo(metdat);

    var dircol, varcol, vertlocs, stab, stabloc, ind, a, b, c;
    [dircol, a, b] = get_vertical_locations(cate_info["columns"]["direction"], {location: vertloc});
    [varcol, vertlocs, c] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});
    [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});

    var stabconds = get_stabconds();
    var other_colors = get_colors(stabconds.length, {basecolor: basecolor});

    for (var cond = 0; cond < stabconds.length; cond++) {

        var plotdat_x = [];
        var plotdat_y = [];
        for (var ii = 0; ii < metdat[dircol].length; ii++) {
            
            // until there is a faster way to remove these                        
            if ((metdat[stab][ii] === stabconds[cond]) && (parseFloat(metdat[dircol][ii]) != -999.0) && (metdat[dircol][ii] != null) && (parseFloat(metdat[varcol][ii]) != -999.0) && (metdat[varcol][ii] != null)) {
                plotdat_x.push(metdat[dircol][ii]);
                plotdat_y.push(metdat[varcol][ii]);
            }

        }
        var maxdat = plotdat_y.filter(Boolean);

        if (Math.max(...maxdat) > max_y) {
            max_y = Math.max(...maxdat);
        }

        if (Math.min(...maxdat) < min_y) {
            min_y = Math.min(...maxdat);
        }

        if (one_plot) {

            var trace = {
                x: plotdat_x,
                y: plotdat_y,
                mode: "markers",
                marker: {
                    color: other_colors[cond]
                },
                type: "scatter",
                name: stabconds[cond],
            };

        } else {

            var trace = {
                x: plotdat_x,
                y: plotdat_y,
                mode: "markers",
                marker: {
                    color: other_colors[cond]
                },
                type: "scatter",
                name: stabconds[cond],
                visible: cond === 0
            };

        }
        graphish = graphish.concat(trace);

    }

    var xstring = "$$ \\text{Wind Direction} [^\\circ] $$";
    var ystring = "$$" + cate_info["labels"][category] + "$$";
    var title_string = "$$ \\text{Wind Direction vs. }" + ystring.replace("$$","") + " $$";

    var diff = max_y - min_y;

    var colors = get_nrelcolors();

    if (one_plot) {

        var layout = {
            font: {
                size: 15
            },
            shapes: [{type: "rect", xref: "xaxis", yref: "yaxis", 
                    x0: exclude_angles[0], y0: min_y-margin*diff, 
                    x1: exclude_angles[1], y1: max_y+margin*diff, 
                    fillcolor: colors["red"][0], 
                    opacity: 0.2, 
                    line: {width: 0}
            }],
            hovermode: "closest",
            showlegend: true,
            title: title_string,
            yaxis: {
                title: ystring,
                range: [min_y-margin*diff, max_y+margin*diff]
            },
            xaxis: {
                title: xstring, 
                range: [0, 360]
            }
        };

    } else {

        buttons = [];
        shapes = [];

        var steps = [];
        for (var j = 0; j < stabconds.length; j++){
            // This array decides when to display a certain trace
            var false_array = [];

            for(var i = 0; i < stabconds.length; i++) {
                if (i == j) {
                    false_array.push(true);
                } else {
                    false_array.push(false);
                }  
            }
            
            steps.push({method: 'restyle', args: ['visible', false_array], 
                        label: stabconds[j]
                        });
            shapes.push({type: "rect", xref: "paper", yref: "paper", 
                        x0: (exclude_angles[0]/360), y0: 0, 
                        x1: (exclude_angles[1]/360), y1: 1, 
                        fillcolor: colors["red"][0], 
                        opacity: 0.2/stabconds.length, 
                        line: {width: 0}
                        });
        }

        var layout = {
            font: {
                size: 15
            },
            sliders: [{
                pad: {t: 30},
                len: ((stabconds.length)/12),
                steps: steps
            }],
            shapes: shapes,
            hovermode: "closest",
            showlegend: false,
            title: title_string,
            yaxis: {
                title: ystring,
                range: [min_y-margin*diff, max_y+margin*diff]
            },
            xaxis: {
                title: xstring, 
                range: [0, 360]
            }
        };

    }

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Groupby Winddir Scatter 

function groupby_winddir_scatter(all_results, input_files, category, abscissa, group_by, vertloc, basecolor, nbins) {

    // Set up data
    var graphish = []; 
    var max_x = -Infinity;
    var min_x = Infinity
    var max_y = -Infinity;
    var min_y = Infinity;
    var margin = 0.25;

    var object1 = process_data(all_results, 0);    

    if ((category === "stability flag") | (abscissa === "stability flag") | (group_by === "stability flag")) {

        var object2 = edit_met_data(object1);
        [stab_conds, stab_cats, metdat] = flag_stability(object2);
        var cate_info = get_catinfo(metdat);

    } else {

        var object2 = edit_met_data(object1);
        var cate_info = get_catinfo(object2);   
        var metdat = object2;

    }

    var varcol, vertlocs, groupcol, abscol, a, b, c, d, e;
    [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});
    [groupcol, b, c] = get_vertical_locations(cate_info["columns"][group_by], {location: vertloc});
    [abscol, d, e] = get_vertical_locations(cate_info["columns"][abscissa], {location: vertloc});

    var colors = get_colors(nbins, {basecolor: basecolor});

    var data_temp = metdat[groupcol];
    var test_mat = [];
    for (var i = 0; i < data_temp.length; i += 1) {
        // until there is a faster way to remove these                        
        if ((parseFloat(data_temp[i]) != -999.0) && (data_temp[i] != null)) {
            test_mat.push(data_temp[i]);
        }
    }

    var test_val = test_mat.sort(function(a, b) {return a - b;});
    var temp = [], i;
    for (i = 0; i < test_val.length; i += test_val.length/nbins) {
        temp.push(test_val.slice(i, i + test_val.length/nbins));
    }

    var bounds = {};
    for (var leng = 0; leng < temp.length; leng++) {
        bounds[""+leng] = [];
        bounds[""+leng].push(temp[leng][0]);
        bounds[""+leng].push(temp[leng][temp[leng].length-1]);
    }

    for (var bd = 0; bd < Object.keys(bounds).length; bd++) {
        x_dat = [];
        y_dat = [];
        for (var datlen = 0; datlen < metdat[abscol].length; datlen++) {
            var x = parseFloat(metdat[abscol][datlen]);
            var y = parseFloat(metdat[varcol][datlen]);
            var f = parseFloat(metdat[groupcol][datlen]);
            
            if ((x != -999.0) && (isNaN(x) === false) && (y != -999.0) && (isNaN(y) === false) && (f >= parseFloat(bounds[""+bd][0])) && (f <= parseFloat(bounds[""+bd][1]))) {

                x_dat.push(x);
                y_dat.push(y);

            }
        }

        if (Math.max(...x_dat) > max_x) {
            max_x = Math.max(...x_dat)
        }

        if (Math.min(...x_dat) < min_x) {
            min_x = Math.min(...x_dat)
        }

        if (Math.max(...y_dat) > max_y) {
            max_y = Math.max(...y_dat)
        }

        if (Math.min(...y_dat) < min_y) {
            min_y = Math.min(...y_dat)
        }

        var trace = {
            x: x_dat,
            y: y_dat,
            mode: "markers",
            name: "[" + bounds[""+bd][0] + ":" + bounds[""+bd][1] + "]",
            marker: {
                color: colors[bd]
            }
        }

        graphish = graphish.concat(trace);
    }

    // Set title and labels
    var title_string = "$$ \\text{Vertical Location = }" + vertloc + "\\text{m, Grouped by: }" + cate_info["labels"][group_by] + "$$";
    //x_string = cate_info["labels"][abscissa];
    var x_string = "$$ " + cate_info["labels"][abscissa] + " $$";
    var y_string = "$$ " + cate_info["labels"][category] + " $$";

    var diffx = max_x - min_x;
    var diffy = max_y - min_y;

    if ((category === "direction") | (abscissa === "direction")) {

        // Create shape to exclude angles, only takes in one set
        // of a range of excluded angles
        var exclude_angles = [46,228];
        var shapes = [];
        var colors = get_nrelcolors();

        if (category === "direction") {

            shapes.push({type: "rect", xref: "paper", yref: "paper", 
                         x0: 0, y0: (exclude_angles[0]/360), 
                         x1: 1, y1: (exclude_angles[1]/360), 
                         fillcolor: colors["red"][0], 
                         opacity: 0.2, 
                         line: {width: 0}
            });

        }

        if (abscissa === "direction") {

            shapes.push({type: "rect", xref: "paper", yref: "paper", 
            x0: (exclude_angles[0]/360), y0: 0, 
            x1: (exclude_angles[1]/360), y1: 1, 
            fillcolor: colors["red"][0], 
            opacity: 0.2, 
            line: {width: 0}
            });

        }

        var layout = {
            font: {
                size: 15
            },
            title: title_string,
            shapes: shapes,
            xaxis: {
                title: x_string,
                range: [min_x-margin*diffx, max_x+margin*diffx]
            },
            yaxis: {
                title: y_string,
                range: [min_y-margin*diffy, max_y+margin*diffy]
            },
            hovermode: "closest"
        }

    } else {

        var layout = {
            font: {
                size: 15
            },
            title: title_string,
            xaxis: {
                title: x_string,
                range: [min_x-margin*diffx, max_x+margin*diffx]
            },
            yaxis: {
                title: y_string,
                range: [min_y-margin*diffy, max_y+margin*diffy]
            },
            hovermode: "closest"
        }

    }

    return [graphish, layout];

}

// if (graphish.length < nbins) {
//     alert("It appears there is missing data, some traces are missing.");
// } 

// ///////////////////////////////////////////////////////////////

// Monthly Groupby Winddir Scatter 

function monthly_groupby_winddir_scatter (all_results, input_files, category, abscissa, group_by, vertloc, basecolor, nbins, format, rows, cols) {

    // Set up data
    var max_x = -Infinity;
    var min_x = Infinity
    var max_y = -Infinity;
    var min_y = Infinity;
    var margin = 0.25;
    var exclude_angles = [46,228];

    var graphish = []; 
    var layout = {annotations: []};
    var full_mat = []; 
    var met_obj = {};

    for (var j = 0; j < input_files.length; j++) {
        // Convert CSV to JSON ... need to create dynamic labels in
        // place of 7 and 10
        var arrays = all_results[j].data;
        var keys = arrays[7];
        var values = arrays.slice(10);

        var object1 = new Object();
        // remove -1 in code with QC data
        for (k = 0; k < (keys.length-1); k++) {
            var new_values = [];
            for (v = 0; v < values.length; v++) {
                new_values.push(values[v][k]);
            }
            if (Object.keys(object1).indexOf(keys[k]) == -1) {
                object1[keys[k]] = new_values;
            } else {
                object1[keys[k]+"_adv"] = new_values;
            }
        }       

        var object2 = edit_met_data(object1);
        var cate_info = get_catinfo(object2);
        var metdat = object2;

        var varcol, vertlocs, groupcol, abscol, a, b, c, d, e;
        [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});
        [groupcol, b, c] = get_vertical_locations(cate_info["columns"][group_by], {location: vertloc});
        [abscol, d, e] = get_vertical_locations(cate_info["columns"][abscissa], {location: vertloc});

        var colors = get_colors(nbins, {basecolor: basecolor});

        var data_temp = metdat[groupcol];
        for (var i = 0; i < data_temp.length; i += 1) {
            // until there is a faster way to remove these                        
            if ((parseFloat(data_temp[i]) != -999.0) && (data_temp[i] != null)) {
                full_mat.push(data_temp[i]);
            }
        }

        met_obj[""+j] = metdat;
    }

    var test_val = full_mat.sort(function(a, b) {return a - b;});
    var temp = [], i;
    for (i = 0; i < test_val.length; i += test_val.length/nbins) {
        temp.push(test_val.slice(i, i + test_val.length/nbins));
    }

    var bounds = {};
    for (var leng = 0; leng < temp.length; leng++) {
        bounds[""+leng] = [];
        bounds[""+leng].push(temp[leng][0]);
        bounds[""+leng].push(temp[leng][temp[leng].length-1]);
    }

    for (var j = 0; j < input_files.length; j++) {
        for (var bd = 0; bd < Object.keys(bounds).length; bd++) {
            x_dat = [];
            y_dat = [];
            var metdat = met_obj[""+j];
            for (var datlen = 0; datlen < metdat[abscol].length; datlen++) {
                var x = parseFloat(metdat[abscol][datlen]);
                var y = parseFloat(metdat[varcol][datlen]);
                var f = parseFloat(metdat[groupcol][datlen]);
                
                if ((x != -999.0) && (isNaN(x) === false) && (y != -999.0) && (isNaN(y) === false) && (f >= parseFloat(bounds[""+bd][0])) && (f <= parseFloat(bounds[""+bd][1]))) {

                    x_dat.push(x);
                    y_dat.push(y);

                }
            }

            if (Math.max(...x_dat) > max_x) {
                max_x = Math.max(...x_dat)
            }

            if (Math.min(...x_dat) < min_x) {
                min_x = Math.min(...x_dat)
            }

            if (Math.max(...y_dat) > max_y) {
                max_y = Math.max(...y_dat)
            }

            if (Math.min(...y_dat) < min_y) {
                min_y = Math.min(...y_dat)
            }

            if ((format === "dropdown") | (format === "slider")) {

                var trace = {
                    x: x_dat,
                    y: y_dat,
                    mode: "markers",
                    name: "[" + bounds[""+bd][0] + ":" + bounds[""+bd][1] + "]",
                    marker: {
                        color: colors[bd]
                    },
                    visible: j === 0
                };
                graphish = graphish.concat(trace);

            }

            if (format === "grid") {
                
                var trace = {
                    x: x_dat,
                    y: y_dat,
                    xaxis: "x"+(j+2),
                    yaxis: "y"+(j+2),
                    mode: "markers",
                    name: "[" + bounds[""+bd][0] + ":" + bounds[""+bd][1] + "]",
                    marker: {
                        color: colors[bd]
                    },
                    showlegend: j === 0
                };
                graphish = graphish.concat(trace);

            }
        }

        if (format === "grid") {

            layout["yaxis" + (j+2)] = {
                domain: calcDomain_y(Math.floor(j/cols),rows)
            };

            layout["xaxis" + (j+2)] = {
                domain: calcDomain_x(j%cols,cols)
            };

        } 

    }

    var buttons = [];
    var shapes = [];
    var diffy = max_y - min_y;
    var diffx = max_x - min_x;

    if ((format === "dropdown") | (format === "slider")) {

        for (var j = 0; j < input_files.length; j++){
            // This array decides when to display a certain trace
            false_array = [];

            for(var i = 0; i < input_files.length; i++) {
                if (i == j) {
                    for (var iah = 0; iah < nbins; iah++) {
                        false_array.push(true);
                    }
                } else {
                    for (var iah = 0; iah < nbins; iah++) {
                        false_array.push(false);
                    }
                }  
            }

            buttons.push({method: 'restyle', args: ['visible', false_array], 
                        label: input_files[j].replace(/_|.csv/g," ")
                        });

            if ((category === "direction") | (abscissa === "direction")) {

                // Create shape to exclude angles, only takes in one set
                // of a range of excluded angles
                var shapes = [];
                var colors = get_nrelcolors();

                if (abscissa === "direction") {

                    shapes.push({type: "rect", xref: "x"+(j+2), yref: "y"+(j+2), 
                                 x0: exclude_angles[0], y0: min_y-margin*diffy, 
                                 x1: exclude_angles[1], y1: max_y+margin*diffy, 
                                 fillcolor: colors["red"][0], 
                                 opacity: 0.2, 
                                 line: {width: 0}
                    });

                }

                if (category === "direction") {

                    shapes.push({type: "rect", xref: "x"+(j+2), yref: "y"+(j+2), 
                                 x0: min_x-margin*diffx, y0: exclude_angles[0], 
                                 x1: max_x+margin*diffx, y1: exclude_angles[1], 
                                 fillcolor: colors["red"][0], 
                                 opacity: 0.2, 
                                 line: {width: 0}
                    });

                }

            }

        }

    }

    if (format === "slider") {

        steps = buttons;

    }

    if ((category === "direction") | (abscissa === "direction")) {

        if (format === "grid") {

            // Create shape to exclude angles, only takes in one set
            // of a range of excluded angles
            var shapes = [];
            var colors = get_nrelcolors();

            for (var j = 0; j < input_files.length; j++){

                if (abscissa === "direction") {

                    shapes.push({type: "rect", xref: "x"+(j+2), yref: "y"+(j+2), 
                                x0: exclude_angles[0], y0: min_y-margin*diffy, 
                                x1: exclude_angles[1], y1: max_y+margin*diffy, 
                                fillcolor: colors["red"][0], 
                                opacity: 0.2, 
                                line: {width: 0}
                    });

                }

                if (category === "direction") {

                    shapes.push({type: "rect", xref: "x"+(j+2), yref: "y"+(j+2), 
                                x0: min_x-margin*diffx, y0: exclude_angles[0], 
                                x1: max_x+margin*diffx, y1: exclude_angles[1], 
                                fillcolor: colors["red"][0], 
                                opacity: 0.2, 
                                line: {width: 0}
                    });

                }

            }

        }

    }

    // Set title and labels
    var title_string = "$$ \\text{Vertical Location = }" + vertloc + "\\text{m, Grouped by: }" + cate_info["labels"][group_by] + "$$";
    var x_string = "$$ " + cate_info["labels"][abscissa] + " $$";
    var y_string = "$$ " + cate_info["labels"][category] + " $$";

    if (format === "slider") {

        if ((category === "direction") | (abscissa === "direction")) {

            var layout = {
                font: {
                    size: 15
                },
                sliders: [{
                    pad: {t: 30},
                    len: ((input_files.length)/12),
                    steps: steps
                }],
                title: title_string,
                shapes: shapes,
                yaxis: {
                    title: y_string,
                    range: [min_y-margin*diffy, max_y+margin*diffy]
                },
                xaxis: {
                    title: x_string,
                    range: [min_x-margin*diffx, max_x+margin*diffx]
                },
                hovermode: "closest"
            };

        } else {
        
            var layout = {
                font: {
                    size: 15
                },
                sliders: [{
                    pad: {t: 30},
                    len: ((input_files.length)/12),
                    steps: steps
                }],
                title: title_string,
                yaxis: {
                    title: y_string,
                    range: [min_y-margin*diffy, max_y+margin*diffy]
                },
                xaxis: {
                    title: x_string,
                    range: [min_x-margin*diffx, max_x+margin*diffx]
                },
                hovermode: "closest"
            };

        }

    }

    if (format === "grid") {

        if ((category === "direction") | (abscissa === "direction")) {

            layout["font"] = {size: 15};
            layout["title"] = title_string;
            layout["hovermode"] = "closest";
            layout["shapes"] = shapes;
            // possible fix if other than 12 month periods
            //index_mat = [8,9,10,11];
            
            for(var i = 0; i < input_files.length; i++) {

                layout["xaxis"+(i+2)]["range"] = [min_x-margin*diffx, max_x+margin*diffx];
                layout["yaxis"+(i+2)]["range"] = [min_y-margin*diffy, max_y+margin*diffy];

                // if (index_mat.indexOf(i) < 0) {
                //     layout["xaxis"+(i+2)]["anchor"] = "x"+(index_mat[i%3]);
                // }

                layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                        x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                        showarrow: true, arrowhead: 0, ax: 0, ay: 0});

            }

            layout.annotations.push({text: x_string, xref: "paper", yref: "paper",
                                    x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                    showarrow: false, font: {size: 15}});

            layout.annotations.push({text: y_string, xref: "paper", yref: "paper",
                                    x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                    showarrow: false, font: {size: 15}}); 


        } else {

            layout["font"] = {size: 15};
            layout["title"] = title_string;
            layout["hovermode"] = "closest";
            // possible fix if other than 12 month periods
            //index_mat = [8,9,10,11];
            
            for(var i = 0; i < input_files.length; i++) {

                layout["xaxis"+(i+2)]["range"] = [min_x-margin*diffx, max_x+margin*diffx];
                layout["yaxis"+(i+2)]["range"] = [min_y-margin*diffy, max_y+margin*diffy];

                // if (index_mat.indexOf(i) < 0) {
                //     layout["xaxis"+(i+2)]["anchor"] = "x"+(index_mat[i%3]);
                // }                

                layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                        x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                        showarrow: true, arrowhead: 0, ax: 0, ay: 0});

            }

            layout.annotations.push({text: x_string, xref: "paper", yref: "paper",
                                    x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                    showarrow: false, font: {size: 15}});

            layout.annotations.push({text: y_string, xref: "paper", yref: "paper",
                                    x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                    showarrow: false, font: {size: 15}}); 

        }

    }

    if (format === "dropdown") {

        if ((category === "direction") | (abscissa === "direction")) {

            var layout = {
                font: {
                    size: 15
                },
                title: title_string,
                yaxis: {
                    title: y_string,
                    range: [min_y-margin*diffy, max_y+margin*diffy]
                },
                xaxis: {
                    title: x_string, 
                    range: [min_x-margin*diffx, max_x+margin*diffx]
                },
                shapes: shapes,
                updatemenus: [{
                    y: 1, 
                    yanchor: "top", 
                    buttons: buttons
                }],
                hovermode: "closest"
            }

        } else {

            var layout = {
                font: {
                    size: 15
                },
                title: title_string,
                yaxis: {
                    title: y_string,
                    range: [min_y-margin*diffy, max_y+margin*diffy]
                },
                xaxis: {
                    title: x_string, 
                    range: [min_x-margin*diffx, max_x+margin*diffx]
                },
                updatemenus: [{
                    y: 1, 
                    yanchor: "top", 
                    buttons: buttons
                }],
                hovermode: "closest"
            }

        }

    }

    return [graphish, layout];

}

// if (graphish.length < nbins*input_files.length) {
//     alert("It appears there is missing data, some traces are missing.");
// } 

// ///////////////////////////////////////////////////////////////

// Histogram

function hist(all_results, input_files, category, vertloc, basecolor, nbins, curvefit) {
    
    // Set up data
    var graphish = []; 
    var layout = {annotations: []};
    var margin = 0.25;

    var object1 = process_data(all_results, 0);   
    var object2 = edit_met_data(object1);
    var cate_info = get_catinfo(object2);

    var varcol, vertlocs, a;
    [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

    var hist_data = object2[varcol];

    var min_hist = Math.min(...hist_data);
    var max_hist = Math.max(...hist_data);
    var filt_dat = hist_data.filter(Boolean);
    var sum = 0;
    for( var i = 0; i < filt_dat.length; i++ ){
        sum += parseFloat(filt_dat[i]);
    }
    var mean = sum/filt_dat.length;

    var colors = get_nrelcolors();

    if (curvefit != "None") {

        var k = 0;
        var l = 0;

        if (curvefit === "Exponential") {

            k = 1;

        }

        if (curvefit === "Rayleigh") {

            k = 2;

        }

        if (curvefit === "Lognormal") {

            k = 2.5;

        }

        if (curvefit === "Normal") {

            k = 3.6;

        }

        if (curvefit === "Weibull") {

            var variance = 0;
            var n = filt_dat.length;
            var v1 = 0;
            var v2 = 0;

            if (n != 1) {

                for (var i = 0; i < n; i++) {
                    v1 = v1 + (filt_dat[i] - mean) * (filt_dat[i] - mean);
                    v2 = v2 + (filt_dat[i] - mean);
                }

                v2 = v2 * v2 / n;
                variance = (v1 - v2) / (n-1);

                if (variance < 0) { 
                    variance = 0; 
                }
        
                std_dev = Math.sqrt(variance);

            }

            k = Math.pow((0.9874/(std_dev/mean)),1.0983);

        }            

        var arg = 1/k;
        l = mean / ((Math.sqrt(2*Math.PI*arg))*(Math.pow((arg/Math.E),arg)));

        var xdat = [];
        var ydat = [];
        for (var iter = min_hist; iter < max_hist; iter += ((max_hist-min_hist)/1000)) {
            xdat.push(iter);
            var wb = (k/l)*(Math.pow((iter/l),k-1))*Math.pow(Math.E,-Math.pow((iter/l),k));
            ydat.push(wb);
        }

        var trace_cv = {
            x: xdat,
            y: ydat,
            mode: "lines",
            line: {
                color: "rgb(0, 0, 0)"
            },
            name: curvefit,
        };

        graphish = graphish.concat(trace_cv);

        layout["annotations"].push({text: "Shape Parameter: " + k.toFixed(2), xref: "paper", yref: "paper",
                                    x: 0.9, y: 0.9, showarrow: false, font: {size: 16}}); 

        layout["annotations"].push({text: "Scale Parameter: " + l.toFixed(2), xref: "paper", yref: "paper",
                                    x: 0.9, y: 0.8, showarrow: false, font: {size: 16}});                                     

    }

    var trace = {
        x: hist_data,
        type: "histogram",
        xbins: {
            start: min_hist,
            end: max_hist,
            size: (max_hist - min_hist)/(nbins)
        },
        histnorm: "probability",
        marker: {
            color: colors[basecolor][0],
            line: {
                width: 2
            }
        },
        name: input_files[0].split("_")[1].split(".")[0],
    };

    graphish = graphish.concat(trace);

    xstring = "$$" + cate_info["labels"][category] + "$$";
    ystring = "$$ \\text{Frequency} [\\%] $$";
    title_string = "$$ \\text{Frequency Histogram of }" + xstring.replace("$$"," ");

    layout["font"] = {size: 15};
    layout["title"] =  title_string;
    layout["xaxis"] = {title: xstring};
    layout["yaxis"] = {title: ystring};
    layout["hovermode"] = "closest";

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Monthly Histogram

function monthly_hist(all_results, input_files, category, vertloc, basecolor, nbins, format, rows, cols) {

    // Set up data
    var graphish = []; 
    var max_x = -Infinity;
    var min_x = Infinity;
    var layout = {annotations: []};
    var max_y = 0.3;
    var margin = 0.25;

    for (var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j);    
        var object2 = edit_met_data(object1);
        var cate_info = get_catinfo(object2);

        var varcol, vertlocs, a;
        [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

        var hist_data = object2[varcol];
        
        var colors = get_colors(input_files.length, {basecolor: basecolor});
        

        if (Math.max(...hist_data) > max_x) {
            max_x = Math.max(...hist_data);
        }

        if (Math.min(...hist_data) < min_x) {
            min_x = Math.min(...hist_data);
        }

        if ((format === "dropdown") | (format === "slider")) {

            var trace = {
                x: hist_data,
                type: "histogram",
                xbins: {
                    start: Math.min(...hist_data),
                    end: Math.max(...hist_data),
                    size: (Math.max(...hist_data) - Math.min(...hist_data))/(nbins)
                },
                histnorm: "probability",
                marker: {
                    color: colors[j],
                    line: {
                        width: 2
                    }
                },
                name: input_files[j].split("_")[1].split(".")[0],
                visible: j === 0
            };
            graphish = graphish.concat(trace);

        }

        if (format === "grid") {
            
            var trace = {
                x: hist_data,
                xaxis: "x" + (j+2),
                yaxis: "y" + (j+2),
                type: "histogram",
                xbins: {
                    start: Math.min(...hist_data),
                    end: Math.max(...hist_data),
                    size: (Math.max(...hist_data) - Math.min(...hist_data))/(nbins)
                },
                histnorm: "probability",
                marker: {
                    color: colors[j],
                    line: {
                        width: 2
                    }
                },
                name: input_files[j].split("_")[1].split(".")[0],
            };
            graphish = graphish.concat(trace);

        }

        if (format === "grid") {

            layout["yaxis" + (j+2)] = {
                domain: calcDomain_y(Math.floor(j/cols),rows)
            };

            layout["xaxis" + (j+2)] = {
                domain: calcDomain_x(j%cols,cols)
            };

        }    

    }

    var buttons = [];
    var shapes = [];

    if ((format === "dropdown") | (format === "slider")) {

        for (var j = 0; j < input_files.length; j++){
            // This array decides when to display a certain trace
            false_array = [];

            for(var i = 0; i < input_files.length; i++) {
                if (i == j) {
                    false_array.push(true);
                } else {
                    false_array.push(false);
                }  
            }
            buttons.push({method: 'restyle', args: ['visible', false_array], 
                        label: input_files[j].replace(/_|.csv/g," ")
                        });
        }

    }

    if (format === "slider") {

        steps = buttons;

    }

    var xstring = "$$" + cate_info["labels"][category] + "$$";
    var ystring = "$$ \\text{Frequency} [\\%] $$";
    var title_string = "$$ \\text{Frequency Histogram of }" + xstring.replace("$$"," ");

    var diff = max_x - min_x;

    if (format === "slider") {
        
        var layout = {
            font: {
                size: 15
            },
            sliders: [{
                pad: {t: 30},
                len: ((input_files.length)/12),
                steps: steps
            }],
            showlegend: false,
            title: title_string,
            yaxis: {
                title: ystring,
                range: [0, max_y]
            },
            xaxis: {
                title: xstring,
                range: [min_x-margin*diff, max_x+margin*diff]
            }
        };

    }

    if (format === "grid") {

        layout["font"] = {size: 15};
        layout["title"] = title_string;
        layout["showlegend"] = false;
        
        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [min_x-margin*diff, max_x+margin*diff];
            layout["yaxis"+(i+2)]["range"] = [0, max_y];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 15}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 15}}); 

    }

    if (format === "dropdown") {

        var layout = {
            font: {
                size: 15
            },
            title: title_string,
            showlegend: false,
            yaxis: {
                title: ystring,
                range: [0, max_y]
            },
            xaxis: {
                title: xstring, 
                range: [min_x-margin*diff, max_x+margin*diff]
            },
            updatemenus: [{
                y: 1, 
                yanchor: "top", 
                buttons: buttons
            }]
        }

    }

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Histogram by Stability

function hist_by_stab(all_results, input_files, category, vertloc, basecolor, nbins) {
    
    // Set up data
    var graphish = []; 
    var max_x = -Infinity;
    var min_x = Infinity;   
    var margin = 0.25; 

    var object1 = process_data(all_results, 0); 
    var object2 = edit_met_data(object1);

    var stab_conds, stab_cats, metdat;
    [stab_conds, stab_cats, metdat] = flag_stability(object2);

    var cate_info = get_catinfo(metdat);

    var varcol, vertlocs, a;
    [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

    var stab, stabloc, ind;
    [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
    var stabconds = get_stabconds();

    var colors = get_colors(stabconds.length, {basecolor: basecolor});


    for (var cond = 0; cond < stabconds.length; cond++) {

        var hist_data = [];
        for (var ii = 0; ii < metdat[varcol].length; ii++) {
            
            // until there is a faster way to remove these                        
            if ((metdat[stab][ii] === stabconds[cond]) && (parseFloat(metdat[varcol][ii]) != -999.0) && (metdat[varcol][ii] != null)) {
                hist_data.push(metdat[varcol][ii]);
            }

        }
        var maxdat = hist_data.filter(Boolean);

        if (Math.max(...maxdat) > max_x) {
            max_x = Math.max(...maxdat);
        }    

        if (Math.min(...maxdat) < min_x) {
            min_x = Math.min(...maxdat);
        }  

        var min_hist = Math.min(...hist_data);
        var max_hist = Math.max(...hist_data);        

        var trace = {
            x: hist_data,
            type: "histogram",
            xbins: {
                start: min_hist,
                end: max_hist,
                size: (max_hist - min_hist)/(nbins)
            },
            histnorm: "probability",
            showlegend: cond === 0,
            visible: cond === 0,
            marker: {
                color: colors[cond],
                line: {
                    width: 2
                }
            },
            name: stabconds[cond]
        };

        graphish = graphish.concat(trace);
    }

    var xstring = "$$" + cate_info["labels"][category] + "$$";
    var ystring = "$$ \\text{Frequency} [\\%] $$";
    var title_string = "$$ \\text{Frequency Histogram of }" + xstring.replace("$$"," ");

    var diff = max_x - min_x;

    var steps = [];
    for (var j = 0; j < stabconds.length; j++){
        // This array decides when to display a certain trace
        var false_array = [];

        for(var i = 0; i < stabconds.length; i++) {
            if (i == j) {
                false_array.push(true);
            } else {
                false_array.push(false);
            }  
        }
        
        steps.push({method: 'restyle', args: ['visible', false_array], 
                    label: stabconds[j]
                    });

    }

    var layout = {
        font: {
            size: 15
        },
        sliders: [{
            pad: {t: 30},
            len: ((stabconds.length)/12),
            steps: steps
        }],
        title: title_string,
        yaxis: {
            title: ystring,
            range: [0, 0.4]
        },
        xaxis: {
            title: xstring, 
            range: [min_x-margin*diff, max_x+margin*diff]
        }
    };

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Stacked Histogram by Stability

function stacked_hist_by_stab(all_results, input_files, category, vertloc, basecolor) {

    // Set up data
    var graphish = []; 
    var layout = {};
    var margin = 0.25;

    var object1 = process_data(all_results, 0); 
    var object2 = edit_met_data(object1);

    var stab_conds, stab_cats, metdat;
    [stab_conds, stab_cats, metdat] = flag_stability(object2);

    var cate_info = get_catinfo(metdat);

    var varcol, vertlocs, a;
    [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

    var stab, stabloc, ind;
    [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
    var stabconds = get_stabconds();

    var colors = get_colors(stabconds.length, {basecolor: basecolor});
    var max_mat = [];

    for (var cond = 0; cond < stabconds.length; cond++) {

        var hist_data = [];
        for (var ii = 0; ii < metdat[varcol].length; ii++) {
            
            // until there is a faster way to remove these                        
            if ((metdat[stab][ii] === stabconds[cond]) && (parseFloat(metdat[varcol][ii]) != -999.0) && (metdat[varcol][ii] != null)) {
                hist_data.push(metdat[varcol][ii]);
            }

        }     

        var trace = {
            x: hist_data,
            type: "histogram",
            histnorm: "probability",
            marker: {
                color: colors[cond],
                line: {
                    width: 2
                }
            },
            name: stabconds[cond]
        };

        graphish = graphish.concat(trace);
    }

    var xstring = "$$" + cate_info["labels"][category] + "$$";
    var ystring = "$$ \\text{Frequency} [\\%] $$";
    var title_string = "$$ \\text{Frequency Histogram of }" + xstring.replace("$$"," ");

    layout["font"] = {size: 15};
    layout["title"] =  title_string;
    layout["xaxis"] = {title: xstring};
    layout["yaxis"] = {title: ystring};
    //layout["hovermode"] = "closest";
    layout["barmode"] = "stack";

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Monthly Stacked Histogram by Stability

function monthly_stacked_hist_by_stab(all_results, input_files, category, vertloc, basecolor, format, rows, cols) {

    // Set up data
    var graphish = []; 
    var layout = {annotations: []};
    var max_x = -Infinity;
    var min_x = Infinity;
    var max_y = 2;
    var margin = 0.25;

    for(var j = 0; j < input_files.length; j++) {

        var object1 = process_data(all_results, j);    
        var object2 = edit_met_data(object1);

        var stab_conds, stab_cats, metdat;
        [stab_conds, stab_cats, metdat] = flag_stability(object2);

        var cate_info = get_catinfo(metdat);

        var varcol, vertlocs, a;
        [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

        var stab, stabloc, ind;
        [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
        var stabconds = get_stabconds();

        var colors = get_colors(stabconds.length, {basecolor: basecolor});

        for (var cond = 0; cond < stabconds.length; cond++) {

            var hist_data = [];
            for (var ii = 0; ii < metdat[varcol].length; ii++) {
                
                // until there is a faster way to remove these                        
                if ((metdat[stab][ii] === stabconds[cond]) && (parseFloat(metdat[varcol][ii]) != -999.0) && (metdat[varcol][ii] != null)) {
                    hist_data.push(metdat[varcol][ii]);
                }

            }
            var maxdat = hist_data.filter(Boolean);

            if (Math.max(...maxdat) > max_x) {
                max_x = Math.max(...maxdat);
            }    

            if (Math.min(...maxdat) < min_x) {
                min_x = Math.min(...maxdat);
            }    

            // var min_hist = Math.min(...hist_data);
            // var max_hist = Math.max(...hist_data);        
        
            if ((format === "dropdown") | (format === "slider")) {
                var trace = {
                    x: hist_data,
                    type: "histogram",
                    // xbins: {
                    //     start: min_hist,
                    //     end: max_hist,
                    //     size: (max_hist - min_hist)/(nbins)
                    // },
                    histnorm: "probability",
                    visible: j === 0,
                    showlegend: j === 0,
                    marker: {
                        color: colors[cond],
                        line: {
                            width: 2
                        }
                    },
                    name: stabconds[cond],
                };

                graphish = graphish.concat(trace);
            }

            if (format === "grid") {
                var trace = {
                    x: hist_data,
                    xaxis: "x" + (j+2),
                    yaxis: "y" + (j+2),
                    type: "histogram",
                    showlegend: j === 0,
                    // xbins: {
                    //     start: min_hist,
                    //     end: max_hist,
                    //     size: (max_hist - min_hist)/(nbins)
                    // },
                    histnorm: "probability",
                    marker: {
                        color: colors[cond],
                        line: {
                            width: 2
                        }
                    },
                    name: stabconds[cond],
                };

                graphish = graphish.concat(trace);
            }
        }

        if (format === "grid") {

            layout["yaxis" + (j+2)] = {
                domain: calcDomain_y(Math.floor(j/cols),rows)
            };

            layout["xaxis" + (j+2)] = {
                domain: calcDomain_x(j%cols,cols)
            };

        }

    }

    buttons = [];
    shapes = [];

    if ((format === "dropdown") | (format === "slider")) {

        for (var j = 0; j < input_files.length; j++){
            // This array decides when to display a certain trace
            false_array = [];

            for(var i = 0; i < input_files.length; i++) {
                if (i == j) {
                    for (var iah = 0; iah < stabconds.length; iah++) {
                        false_array.push(true);
                    }
                } else {
                    for (var iah = 0; iah < stabconds.length; iah++) {
                        false_array.push(false);
                    }
                }  
            }
            buttons.push({method: 'restyle', args: ['visible', false_array], 
                        label: input_files[j].replace(/_|.csv/g," ")
                        });
        }

    }

    if (format === "slider") {

        steps = buttons;

    }

    var xstring = "$$" + cate_info["labels"][category] + "$$";
    var ystring = "$$ \\text{Frequency} [\\%] $$";
    var title_string = "$$ \\text{Frequency Histogram of }" + xstring.replace("$$"," ");

    var diff = max_x - min_x;

    if (format === "slider") {
        
        var layout = {
            font: {
                size: 15
            },
            sliders: [{
                pad: {t: 30},
                len: ((input_files.length)/12),
                steps: steps
            }],
            //showlegend: false,
            barmode: "stack",
            title: title_string,
            yaxis: {
                title: ystring,
                range: [0, max_y]
            },
            xaxis: {
                title: xstring,
                range: [min_x-margin*diff, max_x+margin*diff]
            }
        };

    }

    if (format === "grid") {

        layout["font"] = {size: 15};
        layout["title"] = title_string;
        //layout["showlegend"] = false;
        layout["barmode"] = "stack";
        
        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [min_x-margin*diff, max_x+margin*diff];
            layout["yaxis"+(i+2)]["range"] = [0, max_y];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 15}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 15}}); 

    }

    if (format === "dropdown") {

        var layout = {
            font: {
                size: 15
            },
            title: title_string,
            //showlegend: false,
            barmode: "stack",
            yaxis: {
                title: ystring,
                range: [0, max_y]
            },
            xaxis: {
                title: xstring, 
                range: [min_x-margin*diff, max_x+margin*diff]
            },
            updatemenus: [{
                y: 1, 
                yanchor: "top", 
                buttons: buttons
            }]
        }

    }

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Normalized Histogram by Stability

function norm_hist_by_stab(all_results, input_files, vertloc, basecolor) {

    // Set up data
    var graphish = []; 
    var margin = 0.25;

    var object1 = process_data(all_results, 0);   
    var object2 = edit_met_data(object1);

    var stab_conds, stab_cats, metdat;
    [stab_conds, stab_cats, metdat] = flag_stability(object2);

    var cate_info = get_catinfo(metdat);
    console.log(cate_info);

    var stab, stabloc, ind;
    [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
    var stabconds = get_stabconds();

    var colors = get_colors(stabconds.length, {basecolor: basecolor});

    var all_dat = [[],[],[],[],[]];
    for (var cond = 0; cond < stabconds.length; cond++) {

        var plotdat = [];
        for (var hour = 0; hour < 24; hour++) {

            var array_temp = [];
            var array_temp = metdat[stab];
            var cond_array = [];
            
            for (var i = 0; i < array_temp.length; i += 1) {
                // until there is a faster way to remove these                      
                if ((parseInt(metdat["Date"][i].split(" ")[1].split(":")[0]) === hour) && (parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null) && (array_temp[i] === stabconds[cond])) {
                    cond_array.push(array_temp[i]);
                }
            }

            plotdat.push(cond_array.length/array_temp.length);
        }

        all_dat[cond].push(plotdat);

        var trace = {
            x: range(0,24,1),
            y: plotdat,
            type: "bar",
            marker: {
                color: colors[cond],
            },
            name: stabconds[cond]
        };

        graphish = graphish.concat(trace);

    }

    for (var hour = 0; hour < graphish[0]["y"].length; hour++) {

        var total = 0;
        for (var cond = 0; cond < graphish.length; cond++) {
            total += graphish[cond]["y"][hour];
        }
        for (var cond = 0; cond < graphish.length; cond++) {
            graphish[cond]["y"][hour] = graphish[cond]["y"][hour]*100/total;
        }

    }

    var xstring = "$$ \\text{Time of Day [Hour]} $$";
    var ystring = "$$ \\text{Probability of Stability} [\\%] $$";
    var title_string = "$$ \\text{Time of Day vs. Probability of Stability} $$";

    var layout = {
        font: {
            size: 15
        },
        "title": title_string,
        "xaxis": {
            title: xstring
        },
        "yaxis": {
            title: ystring
        },
        "barmode": "stack"
    };

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Normalized Monthly Histogram by Stability

function monthly_norm_hist_by_stab(all_results, input_files, vertloc, basecolor, format, rows, cols) {

    // Set up data
    var graphish_fin = []; 
    var layout = {annotations: []};
    var margin = 0.25;

    for (var j = 0; j < input_files.length; j++) {
        var graphish = [];

        var object1 = process_data(all_results, j);   
        var object2 = edit_met_data(object1);
    
        var stab_conds, stab_cats, metdat;
        [stab_conds, stab_cats, metdat] = flag_stability(object2);
        var cate_info = get_catinfo(metdat);
    
        var stab, stabloc, ind;
        [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
        var stabconds = get_stabconds();

        var colors = get_colors(stabconds.length, {basecolor: basecolor});
    
        var all_dat = [[],[],[],[],[]];
        for (var cond = 0; cond < stabconds.length; cond++) {
    
            var plotdat = [];
            for (var hour = 0; hour < 24; hour++) {
    
                var array_temp = [];
                var array_temp = metdat[stab];
                var cond_array = [];
                
                for (var i = 0; i < array_temp.length; i += 1) {
                    // until there is a faster way to remove these                      
                    if ((parseInt(metdat["Date"][i].split(" ")[1].split(":")[0]) === hour) && (parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null) && (array_temp[i] === stabconds[cond])) {
                        cond_array.push(array_temp[i]);
                    }
                }

                plotdat.push(cond_array.length/array_temp.length);
            }

            all_dat[cond].push(plotdat);

            if ((format === "dropdown") | (format === "slider")) {

                var trace = {
                    x: range(0,24,1),
                    y: plotdat,
                    type: "bar",
                    visible: j === 0,
                    marker: {
                        color: colors[cond],
                    },
                    name: stabconds[cond]
                };

                graphish = graphish.concat(trace);

            }

            if (format === "grid") {

                var trace = {
                    x: range(0,24,1),
                    y: plotdat,
                    xaxis: "x" + (j+2),
                    yaxis: "y" + (j+2),
                    type: "bar",
                    showlegend: j === 0,
                    marker: {
                        color: colors[cond],
                    },
                    name: stabconds[cond]
                };

                graphish = graphish.concat(trace);

            }
        }

        if (format === "grid") {

            layout["yaxis" + (j+2)] = {
                domain: calcDomain_y(Math.floor(j/cols),rows)
            };

            layout["xaxis" + (j+2)] = {
                domain: calcDomain_x(j%cols,cols)
            };

        }

        for (var hour = 0; hour < graphish[0]["y"].length; hour++) {

            var total = 0;
            for (var cond = 0; cond < graphish.length; cond++) {
                total += graphish[cond]["y"][hour];
            }
            for (var cond = 0; cond < graphish.length; cond++) {
                graphish[cond]["y"][hour] = graphish[cond]["y"][hour]*100/total;
            }
        }

        graphish_fin = graphish_fin.concat(graphish);

    }

    var buttons = [];
    var shapes = [];

    if ((format === "dropdown") | (format === "slider")) {

        for (var j = 0; j < input_files.length; j++){
            // This array decides when to display a certain trace
            false_array = [];

            for(var i = 0; i < input_files.length; i++) {
                if (i == j) {
                    for (var iah = 0; iah < stabconds.length; iah++) {
                        false_array.push(true);
                    }
                } else {
                    for (var iah = 0; iah < stabconds.length; iah++) {
                        false_array.push(false);
                    }
                }  
            }
            buttons.push({method: 'restyle', args: ['visible', false_array], 
                        label: input_files[j].replace(/_|.csv/g," ")
                        });
        }

    }

    if (format === "slider") {

        steps = buttons;

    }

    var xstring = "$$ \\text{Time of Day [Hour]} $$";
    var ystring = "$$ \\text{Probability of Stability} [\\%] $$";
    var title_string = "$$ \\text{Time of Day [Hour] vs. Probability of Stability} [\\%] $$";

    if (format === "slider") {
        
        var layout = {
            font: {
                size: 15
            },
            sliders: [{
                pad: {t: 30},
                len: ((input_files.length)/12),
                steps: steps
            }],
            barmode: "stack",
            title: title_string,
            yaxis: {
                title: ystring,
                range: [0, 100]
            },
            xaxis: {
                title: xstring,
                range: [-0.5, 23.5]
            }
        };

    }

    if (format === "grid") {

        layout["font"] = {size: 15};
        layout["title"] = title_string;
        //layout["showlegend"] = false;
        layout["barmode"] = "stack";
        
        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [-0.5, 23.5];
            layout["yaxis"+(i+2)]["range"] = [0, 100];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]+0.005, y: layout["yaxis"+(i+2)].domain[1]-0.14, textangle: 90,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 15}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 15}}); 

    }

    if (format === "dropdown") {

        var layout = {
            font: {
                size: 15
            },
            title: title_string,
            barmode: "stack",
            yaxis: {
                title: ystring,
                range: [0, 100]
            },
            xaxis: {
                title: xstring, 
                range: [-0.5, 23.5]
            },
            updatemenus: [{
                y: 1, 
                yanchor: "top", 
                buttons: buttons
            }]
        }

    }

    return [graphish_fin, layout];

}

// ///////////////////////////////////////////////////////////////