$(document).ready(function () {
  testrequest();
});

//supporting functions
testrequest = function () {
  $.ajax({
    // url: 'https://s3-us-west-2.amazonaws.com/nrel-nwtc-metmast-uni/int/dt=2017-01/2017_January.csv',
    url: 'https://s3-us-west-2.amazonaws.com/nrel-nwtc-metmast-uni/int/2017_January.csv',
    dataType: 'text',
    success: function (data) {
      parseCSVString(data)
    },
    error: function (e) {
      setInnerHTML("csv_data", e.error);
    }
  });
}

function parseCSVString(csv_string) {
  Papa.parse(csv_string, {
    complete: function (csv) {
      createGraph(csv.data);
    }
  });
}

function setInnerHTML(dom_object_id, data) {
  document.getElementById(dom_object_id).innerHTML = data;
}

function createGraph(csv_data) {
  [graphish, layout] = cumulative_prof(csv_data, "2013_May.csv", "speed", "span");
  Plotly.newPlot("chart", graphish, layout)
}

function cumulative_prof(all_results, month_string, category, basecolor) {
  // default: -,-,-,span

  // Set up data
  var graphish = [];
  var max_x = -Infinity;
  var min_x = Infinity;

  var object1 = process_data(all_results);
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

  var colors = get_colors(1, { basecolor: basecolor });
  
  var trace = {
    x: plotdat,
    y: vertlocs,
    type: "scatter",
    name: month_string.split("_")[1].split(".")[0],
    connectgaps: true,
    line: {
      color: colors[0]
    }
  };

  graphish = trace;
  
  // Set the string labels
  var xstring = "$$" + cate_info["labels"][category] + "$$";
  var ystring = "$$ \\text{Probe Height} [m] $$";
  // need to add $$ for LaTeX to process
  var title_string = "$$ \\text{" + titleCase(category) + " vs. } " + ystring.replace("$$", "") + " $$";

  var diff = max_x - min_x;

  var layout = {
    title: title_string,
    yaxis: {
      title: ystring
    },
    xaxis: {
      title: xstring,
      range: [min_x - 0.5 * diff, max_x + 0.5 * diff]
    },
    hovermode: "closest"
  };

  return [graphish, layout];
}

// ***************************************************************************************************************************************


function process_data(csv_data) {

  // Convert CSV to JSON ... need to create dynamic labels in
  // place of 7 and 10
  var arrays = csv_data;
  var keys = arrays[7];
  var values = arrays.slice(1);

  var object1 = new Object();
  // remove -1 in code with QC data
  for (k = 0; k < (keys.length - 1); k++) {
    var new_values = [];
    for (v = 0; v < values.length; v++) {
      new_values.push(values[v][k]);
    }
    if (Object.keys(object1).indexOf(keys[k]) == -1) {
      object1[keys[k]] = new_values;
    } else {
      object1[keys[k] + "_adv"] = new_values;
    }
  }
  return object1;
}




// ***************************************************************************************************************************************

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

function Round_To_n(x, n) {

  return x.toPrecision(-Math.round(Math.floor(Math.sign(x) * Math.log10(Math.abs(x)))) + n);

}

// Get Values of Interest

function get_vertical_locations(category, { location = null, reverse = false } = {}) {

  var vertlocs = [];
  for (var vari = 0; vari < category.length; vari++) {
    vertlocs.push(parseInt(category[vari].replace(" ", "").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
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

  if (location != null) {
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
    vertlocs.push(parseInt(metdat[category][vari].replace(" ", "").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
  }

  var dirlocs = [];
  for (var vari = 0; vari < metdat[directions].length; vari++) {
    dirlocs.push(parseInt(metdat[directions][vari].replace(" ", "").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
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
    for (var vari = 0; vari < metdat[category].length; vari++) {
      vertlocs.push(parseInt(metdat[category][vari].replace(" ", "").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
    }
    stablocs = [];
    for (var vari = 0; vari < metdat[stability].length; vari++) {
      stablocs.push(parseInt(metdat[stability][vari].replace(" ", "").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
    }
  } else if (typeof category === "string") {
    vertlocs = [parseInt(metdat[stability][vari].replace(" ", "").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0])];
    stablocs = [];
    for (var vari = 0; vari < metdat[stability].length; vari++) {
      stablocs.push(parseInt(metdat[stability][vari].replace(" ", "").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0]));
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
    catind.push(vertlocs.getIndexOf(vertlocs[loc]));
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

function get_stabconds() {

  var stabconds = ['Very Stable', 'Stable', 'Neutral', 'Unstable', 'Very Unstable'];

  return stabconds;

}

// Setup Colors for Plotting

function get_nrelcolors() {

  var nrelcolors = {
    "blue": ["#0079C2", "#00A4E4"],
    "red": ["#933C06", "#D9531E"],
    "green": ["#3D6321", "#5D9732"],
    "gray": ["#3A4246", "#5E6A71"]
  };

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

function RGB_to_hex(RGB) {

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

function linear_gradient(start_hex, finish_hex = "#FFFFFF", n = 10) {

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
      curr_vector.push(parseInt(s[j] + (parseFloat(t) / (n - 1)) * (f[j] - s[j])));
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
      next = linear_gradient(colors[col], colors[col + 1], n_out);
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

function get_colors(ncolors, { basecolor = "cycle", reverse = false } = {}) {

  // NREL official colors
  var nrelcolors = get_nrelcolors();

  if (typeof basecolor === "object") {
    colors = basecolor;
    cdict = polylinear_gradient(colors, ncolors + 2);
    colors = cdict["hex"];
  } else if (basecolor in nrelcolors) {
    var nc = ncolors + 2;
    var colors = [];
    while (colors.length < ncolors) {
      nc += 1;
      colors = ["#D1D5D8", nrelcolors[basecolor][1], nrelcolors[basecolor][0]];
      cdict = polylinear_gradient(colors, nc);
      colors = cdict["hex"];
      colors.splice(2, 1);
    }
  } else if (basecolor == "cycle") {
    var nc = ncolors + 2;
    var colors = [];
    while (colors.length < ncolors) {
      nc += 1;
      colors = ["#0079C2", "#D1D5D8", "#D9531E", "#00A4E4"];
      cdict = polylinear_gradient(colors, nc);
      colors = cdict["hex"];
      colors.splice(2, 1);
    }
  } else if (basecolor == "span") {
    colors = [nrelcolors["blue"][0], "#D1D5D8", nrelcolors["red"][0]];
    cdict = polylinear_gradient(colors, ncolors + 2);
    colors = cdict["hex"];
  }

  if (reverse == true) {
    colors.reverse();
  }

  return colors;
}

// End of Code


function edit_met_data(metdat, verbose = false) {

  temp = [];
  for (var name = 0; name < Object.keys(metdat).length; name++) {
    if (Object.keys(metdat)[name].includes(" QC") === false) {
      temp.push(Object.keys(metdat)[name]);
    }
  }

  qcNames = [];
  for (var name = 0; name < Object.keys(metdat).length; name++) {
    if (Object.keys(metdat)[name].includes(" QC")) {
      qcNames.push(Object.keys(metdat)[name]);
    }
  }

  fNames = [];
  for (var name = 0; name < temp.length; name++) {
    if (qcNames.includes(temp[name] + " QC")) {
      fNames.push(temp[name]);
    }
  }

  if (verbose === true) {
    console.log("dtypes corrected");
  }

  console.log("number of data columns: " + fNames.length);
  //console.log(fNames);
  console.log("number of QC columns: " + qcNames.length);
  //console.log(qcNames);

  // initialize filtered Object
  var new_dataframe = {
    "Date": metdat["Date"],
    "Record": metdat["Record"],
    "Version": metdat["Version"]
  };

  // fArray = [];
  // for (var obj = 0; obj < fNames.length; obj++) {
  //     // apply QC mask to each set of columns individually
  //     fArray.push(fNames[obj],qcNames[obj]);
  // }
  // console.log(fArray);

  //console.log(metdat);
  //console.log(metdat[fNames[2]]);
  //console.log(metdat[qcNames[2]]);

  fObject = {};
  for (var coli = 0; coli < fNames.length; coli++) {
    temp_array = [];
    //console.log(metdat[qcNames[coli]]);
    for (var row = 0; row < metdat[fNames[coli]].length; row++) {
      if (parseInt(metdat[qcNames[coli]][row]) == 1) {
        temp_array.push(metdat[fNames[coli]][row]);
      } else {
        temp_array.push(null);
      }
    }
    //console.log(temp_array);
    fObject[fNames[coli]] = temp_array;
  }


  // var mask = [];
  // for (var iax = 0; iax < qcNames.length; iax++) {
  //     for (var iay = 0; iay < metdat[qcNames[iax]].length; iay++) {
  //         if (metdat[qcNames[iax]][iay] == 1) {
  //             mask.push(true);
  //         } else {
  //             mask.push(false);
  //         }
  //     }
  // }

  // var data_array = [];
  // for (var mv = 0; mv < metdat[fNames[obj]].length; mv++) {
  //     if (metdat[qcNames[obj]][mv] == 1) {
  //         data_array.push(metdat[fNames[obj]][mv]);
  //     } else {
  //         data_array.push(-999.0);
  //     }
  // }
  // fObject[fNames[obj]] = data_array;


  temp = Object.assign(fObject, new_dataframe);
  //console.log(temp);

  metdat = temp;

  // // replace flagged value "-999.0" with null
  // // crazy slow, need to replace
  // for (var key = 0; key < Object.keys(metdat).length; key++) {
  //     //console.log(key);
  //     for (var content = 0; content < metdat[Object.keys(metdat)[key]].length; content++) {
  //         //console.log(content);
  //         //console.log(metdat[Object.keys(metdat)[key]]);
  //         if (metdat[Object.keys(metdat)[key]][content] == -999.0) {
  //             //console.log("True");
  //             metdat[Object.keys(metdat)[key]][content] = null;
  //         }
  //     }
  // }
  // //console.log(metdat);

  return metdat;

}

function flag_stability(metdat) {

  var MOLcols = [];
  for (var col = 0; col < Object.keys(metdat).length; col++) {

    if (Object.keys(metdat)[col].toLowerCase().includes("monin-obukhov length")) {
      MOLcols.push(Object.keys(metdat)[col]);
    }

  }

  for (var col = 0; col < MOLcols.length; col++) {
    // get probe height
    z = parseInt(MOLcols[col].split("m")[0].split("(").slice(-1)[0]);

    // extract data from MetData
    L = Object.assign({}, metdat[MOLcols[col]]);

    // make new column
    newcolname = "Stability Flag (" + z + "m)";

    //metdat[newcolname] = null;
    //console.log(MOLcols);
    //console.log(categoriesIdx);

    var stabcond_array = [];
    for (var iay = 0; iay < Object.keys(L).length; iay++) {
      if ((L[iay] > 0) & (L[iay] <= 200)) {
        stabcond_array.push("Very Stable");
      } else if ((L[iay] > 200) & (L[iay] <= 500)) {
        stabcond_array.push("Stable");
      } else if ((L[iay] < -500) | (L[iay] > 500)) {
        stabcond_array.push("Neutral");
      } else if ((L[iay] >= -500) & (L[iay] <= -200)) {
        stabcond_array.push("Unstable");
      } else if ((L[iay] >= -200) & (L[iay] < 0)) {
        stabcond_array.push("Very Unstable");
      } else {
        stabcond_array.push(null);
      }
    }
    metdat[newcolname] = stabcond_array;

  }

  var stab_array = [];

  for (var x = 0; x < Object.keys(metdat).length; x++) {

    if (Object.keys(metdat)[x].includes("Stability Flag")) {
      stab_array.push(Object.keys(metdat)[x]);
    }

  }

  var stabcat = {
    "stability flag": stab_array,
  }

  categoriesIdx = {
    "Very Stable": (L > 0) & (L <= 200),
    "Stable": (L > 200) & (L <= 500),
    "Neutral": (L < -500) | (L > 500),
    "Unstable": (L >= -500) & (L < -200),
    "Very Unstable": (L >= -200) & (L < 0)
  };

  var stabconds = [];
  for (var x = 0; x < Object.keys(categoriesIdx).length; x++) {
    stabconds.push(Object.keys(categoriesIdx)[x]);
  }
  //console.log(metdat);

  return [stabconds, stabcat, metdat];

}
function categories_to_exclude() {

  excats = ["advection",
    "angle",
    "boom",
    "equivalent",
    "Log-Law",
    "Preciptation Sensor",
    "peak",
    "record",
    "spectral",
    "kaimal",
    "speed U",
    "SF_",
    "std. dev.",
    "surface", "*",
    "structure",
    "total",
    "zero-crossing",
    "sigma",
    "d(t)",
    "Virtual",
    "Brunt",
    "height",
    "sigma",
    "version",
    "sensible",
    "potential",
    "zero-crossing integral length scale (u)",
    "peak coherent",
    "(SF_", "zero-crossing",
    "boom",
    "speed u",
    "valid",
    "kaimal",
    "peak downward",
    "peak upward",
    "velocity structure"];

  return excats;

}

function categories_to_keep() {

  keepcats = ["air density",
    "air pressure",
    "air temperature",
    "coherent tke",
    "cov(u_w)",
    "cov(w_t)",
    "direction",
    "dissipation rate",
    "gradient richardson",
    "integral length scale (u)",
    "integral length scale (v)",
    "integral length scale (w)",
    "mean(w't')",
    "momentum flux",
    "monin-obukhov length",
    "relative humidity",
    "speed",
    "speed gradient richardson",
    "stability flag",
    "stability parameter z/l",
    "ti",
    "turbulent kinetic energy",
    "wind shear",
    "wind veer"];

  return keepcats;

}

function get_units() {

  units = {
    "density": "\\Big[\\frac{kg}{m^3}\\Big]",
    "pressure": "[mbar]",
    "temperature": "[^\\circ C]",
    "tke": "\\Big[\\frac{m^2}{s^2}\\Big]",
    "direction": "[^\\circ]",
    "dissipation": "\\Big[\\frac{m^2}{s^3}\\Big]",
    "richardson": "[--]",
    "length": "[m]",
    "humidity": "$$[%]$$",
    "speed": "\\Big[\\frac{m}{s}\\Big]",
    "stability parameter z/l": "[--]",
    "ti": "[\\%]",
    "turbulent kinetic energy": "\\Big[\\frac{m^2}{s^2}\\Big]",
    "shear": "[--]",
    "veer": "[^\\circ]",
    "flag": "[--]"
  };

  return units;

}

function categorize_fields(metdat, { keeplist = null, excludelist = null } = {}) {

  // missing some columns ... need to investigate
  var colnames = Object.keys(metdat);

  var temp = [];
  for (var x = 0; x < colnames.length; x++) {
    if ((colnames[x].includes("(u)") === false) && (colnames[x].includes("(v)") == false) && (colnames[x].includes("(w)") == false)) {
      temp.push(colnames[x].split(" (")[0].toLowerCase());
    } else {
      temp.push(colnames[x].split(") (")[0].toLowerCase() + ")");
    }
  }

  var seen = {};
  var result = [];
  for (var i = 0; i < temp.length; i++) {

    var el = temp[i];
    if (!seen[el]) {
      seen[el] = true;
      result.push(el);
    }

  }
  temp = result;

  // remove unwanted fields
  if (excludelist != null) {
    if (excludelist === true) {
      excludelist = categories_to_exclude();
    }
    for (var excl = 0; excl < excludelist.length; excl++) {
      for (var x = 0; x < temp.length; x++) {
        if (temp[x].toLowerCase().includes(excludelist[excl].toLowerCase())) {
          var ind = temp.indexOf(temp[x]);
          temp.splice(ind, 1);
        }
      }
    }
    temp.sort();
  }

  // or keep only a select list
  if (keeplist != null) {
    if (keeplist === true) {
      keeplist = categories_to_keep();
    }
    temp = temp.filter(n => keeplist.includes(n));
  }
  // console.log(temp);

  var varcats = {}
  for (var cat = 0; cat < temp.length; cat++) {

    var cat_array = {};
    for (var x = 0; x < colnames.length; x++) {

      if (colnames[x].toLowerCase().split(temp[cat])[0] == "") {
        var replace_with = colnames[x].replace(" ", "").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0].replace(/\s/g, "");
        if (cat_array[replace_with] == null) {
          cat_array[replace_with] = [];
        }
        cat_array[replace_with].push(colnames[x]);
      }
    }
    // console.log(cat_array);
    // cat_keys = Object.keys(cat_array).sort(function(a, b) {return a - b;});
    // console.log(cat_keys);
    var a = Object.values(cat_array);
    //console.log(a);
    function flattenDeep(arr1) {
      return arr1.reduce((acc, val) => Array.isArray(val) ? acc.concat(flattenDeep(val)) : acc.concat(val), []);
    }
    fin_array = flattenDeep(a);
    varcats[temp[cat]] = fin_array;
  }
  console.log(varcats);

  var temp1 = [];
  for (var x = 0; x < varcats["speed"].length; x++) {
    if (varcats["speed"][x].toLowerCase().includes("speed (")) {
      temp1.push(varcats["speed"][x]);
    }
  }
  varcats["speed"] = temp1;

  var temp2 = [];
  //console.log(varcats["dissipation rate"]);
  for (var x = 0; x < varcats["dissipation rate"].length; x++) {
    if (varcats["dissipation rate"][x].toLowerCase().includes("sf") === false) {
      temp2.push(varcats["dissipation rate"][x]);
    }
  }
  varcats["dissipation rate"] = temp2;

  var temp3 = [];
  for (var x = 0; x < colnames.length; x++) {
    if (colnames[x].toLowerCase().includes("cup equivalent ti")) {
      temp3.push(colnames[x]);
    }
  }
  varcats["ti"] = temp3;

  // get units
  var units = get_units();

  var varunits = {};
  for (var cat = 0; cat < Object.keys(varcats).length; cat++) {

    var units_array = [];
    for (var index = 0; index < Object.keys(units).length; index++) {
      // Convert to title-cased
      x = Object.keys(units)[index].toLowerCase().split(" ").map(function (word) {
        return word.replace(word[0], word[0].toUpperCase());
      }).join(" ");

      catT = Object.keys(varcats)[cat].toLowerCase().split(" ").map(function (word) {
        return word.replace(word[0], word[0].toUpperCase());
      }).join(" ");

      if (catT.includes(x)) {
        units_array.push(units[Object.keys(units)[index]]);
      }
    }
    varunits[Object.keys(varcats)[cat]] = units_array;

  }

  // labels for plotting 
  var varlabels = {};
  var labels_array = [];
  for (var x = 0; x < Object.keys(varcats).length; x++) {
    // Convert to title-cased
    label = Object.keys(varcats)[x].toLowerCase().split(" ").map(function (word) {
      return word.replace(word[0], word[0].toUpperCase());
    }).join(" ");

    varlabels[Object.keys(varcats)[x]] = ("\\text{" + label + "} " + varunits[Object.keys(varcats)[x]]);
  }

  // a few ad hoc corrections
  varlabels["turbulent kinetic energy"] = "\\text{TKE}" + varunits["turbulent kinetic energy"];
  varlabels["direction"] = "\\text{Wind }" + varlabels["direction"];
  varlabels["speed"] = "\\text{Wind }" + varlabels["speed"];
  varlabels["stability parameter z/l"] = "\\text{Stability Parameter z/L }[--]";

  // strings for saving files and figures
  var varsave = {};
  var save_array = [];
  for (var x = 0; x < Object.keys(varcats).length; x++) {
    varsave[Object.keys(varcats)[x]] = Object.keys(varcats)[x].replace(" ", "_").replace("/", "");
  }

  return [varcats, varunits, varlabels, varsave];
}

function get_catinfo(metdat) {

  var varcats, varunits, varlabels, varsave;
  [varcats, varunits, varlabels, varsave] = categorize_fields(metdat, { keeplist: true });

  var catinfo = {
    "columns": varcats,
    "units": varunits,
    "labels": varlabels,
    "save": varsave
  };

  return catinfo;

}

function titleCase(str) {
  return str.toLowerCase().split(' ').map(function (word) {
    return word.replace(word[0], word[0].toUpperCase());
  }).join(' ');
}