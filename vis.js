//import "convert-csv-to-json";

// Insert Documentation Here
//
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

// For multiple files
all_results = [];

// For multiple files (works for single also)
function parseData(createGraph, plot_type, category, month_list, {vertloc, range_length, format, row_select, col_select} = {}) {

    //for (var k = 0; k < input_files.length; k++) {
    for (var k = 0; k < month_list.length; k++) {
        Papa.parse(month_list[k], {
            download: true,

            complete: function(results) {
                all_results.push(results);

                if (all_results.length == month_list.length) {
                    createGraph(all_results, plot_type, category, month_list, {vertloc: vertloc, range_length: range_length, format: format, rows: row_select, cols: col_select})
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
    var directions = nsector;
    
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

    var plot_type = ["Cumulative Profile", "Stability Profile", "Hourly", "Rose Figure", "Wind Direction Scatter", "Stability Wind Direction Scatter"];    

    return plot_type;

}

function vertloc_plots() {

    var vertloc_plots = ["Stability Profile", "Rose Figure", "Wind Direction Scatter", "Stability Wind Direction Scatter"];

    return vertloc_plots;

}

function one_month_plots() {

    var one_month_plots = ["Stability Profile", "Stability Wind Direction Scatter"];

    return one_month_plots;

}

function element_select() {

    document.getElementById("plot_select").style.display = "inline"; 
    var plot_list = document.getElementById("plot_select");

    if (plot_list.options.length <= plot_types().length) {

        for (var plot = 0; plot < plot_types().length; plot++) {
            plot_list.options[plot_list.options.length] = new Option(plot_types()[plot],plot_types()[plot]);         
        }

    }  

    var plot_type = document.getElementById("plot_select").value;

    if (plot_type != 0) {

        document.getElementById("cat_select").style.display = "inline"; 
        var cat_list = document.getElementById("cat_select");

        if (cat_list.options.length <= categories_to_keep().length) {

            for (var cat = 0; cat < categories_to_keep().length; cat++) {
                cat_list.options[cat_list.options.length] = new Option(categories_to_keep()[cat],categories_to_keep()[cat]);         
            }

        }  

        var category = document.getElementById("cat_select").value;

        if (category != 0) {

            if (vertloc_plots().indexOf(plot_type) === -1) {

                vertloc = 999;
               
            } else {

                document.getElementById("vertloc_select").style.display = "inline"; 
                var vertloc = document.getElementById("vertloc_select").value;
 
            }

            if (vertloc != 0) {

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

                        document.getElementById("year_select").style.display = "inline";
                        document.getElementById("start").style.display = "inline"; 
                        document.getElementById("next").style.display = "none"; 
                        var select_year = document.getElementById("year_select").value;

                    }
                    
                    var month_final = document.getElementById("month_select").value;
                    var year_final = document.getElementById("year_select").value;

                    if ((month_final != 0) && (year_final != 0)) {

                        var input_file_string = year_final + "_" + month_final + ".csv";
                        var input_file_list = [];
                        input_file_list.push(input_file_string);

                        parseData(createGraph, plot_type, category, input_file_list, {vertloc: vertloc, range_length: range_length});

                    }

                }

                if (range_length === "multiple") {

                    document.getElementById("format_select").style.display = "inline";
                    var format = document.getElementById("format_select").value;

                    // Re-emerge everything
                    if (format != 0) {

                        document.getElementById("start_month_select").style.display = "inline"; 

                        if (document.getElementById("start_month_select").value != 0) {

                            document.getElementById("start_year_select").style.display = "inline"; 

                        }
                    
                        if (document.getElementById("start_year_select").value != 0) {

                            document.getElementById("end_month_select").style.display = "inline"; 

                        }
                            
                        if (document.getElementById("end_month_select").value != 0) {

                            document.getElementById("end_year_select").style.display = "inline"; 

                            if (format != "grid") {

                                document.getElementById("start").style.display = "inline"; 
                                document.getElementById("next").style.display = "none"; 

                            }

                        }
                            
                        if ((document.getElementById("end_year_select").value != 0) && (format === "grid")) {

                            document.getElementById("row_select").style.display = "inline"; 

                        }
                            
                        if ((document.getElementById("row_select").value != 0) && (format === "grid")) {

                            document.getElementById("col_select").style.display = "inline"; 
                            document.getElementById("start").style.display = "inline"; 
                            document.getElementById("next").style.display = "none"; 
                            
                            
                        }

                        var select_start_month = document.getElementById("start_month_select");
                        var start_year = document.getElementById("start_year_select").value;
                        var select_end_month = document.getElementById("end_month_select");
                        var end_year = document.getElementById("end_year_select").value;

                        if ((select_start_month.options.length <= monthnames().length) && (select_end_month.options.length <= monthnames().length)) {

                            for (var mon = 0; mon < monthnames().length; mon++) {
                                select_start_month.options[select_start_month.options.length] = new Option(monthnames()[mon],monthnames()[mon]);
                                select_end_month.options[select_end_month.options.length] = new Option(monthnames()[mon],monthnames()[mon]);            
                            }

                        }

                        if ((start_month != 0) && (start_year != 0) && (end_month != 0) && (end_year != 0)) {
                            
                            var start_month = document.getElementById("start_month_select").value;
                            var end_month = document.getElementById("end_month_select").value;
                            var month_list = get_file_range(String(start_month), parseInt(start_year), String(end_month), parseInt(end_year));

                        }
                            
                        if (format === "grid") {

                            if ((start_month != 0) && (start_year != 0) && (end_month != 0) && (end_year != 0)) {

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
                            }
                                
                            var row_select = document.getElementById("row_select").value;
                            var col_select = document.getElementById("col_select").value;

                            if ((row_select != 0) && (col_select != 0) && (start_month != 0) && (start_year != 0) && (end_month != 0) && (end_year != 0)) {

                                if (vertloc === 999) {

                                    parseData(createGraph, plot_type, category, month_list, {range_length: range_length, format: format, row_select: row_select, col_select: col_select});

                                } else {

                                    parseData(createGraph, plot_type, category, month_list, {range_length: range_length, vertloc: vertloc, format: format, row_select: row_select, col_select: col_select});

                                }

                            }

                        } else {

                            if ((start_month != 0) && (start_year != 0) && (end_month != 0) && (end_year != 0)) {

                                parseData(createGraph, plot_type, category, month_list, {vertloc: vertloc, range_length: range_length, format: format});

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
      
            if (quotient === Math.floor(quotient) && (i != 1) & (i != graph_total+1)){
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
function createGraph(all_results, plot_type, category, new_files, {vertloc, range_length, format, rows, cols} = {}) { 

    //var category = "speed";
    var basecolor = "span";
    //var vertloc = 80;
    //var format = "slider";

    if (plot_type === "Cumulative Profile") {

        [graphish, layout] = cumulative_prof(all_results, new_files, category, basecolor);

    }

    if (plot_type === "Stability Profile") {

        if (range_length === "one_month") {
            [graphish, layout] = stab_prof(all_results, new_files, category, vertloc, basecolor);
        }
        if (range_length === "multiple") {
            [graphish, layout] = monthly_stab_prof(all_results, new_files, category, vertloc, basecolor, format, rows, cols);
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
        // Rose_fig
        var bins = 6;
        var nsector = 32;
        var bin_arrange = "linear";

        [graphish, layout] = rose_fig(all_results, new_files, category, vertloc, basecolor, bins, bin_arrange, nsector);

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

    Plotly.newPlot("chart", graphish, layout)

}
    
// Reload the page if required
function reloadPage() {

    location.reload();

}

//parseData(createGraph,input_files)

///////////////////////////////////////////////////////////////

function process_data(all_results, j) {

    // Convert CSV to JSON ... need to create dynamic labels in
    // place of 7 and 10
    var arrays = all_results[j].data;
    var keys = arrays[7];
    var values = arrays.slice(10);
    console.log(keys);
    console.log(values);

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

        var colors = get_colors(input_files.length, {basecolor: basecolor});
            
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
        title: title_string,
        yaxis: {
            title: ystring
        },
        xaxis: {
            title: xstring,
            range: [min_x-0.5*diff, max_x+0.5*diff]
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
        title: title_string,
        yaxis: {
            title: ystring
        },
        xaxis: {
            title: xstring, 
            range: [min_x-0.5*diff, max_x+0.5*diff]
        },
        hovermode: "closest"
    };

    return [graphish, layout];

}

// ///////////////////////////////////////////////////////////////

// Monthly Stability Profile
// Any-month

function monthly_stab_prof(all_results, input_files, category, vertloc, basecolor, format, rows, cols) {
    // default: -,-,-,80,red,-,-,-

    // Set up data
    var graphish = []; 
    var max_x = -Infinity;
    var min_x = Infinity;
    var layout = {annotations: []};

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
                range: [min_x-0.5*diff, max_x+0.5*diff]
            },
            hovermode: "closest"
        };

    }

    if (format === "grid") {

        layout["title"] = title_string;
        layout["hovermode"] = "closest";
        
        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [min_x-0.5*diff, max_x+0.5*diff];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 12}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 12}}); 

        layout["xaxis"] = {title: xstring, range: [0, 1.1*max_x]};

    }

    if (format === "dropdown") {

        var layout = {
            title: title_string,
            yaxis: {
                title: ystring
            },
            xaxis: {
                title: xstring, 
                range: [min_x-0.5*diff, max_x+0.5*diff]
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
    xstring = "$$ \\text{Time [hour]} $$";
    ystring = "$$" + cate_info["labels"][category] + "$$";
    // need to add $$ for LaTeX to process
    title_string = "$$ " + " \\text{Time[hour] vs. "+ titleCase(category) + "} $$";
        
    var diff = max_y - min_y;

    var layout = {
        title: title_string,
        yaxis: {
            title: ystring,
            range: [min_y-0.5*diff, max_y+0.5*diff]
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
            sliders: [{
                pad: {t: 30},
                len: ((input_files.length)/12),
                steps: steps
            }],
            title: title_string,
            yaxis: {
                title: ystring,
                range: [min_y-0.5*diff, max_y+0.5*diff]
            },
            xaxis: {
                title: xstring, 
                range: [0, 24]
            }
        };

    }

    if (format === "grid") {

        layout["title"] = title_string;
        
        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [0, 24];
            layout["yaxis"+(i+2)]["range"] = [min_y-0.5*diff, max_y+0.5*diff];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 12}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 12}}); 

    }

    if (format === "dropdown") {

        var layout = {
            title: title_string,
            yaxis: {
                title: ystring,
                range: [min_y-0.5*diff, max_y+0.5*diff]
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

    var object1 = process_data(all_results, 0);
    var object2 = edit_met_data(object1);
    var cate_info = get_catinfo(object2);
    var metdat = object2;
    console.log(vertloc);

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
                    x: 0, y: 0, showarrow: false, font: {size: 12}}]
    }

    graphish = graphish.reverse();

    return [graphish, layout];

}


// ///////////////////////////////////////////////////////////////

// // Monthly Rose Fig

// // Set up data
// var vertloc = 87;
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
//                             showarrow: false, font: {size: 12}});
//     layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
//                             x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
//                             showarrow: false, font: {size: 12}}); 

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
    var exclude_angles = [46,228];
    var basecolor = "red";
    var graphish = []; 

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
                fillcolor: colors[basecolor][0], 
                opacity: 0.2, 
                line: {width: 0}
                });

    var xstring = "$$ Wind Direction [^\\circ] $$";
    var ystring = "$$" + cate_info["labels"][category] + "$$";
    var title_string = "$$ \\text{Wind Direction vs. }" + ystring.replace("$$","") + " $$";

    var layout = {
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
    var exclude_angles = [46,228];
    var basecolor = "cycle";
    var graphish = []; 
    var layout = {annotations: []};
    var max_y = -Infinity;
    var min_y = Infinity;

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
                        x0: exclude_angles[0], y0: 0, 
                        x1: exclude_angles[1], y1: max_y, 
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
                        x0: exclude_angles[0], y0: 0, 
                        x1: exclude_angles[1], y1: max_y, 
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
                range: [min_y-0.5*diff, max_y+0.5*diff]
            },
            xaxis: {
                title: xstring, 
                range: [0, 360]
            }
        };

    }

    if (format === "grid") {

        layout["title"] = title_string;
        layout["shapes"] = shapes;
        layout["hovermode"] = "closest";
        layout["showlegend"] = false;
        
        for(var i = 0; i < input_files.length; i++) {
            layout["xaxis"+(i+2)]["range"] = [0, 360];
            layout["yaxis"+(i+2)]["range"] = [min_y-0.5*diff, max_y+0.5*diff];
            layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
                                    x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
                                    showarrow: true, arrowhead: 0, ax: 0, ay: 0});
        }
        layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
                                x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
                                showarrow: false, font: {size: 12}});
        layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
                                x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
                                showarrow: false, font: {size: 12}}); 

    }

    if (format === "dropdown") {

        var layout = {
            title: title_string,
            hovermode: "closest",
            showlegend: false,
            yaxis: {
                title: ystring,
                range: [min_y-0.5*diff, max_y+0.5*diff]
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
    var colors = get_colors(stabconds.length, {basecolor: basecolor});

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
                    color: colors[cond]
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
                    color: colors[cond]
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

    if (one_plot) {

        var layout = {
            shapes: [{type: "rect", xref: "paper", yref: "paper", 
                    x0: (exclude_angles[0]/360), y0: 0, 
                    x1: (exclude_angles[1]/360), y1: 1, 
                    fillcolor: colors[j], 
                    opacity: 0.2/stabconds.length, 
                    line: {width: 0}
            }],
            hovermode: "closest",
            showlegend: true,
            title: title_string,
            yaxis: {
                title: ystring,
                range: [min_y-0.5*diff, max_y+0.5*diff]
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
                        fillcolor: colors[j], 
                        opacity: 0.2/stabconds.length, 
                        line: {width: 0}
                        });
        }

        var layout = {
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
                range: [min_y-0.5*diff, max_y+0.5*diff]
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

// // Groupby Winddir Scatter 

// // Set up data
// var vertloc = 87;
// var nbins = 5;
// var category = "ti";
// var abscissa = "speed";
// var group_by = "turbulent kinetic energy";
// var basecolor = "span";
// var graphish = []; 

// // Convert CSV to JSON ... need to create dynamic labels in
// // place of 7 and 10
// var arrays = all_results[0].data;
// var keys = arrays[7];
// var values = arrays.slice(10);

// var object1 = new Object();
// // remove -1 in code with QC data
// for (k = 0; k < (keys.length-1); k++) {
//     var new_values = [];
//     for (v = 0; v < values.length; v++) {
//         new_values.push(values[v][k]);
//     }
//     if (Object.keys(object1).indexOf(keys[k]) == -1) {
//         object1[keys[k]] = new_values;
//     } else {
//         object1[keys[k]+"_adv"] = new_values;
//     }
// }       

// var object2 = edit_met_data(object1);
// var cate_info = get_catinfo(object2);
// //[stab_conds, stab_cats, metdat] = flag_stability(object2);
// //var cate_info = get_catinfo(metdat);
// var metdat = object2;

// var varcol, vertlocs, groupcol, abscol, a, b, c, d, e;
// [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});
// [groupcol, b, c] = get_vertical_locations(cate_info["columns"][group_by], {location: vertloc});
// [abscol, d, e] = get_vertical_locations(cate_info["columns"][abscissa], {location: vertloc});

// var colors = get_colors(nbins, {basecolor: basecolor});

// var data_temp = metdat[groupcol];
// var test_mat = [];
// for (var i = 0; i < data_temp.length; i += 1) {
//     // until there is a faster way to remove these                        
//     if ((parseFloat(data_temp[i]) != -999.0) && (data_temp[i] != null)) {
//         test_mat.push(data_temp[i]);
//     }
// }

// var test_val = test_mat.sort(function(a, b) {return a - b;});
// var temp = [], i;
// for (i = 0; i < test_val.length; i += test_val.length/nbins) {
//     temp.push(test_val.slice(i, i + test_val.length/nbins));
// }

// var bounds = {};
// for (var leng = 0; leng < temp.length; leng++) {
//     bounds[""+leng] = [];
//     bounds[""+leng].push(temp[leng][0]);
//     bounds[""+leng].push(temp[leng][temp[leng].length-1]);
// }

// for (var bd = 0; bd < Object.keys(bounds).length; bd++) {
//     x_dat = [];
//     y_dat = [];
//     for (var datlen = 0; datlen < metdat[abscol].length; datlen++) {
//         var x = parseFloat(metdat[abscol][datlen]);
//         var y = parseFloat(metdat[varcol][datlen]);
//         var f = parseFloat(metdat[groupcol][datlen]);
        
//         if ((x != -999.0) && (isNaN(x) === false) && (y != -999.0) && (isNaN(y) === false) && (f >= parseFloat(bounds[""+bd][0])) && (f <= parseFloat(bounds[""+bd][1]))) {

//             x_dat.push(x);
//             y_dat.push(y);

//         }
//     }

//     var trace = {
//         x: x_dat,
//         y: y_dat,
//         mode: "markers",
//         name: "[" + bounds[""+bd][0] + ":" + bounds[""+bd][1] + "]",
//         marker: {
//             color: colors[bd]
//         }
//     }

//     graphish = graphish.concat(trace);
// }

// // Set title and labels
// title_string = "$$ \\text{Vertical Location = }" + vertloc + "\\text{m, Grouped by: }" + cate_info["labels"][group_by] + "$$";
// //x_string = cate_info["labels"][abscissa];
// x_string = "$$ " + cate_info["labels"][abscissa] + " $$";
// y_string = "$$ " + cate_info["labels"][category] + " $$";

// var layout = {
//     title: title_string,
//     xaxis: {
//         title: x_string
//     },
//     yaxis: {
//         title: y_string
//     },
//     hovermode: "closest"
// }

// Plotly.newPlot("chart", graphish, layout)

// if (graphish.length < nbins) {
//     alert("It appears there is missing data, some traces are missing.");
// } 

// ///////////////////////////////////////////////////////////////

// // Monthly Groupby Winddir Scatter 

// // Set up data
// var vertloc = 100;
// var nbins = 5;
// var category = "ti";
// var abscissa = "speed";
// var group_by = "turbulent kinetic energy";
// var basecolor = "span";
// var graphish = []; 
// var max_x = 0;
// var max_y = 0;
// var format = "grid";
// var layout = {annotations: []};
// var full_mat = []; 
// var met_obj = {};

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

//     var varcol, vertlocs, groupcol, abscol, a, b, c, d, e;
//     [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});
//     [groupcol, b, c] = get_vertical_locations(cate_info["columns"][group_by], {location: vertloc});
//     [abscol, d, e] = get_vertical_locations(cate_info["columns"][abscissa], {location: vertloc});

//     var colors = get_colors(nbins, {basecolor: basecolor});

//     var data_temp = metdat[groupcol];
//     for (var i = 0; i < data_temp.length; i += 1) {
//         // until there is a faster way to remove these                        
//         if ((parseFloat(data_temp[i]) != -999.0) && (data_temp[i] != null)) {
//             full_mat.push(data_temp[i]);
//         }
//     }

//     met_obj[""+j] = metdat;
// }

// var test_val = full_mat.sort(function(a, b) {return a - b;});
// var temp = [], i;
// for (i = 0; i < test_val.length; i += test_val.length/nbins) {
//     temp.push(test_val.slice(i, i + test_val.length/nbins));
// }

// var bounds = {};
// for (var leng = 0; leng < temp.length; leng++) {
//     bounds[""+leng] = [];
//     bounds[""+leng].push(temp[leng][0]);
//     bounds[""+leng].push(temp[leng][temp[leng].length-1]);
// }

// for (var j = 0; j < input_files.length; j++) {
//     for (var bd = 0; bd < Object.keys(bounds).length; bd++) {
//         x_dat = [];
//         y_dat = [];
//         var metdat = met_obj[""+j];
//         for (var datlen = 0; datlen < metdat[abscol].length; datlen++) {
//             var x = parseFloat(metdat[abscol][datlen]);
//             var y = parseFloat(metdat[varcol][datlen]);
//             var f = parseFloat(metdat[groupcol][datlen]);
            
//             if ((x != -999.0) && (isNaN(x) === false) && (y != -999.0) && (isNaN(y) === false) && (f >= parseFloat(bounds[""+bd][0])) && (f <= parseFloat(bounds[""+bd][1]))) {

//                 x_dat.push(x);
//                 y_dat.push(y);

//             }
//         }

//         if (Math.max(...x_dat) > max_x) {
//             max_x = Math.max(...x_dat)
//         }

//         if (Math.max(...y_dat) > max_y) {
//             max_y = Math.max(...y_dat)
//         }

//         if ((format === "dropdown") | (format === "slider")) {

//             var trace = {
//                 x: x_dat,
//                 y: y_dat,
//                 mode: "markers",
//                 name: "[" + bounds[""+bd][0] + ":" + bounds[""+bd][1] + "]",
//                 marker: {
//                     color: colors[bd]
//                 },
//                 visible: j === 0
//             };
//             graphish = graphish.concat(trace);

//         }

//         if (format === "grid") {
            
//             var trace = {
//                 x: x_dat,
//                 y: y_dat,
//                 xaxis: "x"+(j+2),
//                 yaxis: "y"+(j+2),
//                 mode: "markers",
//                 name: "[" + bounds[""+bd][0] + ":" + bounds[""+bd][1] + "]",
//                 marker: {
//                     color: colors[bd]
//                 },
//                 showlegend: j === 0
//             };
//             graphish = graphish.concat(trace);

//         }
//     }

//     if (format === "grid") {

//         layout["yaxis" + (j+2)] = {
//             domain: calcDomain_y(Math.floor(j/4),3)
//         };

//         layout["xaxis" + (j+2)] = {
//             domain: calcDomain_x(j%4,4)
//         };

//     }   
// }

// buttons = [];
// shapes = [];

// if ((format === "dropdown") | (format === "slider")) {

//     for (var j = 0; j < input_files.length; j++){
//         // This array decides when to display a certain trace
//         false_array = [];

//         for(var i = 0; i < input_files.length; i++) {
//             if (i == j) {
//                 for (var iah = 0; iah < nbins; iah++) {
//                     false_array.push(true);
//                 }
//             } else {
//                 for (var iah = 0; iah < nbins; iah++) {
//                     false_array.push(false);
//                 }
//             }  
//         }
//         buttons.push({method: 'restyle', args: ['visible', false_array], 
//                       label: input_files[j].replace(/_|.csv/g," ")
//                     });
//     }

// }

// if (format === "slider") {

//     steps = buttons;

// }

// // Set title and labels
// title_string = "$$ \\text{Vertical Location = }" + vertloc + "\\text{m, Grouped by: }" + cate_info["labels"][group_by] + "$$";
// x_string = "$$ " + cate_info["labels"][abscissa] + " $$";
// y_string = "$$ " + cate_info["labels"][category] + " $$";

// if (format === "slider") {
    
//     var layout = {
//         sliders: [{
//             pad: {t: 30},
//             len: ((input_files.length)/12),
//             steps: steps
//         }],
//         title: title_string,
//         yaxis: {
//             title: y_string,
//             range: [0, 1.1*max_y]
//         },
//         xaxis: {
//             //ticks: false,
//             title: x_string,
//             range: [0, 1.1*max_x]
//         },
//         hovermode: "closest"
//     };

// }

// if (format === "grid") {

//     layout["title"] = title_string;
//     layout["hovermode"] = "closest";
//     // possible fix if other than 12 month periods
//     index_mat = [8,9,10,11];
    
//     for(var i = 0; i < input_files.length; i++) {
//         layout["xaxis"+(i+2)]["range"] = [0, 1.1*max_x];
//         layout["yaxis"+(i+2)]["range"] = [0, 1.1*max_y];
//         if (index_mat.indexOf(i) < 0) {
//             layout["xaxis"+(i+2)]["anchor"] = "x"+(index_mat[i%3]);
//         }
//         // } else {
//         //     layout["xaxis"+(i+2)]["anchor"] = false;
//         // }
        

//         layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
//                                 x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
//                                 showarrow: true, arrowhead: 0, ax: 0, ay: 0});
//     }
//     layout.annotations.push({text: x_string, xref: "paper", yref: "paper",
//                             x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
//                             showarrow: false, font: {size: 12}});
//     layout.annotations.push({text: y_string, xref: "paper", yref: "paper",
//                             x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
//                             showarrow: false, font: {size: 12}}); 

// }

// if (format === "dropdown") {

//     var layout = {
//         title: title_string,
//         yaxis: {
//             title: y_string,
//             range: [0, 1.1*max_y]
//         },
//         xaxis: {
//             title: x_string, 
//             range: [0, 1.1*max_x]
//         },
//         updatemenus: [{
//             y: 1, 
//             yanchor: "top", 
//             buttons: buttons
//         }],
//         hovermode: "closest"
//     }

// }

// Plotly.newPlot("chart", graphish, layout)

// if (graphish.length < nbins*input_files.length) {
//     alert("It appears there is missing data, some traces are missing.");
// } 

// ///////////////////////////////////////////////////////////////

// // Histogram

// // Set up data
// var vertloc = 80;
// var category = "speed";
// var basecolor = "blue";
// var graphish = []; 
// var curvefit = "Weibull";
// var layout = {annotations: []};

// // Convert CSV to JSON ... need to create dynamic labels in
// // place of 7 and 10
// var arrays = all_results[0].data;
// var keys = arrays[7];
// var values = arrays.slice(10);

// var object1 = new Object();
// // remove -1 in code with QC data
// for (k = 0; k < (keys.length-1); k++) {
//     var new_values = [];
//     for (v = 0; v < values.length; v++) {
//         new_values.push(values[v][k]);
//     }
//     if (Object.keys(object1).indexOf(keys[k]) == -1) {
//         object1[keys[k]] = new_values;
//     } else {
//         object1[keys[k]+"_adv"] = new_values;
//     }
// }       

// var object2 = edit_met_data(object1);
// var cate_info = get_catinfo(object2);

// var varcol, vertlocs, a;
// [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

// var hist_data = object2[varcol];

// var min_hist = Math.min(...hist_data);
// var max_hist = Math.max(...hist_data);
// var filt_dat = hist_data.filter(Boolean);
// var sum = 0;
// for( var i = 0; i < filt_dat.length; i++ ){
//     sum += parseFloat(filt_dat[i]);
// }
// var mean = sum/filt_dat.length;

// var colors = get_nrelcolors();
// var nbins = 35;

// if (curvefit != "None") {

//     var k = 0;
//     var l = 0;

//     if (curvefit === "Exponential") {

//         k = 1;

//     }

//     if (curvefit === "Rayleigh") {

//         k = 2;

//     }

//     if (curvefit === "Lognormal") {

//         k = 2.5;

//     }

//     if (curvefit === "Normal") {

//         k = 3.6;

//     }

//     if (curvefit === "Weibull") {

//         var variance = 0;
//         var n = filt_dat.length;
//         var v1 = 0;
//         var v2 = 0;

//         if (n != 1) {

//             for (var i = 0; i < n; i++) {
//                 v1 = v1 + (filt_dat[i] - mean) * (filt_dat[i] - mean);
//                 v2 = v2 + (filt_dat[i] - mean);
//             }

//             v2 = v2 * v2 / n;
//             variance = (v1 - v2) / (n-1);

//             if (variance < 0) { 
//                 variance = 0; 
//             }
    
//             std_dev = Math.sqrt(variance);

//         }

//         k = Math.pow((0.9874/(std_dev/mean)),1.0983);

//     }            

//     var arg = 1/k;
//     l = mean / ((Math.sqrt(2*Math.PI*arg))*(Math.pow((arg/Math.E),arg)));

//     var xdat = [];
//     var ydat = [];
//     for (var iter = min_hist; iter < max_hist; iter += ((max_hist-min_hist)/1000)) {
//         xdat.push(iter);
//         var wb = (k/l)*(Math.pow((iter/l),k-1))*Math.pow(Math.E,-Math.pow((iter/l),k));
//         ydat.push(wb);
//     }

//     var trace_cv = {
//         x: xdat,
//         y: ydat,
//         mode: "lines",
//         line: {
//             color: "rgb(0, 0, 0)"
//         },
//         name: curvefit,
//     };

//     graphish = graphish.concat(trace_cv);

//     layout["annotations"].push({text: "Shape Parameter: " + k.toFixed(2), xref: "paper", yref: "paper",
//                                 x: 0.9, y: 0.9, showarrow: false, font: {size: 16}}); 

//     layout["annotations"].push({text: "Scale Parameter: " + l.toFixed(2), xref: "paper", yref: "paper",
//                                 x: 0.9, y: 0.8, showarrow: false, font: {size: 16}});                                     

// }

// var trace = {
//     x: hist_data,
//     type: "histogram",
//     xbins: {
//         start: min_hist,
//         end: max_hist,
//         size: (max_hist - min_hist)/(nbins)
//     },
//     histnorm: "probability",
//     marker: {
//         color: colors[basecolor][0],
//         line: {
//             width: 2
//         }
//     },
//     name: input_files[0].split("_")[1].split(".")[0],
// };

// graphish = graphish.concat(trace);

// xstring = "$$" + cate_info["labels"][category] + "$$";
// ystring = "$$ \\text{Frequency} [\\%] $$";
// title_string = "$$ \\text{Frequency Histogram of_}" + xstring.replace("$$"," ");

// layout["title"] =  title_string;
// layout["xaxis"] = {title: xstring};
// layout["yaxis"] = {title: ystring};
// layout["hovermode"] = "closest";

// Plotly.newPlot("chart", graphish, layout)

// ///////////////////////////////////////////////////////////////

// // Monthly Histogram

// // Set up data
// var vertloc = 87;
// var category = "speed";
// var basecolor = "blue";
// var graphish = []; 
// var max_x = 0;
// var layout = {annotations: []};
// var nbins = 35;
// var max_y = 0.3;

// // User input
// var format = "grid";

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

//     var varcol, vertlocs, a;
//     [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

//     var hist_data = object2[varcol];
    
//     var colors = get_colors(input_files.length, {basecolor: basecolor});
    

//     if (Math.max(...hist_data) > max_x) {
//         max_x = Math.max(...hist_data);
//     }

//     if ((format === "dropdown") | (format === "slider")) {

//         var trace = {
//             x: hist_data,
//             type: "histogram",
//             xbins: {
//                 start: Math.min(...hist_data),
//                 end: Math.max(...hist_data),
//                 size: (Math.max(...hist_data) - Math.min(...hist_data))/(nbins)
//             },
//             histnorm: "probability",
//             marker: {
//                 color: colors[j],
//                 line: {
//                     width: 2
//                 }
//             },
//             name: input_files[j].split("_")[1].split(".")[0],
//             visible: j === 0
//         };
//         graphish = graphish.concat(trace);

//     }

//     if (format === "grid") {
        
//         var trace = {
//             x: hist_data,
//             xaxis: "x" + (j+2),
//             yaxis: "y" + (j+2),
//             type: "histogram",
//             xbins: {
//                 start: Math.min(...hist_data),
//                 end: Math.max(...hist_data),
//                 size: (Math.max(...hist_data) - Math.min(...hist_data))/(nbins)
//             },
//             histnorm: "probability",
//             marker: {
//                 color: colors[j],
//                 line: {
//                     width: 2
//                 }
//             },
//             name: input_files[j].split("_")[1].split(".")[0],
//         };
//         graphish = graphish.concat(trace);

//     }

//     if (format === "grid") {

//         layout["yaxis" + (j+2)] = {
//             domain: calcDomain_y(Math.floor(j/4),3)
//         };

//         layout["xaxis" + (j+2)] = {
//             domain: calcDomain_x(j%4,4)
//         };

//     }        

// }

// buttons = [];
// shapes = [];

// if ((format === "dropdown") | (format === "slider")) {

//     for (var j = 0; j < input_files.length; j++){
//         // This array decides when to display a certain trace
//         false_array = [];

//         for(var i = 0; i < input_files.length; i++) {
//             if (i == j) {
//                 false_array.push(true);
//             } else {
//                 false_array.push(false);
//             }  
//         }
//         buttons.push({method: 'restyle', args: ['visible', false_array], 
//                       label: input_files[j].replace(/_|.csv/g," ")
//                     });
//     }

// }

// if (format === "slider") {

//     steps = buttons;

// }

// xstring = "$$" + cate_info["labels"][category] + "$$";
// ystring = "$$ \\text{Frequency} [\\%] $$";
// title_string = "$$ \\text{Frequency Histogram of_}" + xstring.replace("$$"," ");

// if (format === "slider") {
    
//     var layout = {
//         sliders: [{
//             pad: {t: 30},
//             len: ((input_files.length)/12),
//             steps: steps
//         }],
//         showlegend: false,
//         title: title_string,
//         yaxis: {
//             title: ystring,
//             range: [0, max_y]
//         },
//         xaxis: {
//             title: xstring,
//             range: [0, 1.1*max_x]
//         }
//     };

// }

// if (format === "grid") {

//     layout["title"] = title_string;
//     layout["showlegend"] = false;
    
//     for(var i = 0; i < input_files.length; i++) {
//         layout["xaxis"+(i+2)]["range"] = [0, 1.1*max_x];
//         layout["yaxis"+(i+2)]["range"] = [0, max_y];
//         layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
//                                 x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
//                                 showarrow: true, arrowhead: 0, ax: 0, ay: 0});
//     }
//     layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
//                             x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
//                             showarrow: false, font: {size: 12}});
//     layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
//                             x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
//                             showarrow: false, font: {size: 12}}); 

// }

// if (format === "dropdown") {

//     var layout = {
//         title: title_string,
//         showlegend: false,
//         yaxis: {
//             title: ystring,
//             range: [0, max_y]
//         },
//         xaxis: {
//             title: xstring, 
//             range: [0, 1.1*max_x]
//         },
//         updatemenus: [{
//             y: 1, 
//             yanchor: "top", 
//             buttons: buttons
//         }]
//     }

// }

// Plotly.newPlot("chart", graphish, layout)

// ///////////////////////////////////////////////////////////////

// // Histogram by Stability

// // Set up data
// var vertloc = 87;
// var category = "speed";
// var basecolor = "span";
// var graphish = []; 
// // var curvefit = "Weibull";
// // var layout = {annotations: []};

// // Convert CSV to JSON ... need to create dynamic labels in
// // place of 7 and 10
// var arrays = all_results[0].data;
// var keys = arrays[7];
// var values = arrays.slice(10);

// var object1 = new Object();
// // remove -1 in code with QC data
// for (k = 0; k < (keys.length-1); k++) {
//     var new_values = [];
//     for (v = 0; v < values.length; v++) {
//         new_values.push(values[v][k]);
//     }
//     if (Object.keys(object1).indexOf(keys[k]) == -1) {
//         object1[keys[k]] = new_values;
//     } else {
//         object1[keys[k]+"_adv"] = new_values;
//     }
// }       

// var object2 = edit_met_data(object1);

// var stab_conds, stab_cats, metdat;
// [stab_conds, stab_cats, metdat] = flag_stability(object2);

// var cate_info = get_catinfo(metdat);

// var varcol, vertlocs, a;
// [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

// var stab, stabloc, ind;
// [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
// var stabconds = get_stabconds();

// var colors = get_colors(stabconds.length, {basecolor: basecolor});
// var nbins = 35;
// var max_x = 0;

// for (var cond = 0; cond < stabconds.length; cond++) {

//     var hist_data = [];
//     for (var ii = 0; ii < metdat[varcol].length; ii++) {
        
//         // until there is a faster way to remove these                        
//         if ((metdat[stab][ii] === stabconds[cond]) && (parseFloat(metdat[varcol][ii]) != -999.0) && (metdat[varcol][ii] != null)) {
//             hist_data.push(metdat[varcol][ii]);
//         }

//     }
//     var maxdat = hist_data.filter(Boolean);

//     if (Math.max(...maxdat) > max_x) {
//         max_x = Math.max(...maxdat);
//     }    

//     var min_hist = Math.min(...hist_data);
//     var max_hist = Math.max(...hist_data);        

//     var trace = {
//         x: hist_data,
//         type: "histogram",
//         xbins: {
//             start: min_hist,
//             end: max_hist,
//             size: (max_hist - min_hist)/(nbins)
//         },
//         histnorm: "probability",
//         showlegend: cond === 0,
//         visible: cond === 0,
//         marker: {
//             color: colors[cond],
//             line: {
//                 width: 2
//             }
//         },
//         name: stabconds[cond]
//     };

//     graphish = graphish.concat(trace);
// }

// xstring = "$$" + cate_info["labels"][category] + "$$";
// ystring = "$$ \\text{Frequency} [\\%] $$";
// title_string = "$$ \\text{Frequency Histogram of_}" + xstring.replace("$$"," ");

// var steps = [];
// for (var j = 0; j < stabconds.length; j++){
//     // This array decides when to display a certain trace
//     var false_array = [];

//     for(var i = 0; i < stabconds.length; i++) {
//         if (i == j) {
//             false_array.push(true);
//         } else {
//             false_array.push(false);
//         }  
//     }
    
//     steps.push({method: 'restyle', args: ['visible', false_array], 
//                 label: stabconds[j]
//                 });

// }

// var layout = {
//     sliders: [{
//         pad: {t: 30},
//         len: ((stabconds.length)/12),
//         steps: steps
//     }],
//     title: title_string,
//     yaxis: {
//         title: ystring,
//         range: [0, 0.4]
//     },
//     xaxis: {
//         title: xstring, 
//         range: [0, 1.1*max_x]
//     }
// };

// Plotly.newPlot("chart", graphish, layout)

// ///////////////////////////////////////////////////////////////

// // Stacked Histogram by Stability

// // Set up data
// var vertloc = 87;
// var category = "speed";
// var basecolor = "span";
// var graphish = []; 
// // var curvefit = "Weibull";
// // var layout = {annotations: []};

// // Convert CSV to JSON ... need to create dynamic labels in
// // place of 7 and 10
// var arrays = all_results[0].data;
// var keys = arrays[7];
// var values = arrays.slice(10);

// var object1 = new Object();
// // remove -1 in code with QC data
// for (k = 0; k < (keys.length-1); k++) {
//     var new_values = [];
//     for (v = 0; v < values.length; v++) {
//         new_values.push(values[v][k]);
//     }
//     if (Object.keys(object1).indexOf(keys[k]) == -1) {
//         object1[keys[k]] = new_values;
//     } else {
//         object1[keys[k]+"_adv"] = new_values;
//     }
// }       

// var object2 = edit_met_data(object1);

// var stab_conds, stab_cats, metdat;
// [stab_conds, stab_cats, metdat] = flag_stability(object2);

// var cate_info = get_catinfo(metdat);

// var varcol, vertlocs, a;
// [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

// var stab, stabloc, ind;
// [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
// var stabconds = get_stabconds();

// var colors = get_colors(stabconds.length, {basecolor: basecolor});
// // var nbins = 35;
// var max_mat = [];

// for (var cond = 0; cond < stabconds.length; cond++) {

//     var hist_data = [];
//     for (var ii = 0; ii < metdat[varcol].length; ii++) {
        
//         // until there is a faster way to remove these                        
//         if ((metdat[stab][ii] === stabconds[cond]) && (parseFloat(metdat[varcol][ii]) != -999.0) && (metdat[varcol][ii] != null)) {
//             hist_data.push(metdat[varcol][ii]);
//         }

//     }
//     // var maxdat = plotdat.filter(Boolean);

//     // if (Math.max(...maxdat) > max_y) {
//     //     max_mat[cond].push(Math.max(...maxdat));
//     // }    

//     // var min_hist = Math.min(...hist_data);
//     // var max_hist = Math.max(...hist_data);        

//     var trace = {
//         x: hist_data,
//         type: "histogram",
//         // xbins: {
//         //     start: min_hist,
//         //     end: max_hist,
//         //     size: (max_hist - min_hist)/(nbins)
//         // },
//         histnorm: "probability",
//         marker: {
//             color: colors[cond],
//             line: {
//                 width: 2
//             }
//         },
//         name: stabconds[cond]
//     };

//     graphish = graphish.concat(trace);
// }

// xstring = "$$" + cate_info["labels"][category] + "$$";
// ystring = "$$ \\text{Frequency} [\\%] $$";
// title_string = "$$ \\text{Frequency Histogram of_}" + xstring.replace("$$"," ");

// layout["title"] =  title_string;
// layout["xaxis"] = {title: xstring};
// layout["yaxis"] = {title: ystring};
// //layout["hovermode"] = "closest";
// layout["barmode"] = "stack";

// console.log(graphish);

// Plotly.newPlot("chart", graphish, layout)

// ///////////////////////////////////////////////////////////////

// // Monthly Stacked Histogram by Stability

// // Set up data
// var vertloc = 87;
// var category = "speed";
// var basecolor = "span";
// var graphish = []; 
// // var curvefit = "Weibull";
// var layout = {annotations: []};
// var format = "grid";
// var max_x = 0;
// var max_y = 2;

// for(var j = 0; j < input_files.length; j++) {
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

//     var stab_conds, stab_cats, metdat;
//     [stab_conds, stab_cats, metdat] = flag_stability(object2);

//     var cate_info = get_catinfo(metdat);

//     var varcol, vertlocs, a;
//     [varcol, vertlocs, a] = get_vertical_locations(cate_info["columns"][category], {location: vertloc});

//     var stab, stabloc, ind;
//     [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
//     var stabconds = get_stabconds();

//     var colors = get_colors(stabconds.length, {basecolor: basecolor});
//     // var nbins = 35;

//     for (var cond = 0; cond < stabconds.length; cond++) {

//         var hist_data = [];
//         for (var ii = 0; ii < metdat[varcol].length; ii++) {
            
//             // until there is a faster way to remove these                        
//             if ((metdat[stab][ii] === stabconds[cond]) && (parseFloat(metdat[varcol][ii]) != -999.0) && (metdat[varcol][ii] != null)) {
//                 hist_data.push(metdat[varcol][ii]);
//             }

//         }
//         var maxdat = hist_data.filter(Boolean);

//         if (Math.max(...maxdat) > max_x) {
//             max_x = Math.max(...maxdat);
//         }    

//         // var min_hist = Math.min(...hist_data);
//         // var max_hist = Math.max(...hist_data);        
    
//         if ((format === "dropdown") | (format === "slider")) {
//             var trace = {
//                 x: hist_data,
//                 type: "histogram",
//                 // xbins: {
//                 //     start: min_hist,
//                 //     end: max_hist,
//                 //     size: (max_hist - min_hist)/(nbins)
//                 // },
//                 histnorm: "probability",
//                 visible: j === 0,
//                 showlegend: j === 0,
//                 marker: {
//                     color: colors[cond],
//                     line: {
//                         width: 2
//                     }
//                 },
//                 name: stabconds[cond],
//             };

//             graphish = graphish.concat(trace);
//         }

//         if (format === "grid") {
//             var trace = {
//                 x: hist_data,
//                 xaxis: "x" + (j+2),
//                 yaxis: "y" + (j+2),
//                 type: "histogram",
//                 showlegend: j === 0,
//                 // xbins: {
//                 //     start: min_hist,
//                 //     end: max_hist,
//                 //     size: (max_hist - min_hist)/(nbins)
//                 // },
//                 histnorm: "probability",
//                 marker: {
//                     color: colors[cond],
//                     line: {
//                         width: 2
//                     }
//                 },
//                 name: stabconds[cond],
//             };

//             graphish = graphish.concat(trace);
//         }
//     }

//     if (format === "grid") {

//         layout["yaxis" + (j+2)] = {
//             domain: calcDomain_y(Math.floor(j/4),3)
//         };

//         layout["xaxis" + (j+2)] = {
//             domain: calcDomain_x(j%4,4)
//         };

//     }  

// }

// buttons = [];
// shapes = [];

// if ((format === "dropdown") | (format === "slider")) {

//     for (var j = 0; j < input_files.length; j++){
//         // This array decides when to display a certain trace
//         false_array = [];

//         for(var i = 0; i < input_files.length; i++) {
//             if (i == j) {
//                 for (var iah = 0; iah < stabconds.length; iah++) {
//                     false_array.push(true);
//                 }
//             } else {
//                 for (var iah = 0; iah < stabconds.length; iah++) {
//                     false_array.push(false);
//                 }
//             }  
//         }
//         buttons.push({method: 'restyle', args: ['visible', false_array], 
//                       label: input_files[j].replace(/_|.csv/g," ")
//                     });
//     }

// }

// if (format === "slider") {

//     steps = buttons;

// }

// xstring = "$$" + cate_info["labels"][category] + "$$";
// ystring = "$$ \\text{Frequency} [\\%] $$";
// title_string = "$$ \\text{Frequency Histogram of_}" + xstring.replace("$$"," ");

// if (format === "slider") {
    
//     var layout = {
//         sliders: [{
//             pad: {t: 30},
//             len: ((input_files.length)/12),
//             steps: steps
//         }],
//         //showlegend: false,
//         barmode: "stack",
//         title: title_string,
//         yaxis: {
//             title: ystring,
//             range: [0, max_y]
//         },
//         xaxis: {
//             title: xstring,
//             range: [0, 1.1*max_x]
//         }
//     };

// }

// if (format === "grid") {

//     layout["title"] = title_string;
//     //layout["showlegend"] = false;
//     layout["barmode"] = "stack";
    
//     for(var i = 0; i < input_files.length; i++) {
//         layout["xaxis"+(i+2)]["range"] = [0, 1.1*max_x];
//         layout["yaxis"+(i+2)]["range"] = [0, max_y];
//         layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
//                                 x: layout["xaxis"+(i+2)].domain[1]-0.02, y: layout["yaxis"+(i+2)].domain[1]-0.05,
//                                 showarrow: true, arrowhead: 0, ax: 0, ay: 0});
//     }
//     layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
//                             x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
//                             showarrow: false, font: {size: 12}});
//     layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
//                             x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
//                             showarrow: false, font: {size: 12}}); 

// }

// if (format === "dropdown") {

//     var layout = {
//         title: title_string,
//         //showlegend: false,
//         barmode: "stack",
//         yaxis: {
//             title: ystring,
//             range: [0, max_y]
//         },
//         xaxis: {
//             title: xstring, 
//             range: [0, 1.1*max_x]
//         },
//         updatemenus: [{
//             y: 1, 
//             yanchor: "top", 
//             buttons: buttons
//         }]
//     }

// }

// Plotly.newPlot("chart", graphish, layout)

// ///////////////////////////////////////////////////////////////

// // Normalized Histogram by Stability

// // Set up data
// var vertloc = 80;
// var basecolor = "span";
// var graphish = []; 

// // Convert CSV to JSON ... need to create dynamic labels in
// // place of 7 and 10
// var arrays = all_results[0].data;
// var keys = arrays[7];
// var values = arrays.slice(10);

// var object1 = new Object();
// // remove -1 in code with QC data
// for (k = 0; k < (keys.length-1); k++) {
//     var new_values = [];
//     for (v = 0; v < values.length; v++) {
//         new_values.push(values[v][k]);
//     }
//     if (Object.keys(object1).indexOf(keys[k]) == -1) {
//         object1[keys[k]] = new_values;
//     } else {
//         object1[keys[k]+"_adv"] = new_values;
//     }
// }       

// var object2 = edit_met_data(object1);

// var stab_conds, stab_cats, metdat;
// [stab_conds, stab_cats, metdat] = flag_stability(object2);

// var cate_info = get_catinfo(metdat);

// var stab, stabloc, ind;
// [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
// var stabconds = get_stabconds();

// var colors = get_colors(stabconds.length, {basecolor: basecolor});

// var all_dat = [[],[],[],[],[]];
// for (var cond = 0; cond < stabconds.length; cond++) {

//     var plotdat = [];
//     for (var hour = 0; hour < 24; hour++) {

//         var array_temp = [];
//         var array_temp = metdat[stab];
//         var cond_array = [];
        
//         for (var i = 0; i < array_temp.length; i += 1) {
//             // until there is a faster way to remove these                      
//             if ((parseInt(metdat["Date"][i].split(" ")[1].split(":")[0]) === hour) && (parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null) && (array_temp[i] === stabconds[cond])) {
//                 cond_array.push(array_temp[i]);
//             }
//         }

//         plotdat.push(cond_array.length/array_temp.length);
//     }

//     all_dat[cond].push(plotdat);

//     var trace = {
//         x: range(0,24,1),
//         y: plotdat,
//         type: "bar",
//         marker: {
//             color: colors[cond],
//         },
//         name: stabconds[cond]
//     };

//     graphish = graphish.concat(trace);

// }

// for (var hour = 0; hour < graphish[0]["y"].length; hour++) {

//     var total = 0;
//     for (var cond = 0; cond < graphish.length; cond++) {
//         total += graphish[cond]["y"][hour];
//     }
//     for (var cond = 0; cond < graphish.length; cond++) {
//         graphish[cond]["y"][hour] = graphish[cond]["y"][hour]*100/total;
//     }
// }

// var xstring = "$$ \\text{Time of Day [Hour]} $$";
// var ystring = "$$ \\text{Probability of Stability} [\\%] $$";
// var title_string = "$$ \\text{Time of Day vs. Probability of Stability} $$";

// var layout = {
//     "title": title_string,
//     "xaxis": {
//         title: xstring
//     },
//     "yaxis": {
//         title: ystring
//     },
//     "barmode": "stack"
// };

// Plotly.newPlot("chart", graphish, layout)

// ///////////////////////////////////////////////////////////////

// // Normalized Monthly Histogram by Stability

// // Set up data
// var vertloc = 80;
// var basecolor = "span";
// var graphish_fin = []; 
// var format = "dropdown";
// var layout = {annotations: []};

// for (var j = 0; j < input_files.length; j++) {
//     var graphish = [];
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

//     var stab_conds, stab_cats, metdat;
//     [stab_conds, stab_cats, metdat] = flag_stability(object2);

//     var cate_info = get_catinfo(metdat);

//     var stab, stabloc, ind;
//     [stab, stabloc, ind] = get_vertical_locations(cate_info["columns"]["stability flag"], {location: vertloc});
//     var stabconds = get_stabconds();

//     var colors = get_colors(stabconds.length, {basecolor: basecolor});

//     var all_dat = [[],[],[],[],[]];
//     for (var cond = 0; cond < stabconds.length; cond++) {

//         var plotdat = [];
//         for (var hour = 0; hour < 24; hour++) {

//             var array_temp = [];
//             var array_temp = metdat[stab];
//             var cond_array = [];
            
//             for (var i = 0; i < array_temp.length; i += 1) {
//                 // until there is a faster way to remove these                      
//                 if ((parseInt(metdat["Date"][i].split(" ")[1].split(":")[0]) === hour) && (parseFloat(array_temp[i]) != -999.0) && (array_temp[i] != null) && (array_temp[i] === stabconds[cond])) {
//                     cond_array.push(array_temp[i]);
//                 }
//             }

//             plotdat.push(cond_array.length/array_temp.length);
//         }

//         all_dat[cond].push(plotdat);

//         if ((format === "dropdown") | (format === "slider")) {

//             var trace = {
//                 x: range(0,24,1),
//                 y: plotdat,
//                 type: "bar",
//                 visible: j === 0,
//                 marker: {
//                     color: colors[cond],
//                 },
//                 name: stabconds[cond]
//             };

//             graphish = graphish.concat(trace);

//         }

//         if (format === "grid") {

//             var trace = {
//                 x: range(0,24,1),
//                 y: plotdat,
//                 xaxis: "x" + (j+2),
//                 yaxis: "y" + (j+2),
//                 type: "bar",
//                 showlegend: j === 0,
//                 marker: {
//                     color: colors[cond],
//                 },
//                 name: stabconds[cond]
//             };

//             graphish = graphish.concat(trace);

//         }
//     }

//     if (format === "grid") {

//         layout["yaxis" + (j+2)] = {
//             domain: calcDomain_y(Math.floor(j/4),3)
//         };

//         layout["xaxis" + (j+2)] = {
//             domain: calcDomain_x(j%4,4)
//         };

//     }  

//     for (var hour = 0; hour < graphish[0]["y"].length; hour++) {

//         var total = 0;
//         for (var cond = 0; cond < graphish.length; cond++) {
//             total += graphish[cond]["y"][hour];
//         }
//         for (var cond = 0; cond < graphish.length; cond++) {
//             graphish[cond]["y"][hour] = graphish[cond]["y"][hour]*100/total;
//         }
//     }

//     graphish_fin = graphish_fin.concat(graphish);

// }

// buttons = [];
// shapes = [];

// if ((format === "dropdown") | (format === "slider")) {

//     for (var j = 0; j < input_files.length; j++){
//         // This array decides when to display a certain trace
//         false_array = [];

//         for(var i = 0; i < input_files.length; i++) {
//             if (i == j) {
//                 for (var iah = 0; iah < stabconds.length; iah++) {
//                     false_array.push(true);
//                 }
//             } else {
//                 for (var iah = 0; iah < stabconds.length; iah++) {
//                     false_array.push(false);
//                 }
//             }  
//         }
//         buttons.push({method: 'restyle', args: ['visible', false_array], 
//                       label: input_files[j].replace(/_|.csv/g," ")
//                     });
//     }

// }

// if (format === "slider") {

//     steps = buttons;

// }

// var xstring = "$$ \\text{Time of Day [Hour]} $$";
// var ystring = "$$ \\text{Probability of Stability} [\\%] $$";
// var title_string = "$$ \\text{Time of Day [Hour] vs. Probability of Stability} [\\%] $$";

// if (format === "slider") {
    
//     var layout = {
//         sliders: [{
//             pad: {t: 30},
//             len: ((input_files.length)/12),
//             steps: steps
//         }],
//         barmode: "stack",
//         title: title_string,
//         yaxis: {
//             title: ystring,
//             range: [0, 100]
//         },
//         xaxis: {
//             title: xstring,
//             range: [-0.5, 23.5]
//         }
//     };

// }

// if (format === "grid") {

//     layout["title"] = title_string;
//     //layout["showlegend"] = false;
//     layout["barmode"] = "stack";
    
//     for(var i = 0; i < input_files.length; i++) {
//         layout["xaxis"+(i+2)]["range"] = [-0.5, 23.5];
//         layout["yaxis"+(i+2)]["range"] = [0, 100];
//         layout.annotations.push({text: input_files[i].split("_")[1].split(".")[0], xref: "paper", yref: "paper", 
//                                 x: layout["xaxis"+(i+2)].domain[1], y: layout["yaxis"+(i+2)].domain[1]-0.14, textangle: 90,
//                                 showarrow: true, arrowhead: 0, ax: 0, ay: 0});
//     }
//     layout.annotations.push({text: xstring, xref: "paper", yref: "paper",
//                             x: 0.5, y: 1, xanchor: "center", yanchor: "bottom",
//                             showarrow: false, font: {size: 12}});
//     layout.annotations.push({text: ystring, xref: "paper", yref: "paper",
//                             x: 1, y: 0.5, xanchor: "left", yanchor: "middle", textangle: 90,
//                             showarrow: false, font: {size: 12}}); 

// }

// if (format === "dropdown") {

//     var layout = {
//         title: title_string,
//         barmode: "stack",
//         yaxis: {
//             title: ystring,
//             range: [0, 100]
//         },
//         xaxis: {
//             title: xstring, 
//             range: [-0.5, 23.5]
//         },
//         updatemenus: [{
//             y: 1, 
//             yanchor: "top", 
//             buttons: buttons
//         }]
//     }

// }

// Plotly.newPlot("chart", graphish_fin, layout)

// ///////////////////////////////////////////////////////////////