$(document).ready(function() {

    //
    // Section Nav
    //
    // Helper functions
    var disablePrev = function(){
        $("nav .prev").attr("disabled", "disabled");
    };
    var enablePrev = function(){
        $("nav .prev").removeAttr("disabled");
    }


    var sections = $("section");
    var quiz = $("div.quiz_js");
    var form = $("#form");
    // Give first section display
    sections.eq(0).addClass("selected");
    form.addClass("selected_section_0");

    if (sections.length > 1){
        // Make the nav dots
        var dot_h = $("<div class='dots'></div>").css("width", sections.length*(14 + 20) - 20);
        $("nav").prepend(dot_h);
        sections.each(function(){
            $(dot_h).append("<div class='dot'></div>");
        });
        var dots = $(".dot", dot_h);
        dots.eq(0).addClass("selected");

        // Helper function
        var selectSection = function(selected, i){
            // form, dots, and sections are in scope
            if(i == sections.length){
                // this is better than form.submit bc it gets the browsers field validation
                $("nav input[type='submit']").click();
                // in case submit fails due to field validation
                return selected;
            }
            sections.eq(selected).removeClass("selected");
            dots.eq(selected).removeClass("selected");
            form.removeClass("selected_section_" + selected)
            selected = i;

            // New selected
            sections.eq(selected).addClass("selected");
            dots.eq(selected).addClass("selected");
            form.addClass("selected_section_" + selected)

            if(selected == 0) {
                disablePrev();
            } else{
                enablePrev();
            }
            return selected;
        }

        // Implement js pagination
        var selected = 0;
        disablePrev();

        // Dot clicking
        dots.each(function(i, dot){
            $(dot).click(function(){
                selected = selectSection(selected, i);
            })
        })
        // Next Button Click
        $("nav .next").click(function(){
            selected = selectSection(selected, selected + 1)
        });
        // Prev Button Click
        $("nav .prev").click(function(){
            selected = selectSection(selected, selected - 1)
        });

    } else if (quiz.length > 0){
        // quiz logic moved to quiz.js
    } else{

        // There is only one section here. No pagination necessary.
        disablePrev();
        // $("nav .next").attr("type", "submit");
        $("nav .next").click(function(){
            // Every page should have this element, and invisible submit input.
            // It would be easier to make the next button into a "submit" type, but this methodolody matches
            //  the methodology for multiple navigation pages
            $("nav input[type='submit']").click();
        });
    }


});