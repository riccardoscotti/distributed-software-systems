$( document ).ready(function () {

    apikey = "d521fa844c4242318ee160230230611";


        $.ajax({

            url: "http://api.weatherapi.com/v1/forecast.json?key=" + apikey + "&q=Bologna&days=2&aqi=no&alerts=no",
            type: 'GET',
            headers: {
                'Access-Control-Allow-Credentials' : true,
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Methods':'GET',
                'Access-Control-Allow-Headers':'application/json',
            },
            success: function(data) {

                //current conditions
                $("#ccondition").text(data["current"]["condition"]["text"]);
                $("#ctemp").text("Temperature: " + data["current"]["temp_c"] + "°C");
                $("#cwind").text("Wind: " + data["current"]["wind_kph"] + "kph");
                $("#chumidity").text("Humidity: " + data["current"]["humidity"] + "%");
                $("#cwinddir").text("Wind direction: " + data["current"]["wind_dir"]);
                $("#cprecipitation").text("Precipitations: " + data["current"]["precip_mm"] + "mm");
                $("#clastupdate").text("Last updated: " + data["current"]["last_updated"]);
                $("#cicon").html('<img src="http:' + data["current"]["condition"]["icon"] +'"></img>')

                //next 24 hours
                let currentdate = new Date();
                let currenthour = currentdate.getHours();

                let today = data["forecast"]["forecastday"][0];
                let tomorrow = data["forecast"]["forecastday"][1];

                let iterations = 0;
                let forecasthtml = "<tr>";
                if (currenthour < 23) {
                    for (let i = currenthour + 1; i < 24; i++) {
                        iterations++;
                        let forecasthour = currenthour + iterations;
                        forecasthtml += '<td class="ftd">';
                        forecasthtml += '<div class="center">Hour: ' + forecasthour + ':00</div>';
                        forecasthtml += '<img class="centerimg" src="http:' + today["hour"][i]["condition"]["icon"] +'"></img>';
                        forecasthtml += '<h4>' + today["hour"][i]["condition"]["text"] + '</h4>';
                        forecasthtml += '<div class="center">Temperature:</div>'; 
                        forecasthtml += '<div class="center">' + today["hour"][i]["temp_c"] + '°C</div>';
                        forecasthtml += '<div class="center">Rain chance:</div>';
                        forecasthtml += '<div class="center">' + today["hour"][i]["chance_of_rain"] + '%</div>';
                        forecasthtml += '</td>';
                        if (iterations == 24) {
                            forecasthtml += "</tr>";
                        }
                        else if ((iterations % 8) == 0) {
                            forecasthtml += "</tr><tr>";
                        }
                    };
                }

                if (iterations < 24) {
                    for (let i = 0; i < currenthour + 1; i++) {
                        iterations++;
                        let forecasthour = i;
                        forecasthtml += '<td class="ftd">';
                        forecasthtml += '<div class="center">Hour: ' + forecasthour + ':00</div>';
                        forecasthtml += '<img class="centerimg" src="http:' + tomorrow["hour"][i]["condition"]["icon"] +'"></img>';
                        forecasthtml += '<h4>' + tomorrow["hour"][i]["condition"]["text"] + '</h4>';
                        forecasthtml += '<div class="center">Temperature:</div>'; 
                        forecasthtml += '<div class="center">' + tomorrow["hour"][i]["temp_c"] + '°C</div>';
                        forecasthtml += '<div class="center">Rain chance:</div>';
                        forecasthtml += '<div class="center">' + tomorrow["hour"][i]["chance_of_rain"] + '%</div>';
                        forecasthtml += '</td>';
                        if (iterations == 24) {
                            forecasthtml += "</tr>";
                        }
                        else if ((iterations % 8) == 0) {
                            forecasthtml += "</tr><tr>";
                        }
                    }
                }

                $("#forecast").html(forecasthtml);

                daily(data["location"]["lat"], data["location"]["lon"])
            },
            error: function() { alert('Failed!'); }
        });


    function daily(lat, lon) {

        reqdata = {
            "numDays": 6,
            "loc": {
                "lat": lat,
                "lon": lon
            }
        }
        
        $.ajax({
            url: "http://localhost:5000/api/daily",
            type: "POST",
            data: JSON.stringify(reqdata),
            dataType: 'json',
            contentType: 'application/json',
            headers: {
                'Access-Control-Allow-Credentials' : true,
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Methods':'POST',
                'Access-Control-Allow-Headers':'application/json'
            }, 
            success: function(resdata) {
                let dailyhtml = "<tr>";

                for (let i = 1; i < 6; i++) {
                    srise = resdata[i]["sunrise"];
                    sset = resdata[i]["sunset"];
                    dailyhtml += '<td class="ftd">';
                    dailyhtml += '<div class="center">Day: ' + resdata[i]["date"] + '</div>';
                    dailyhtml += '<div class="center">Temperatures:</div>'; 
                    dailyhtml += '<div class="center">Min: ' + resdata[i]["minTemperature"] + '</div>';
                    dailyhtml += '<div class="center">Max: ' + resdata[i]["maxTemperature"] + '</div>';
                    dailyhtml += '<div class="center">Sunrise: ' + srise.slice(0, srise.length - 3) + '</div>';
                    dailyhtml += '<div class="center">Sunset: ' + sset.slice(0, sset.length - 3) + '</div>';
                    dailyhtml += '</td>';
                }

                dailyhtml += "</tr>"

                $("#daily").html(dailyhtml);
            },
            error: function() { alert('Failed!'); }
          });
        
    };

});