// change color and value for client status
// setInterval("getClientStatus()", 10000);
function getClientStatus() {
    $('.client-status-td').ready(function () {
        $('.client-status').each(function () {
            var theThis = this; // this is something unsolved.
            $.ajax({
                cache: false,
                type: "GET",
                url: $(theThis).attr("data-url"),
                dataType: "json",
                async: true,
                beforeSend: function() {
                    $(theThis).removeClass('btn-success').removeClass('btn-danger').addClass('btn-warning').text('Connecting');
                },
                success: function (ret) {
                    // $(theThis).removeClass('btn-danger').addClass('btn-success').text('Normal');
                    if (ret['result'] == "1"){
                        $(theThis).removeClass('btn-danger').removeClass('btn-warning').addClass('btn-success').text('Normal');
                    }
                },
                error: function(){
                    $(theThis).removeClass('btn-success').removeClass('btn-warning').addClass('btn-danger').text('Error');
                }
            });
        });
    });
}

$(function () {
    /* Functions */
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-client .modal-content").html("");
                $("#modal-client").modal("show");
            },
            success: function (data) {
                $("#modal-client .modal-content").html(data.html_form);
            }
        });
    };
    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#client-table tbody").html(data.html_client_list);
                    $("#modal-client").modal("hide");
                    getClientStatus();
                }
                else {
                    $("#modal-client .modal-content").html(data.html_form);
                }
            }
        });
        setTimeout(function () {
            window.location.reload(true);
        }, 200);
        return false;
    };

    // Create client
    $(".js-create-client").click(loadForm);
    $("#modal-client").on("submit", ".js-client-create-form", saveForm);

    // Update client
    $("#client-table").on("click", ".js-update-client", loadForm);
    $("#modal-client").on("submit", ".js-client-update-form", saveForm);

    // Delete client
    $("#client-table").on("click", ".js-delete-client", loadForm);
    $("#modal-client").on("submit", ".js-client-delete-form", saveForm);
});


// modify the attribute of html element
function modifyElementAttr(project_id){
    var arr = [];
    var panelJob = $('.panel-spider-job_' + project_id);
    panelJob.each(function () {
        var btn = $(this);
        var myId = btn.attr('id').split("_");
        var spider_project_id = myId.slice(myId.length - 2, myId.length-1);
        if (spider_project_id[0] == project_id){
            arr.push(parseInt(myId[myId.length -1]));
        }
    });
    var newMax = Math.max.apply(Math, arr) + 1;
    if (newMax == Infinity || newMax == -Infinity){
        newMax = 1;
    }
    return "_" + newMax
}

function appendSpiderElement(project_id, append_obj){
    // Maybe you need to Overriding regular expressions !
    var appendElement = append_obj.replace(/_[0-9]+/g, modifyElementAttr(project_id));
    // $('.panel-group-accordion_' + project_id).append(appendElement);
    $('.panel-group-accordion_' + project_id).prepend(appendElement);
}

// add data(from spider job list) to dom
function processingSpiderData(base_selector, spider_id, spider_name, start_obj, end_obj, spider_status) {
    // modify the cancel button url if spider is click on start
    var cancelUrl = $(base_selector  + " " + "#job-cancel-button").attr('data-url').replace(/job.*/g, 'job/' + spider_id + '/cancel');
    $(base_selector  + " " + "#job-cancel-button").attr('data-url', cancelUrl);

    // modify the job log  url if spider is click on start
    var logUrl = $(base_selector  + " " + "#job-log-a-id").attr('data-url');
    logUrl = logUrl.replace(/crawler\/.*/g, 'crawler/' + spider_name + '/job/' + spider_id + '/log');
    $(base_selector  + " " + "#job-log-a-id").attr('data-url', logUrl);
    //
    $(base_selector  + " " + "#spider-job-id").text(spider_id);  // insert job id
    $(base_selector  + " " + "#spider-job-name").text(spider_name);  // insert spider name of job
    $(base_selector  + " " + "span[data-value=\"spider-start-time\"]").text(start_obj);  // insert start time

    if (spider_status == "finished") {
        $(base_selector  + " " + "#job-cancel-span").css({"display": "none"});  // hidden the button of cancel span
        $(base_selector  + " " + "#end-time-display-span").css("display", "");  // show the end time
        // modify the css of the job status button
        $(base_selector  + " " + "#spider-job-status-button").removeClass("btn-warning").removeClass("btn-theme03").addClass("btn-info");
        $(base_selector  + " " + "span[data-value=\"spider-end-time\"]").text(end_obj);   //   insert end time of job
    }
    if (spider_status == "pending") {
        $(base_selector  + " " + "#end-time-display-span").css({"display": "none"});
        $(base_selector  + " " + "#job-cancel-span").css("display", "");  // show the cancel button
        $(base_selector  + " " + "#spider-job-status-button").removeClass("btn-theme03").removeClass("btn-info").addClass("btn-warning");
    }
    if (spider_status == "running") {
        $(base_selector  + " " + "#end-time-display-span").css({"display": "none"});
        $(base_selector  + " " + "#job-cancel-span").css("display", "");
        $(base_selector  + " " + "#spider-job-status-button").removeClass("btn-warning").removeClass("btn-info").addClass("btn-theme03");
        $(base_selector  + " " + "#spider-job-cancel-span").text("stop");  //   insert stop text to span
    }
    $(base_selector  + " " + "#spider-job-status-span").text(spider_status);  // insert job status
}

setInterval("getSpiderJobList()", 4500);
function getSpiderJobList() {
    $('.spider-job-list-div').each(function () {
        var btn = $(this);
        var myUrl = btn.attr("data-url");
        $.ajax({
            cache: false,
            type: "GET",
            url: myUrl,
            dataType: "json",
            async: true,
            success: function (ret) {
                var data = ret[ret.length - 1];
                var project_id = data["project"];
                var btn = $('.panel-spider-job_' + project_id);
                var lengthDiff = ret.length - btn.length;
                while (lengthDiff > 0) {
                    appendSpiderElement(project_id, data["html_spider_job"]);
                    lengthDiff = lengthDiff - 1
                }
                btn.each(function (n) {
                    var newId = $(this).attr('id');
                    processingSpiderData("#" + newId, ret[n]["id"], ret[n]["spider"],
                        ret[n]["start_time"], ret[n]["end_time"], ret[n]["status"]);
                });
            }
        });
    })
}


function processClick(target) {
    var btn = $(target).next();
    if (btn.css("display")=="none") {
        btn.css({"display": ""});
    } else {
        btn.css({"display": "none"});
    }
}


// start a spider job and append div block
$("button[name='spider-run']").each(function () {
    var btn = $(this);
    btn.click(function () {
        var myUrl = $(this).attr("data-url");
        var myId = $(this).attr("id");
        $.ajax({
            cache: false,
            type: "GET",
            url: myUrl,
            dataType: "json",
            async: true,
            success: function (ret) {
                appendSpiderElement(myId, ret["html_spider_job"]);
                getSpiderJobList();
                showNotifications("success", "Run Spider successfully");
                // hidden the span of end time when spider start
                $(myId  + " " + "#end-time-display-span").css({"display": "none"});
                // if finish append opreation, should call cancel click function, else No reply when click
                getJobLog();
                cancelSpiderJob();
            },
            error: function(){
                console.log("error");
            }
        });

    })
});


// cancel a spider job
function cancelSpiderJob() {
    $("button[id='job-cancel-button']").each(function () {
        var btn = $(this);
        btn.click(function () {
            $("div[id^='panel-spider-job__']").css({"display": "none"});
            var myUrl = $(this).attr("data-url");
            $.ajax({
                cache: false,
                type: "GET",
                url: myUrl,
                dataType: "json",
                async: true,
                success: function (ret) {
                    console.log("停止信号" + ret);
                    getSpiderJobList();
                },
                error: function(){
                    console.log("error");
                }
            })
        });
    });
}


// get the spider job log text from the HttpResponse
setInterval("getJobLog()", 3000);
function getJobLog() {
    $('.client-container-div').each(function () {
        var btn = $(this);
        var containerId = btn.attr("id");
        $(".panel-spider-job_" + containerId).each(function () {
            var btn = $(this);
            var myId = btn.attr('id');
            var logUrl = $("#" + myId + " " + "#job-log-a-id").attr("data-url");
            $.ajax({
                cache: false,
                dataType: "text",
                type: "GET",
                url: logUrl,
                async: true,
                success: function (res) {
                    $("#" + myId + " " + "#job-log-text #log-pre").text(res);
                }
            });
        });
    });
}


// load page data where project table load
$("#project-deploy-tbody").ready(function () {
    // console.log(btn.attr("href"));
    $(".project-build-a").each(function () {
        var aSelector = $(this);
        var myId = aSelector.attr('id');
        $.ajax({
            cache: false,
            type: "GET",
            url: aSelector.attr("href"),
            dataType: "json",
            async: true,
            success: function (ret) {
                $("#" + myId + " " + ".project-desc").text(ret["desc"]);
                if (ret["built_at"] != null){
                    $("#" + myId + " " + ".project-build-td").text("✓");
                } else {
                    $("#" + myId + " " + ".project-build-td").text("✗");
                }
                if (ret["configurable"] === 0) {
                    $("#" + myId + " " + ".project-config-td").text("✗");
                } else {
                    $("#" + myId + " " + ".project-config-td").text("✓");
                }
                $("#" + myId + " " + ".project-build-time-td").text(ret["built_at"]);
            }
        })
    });
});

// // The function of project deploy
// get egg information for built project
function getEggInfo() {
    $.ajax({
        cache: false,
        dataType: "json",
        type: "GET",
        url: $("#build-info-a").attr("href"),
        async: true,
        success: function (res) {
            if (res["egg"] != null) {
                $("#build-span").text("rebuild");
            }
            $("#package-egg").text(res["egg"]);
            $("#package-build-at").text(res["built_at"]);
        }
    });
}

// insert client info to table
function clientDeployInfo() {
    $(".deploy-tr").each(function () {
        var btn = $(this);
        var clientId = btn.attr('id');
        var deployVersionUrl = $("#" + clientId + " " + "#deploy-version-a").attr("href");
        $.ajax({
            cache: false,
            dataType: "json",
            type: "GET",
            url: deployVersionUrl,
            async: true,
            success: function (res) {
                $("#" + clientId + " " + "#deploy-at-span").text(res["deployed_at"]);
                if (res["desc"] != null){
                    $("#" + clientId + " " + ".deploy-desc").text(res["desc"])
                }
            },
            error: function () {
                console.log("get deploy url error");
            }
        })
    });
}

function deployProject() {
    $("button[id='deploy-operation-button']").each(function () {
        var btn = $(this);
        btn.click(function () {
            var deployUrl = $(this).attr("data-url");
            $.ajax({
                cache: false,
                type: "POST",
                url: deployUrl,
                dataType: "json",
                async: true,
                success: function (ret) {
                    showNotifications("success", // Client 18 Failed to Deploy
                        "Client %s  deployed successfully".format(ret['client']));
                    clientDeployInfo();
                },
                error: function(ret){
                    console.log(ret);
                    showNotifications("error", "Deployed failure",
                        JSON.stringify(ret, null, 4));
                }
            });
        })
    });
}

// 点击回车键禁止提交表单
$("#build-project-desc").bind("keydown",function(event){
    if(event.keyCode == 13){
        return false;
    }
});


// build project to egg and post data
function buildPackageEgg() {
    $("button[id='build-project-button']").click(function () {
        var btn = $(this);
        var buildUrl = btn.attr("data-url");
        var description = {"description": $("#build-project-desc").val()};

        $.ajax({
            cache: false,
            dataType: "json",
            type: "POST",
            data: description,
            url: buildUrl,
            async: true,
            success: function (ret) {
                showNotifications("success",
                    "The %s project was successfully built".format(ret['name']));
                console.log(ret);
                getEggInfo();
            },
            error: function(){
                showNotifications("error", "Construction failure", "Just check it again!");
            }
        });
    });
}

$(function () {
    getClientStatus();
    getSpiderJobList();
    getJobLog();
    getEggInfo();
    clientDeployInfo();
    deployProject();
    buildPackageEgg();
});


