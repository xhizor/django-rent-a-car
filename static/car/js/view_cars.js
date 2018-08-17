$('#view_cars').click(function(){
    axios
        .get('http://localhost:8000/car/list/')
        .then(r => {
            $(this).off('click');
            $('#car_list').show();
            let output = '';
            $.each(r.data, function(key, val) {
                output += '<div class="column is-4"><div class="card"><div class="card-content"><div class="media">' +
                    '<div class="media-left"><figure class="image"><a href="http://localhost:8000/car/' + val.id + '/info/">' +
                    '<img class="car' + val.id + '"></a></figure></div><div class="media-content"><p class="title is-5">' +
                     val.model.name + ' ' + val.name + '</p><p class="subtitle is-6"><i>' + val.engine.name + '</i><br>' +
                     val.engine.power + ' hp</p></div></div><div class="content">Price per hour: <b>$' + val.price_hourly +
                     '</b><br><a href="#"><span class="tag is-success">Rent a car</span></a></div></div></div></div>';

    axios
        .get('http://localhost:8000/car/list/' + val.id + '/gallery/')
        .then(r => {
            let len = r.data.length; // number of car photos
            let i = Math.floor((Math.random() * len)); // get random number from 0 to len
            $('img.car' + val.id).attr('src', r.data[i].photo)
                                 .css({'height': '130px', 'width': '150px'});
            });

    });

         $('div.cars').html('<div class="box" style="width:59%; margin-left: 20.5%;"><div class="columns">' + output +
                            '</div></div><div style="margin-top: 10%;"></div>'); // show output html data

    });

});
