$('#issue-select').on({
    'change': function(){
	var value = this.value;  
	console.log(value);
    if (value==1)
    {
		document.getElementById('hist-issue-image').src='{{url_root}}/media/mobile/img/daily_update/Sustainability, Environment, and Sanitation.svg';
	}
	if (value==2)
    {
		document.getElementById('hist-issue-image').src='{{url_root}}/media/mobile/img/daily_update/Transportation.svg';
	}
	if (value==3)
    {
		document.getElementById('hist-issue-image').src='{{url_root}}/media/mobile/img/daily_update/Education.svg';
	}

    }
});

//todo  participant histogram
