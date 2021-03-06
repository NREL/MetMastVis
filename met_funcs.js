// module: met_funcs
// platform: Unix, Windows
// synopsis: This code is used as a general family of functions and classes that can be used in the MET tower data analysis. 
// moduleauthor: Nicholas Hamilton <Nicholas.Hamilton@nrel.gov> Rafael Mudafort <Rafael.Mudafort@nrel.gov> Lucas McCullum <Lucas.McCullum@nrel.gov>   

// Functions converted from Python
//
// D = debugged, * = converted/buggy, + = incomplete, ~ = not started, X = not needed
//
// * met_funcs.categories_to_exclude()
// * met_funcs.categories_to_keep()
// * met_funcs.categorize_fields(metdat, keeplist=None, excludelist=None)
// X met_funcs.drop_nan_cols(metdat)
// ~ met_funcs.find_ECD_events(sonicdat, params, T=10)
// ~ met_funcs.find_EDC_events(sonicdat, params, T=6)
// ~ met_funcs.find_EOG_events(sonicdat, params, T=10.5)
// ~ met_funcs.find_ETM_events(sonicdat, params)
// ~ met_funcs.find_EWM_events(sonicdat, params)
// ~ met_funcs.find_EWS_events(sonicdat, params, T=12)
// ~ met_funcs.setup_IEC_params(sonicdat, probeheight=100)
// * met_funcs.flag_stability(metdat)
// * met_funcs.get_catinfo(metdat)
// * met_funcs.get_units()
// X met_funcs.groom_data(metdat, varcats)
// X met_funcs.load_met_data(inputfiles, verbose=False)
// X met_funcs.load_met_data_alt(inputfiles, verbose=False)
// ~ met_funcs.make_dataframe_for_height(inputdata, timerange, probeheight=74, include_UTC=False)
// ~ met_funcs.make_datetime_vector(filename, span=10, freq=20.0)
// ~ met_funcs.qc_mask(metdat)
// X met_funcs.reject_outliers(data, m=5)


// Data loading
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
    for(var coli = 0; coli < fNames.length; coli++) {
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
        
    
    temp = Object.assign(fObject,new_dataframe);
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

    categoriesIdx = {"Very Stable": (L>0) & (L<=200),
                     "Stable" : (L>200) & (L<=500),
                     "Neutral" : (L<-500) | (L>500),
                     "Unstable" : (L>=-500) & (L<-200),
                     "Very Unstable": (L>=-200) & (L<0)};

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
              "surface","*",
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
              "(SF_",
              "zero-crossing",
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

function cat_extra() {

    keepcats = ["Global PSP [W/m^2]",
                "Global PSP (Accumulated) [kWhr/m^2]",
                "Precipitation (Accumulated) [mm]",
                "Atmospheric Electric Field [kV/m]"];

    return keepcats;

}

function get_units() {

    units = {"density": "\\Big[\\frac{kg}{m^3}\\Big]",
             "pressure": "[mbar]",
             "temperature": "[^\\circ C]",
             "tke":"\\Big[\\frac{m^2}{s^2}\\Big]",
             "direction": "[^\\circ]",
             "dissipation": "\\Big[\\frac{m^2}{s^3}\\Big]",
             "richardson": "[--]",
             "length": "[m]",
             "humidity": "[\\%]",
             "speed": "\\Big[\\frac{m}{s}\\Big]",
             "stability parameter z/l": "[--]",
             "ti": "[\\%]",
             "turbulent kinetic energy": "\\Big[\\frac{m^2}{s^2}\\Big]",
             "shear": "[--]",
             "veer": "[^\\circ]",
             "flag": "[--]"};

    return units;

}

function categorize_fields(metdat, {keeplist = null, excludelist = null} = {}) {

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
                    temp.splice(ind,1);
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
                var replace_with = colnames[x].replace(" ","").split("(").slice(-1)[0].split("_").slice(-1)[0].split("m")[0].replace(/\s/g, "");
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
    // console.log(varcats);

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
            x = Object.keys(units)[index].toLowerCase().split(" ").map(function(word) {
                return word.replace(word[0], word[0].toUpperCase());
            }).join(" ");

            catT = Object.keys(varcats)[cat].toLowerCase().split(" ").map(function(word) {
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
        label = Object.keys(varcats)[x].toLowerCase().split(" ").map(function(word) {
            return word.replace(word[0], word[0].toUpperCase());
        }).join(" ");

        varlabels[Object.keys(varcats)[x]] = ("\\text{" + label + "} " + varunits[Object.keys(varcats)[x]]);
    }

    // a few ad hoc corrections
    varlabels["turbulent kinetic energy"] = "\\text{TKE}"+ varunits["turbulent kinetic energy"];
    varlabels["direction"] = "\\text{Wind }" + varlabels["direction"];
    varlabels["speed"] = "\\text{Wind }" + varlabels["speed"];
    varlabels["stability parameter z/l"] =  "\\text{Stability Parameter z/L }[--]";

    // strings for saving files and figures
    var varsave = {};
    var save_array = [];
    for (var x = 0; x < Object.keys(varcats).length; x++) {
        varsave[Object.keys(varcats)[x]] = Object.keys(varcats)[x].replace(" ","_").replace("/","");
    }

    return [varcats, varunits, varlabels, varsave];
}

function get_catinfo(metdat) {

    var varcats, varunits, varlabels, varsave;
    [varcats, varunits, varlabels, varsave] = categorize_fields(metdat, {keeplist: true});

    var catinfo = {
        "columns": varcats,
        "units": varunits,
        "labels": varlabels,
        "save": varsave
    };

    return catinfo;

}


// function groom_data(metdat, varcats) {

//     // drop columns
//     keepcols = [];
//     for (var x = 0; x < varcats.length; x++){
//         for (var v = 0; v < varcats[x].length; v++) {
//             keepcols.push(varcats[x][v]);
//         }
//     }

//     dropcols = [];
//     for (var col = 0; col < Object.keys(metdat).length; col++) {
//         if (Object.keys(metdat)[col] ) {
//             dropcols.push(Object.keys(metdat)[col]);
//         }
//     }

//     console.log("Number of columns after filtering: " + Object.keys(metdat).length);
//     return metdat;

// }