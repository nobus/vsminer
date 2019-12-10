$(document).ready(function(){
    function getUrlParams() {
        var params = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');

        for(var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            params.push(hash[0]);
            params[hash[0]] = hash[1];
        }

        return params;
    }

    var params = getUrlParams();
    var astroJob = params['job'];

    $("#dialog").dialog({
        width: 400,
        height: 500,
        buttons: {
            "Cross on/off": function() {
                var current = crossChair.visible();
                crossChair.visible(!current);
            },
            "Stars on/off": function() {
                var current = starLayer.visible();
                starLayer.visible(!current);
            },
        },
    }).dialogExtend({
        "closable": false,
        "collapsable" : true,
    });

    $("#dialog").parent().css('position', 'fixed');

    var titleBar = $("#dialog").parent().children(".ui-dialog-titlebar");

    var WIDTH = 5202;
    var HEIGHT = 3465;

    var stage = new Konva.Stage({
        container: 'container',
        width: WIDTH,
        height: HEIGHT,
        //draggable: true,
    });

    var layer = new Konva.Layer();
    stage.add(layer);

    var imageObj = new Image();

    imageObj.onload = function() {
        var new_fits = new Konva.Image({
            x: 0,
            y: 0,
            image: imageObj,
            width: WIDTH,
            height: HEIGHT,
        });

        layer.add(new_fits);
        layer.batchDraw();
        };

    // http://nova.astrometry.net/user_images/3210682#annotated
    imageObj.src = '../data/' + astroJob + '/new_fits.png';

    var crossChair = new Konva.Layer();
    stage.add(crossChair);

    var redLineVert = new Konva.Line({
        points: [WIDTH/2, 0, WIDTH/2, HEIGHT],
        stroke: 'red',
        strokeWidth: 1,
    });

    var redLineHor = new Konva.Line({
        points: [0, HEIGHT/2, WIDTH, HEIGHT/2],
        stroke: 'red',
        strokeWidth: 1,
    });

    crossChair.add(redLineVert);
    crossChair.add(redLineHor);
    crossChair.batchDraw();

    var title = $("#dialog").parent().children(".ui-dialog-titlebar").children(".ui-dialog-title");

    stage.on('mousemove', function() {
        var mousePos = stage.getPointerPosition();
        title.html('x: ' + mousePos.x + '; y: ' + mousePos.y);
    });

    var starLayer = new Konva.Layer();
    stage.add(starLayer);

    $.ajax("/api/star_data/?astro_job=" + astroJob + "&format=json")
        .done(function(data) {
            for (var i = 0; i < data.length; i++) {
                var aavso = data[i].aavso_data;
                var simbad = data[i].simbad_data;

                var starName = simbad.MAIN_ID;

                var color = 'lime';
                var minMag, maxMag;

                if (aavso) {
                    color = (aavso.Category === 'Variable') ? 'red' : 'lime';
                    minMag = aavso.MinMag;
                    maxMag = aavso.MaxMag;
                }

                var tableRec = '<tr>'
                    + '<td>' + starName + '</td>'
                    + '<td>' + data[i].field_ra + '</td>'
                    + '<td>' + data[i].field_dec + '</td>'
                    + '<td>' + minMag + '</td>'
                    + '<td>' + maxMag + '</td>'
                    + '</tr>';

                $('#myTable').children('.tablebody').append(tableRec);

                var circle = new Konva.Circle({
                    x: data[i].field_x,
                    y: data[i].field_y,
                    radius: 15,
                    stroke: color,
                    strokeWidth: 2,
                    starName: starName,
                });

                circle.on('click', function () {
                    console.log(this);
                });

                var text = new Konva.Text({
                    x: data[i].field_x + 16,
                    y: data[i].field_y,
                    text: starName,
                    fontSize: 20,
                    fontFamily: 'Arial',
                    fill: color,
                    starName: starName,
                });

                text.on('click', function () {
                    console.log(this.attrs.starName);
                });

                starLayer.add(circle);
                starLayer.add(text);


            }

            $("#myTable").tablesorter();
            starLayer.batchDraw();
        }).fail(function(err) {
            alert("error " + err.status);
        });

});
