

function get_stdev(ask_total, numdims){
    // This was estimated via data from the first experiment
    // stata command:

    ask_avg = ask_total/numdims;

    stdev = Math.exp(0.7079252 + 0.0655263*ask_avg - 0.000551*Math.pow(ask_avg, 2));

    return stdev;
}


