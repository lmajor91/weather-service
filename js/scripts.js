// exporting all the functions to be used in another script
// the functions get used in index.php

export function populateCountryBox(){
    $.post("./php/getcountries.php", function(data){
        var countries = data.split("\n"); countries.pop(); // to get rid of the undefined option

        // iterating through all the countries called back
        countries.map(function(item){
            var [id, name] = item.split("||");
            $("#country-list").append(`<option value='${id}'>${name}</option>`);
        });
    });
}

export function populateCityBox(){
    // emptying state-list from the last function run
    $("#city-list").empty();

    // adding processing placeholder
    $("#city-list").append("<option selected disabled hidden>processing...</option>");

    // showing the tag
    $(".city_input").show();

    // getting cities depending on state seleciton
    $.post(`./php/getcities.php?country_id=${document.getElementById("country-list").value}&state_id=${document.getElementById("state-list").value}`, function(data){
        var cities = data.split("\n"); 
        cities.pop(); // to get rid of the undefined option

        // iterate through all the cities which have been called back
        cities.map(function(item){
            var [id, name] = item.split("||");
            // adding all 
            $("#city-list").append(`<option value='${id}'>${name}</option>`);
        });
        // adding a tag to let the user know that everything is ready
        $("#city-list").append('<option selected disabled hidden>Select a city</option>');
    });
}

export function populateStateBox(){
    // emptying state-list from the last function run
    $("#state-list").empty();

    // adding processing placeholder
    $("#state-list").append("<option selected disabled hidden>processing...</option>");

    // showing the tag
    $(".state_input").show();

    // getting states
    $.post(`./php/getstates.php?id=${document.getElementById("country-list").value}`, function(data){
        var states = data.split("\n"); 
        // popping the last item to get rid of the null element
        states.pop();    
        
        // iterate through all the states which have been returned from the database
        states.map(function(item){
            var [name, id] = item.split("||");
            // adding all the options to the list
            $("#state-list").append(`<option value='${id}'>${name}</option>`);
        });
        $("#state-list").append('<option selected disabled hidden>Select a state/province</option>');
    });
}

// function determines whether to activate the statebox or citybox
export function determineBox(){
    // hiding both boxes
    $(".city_input").hide();
    $(".state_input").hide();

    // determining box
    $.post(`./php/determinebox.php?id=${document.getElementById("country-list").value}`, function(data){
        if (data === 'CITY'){
            populateCityBox();
        } else if (data === 'STATE'){
            populateStateBox();
        } else {
            $("#country-list").empty();
            $("#country-list").append('<option selected disabled hidden >Database error!</option>');
        }
    });
}

export function getWeatherFromAPI(){
    $.post(`./php/apicall.php?cityid=${document.getElementById("city-list").value}`, function(data){
        // if the apicall returned anything
        if (data){
            var json = JSON.parse(data);
            //console.log(json);
            $("#output").html(data);

            $("#weather").html(json.weather[0].main);
            $("#wind").html("Winds speed\n"+json.wind["speed"]+"km");
            $("#temperature").html(json.main["temp"]+"°C");
            $("#feelsliketemp").html("Feels like\n"+json.main["feels_like"]+"°C");
            if(json.visibility){
                $("#visibility").html("Visibility\n"+json.visibility+"km");
            } else {
                $("#visibility").empty();
            }
            
            $("#title").html("Weather in " + json.sys.country + ", " + json.name)
        } else {
            $("#weather").html("Check your internet connection! No data received.");
        }
    });
}