var diff=new Date("{{now | date:"o-n-j G:i:s"}}").getTime()-new Date().getTime();
// alert(diff);
function clock()
    {
      var x,h,m,s,n,xingqi,y,mon,d;
      var x = new Date(new Date().getTime()+diff);
      y = x.getYear()+1900;
      if (y>3000) y-=1900;
      mon = x.getMonth()+1;
      d = x.getDate();
      xingqi = x.getDay();
      h=x.getHours();
      m=x.getMinutes();
      s=x.getSeconds();
  
      n=y+"-"+mon+"-"+d+" "+(h>=10?h:"0"+h)+":"+(m>=10?m:"0"+m)+":"+(s>=10?s:"0"+s);
      // alert(n);
      document.getElementById('date').innerHTML=n;
      setTimeout("clock()",1000);
    } 
    clock();
var planstart=new Date("{{contest.start_time | date:"o-n-j G:i:s" }}");
var planend=new Date("{{contest.end_time | date:"o-n-j G:i:s"}}");
function update(){
    var now = new Date(new Date().getTime()+diff);
    if(now<planend && now >planstart){
       var   progress=0;
        progress=(planend-now)/(planend-planstart)*100+"%";
        
        $(".progress-bar").css("width",progress);
        
        $(".progress").addClass("progress-striped active");
        n="Runing";
        document.getElementById('status').innerHTML=n;
    }
    setTimeout("update()",1000);
}
    update();
    var now = new Date(new Date().getTime()+diff);
    if(now>planend){
        $(".progress-bar").css("width",0+"%");
        $("#status").removeClass("label-primary").addClass("label-default");
        n="End";
        document.getElementById('status').innerHTML=n;
    }
    if(now<planstart){
        $(".progress-bar").removeClass("progress-striped active").addClass("progress-bar-success");       
        $(".progress-bar").css("width",100+"%");
        n="scheduled";
        document.getElementById('status').innerHTML=n;
        $("#status").removeClass("label-primary").addClass("label-success");
    }
