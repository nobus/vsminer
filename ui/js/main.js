$(document).ready(function(){
    var scale = 4; // 1440x1440
    var width = 360*scale;
    var height = 360*scale;

    var stage = new Konva.Stage({
        container: 'celestial',
        width: width,
        height: height,
    });

    function pix2deg (x, y) {
        // x = ra, y = dec
        return {'ra': (x/scale)-180, 'dec': 180-(y/scale)};
    }

    function deg2pix (ra, dec) {
        // ra = x, dec = y
        return {'x': (ra+180)*scale, 'y': ((dec-180)*scale)*-1};
    }

    var layer = new Konva.Layer();
    stage.add(layer);

    var rect = new Konva.Rect({
        width: width,
        height: height,
        fill: 'black',
        stroke: 'gray',
        strokeWidth: 5
      });

    layer.add(rect);

    for (var i = 0; i < 360*scale; i = i + 10*scale) {
        var lineRA = new Konva.Line({
            points: [i, 0, i, height],
            stroke: (i === ((360*scale)/2) ? 'red': 'white'),
            strokeWidth: 1,
        });

        var lineDec = new Konva.Line({
            points: [0, i, width, i],
            stroke: (i === ((360*scale)/2) ? 'red': 'white'),
            strokeWidth: 1,
        });

        layer.add(lineRA);
        layer.add(lineDec);
    }

    $.ajax("/api/jobs/?format=json")
        .done(function(data) {
            for (var i = 0; i < data.length; i++) {
                var coord = deg2pix(data[i].center_ra, data[i].center_dec);

                var circle = new Konva.Circle({
                    x: coord.x,
                    y: coord.y,
                    radius: data[i].radius*scale,
                    stroke: 'lime',
                    strokeWidth: 2,
                    astroJob: data[i].job_number,
                });

                circle.on('click', function () {
                    var win = window.open('/viewer.html?job='+this.attrs.astroJob, '_blank');
                    if (win) {
                        win.focus();
                    } else {
                        alert('Please allow popups for this website');
                    };
                });

                layer.add(circle);
            }

            layer.batchDraw();        
        }).fail(function(err) {
            alert("error " + err.status);
        });

    

    stage.on('mousemove', function() {
        var mousePos = stage.getPointerPosition();
        var coord = pix2deg(mousePos.x, mousePos.y);
        //console.log(deg2pix(coord.ra, coord.dec));
    });
});
