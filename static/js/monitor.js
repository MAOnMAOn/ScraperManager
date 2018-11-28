var timer;
function getDatabaseStatus() {
    $('.monitor-status-td').ready(function () {
        $('.monitor-status').each(function () {
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
    getDatabaseStatus();
    viewDatabaseConnection();
    viewServer();
});

// form
$(function () {
    /* Functions */
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-monitor .modal-content").html("");
                $("#modal-monitor").modal("show");
            },
            success: function (data) {
                $("#modal-monitor .modal-content").html(data.html_form);
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
                    $("#monitor-table tbody").html(data.html_monitor_list);
                    $("#modal-monitor").modal("hide");
                    getDatabaseStatus();
                    viewDatabaseConnection();
                    viewServer();
                }
                else {
                    $("#modal-monitor .modal-content").html(data.html_form);
                }
            }
        });
        setTimeout(function () {
            window.location.reload(true);
        }, 500);
        return false;
    };

    // Create monitor
    $(".js-create-monitor").click(loadForm);
    $("#modal-monitor").on("submit", ".js-monitor-create-form", saveForm);

    // Update monitor
    $("#monitor-table").on("click", ".js-update-monitor", loadForm);
    $("#modal-monitor").on("submit", ".js-monitor-update-form", saveForm);

    // Delete monitor
    $("#monitor-table").on("click", ".js-delete-monitor", loadForm);
    $("#modal-monitor").on("submit", ".js-monitor-delete-form", saveForm);
});


function viewCpuUsage(dataArr) {
    var theCanvas = document.getElementById('server-cpu-chart');
    var resizeContainer = function () {
        theCanvas.style.width = $('#server-cpu-container').innerWidth + 'px';
        theCanvas.style.height = $('#server-cpu-container').innerHeight + 'px';
    };
    resizeContainer();

    var myChart = echarts.init(theCanvas);

    option = {
        title: {
            text: 'CPU使用率分时图'
        },
        tooltip : {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        legend: {
            data:['cpu使用率']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                axisLabel:{interval: 1},
                boundaryGap : false,
                data : ['60', '57', '54', '51', '48', '45', '42', '39', '36', '33', '30', '27', '24', '21', '18', '15', '12', '9', '6', '3']
            }
        ],
        yAxis : [
            {
                max: 1.0,
                type : 'value'
            }
        ],
        series : [
            {
                name:'cpu使用率',
                type:'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data: dataArr
            }
        ]
    };
    myChart.setOption(option);
    window.onresize = function () {
        resizeContainer();
        myChart.resize();
    }
}
function viewMemUsage(dataArr) {
    var theCanvas = document.getElementById('server-mem-chart');
    var resizeContainer = function () {
        theCanvas.style.width = $('#server-mem-container').innerWidth + 'px';
        theCanvas.style.height = $('#server-mem-container').innerHeight + 'px';
    };
    resizeContainer();
    var myChart = echarts.init(theCanvas);

    option = {
        title: {
            text: 'Memory使用率分时图'
        },
        tooltip : {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#4cae4c'
                }
            }
        },
        legend: {
            data:['mem使用率']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                axisLabel:{interval: 1},
                boundaryGap : false,
                data : ['60', '57', '54', '51', '48', '45', '42', '39', '36', '33', '30', '27', '24', '21', '18', '15', '12', '9', '6', '3']
            }
        ],
        yAxis : [
            {
                max: 1.0,
                type : 'value'
            }
        ],
        series : [
            {
                name:'mem使用率',
                type:'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {type: 'light'}},
                data: dataArr
            }
        ]
    };
    myChart.setOption(option);
    window.onresize = function () {
        resizeContainer();
        myChart.resize();
    }
}


var cpuDataArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var memDataArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

function viewServerInfo(targetUrl){
    $.ajax({
        cache: false,
        type: "GET",
        url: targetUrl,
        dataType: "json",
        async: true,
        success: function (ret) {
            $("#server-info-div" + " " + "pre").css("display", "");
            $("#server-info-div" + " " + "pre").text(ret['message']);
            $("#server-info-div" + " " + "#server-name-i").text('Server: ' + ret['name']);
            var info = "cores: %s, processor: %s, memory: %s";
            $("#server-info-div" + " " + "#server-hardware-i").text(info.format(ret['physical_cores'],
                ret['processor_cores'], ret['total_mem']));
            cpuDataArray.push(ret['cpu_use']);
            memDataArray.push(ret['mem_used_percent']);
            cpuDataArray.shift();
            memDataArray.shift();
            viewCpuUsage(cpuDataArray);
            viewMemUsage(memDataArray);
        },
        error: function(){
            // throw new Error("搞什么鬼！");
            showNotifications("error", "Connection failed... Please check again", "", 15000, true);
        }
    });
}


// view the page of server monitor
function viewServer() {
    $("button[name='view-server-info']").each(function () {
        var btn = $(this);
        btn.click(function () {
            showNotifications("success", "Starting... Please Wait");
            var thisId = btn.attr('id');
            var dataUrl = $("#" + thisId).attr("data-url");

            clearInterval(timer);
            timer = setInterval(function () {
                viewServerInfo(dataUrl);
            }, 3000);
        })
    });
}


// the page of the database client monitor
// db connection tree view
function viewDatabaseConnection(){
    $("button[id='view-db-connection']").each(function () {
        var btn = $(this);
        btn.click(function () {
            showNotifications("info", "Connecting... Please Wait", undefined, "1500");
            var myUrl = $(this).attr("data-url");
            $.ajax({
                cache: false,
                type: "GET",
                url: myUrl,
                dataType: "json",
                async: true,
                success: function (ret) {
                    $('#db-connect-tree').treeview({
                        data: ret,
                        color: "#428bca",
                        expandIcon: "fa fa-database",
                        collapseIcon: "fa fa-database",
                        emptyIcon: "fa fa-table",
                        enableLinks: true,
                        levels: 1
                    });
                    var dbType;
                    var tags = ret[0]['tags'];
                    if (tags[1] == 1) {
                        dbType = 'MySQL';
                    } else if (tags[1] == 2) {
                        dbType = 'MongoDB';
                    } else if (tags[1] == 3) {
                        dbType = 'Redis';
                    }
                    $('#monitor-db-title').html('<i class="fa fa-database"></i>&nbsp;' +
                        dbType + ': ' + ret[0]['tags'][0]);
                },
                error: function(){
                    showNotifications("error", "Connection failed... Please check again");
                }
            });
        })
    });

}

// 增加点击事件，单击菜单也能展开和折叠
function itemOnclick(target){
    //找到当前节点id
    var nodeid = $(target).attr('data-nodeid');
    var tree = $('#db-connect-tree');
    //获取当前节点对象
    var node = tree.treeview('getNode', nodeid);
    if(node.state.expanded){
        //处于展开状态则折叠
        tree.treeview('collapseNode', node.nodeId);
    } else {
        //展开
        tree.treeview('expandNode', node.nodeId);
    }
}


// Builds the HTML Table out of myList.
function buildHtmlTable(myList, selector) {
    var columns = addAllColumnHeaders(myList, selector);
    for (var i = 0; i < myList.length; i++) {
        var row$ = $('<tr/>');
        for (var colIndex = 0; colIndex < columns.length; colIndex++) {
            var cellValue = myList[i][columns[colIndex]];
            if (cellValue == null) cellValue = "";
            row$.append($('<td/>').html(cellValue));
        }
        $(selector).append(row$);
    }
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain all records.
function addAllColumnHeaders(myList, selector) {
    var columnSet = [];
    var headerTr$ = $('<tr/>');
    for (var i = 0; i < myList.length; i++) {
        var rowHash = myList[i];
        for (var key in rowHash) {
            if ($.inArray(key, columnSet) == -1) {
                columnSet.push(key);
                headerTr$.append($('<th/>').html(key));
            }
        }
    }
    $(selector).append(headerTr$);
    return columnSet;
}

function getTableOnClick(target) {
    var myUrl = $(target).attr("data-url");
    $.ajax({
        cache: false,
        type: "GET",
        url: myUrl,
        dataType: "json",
        async: true,
        success: function (ret) {
            var btn = $("#DBDataTable");
            btn.empty();
            btn.colResizable({disable: true});
            buildHtmlTable(ret[0], '#DBDataTable');
            // resize the width of the table td cell
            var cells = document.getElementById("DBDataTable").rows.item(0).cells.length;
            if (cells > 10) {
                btn.colResizable({resizeMode: 'overflow'});
            } else {
                btn.colResizable({resizeMode: 'fit'});
            }
            btn.colResizable({liveDrag: true});
            if (ret[1]['db_type'] == 'mysql') {
                var info = "%s@%s";
                $(".table-info1").text(info.format(ret[1]['table'], ret[1]['database']));
                $(".table-info2").text('table size: ' + ret[1]['size'])
            }
            if (ret[1]['db_type'] == 'mongodb') {
                var info = "database:%s>%s";
                $(".table-info1").text(info.format(ret[1]['database'], ret[1]['collection']));
                $(".table-info2").text('collection size: ' + ret[1]['size'])
            }
            if (ret[1]['db_type'] == 'redis') {
                var info = "db:%s>collection:%s";
                $(".table-info1").text(info.format(ret[1]['database'], ret[1]['key']));
                $(".table-info2").text('key size: ' + ret[1]['size'])
            }
        },
        error: function(){
            console.log("get table error");
        }
    });
}


