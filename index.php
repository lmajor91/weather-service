<!DOCTYPE HTML>

<!-- Scripts -->
<!-- jQuery include -->
<script src="js/jquery.js"></script>
<script type="module" text="text/javascript">
    import * as controller from './js/scripts.js';

    /* pulls all the countries from the master DB
    * this should be put here so the code doesnt wait for the webpage to load THEN populate it
    * it should be completed then presented
    **/     
    controller.populateCountryBox();

    // api call woooooo
    $(document).ready(function(){
        /* when the user selects a country and the box is not empty,
        * the city datalist tag will appear and be populated by the cities which reside in the selected country
        **/
        $("#country-list").change(function(){
            controller.determineBox();
        });

        $("#state-list").change(function(){
            controller.populateCityBox();
        });

        // waits for the user to select a city then, once clicked it will execute the call to the API
        $('#weatherAPIButton').on("click", function() {
            if (document.getElementById("city-list").value){
                controller.getWeatherFromAPI();
            }
        });
    });
</script>

<html lang="en">
<head>
    <!-- title tag, going to be changed to the name of the location of user's choice -->
    <title id="title">Weather Service</title>

    <!-- standard meta tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="application-name" content="Weather Service">
    <meta name="description" content="Finds the weather at a specified area">

    <!-- stylesheets include -->
    <link rel="stylesheet" type="text/css" href="css/styles.css">
    <link rel="stylesheet" type="text/css" href="css/header.css">
    <link rel="stylesheet" type="text/css" href="css/footer.css">
    <link rel="stylesheet" type="text/css" href="css/weather.css">
</head>

<body>
    <section class="header">
        <header class="inner_header">
            <div class="header_text">
                <h2>testing header</h2>
            </div>
        </header>
    </section>

    <!-- User input forms -->
    <section class="userform">
        <div class="country_input">
            <select id="country-list">
                <option selected disabled hidden>Select a country</option>
            </select>
        </div>
        <div class="state_input" style="display:none">
            <select id="state-list"></select>
        </div>
        <div class="city_input" style="display:none">
            <select id="city-list"></select>
            <input id="weatherAPIButton" type="button" value="submit"/>
        </div>
    </section>

    <section class="wrapper">
        <!-- Website Content -->
        <section class="content_container">
            <div id="weather">weather</div>
            <div id="wind">winds</div>
            <div id="visibility">visibility</div>
            <div id="temperature">temperature</div>
            <div id="feelsliketemp">feels like</div>
        </section>
    </section>

    <!-- Footer -->
    <section class="footer">
        <footer class="inner_footer">
            <div class="footer_text">
                <h2>testing footer</h2>
            </div>
        </footer>
    </section>
</body>
</html>
