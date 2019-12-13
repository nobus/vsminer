$(document).ready(function(){
    var period = 20000;

    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');

        for(var i = 0; i <ca.length; i++) {
          var c = ca[i];

          while (c.charAt(0) == ' ') {
            c = c.substring(1);
          }

          if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
          }
        }
        return "";
      }


    function getCeletyInfo () {
        $.ajax({
                url: "/api/celery_status/",
                method: "GET",
            })
            .done(function(data) {
                var html = "";
                var resp = data.resp;

                for (var i = 0; i < resp.length; i++) {
                    html += "id: " + resp[i]["id"] + "</br>"
                        + "name: " + resp[i]["name"] + "</br>"
                        + "args: " + resp[i]["args"] + "</br>"
                        + "kwargs: " + resp[i]["kwargs"] + "</br>"
                }

                $("#job_list").html(html);

                setTimeout(getCeletyInfo, period);
            })
            .fail(function(err) {
                alert("error " + err.status);
                setTimeout(getCeletyInfo, period);
            });
    }

    $('#submit').click(function() {
        var data = {
            'job_number': $('#job_number').val(),
            'status_url': $('#status_url').val(),
        };

        $.ajax({
                url: "/api/put_astrojob/",
                method: "POST",
                contentType: "application/json",
                dataType: 'json',
                data: JSON.stringify(data),
            })
            .done(function(data) {
                alert(data);
                $('#job_number').val('');
                $('#status_url').val('');
            })
            .fail(function(err) {
                alert("error " + err.status);
            });

    });

    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    getCeletyInfo();
});
