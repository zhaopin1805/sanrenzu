




//页签切换效果
function setTab(name,cursel,n){
	for(i=1;i<=n;i++){
		var menu=$("#"+name+i);
		var con=$("#con_"+name+"_"+i);		
		if(i==cursel)
		{
			$(menu).addClass("hover");
			$(con).fadeTo("slow", 1);
		}
		else
		{
			$(menu).removeClass("hover");
			$(con).hide();
		}
	}
}

// function changeClick (){
//     var demo = document.getElementById("demo");
// 	if(demo.style.display=='none'){
// 		demo.style.display='block'
// 	}else if(demo.style.display=='block'){
// 		demo.style.display='none'
// 	}
// }

	$(function(){
		$('.grzx').hover(function () {
		  $('.grzx-xsnav').show()
		}, function () {
		  $('.grzx-xsnav').hide()
		})
		$('.grzx-xsnav').hover(function () {
		  $(this).show()
		}, function () {
		  $(this).hide()
		})
	})


