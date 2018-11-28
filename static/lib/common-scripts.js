/*---LEFT BAR ACCORDION----*/
$(function() {
  $('#nav-accordion').dcAccordion({
    eventType: 'click',
    autoClose: true,
    saveState: true,
    disableLink: true,
    speed: 'slow',
    showCount: false,
    autoExpand: true,
    classExpand: 'dcjq-current-parent'
  });
});

var Script = function() {

  //    sidebar dropdown menu auto scrolling

  jQuery('#sidebar .sub-menu > a').click(function() {
    var o = ($(this).offset());
    diff = 250 - o.top;
    if (diff > 0)
      $("#sidebar").scrollTo("-=" + Math.abs(diff), 500);
    else
      $("#sidebar").scrollTo("+=" + Math.abs(diff), 500);
  });


  //    sidebar toggle

  $(function() {
    function responsiveView() {
      var wSize = $(window).width();
      if (wSize <= 768) {
        $('#container').addClass('sidebar-close');
        $('#sidebar > ul').hide();
      }

      if (wSize > 768) {
        $('#container').removeClass('sidebar-close');
        $('#sidebar > ul').show();
      }
    }
    $(window).on('load', responsiveView);
    $(window).on('resize', responsiveView);
  });

  $('.fa-bars').click(function() {
    if ($('#sidebar > ul').is(":visible") === true) {
      $('#main-content').css({
        'margin-left': '0px'
      });
      $('#sidebar').css({
        'margin-left': '-210px'
      });
      $('#sidebar > ul').hide();
      $("#container").addClass("sidebar-closed");
    } else {
      $('#main-content').css({
        'margin-left': '210px'
      });
      $('#sidebar > ul').show();
      $('#sidebar').css({
        'margin-left': '0'
      });
      $("#container").removeClass("sidebar-closed");
    }
  });

  // custom scrollbar
  $("#sidebar").niceScroll({
    styler: "fb",
    cursorcolor: "#4ECDC4",
    cursorwidth: '3',
    cursorborderradius: '10px',
    background: '#404040',
    spacebarenabled: false,
    cursorborder: ''
  });

  // widget tools

  jQuery('.panel .tools .fa-chevron-down').click(function() {
    var el = jQuery(this).parents(".panel").children(".panel-body");
    if (jQuery(this).hasClass("fa-chevron-down")) {
      jQuery(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
      el.slideUp(200);
    } else {
      jQuery(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
      el.slideDown(200);
    }
  });

  jQuery('.panel .tools .fa-times').click(function() {
    jQuery(this).parents(".panel").parent().remove();
  });


  //    tool tips

  $('.tooltips').tooltip();

  //    popovers

  $('.popovers').popover();



  // custom bar chart

  if ($(".custom-bar-chart")) {
    $(".bar").each(function() {
      var i = $(this).find(".value").html();
      $(this).find(".value").html("");
      $(this).find(".value").animate({
        height: i
      }, 2000)
    })
  }

}();

jQuery(document).ready(function( $ ) {

  // Go to top
  $('.go-top').on('click', function(e) {
    e.preventDefault();
    $('html, body').animate({scrollTop : 0},500);
  });
});


// process the error of csrf token
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


String.prototype.format= function(){
    var args = Array.prototype.slice.call(arguments);
    var count=0;
    return this.replace(/%s/g,function(s,i){
        return args[count++];
    });
};

// the function to show the notifications of event
function showNotifications(toastType, title, message, timeOut, preventDuplicates){
    timeOut = timeOut||"5000";
    preventDuplicates = preventDuplicates||false;
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-center",
        "preventDuplicates": preventDuplicates,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": timeOut,
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
    toastr[toastType](message, title)
}

// batch operation
$(function () {
    //获取被选中checkbox值
    var checked = function(){
        var checks = $("input[name='check[]']:checked");
        if(checks.length == 0){ alert('未选中任何项！');return false;}

        var checkData = new Array();
        checks.each(function(){
            checkData.push($(this).val());
        });
        console.log(checkData);
        return checkData;
    };

    // 选中单个 checkbox
    $("input[name='check[]']").each(function () {
        var btn = $(this);
        btn.bind("click", function () {
            btn.prop("checked", this.checked);
            if(this.checked == true){
                $("#batch-operate-div #batch-operate").removeAttr("disabled");
            }else{
                $("#batch-operate-div #batch-operate").attr("disabled", "disabled");
            }
        })
    });

    //全选/全不选
    $("#check-all").bind("click",function(){
        $("input[name='check[]']").prop("checked", this.checked);
        // 显示批量操作按钮按钮
        if(this.checked == true){
            $("#batch-operate-div #batch-operate").removeAttr("disabled");
        }else{
            $("#batch-operate-div #batch-operate").attr("disabled", "disabled");
        }
    });

    // 批量操作
    $("#batch-operate").click(function(){
        var checkArr = checked();
        var urlArr = Array();
        for (var i = 0; i < checkArr.length; i ++) {
            if (window.location.href.search("index") != -1) {
                urlArr.push(window.location.href.replace(/index.*$/, "") + checkArr[i] + "/remove/");
            } else {
                var deployUrl = $("button[id='deploy-operation-button']").attr("data-url").replace(/[0-9]+/g, checkArr[i]);
                urlArr.push(deployUrl);
            }
        }

        if(checkArr){
            $("#modal-batch-operate").modal("show");
            $(".js-batch-operate").click(function () {
                for (var i = 0; i < urlArr.length; i ++){
                    $.ajax({
                        cache: false,
                        type: "POST",
                        url: urlArr[i],
                        dataType: "json",
                        async: true,
                        success: function (ret) {
                            if (window.location.href.search("index") == -1) {
                                showNotifications("success",
                                    "Client %s  deployed successfully".format(ret['client']), "", 5000, true);
                            }
                        },
                        error: function(ret){
                            if (window.location.href.search("index") != -1) {
                                showNotifications("error", "Delete failure", JSON.stringify(ret, null, 4));
                            } else {
                                showNotifications("error", "Deployed failure", "", 5000, true);
                                // showNotifications("error", "Deployed failure", JSON.stringify(ret, null, 4));
                            }
                        }
                    })
                }
                $("#modal-batch-operate").modal("hide");
                setTimeout(function () {
                    if (window.location.href.search("index") != -1) {
                        window.location.href = window.location.href.replace(/[?].*$/, "");
                    } else {
                        clientDeployInfo();
                    }
                }, 1000);
            });
        }
    });
});


function searchClick(){
    var keywords = $('#search-keywords').val(),
        request_url = '';
    if(keywords == ""){
        return
    }
    request_url = window.location.href.replace(/[?].*$/, "") + "?keywords=" + keywords;
    window.location.href = request_url
}

$('#searchButton').on('click',function(){
    searchClick()
});
//搜索表单键盘事件(回车)
$("#search-keywords").keydown(function(event){
    if(event.keyCode == 13){
        $('#searchButton').trigger('click');
    }
});

// 处理火狐浏览器跳转问题
function getHref() {
    var index = 0;
    $("button[id='getAHref']").each(function(){
        $(this).click(function(){
            var index_inner = index;
            return function(){
                window.location.href = $("#getAHref a").eq(index_inner).attr('href');
            }
        }(index));
        index++;
    });
}

$(function () {
    getHref();
});


