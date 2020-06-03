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
    
    if(age === '' || gender=== '' || weight=== '' || height=== '' || heartrate=== '' || bloodpressuresys=== '' || bloodpressuredia=== '' || cholestrol=== '' || avgbloodsugar=== '' || alcoholconsumptiondaily=== '' || alocholconsumptionweekly=== '' || smoker=== ''){
        alert("Please Enter Values in all the fields!!");
    } else{
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
                console.log(data['recommendations']);
                for(let i=0;i<data['recommendations'].length;i++) {
                    $("#pageSubmenu").append('<li><a href="#">'+data['recommendations'][i]+'</a></li>');
                }
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