$('#get_car_info').click(function () {
   let id = window.location.pathname.split('/')[2];
   const baseUrl = 'http://localhost:8000/car/list/' + id + '/';

   axios
       .get(baseUrl)
       .then(r =>{
           let car = r.data;
           $(this).off('click');
           $('div.card').show();
           $('p.title').html(car.model.name + ' ' + car.name);
           let output = '<i>Engine</i>: ' + car.engine.name + ', ' +
           car.engine.power + ' hp, <br>' + car.engine.fuel_type.name + ' ' +
           car.engine.consumation + ' l.<br><br><i>Additional Equipment</i>: <ul>';
           let equipment = car.additional_equipment;
           $.each(equipment, function(key, val){
                output += '<li>- ' + val.name + '<li>';
           });
           $('p.subtitle').html(output + '</ul><br><i>Price per hour:</i> <b>$'
                                + car.price_hourly + '</b>');
       });

   axios
       .get(baseUrl + 'gallery/')
       .then(r => {
           let gallery = r.data;
           let output = '<div class="w3-content w3-display-container">';
           $.each(gallery, function(key, val) {
               output += '<img class="mySlides" src="' + val.photo + '" style="width:100%;">';
           });

           output += '<button class="w3-button w3-black w3-display-left" onclick="plusDivs(-1)">&#10094;</button>' +
                     '<button class="w3-button w3-black w3-display-right" onclick="plusDivs(1)">&#10095;</button></div>';
            $('div.gallery').html(output);
            $('img.mySlides:first').hide();

       });

});
