/**  
 *  页面加载等待页面  
 *  
 * @author gxjiang  
 * @date 2010/7/24  
 *  
 */  
 var height = window.screen.height-250;   
 var width = window.screen.width;   
 var leftW = 300;   
 if(width>1200){   
    leftW = 500;   
 }else if(width>1000){   
    leftW = 350;   
 }else {   
    leftW = 100;   
 }   
    
 var _html = "<div id='Loading' style="position: absolute; z-index: 1000; top: 0px; left: 0px;\
width: 100%; height: 100%; background: white; text-align: left;padding:5px 10px">\
<font>加载中···</font>\
</div>";
    
 window.onload = function(){   
    var _mask = document.getElementById('loading');   
    _mask.parentNode.removeChild(_mask);   
 }   
  
        
 document.write(_html);