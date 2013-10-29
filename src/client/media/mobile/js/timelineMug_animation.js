//loading data
var number_time_point=4
var xValue=new Array(number_time_point);
var yValue=new Array(number_time_point);
var number_user=new Array();

$.getJSON( "data_simulated.json", function( data ) {

    xValue[0]=data.x0;
    xValue[1]=data.x1;
    xValue[2]=data.x2;
    xValue[3]=data.x3;
    yValue[0]=data.y0;
    yValue[1]=data.y1;
    yValue[2]=data.y2;
    yValue[3]=data.y3;
    number_user[0]=data.x0.length;
    number_user[1]=data.x1.length;
    number_user[2]=data.x2.length;
    number_user[3]=data.x3.length;
    init();
});

// xValue[i][j] user j's x at i timepoint
//Animation
var canvas;
var ctx;
var background;

var width;
var height;

var mug=new Array(); //store mug image 1-dim
var mug_x=new Array(); // record user i's position at given time point from data 2-dim
var mug_y=new Array(); // 2-dim
var mug_x_current=new Array(); //used in update 1-dim
var mug_y_current=new Array();
var speed_ratio=new Array(); //record user i's speed on x axis from point j to point j+1, 2-dim
var x_vel_direction=new Array(); //velocity=direction*speed_ratio 2-dim
var y_vel_direction=new Array();
var x_vel_current=new Array();
var y_vel_current=new Array();
var time_thresholds=new Array; // used to check which velocity to use
var time_steps=0; //accumulate thorugh update
function init() {
	
	canvas = document.getElementById("MugAnimation");
	width = canvas.width;
	height = canvas.height;
	ctx = canvas.getContext("2d");

	// init mug
    for (var i=0; i<number_user[number_time_point-1]; i++)
    {
       mug[i] = new Image();
	   mug[i].src = 'cafe'+(Math.round(Math.random()*5)).toString()+'.png';
    }
    // assign position
    for (var i=0; i<number_time_point; i++){
       var i_x_Position=new Array();
       var i_y_Position=new Array();
       for (var j=0; j<number_user[i]; j++)       
       {
	       i_x_Position[j] = xValue[i][j]*width;
           i_y_Position[j] = yValue[i][j]*height;
       }
       mug_x[i]=i_x_Position;
       mug_y[i]=i_y_Position;
    }
    
    // calculate speed and velocity for each transition
    
    for (var i=0; i<number_time_point-1; i++)
    {
       ref_dis=Math.sqrt(Math.pow(mug_x[i+1][0]-mug_x[i][0],2)+Math.pow(mug_y[i+1][0]-mug_y[i][0],2));
       if (i==0){
       time_thresholds[i]=ref_dis;}
       else{
       time_thresholds[i]=time_thresholds[i-1]+ref_dis;     // calulate threshold
       }
       var currentRatio=new Array();
       currentRatio[0]=1;
       for (var j=1; j<number_user[i]; j++)
       {
           currentRatio[j]=Math.sqrt(Math.pow(mug_x[i+1][j]-mug_x[i][j],2)+Math.pow(mug_y[i+1][j]-mug_y[i][j],2))/ref_dis;
       }
       speed_ratio[i]=currentRatio;       
    }

    for (var i=0; i<number_time_point-1; i++)
    {
        var x_dir=new Array();
        var y_dir=new Array();
        for (var j=0; j<number_user[i]; j++)
        {
            var dist=Math.sqrt(Math.pow(mug_x[i+1][j]-mug_x[i][j],2)+Math.pow(mug_y[i+1][j]-mug_y[i][j],2));
            x_dir[j]=(mug_x[i+1][j]-mug_x[i][j])/dist;
            y_dir[j]=(mug_y[i+1][j]-mug_y[i][j])/dist;
        }
        x_vel_direction[i]=x_dir;
        y_vel_direction[i]=y_dir;
    }

 	for (var j=0; j<number_user[0]; j++)
	{
		mug_x_current[j]=mug_x[0][j];
		mug_y_current[j]=mug_y[0][j];
        x_vel_current[j]=x_vel_direction[0][j];
        y_vel_current[j]=y_vel_direction[0][j];
	}

    draw();
    
}

function update(){
    if (time_steps<time_thresholds[0])
    {

	    for (var i=0; i<number_user[0]; i++)
        {    
           mug_x_current[i]=mug_x_current[i]+x_vel_current[i]*speed_ratio[0][i];
           mug_y_current[i]=mug_y_current[i]+y_vel_current[i]*speed_ratio[0][i];           
        }
        
        if (time_steps-(time_thresholds[0]-1)>=0)
        {
			
			for (var j=0; j<number_user[1]; j++)
			{
				mug_x_current[j]=mug_x[1][j];
				mug_y_current[j]=mug_y[1][j];
				x_vel_current[j]=x_vel_direction[1][j];
                y_vel_current[j]=y_vel_direction[1][j];
			}
		}
        time_steps+=1; 
        
    }
    else if(time_steps>=time_thresholds[0] && time_steps<time_thresholds[1])
    {

        for (var i=0; i<number_user[1]; i++)
        {    
           mug_x_current[i]=mug_x_current[i]+x_vel_current[i]*speed_ratio[1][i];
           mug_y_current[i]=mug_y_current[i]+y_vel_current[i]*speed_ratio[1][i];           
        }
        if (time_steps-(time_thresholds[1]-1)>=0)
        {

			for (var j=0; j<number_user[2]; j++)
			{
				mug_x_current[j]=mug_x[2][j];
				mug_y_current[j]=mug_y[2][j];
			    x_vel_current[j]=x_vel_direction[2][j];
                y_vel_current[j]=y_vel_direction[2][j];
			}
		}
        time_steps+=1; 
    }
    else if (time_steps>=time_thresholds[1] && time_steps<time_thresholds[2])
    {

        for (var i=0; i<number_user[2]; i++)
        {    
           mug_x_current[i]=mug_x_current[i]+x_vel_current[i]*speed_ratio[2][i];
           mug_y_current[i]=mug_y_current[i]+y_vel_current[i]*speed_ratio[2][i];           
        }
        time_steps+=1; 
	}
}
 
function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    if (time_steps<time_thresholds[0]){
		for (var i=0; i<number_user[0]; i++)
        {
            ctx.drawImage(mug[i], mug_x_current[i], mug_y_current[i],mug[i].width/4,mug[i].height/4);
        }
	}
    else if(time_steps>=time_thresholds[0] && time_steps<time_thresholds[1])
    {
		for (var i=0; i<number_user[1]; i++)
        {   
            ctx.drawImage(mug[i], mug_x_current[i], mug_y_current[i],mug[i].width/4,mug[i].height/4);
        }
	}
	else
	{
		for (var i=0; i<number_user[2]; i++)
        {   
            ctx.drawImage(mug[i], mug_x_current[i], mug_y_current[i],mug[i].width/4,mug[i].height/4);
        }
	}
	
		
}
 
function main_loop() {
	draw();
	update();
	
}
var setID;
function clickreset(){
	
	setID=setInterval(main_loop, 15);	
}

function reset(){
	clearInterval(setID);
	time_steps=0;   
	for (var j=0; j<number_user[0]; j++)
	{
		mug_x_current[j]=mug_x[0][j];
		mug_y_current[j]=mug_y[0][j];
        x_vel_current[j]=x_vel_direction[0][j];
        y_vel_current[j]=y_vel_direction[0][j];
	} 
}

	


