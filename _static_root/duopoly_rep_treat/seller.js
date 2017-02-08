



var resultHandler = function(result) {
    // Over-writing user-input to enforce consistency.  The only reason this should ever be different
    //  is if the user tried to enter a decimal-point

    $.each(result.pricedims, function(i, pd){
        $("#dim_" + (i+1)).val(pd);
    });

    $("#id_ask_total").val(result.ask_total);
    $("#id_ask_stdev").val(result.ask_stdev);
};
$(document).ready(function() {
    // when this is called from the instructions page, the example flag should be set to True, which should prevent
    // the server from adding a row to the Ask database.

    // in utils.js
    setup_csrf();

    // When player manually changes a field, we want to send the whole list of fields back as a list
    $(".pricedim").change(function () {

        var pricedims = [];
        $(".pricedim").each(function (i, input) {
            pricedims.push($(input).val());
        });

        var data = get_metadata($("#distribute"));
        data.pricedims = pricedims.toString();

        $.ajax({
            type: "POST",
            url: $("#distribute").attr("data-manual-url"),//"/duopoly_rep_treat/manualpricedims/",
            data: data,
            dataType: "json",
            success: resultHandler
        });
    });

    // When a player clicks the automatic distribute button, we ask the server for the list of price dims
    $("#distribute").click(function () {
        // #Distribute field validation.  Don't send if number not in range.
        var myForm = $("form");
        var myVal = $("#id_ask_total").val();
        if (!myForm[0].checkValidity() && myVal > 800 || myVal < 0 || myVal == "") {
            // Leveraging built-in styling for "distribute" validation
            // Validation technique taken from
            //   http://stackoverflow.com/questions/10092580/stop-form-from-submitting-using-jquery#10092636
            // If the form is invalid, submit it. The form won't actually submit;
            //   this will just cause the browser to display the native HTML5 error messages.
            $("input[type=submit]").click();
            return;
        }

        var data = get_metadata($(this));
        data.ask_total = $("#id_ask_total").val();
        data.numdims = $("input.pricedim").length;

        $.ajax({
            type: "POST",
            url: $("#distribute").attr("data-auto-url"),//"/duopoly_rep_treat/autopricedims/",
            data: data,
            dataType: "json",
            success: resultHandler
        });
    });

})