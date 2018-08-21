$('input[type="checkbox"], input[type="radio"], #search_cars').click(function () {
    let url = 'http://localhost:8000/car/list/';
    const car_name = $('#car_name').val().trim();
    const brand = $('#brand').val();
    const model_year = $('#model_year').val();
    const price_from = $('#price_from').val();
    const price_to = $('#price_to').val();
    const top_rated = $('#top_rated:checked').val();
    const fuel_type = $('input[type="radio"]:checked')
                      .parent('label').text();

    if (car_name)
        url += '?search=' + car_name;
    else if (brand)
        url += '?search=' + brand;
    else if (model_year) {
        if (model_year === '2000')
            url += '?year_from=0&year_to=2000';
        else if (model_year === '2005')
            url += '?year_from=2001&year_to=2005';
        else if (model_year === '2010')
            url += '?year_from=2006&year_to=2010';
        else if (model_year === '2015')
            url += '?year_from=2011&year_to=2015';
        else
            url += '?year_from=2016&year_to=2018';
    }
    else if (price_from && price_to)
        url += '?price_from=' + price_from + '&price_to=' + price_to;
    else if (top_rated)
        url += '?top_rated=True';
    else if (fuel_type)
        url += '?fuel_type=' + fuel_type;

    axios
        .get(url)
        .then(r => {
            $('#car_list').show();
            let output = '';
            let cars = r.data;
            let total_cars = Object.keys(cars).length;
            let counter = 0;
            if (!total_cars) {
                $('div.cars').html('<div class="box" style="width:59%; margin-left: 20.5%;">' +
                    '<div class="columns"><div class="column is-5"></div><div class="column">' +
                    '<i style="color:rgb(255, 56, 96);"><b>Oops! No results found.</b></i></div></div></div>' +
                    '<div style="margin-top: 20%;"></div>'); // if car not found
                return;
            }
            $.each(cars, function (key, val) {
                   if (counter >= 3)
                        output += '</div>';
                    if (!(counter % 3))
                        output += '<div class=columns>';
                output += '<div class="column is-4"><div class="card"><div class="card-content"><div class="media">' +
                    '<div class="media-left"><figure class="image"><a href="http://localhost:8000/car/' + val.id + '/info/">' +
                    '<img class="car' + val.id + '"></a></figure></div><div class="media-content"><p class="title is-5">' +
                    val.model.name + ' ' + val.name + '</p><p class="subtitle is-6"><i>' + val.engine.name + '</i><br>' +
                    val.engine.power + ' hp<br>' + val.model_year + '</p></div></div><div class="content">Price per hour: <b>$' +
                    val.price_hourly + '</b><br><a href="#"><span class="tag is-success">Rent a car</span></a></div></div></div></div>';
                counter++;
        axios
            .get('http://localhost:8000/car/list/' + val.id + '/gallery/')
            .then(r => {
                let photos = r.data;
                let len = photos.length; // number of car photos
                let i = Math.floor((Math.random() * len)); // get random number from 0 to len
                $('img.car' + val.id).attr('src', photos[i].photo)
                                     .css({'height': '130px', 'width': '150px'});
                });
           });

            $('div.cars').html('<span style="margin-left: 20.5%;" class="tag is-primary">Total cars: ' + total_cars +
            '</span><br><br><br><div class="columns"><div class="box" style="width:59%; margin-left: 20.5%;">' + output +
            '</div></div></div><div style="margin-top: 5%;"></div>');

        });
});