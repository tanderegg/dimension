$(document).ready(function() {
    // I think this works for multiple questions on a page.
    //  I think I'd need to add css for .quiz_js.selected
    // Currently just tested for a single quiz question per page.
    var quizzes = $("div.quiz_js");


    var selectQuestion = function(selected, i){
        if(i == quizzes.length){
            $("form").submit();
            return 0;
        }
        quizzes.eq(selected).removeClass("selected");
        selected = i;

        // New selected
        var quiz = quizzes.eq(selected).addClass("selected");
        $(".question", quiz).show();
        $(".answer", quiz).hide();

        // Next Button Click
        $("nav .next").unbind().click(function(){
            selected = selectAnswer(selected)
        });

        return selected;
    }

    var selectAnswer = function(selected){
        var quiz = quizzes.eq(selected);
        // Capture the participant's answer
        var name = "q" + (selected + 1).toString();
        var correct = $("input:radio[name='" + name + "']:checked").attr("data-correct");

        // Show what must be shown
        $(".question", quiz).hide();
        $(".answer", quiz).show();
        if(correct == "true"){
            $(".correct", quiz).show()
        } else{
            $(".incorrect", quiz).show()
        }
        // Change Next behavior to view the next question
        $("nav .next").unbind().click(function(){
            selected = selectQuestion(selected, selected + 1)
        });
    }

    // Init
    var selected = selectQuestion(0, 0);
});