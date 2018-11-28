$(
    function () {
        $.ajax({
            cache: false,
            type: "GET",
            url: 'deployment/status',
            dataType: "json",
            async: true,
            success: function (ret) {
                $('#client-success').text(ret['client_success']);
                $('#client-error').text(ret['client_error']);
                $('#spider-project').text(ret['project']);
            },
            error: function () {
                console.log('error');
            }
        });
        $.ajax({
            cache: false,
            type: "GET",
            url: 'monitor/server/ping/status',
            dataType: "json",
            async: true,
            success: function (ret) {
                $("#success-server").text(ret['server_success']);
                $("#fail-server").text(ret['server_error']);
            },
            error: function () {
                console.log('error');
            }
        })
    }
);

