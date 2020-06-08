function checkAge(age){
    if(age === ''){
        alert("Fill provide a value");
        return false;
    } else if( age < 18){
        alert("Age must be greater than 18");
        return false;
    } else if(!/^[0-9]+$/.test(age)){
        alert("Enter Numeric Value only");
        return false;
    }
    return true;
}

function checkField(fieldName){
    if(fieldName === ''){
        alert("Fill provide a value");
        return false;
    } else if($.isNumeric(fieldName) == false) {
        alert("Please provide numeric value");
        return false;
    }
    return true;
}

$(document).ready(function(){
    $("#loaderImg").hide();
    $("#notibadge").hide();
});
$("#submitbtn").click(function(e){
    e.preventDefault();
    const age=$("input[name=age]").val();
	const gender=$("input[name=gender]:checked").val();
	const weight=$("input[name=weight]").val();
	const height=$("input[name=height]").val();
	const heartrate=$("input[name=heartrate]").val();
	const bloodpressuresys=$("input[name=bloodpressuresys]").val();
	const bloodpressuredia=$("input[name=bloodpressuredia]").val();
	const cholestrol=$("input[name=cholestrol]").val();
	const avgbloodsugar=$("input[name=avgbloodsugar]").val();
	const alcoholconsumptiondaily=$("input[name=alcoholconsumptiondaily]").val();
	const alocholconsumptionweekly=$("input[name=alocholconsumptionweekly]").val();
    const smoker=$("input[name=smoker]:checked").val();
    
    if(checkAge(age) === false || checkField(weight) === false || checkField(height) === false || checkField(heartrate) === false || checkField(bloodpressuresys) === false || checkField(bloodpressuredia) === false || checkField(cholestrol) === false || checkField(avgbloodsugar) === false || checkField(alcoholconsumptiondaily) === false || checkField(alocholconsumptionweekly) === false){
        console.error("Fill all the values");
        return;
    }
    if(gender === undefined || smoker === undefined){
        alert("Fill all the values for gender / smoke");
        return;
    }
    else{
        $.ajax({
            url: '/api/getScore',
            beforeSend: function(){
                $("#loaderImg").show();
            },
            data: {
                "age":age,
                "gender":gender,
                "weight":weight,
                "height":height,
                "heartrate":heartrate,
                "bloodpressuresys":bloodpressuresys,
                "bloodpressuredia":bloodpressuredia,
                "cholestrol":cholestrol,
                "avgbloodsugar":avgbloodsugar,
                "alcoholconsumptiondaily":alcoholconsumptiondaily,
                "alocholconsumptionweekly":alocholconsumptionweekly,
                "smoker":smoker
            },
            method: 'POST',
            success: function(data){
                data = JSON.parse(data);
                console.log(data['score']);
                $("#healthScoreDisp").html(data['score']);
                let scorecomment = ""
                if(data['score'] >= 80){
                    scorecomment = "You are doing very good"
                    $("#scoreComment").html(scorecomment);
                } else if(data['score'] >= 60 && data['score'] < 80){
                    scorecomment = "Your health score is average";
                    $("#scoreComment").html(scorecomment);
                } else if(data['score'] >= 40 && data['score'] < 60) {
                    scorecomment = "You are not doing well take care";
                    $("#scoreComment").html(scorecomment);
                }
                else if(data['score'] < 40) {
                    scorecomment = "Your health score is very low consult a doctor";
                    $("#scoreComment").html(scorecomment);
                }
                console.log(data['recommendations']);
                for(let i=0;i<data['recommendations'].length;i++) {
                    $("#pageSubmenu").append('<li><a href="#">'+data['recommendations'][i]+'</a></li>');
                }
                alert("Your Health Score is "+data['score']+", "+scorecomment+", for more details please view it on the sidebar");
            },
            complete:function(data){
                $("#loaderImg").hide();
                $("#notibadge").show();
            },
            error: function(jqXHR, exception){
                $("#notibadge").html("Error");
                alert("Error in Health Score calculation. Please check your data and try again");
            }
        });
    }
});
