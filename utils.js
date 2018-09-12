// utils.js
// module:	utils
// platform:	Unix, Windows
// synopsis:	This code is used as a general family of utilities that can be used for plotting.
// moduleauthor:	Nicholas Hamilton <Nicholas.Hamilton@nrel.gov> Rafael Mudafort <Rafael.Mudafort@nrel.gov> Lucas McCullum <Lucas.McCullum@nrel.gov>

// Functions converted from Python
//
// D = debugged, * = converted/buggy, + = incomplete, ~ = not started, X = not needed
//
// D utils.Round_To_n(x, n)
// D utils.RGB_to_hex(RGB)
// D utils.color_dict(gradient)
// D utils.get_colors(ncolors, basecolor='cycle', reverse=False)
// * utils.get_nearest_direction(metdat, directions, category)
// * utils.get_nearest_stability(metdat, stability, category)
// D utils.get_nrelcolors()
// D utils.get_stabconds()
// * utils.get_vertical_locations(category, location=None, reverse=False)
// D utils.hex_to_RGB(hex)
// D utils.linear_gradient(start_hex, finish_hex='#FFFFFF', n=10)
// X utils.matlab_datenum_to_python_datetime(datenum)
// D utils.monthnames()
// D utils.polylinear_gradient(colors, n)

// Helper Functions
// Start: Python common functions to Javascript

function range(start, stop, step) {

    if (typeof stop == "undefined") {
        // one param defined
        stop = start;
        start = 0;
    }

    if (typeof step == "undefined") {
        step = 1;
    }

    if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
        return [];
    }

    var result = [];
    for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
        result.push(i);
    }

    return result;

}

// End: Python common functions to Javascript

// Arithmetic (Rounding)

function Round_To_n(x,n) {

    return x.toPrecision(-Math.round(Math.floor(Math.sign(x) * Math.log10(Math.abs(x)))) + n);

}

// Get Values of Interest

function get_vertical_locations(category, {location = null, reverse = false} = {}) {

    var vertlocs = [];
    for (var vari = 0; vari < category.length; vari ++) {
        vertlocs.push(parseInt(category[vari].replace(" ","").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
    }

    var ind = Array.from(Array(vertlocs.length).keys()).sort((a, b) => vertlocs[a] < vertlocs[b] ? -1 : (vertlocs[b] < vertlocs[a]) | 0);
    //console.log(ind);
    
    //var interm1 = range(vertlocs.length);
    //ind = interm1.sort(function(a, b){return a - b});
        
    // sort vertical locations
    var vertlocs_interm = [];
    for (var x = 0; x < ind.length; x++) {
        vertlocs_interm.push(vertlocs[ind[x]]);
    }
    vertlocs = vertlocs_interm;

    var category_interm = [];
    for (var x = 0; x < ind.length; x++) {
        category_interm.push(category[ind[x]]);
    }
    category = category_interm;

    if (location !=  null) {
        temp = vertlocs.map(x => Math.abs(x - location));
        ind = parseInt(temp.indexOf(Math.min(...temp)));
        category = category[ind];
        vertlocs = vertlocs[ind];
    }

    if (reverse == true) {
        category = category.reverse();
        vertlocs = vertlocs.reverse();
    }

    return [category, vertlocs, ind];

}

function get_nearest_direction(metdat, directions, category) {

    var vertlocs = [];
    for (var vari = 0; vari < metdat[category].length; vari++) {
        vertlocs.push(parseInt(metdat[category][vari].replace(" ","").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
    }

    var dirlocs = [];
    for (var vari = 0; vari < metdat[directions].length; vari++) {
        dirlocs.push(parseInt(metdat[directions][vari].replace(" ","").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
    }

    var dirind = [];
    for (var loc = 0; loc < vertlocs.length; loc++) {
        temp = dirlocs.map(x => Math.abs(x - vertlocs[loc]));
        ind = parseInt(dirlocs.indexOf(temp));
        dirind.push(ind);
    }

    var catind = [];
    for (var loc = 0; loc < vertlocs.length; loc++) {
        catind.push(vertlocs.getIndexOf(vertlocs[loc])); 
    }

    return [dirind, catind, vertlocs];

}

function get_nearest_stability(metdat, stability, category) {

    if (typeof category === "object") {
        vertlocs = [];
        for (var vari = 0; vari < metdat[category].length; vari ++) {
            vertlocs.push(parseInt(metdat[category][vari].replace(" ","").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
        }
        stablocs = [];
        for (var vari = 0; vari < metdat[stability].length; vari ++) {
            stablocs.push(parseInt(metdat[stability][vari].replace(" ","").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
        }
    } else if (typeof category === "string") {
        vertlocs = [parseInt(metdat[stability][vari].replace(" ","").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0])];
        stablocs = [];
        for (var vari = 0; vari < metdat[stability].length; vari ++) {
            stablocs.push(parseInt(metdat[stability][vari].replace(" ","").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
        }
    }

    var stabind = [];
    for (var loc = 0; loc < vertlocs.length; loc++) {
        temp = stablocs.map(x => Math.abs(x - vertlocs[loc]));
        ind = parseInt(stablocs.indexOf(temp));
        stabind.push(ind);
    }

    var catind = [];
    for (var loc = 0; loc < vertlocs.length; loc++) {
        catind.push(vertlocs.getIndexOf(vertlocs[loc]) ); 
    }

    return [dirind, catind, vertlocs];

}

// Get Desired Information for Plotting

function monthnames() {

    var months = ['January',
                  'February',
                  'March',
                  'April',
                  'May',
                  'June',
                  'July',
                  'August',
                  'September',
                  'October',
                  'November',
                  'December'];

    return months;

}

function yearnames() {

    var years = [2013, 
                 2017];

    return years;

}

function get_stabconds() {

    var stabconds = ['Very Stable', 'Stable', 'Neutral', 'Unstable', 'Very Unstable'];

    return stabconds;

}

// Setup Colors for Plotting

function get_nrelcolors() {

    var nrelcolors = {"blue": ["#0079C2","#00A4E4"],
                      "red": ["#933C06","#D9531E"],
                      "green": ["#3D6321","#5D9732"],
                      "gray": ["#3A4246","#5E6A71"]};

    return nrelcolors;

}

function hex_to_RGB(hex) {

    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);

    var RGB = [];
    for (var i = 1; i < 4; i++) {
        RGB.push(parseInt(result[i], 16));
    }

    return RGB;

}

function RGB_to_hex (RGB) {

    return "#" + ((1 << 24) + (RGB[0] << 16) + (RGB[1] << 8) + RGB[2]).toString(16).slice(1);

}

function color_dict(gradient) {

    hex_array = [];
    r_array = [];
    g_array = [];
    b_array = [];

    for (var RGB = 0; RGB < gradient.length; RGB++) {
        hex_array.push(RGB_to_hex(gradient[RGB]));
        r_array.push(gradient[RGB][0]);
        g_array.push(gradient[RGB][1]);
        b_array.push(gradient[RGB][2]);
    }
        
    var dict = {
        "hex": hex_array,
        "r": r_array,        
        "g": g_array,        
        "b": b_array,
    }
        
    return dict;

}

function linear_gradient(start_hex, finish_hex="#FFFFFF", n=10) {

    // Starting and ending colors in RGB form
    var s = hex_to_RGB(start_hex)
    var f = hex_to_RGB(finish_hex)

    // Initilize a list of the output colors with the starting color
    var RGB_list = [s]

    // Calcuate a color at each evenly spaced value of t from 1 to n
    for (var t = 1; t < n; t++) {
        var curr_vector = [];
        // Interpolate RGB vector for color at the current value of t
        for (var j = 0; j < 3; j++) {
            curr_vector.push(parseInt(s[j] + (parseFloat(t)/(n-1)) * (f[j] - s[j])));
        }
        // Add it to our list of output colors
        RGB_list[t] = curr_vector;

    }

    return color_dict(RGB_list);

}

function polylinear_gradient(colors, n) {

    // The number of colors per individual linear gradient
    var n_out = parseInt(parseFloat(n) / (colors.length - 1));

    // returns dictionary defined by color_dict()
    var gradient_dict = linear_gradient(colors[0], colors[1], n_out);
    var color_marks = ["hex", "r", "g", "b"];

    if (colors.length > 1) {
        for (var col = 1; col < (colors.length - 1); col++) {
            next = linear_gradient(colors[col], colors[col+1], n_out);
            for (var k = 0; k < color_marks.length; k++) {
                for (var x = 1; x < next[color_marks[k]].length; x++) {
                    // Exclude first point to avoid duplicates
                    gradient_dict[color_marks[k]].push(next[color_marks[k]][x]);
                }
            }
        }
    }

    return gradient_dict;

}

function get_colors(ncolors, {basecolor, reverse = false} = {}) {

    // NREL official colors
    var nrelcolors = get_nrelcolors();

    if (typeof basecolor === "object") {

        colors = basecolor;
        cdict = polylinear_gradient(colors, ncolors+2);
        colors = cdict["hex"];

    } else if (basecolor in nrelcolors) {

        var nc = ncolors + 2;
        var colors = [];
        while (colors.length < ncolors) {
            nc += 1;
            colors = ["#D1D5D8", nrelcolors[basecolor][1], nrelcolors[basecolor][0]];
            cdict = polylinear_gradient(colors, nc);
            colors = cdict["hex"];
            colors.splice(2,1);
        }

    } else if (basecolor === "cycle") {

        var nc = ncolors + 2;
        var colors = [];
        while (colors.length < ncolors) {
            nc += 1;
            colors = ["#0079C2","#D1D5D8","#D9531E","#00A4E4"];
            cdict = polylinear_gradient(colors,nc);
            colors = cdict["hex"];
            colors.splice(2,1);
        }

    } else if (basecolor === "span") {

        colors = [nrelcolors["blue"][0], "#D1D5D8", nrelcolors["red"][0]];
        cdict = polylinear_gradient(colors, ncolors+2);
        colors = cdict["hex"];

    }

    if (reverse == true) {

        colors.reverse();

    }

    return colors;
}

// End of Code