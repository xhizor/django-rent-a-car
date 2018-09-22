$('#get_car_info').click(function () {
   let id = window.location.pathname.split('/')[2];
   const base_url = 'http://localhost:8000/car/list/' + id + '/';

   axios
       .get(base_url)
       .then(r =>{
           $('#back').show();
           $(this).off('click');
           $('div.card').show();
           let car = r.data;
           $('p.title').html(car.model.name + ' ' + car.name);
           let output = '<i>Engine</i>: ' + car.engine.name + ', ' +
           car.engine.power + ' hp, <br>' + car.engine.fuel_type.name + ' ' +
           car.engine.consumation + ' l.<br><br><i>Model year</i>: ' + car.model_year +
           '<br><br><i>Additional Equipment</i>: <ul>';
           let equipment = car.additional_equipment;
           $.each(equipment, function(key, val){
                output += '<li>- ' + val.name + '<li>';
           });
           let img = ''; // rate stars image
           if (!car.rate)
               img = '<img src="/static/car/img/0-star.png" height="150" width="150">';
           else if(Math.round(car.rate) === 1)
               img = '<img src="/static/car/img/1-star.png" height="150" width="150">';
           else if(Math.round(car.rate) === 2)
               img = '<img src="/static/car/img/2-star.png" height="150" width="150">';
           else if(Math.round(car.rate) === 3)
               img = '<img src="/static/car/img/3-star.png" height="150" width="150">';
           else if(Math.round(car.rate) === 4)
               img = '<img src="/static/car/img/4-star.png" height="150" width="150">';
           else
               img = '<img src="/static/car/img/5-star.png" height="150" width="150">';

           $('p.subtitle').html(output + '</ul><br><i>Price per hour:</i> <b>$'
                                + '<span id="car_price">' + car.price_hourly + '</span></b><br><br>' + img);


       });

   axios
       .get(base_url + 'gallery/')
       .then(r => {
           let gallery = r.data;
           let output = '<div class="w3-content w3-display-container">';
           $.each(gallery, function(key, val) {
               output += '<img class="mySlides" src="' + val.photo + '" style="width:100%;">';
           });

           output += '<button class="w3-button w3-black w3-display-left" onclick="plusDivs(-1)">&#10094;</button>' +
                     '<button class="w3-button w3-black w3-display-right" onclick="plusDivs(1)">&#10095;</button></div>';
            $('div.gallery').html(output);
            $('img.mySlides').hide();
            $('img.mySlides:first').show();
       });

});

