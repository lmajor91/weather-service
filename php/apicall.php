<?php
    $id = $_REQUEST['cityid'];
    //$name = "London";

    function get_api_data($id) {
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_AUTOREFERER, TRUE);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_URL, "api.openweathermap.org/data/2.5/weather?id=".$id."&APPID=b88346c9da96e327b8c0c390040486ce&units=metric");
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);       

        $data = curl_exec($ch);
        curl_close($ch);

        return $data;
    }

// use a dot ( . ) to concat strings, also stores json objects in a designated json folder
// commment this out for the time being
//$temp = get_api_data();
//file_put_contents(date("h:i:sa") . ".json", $temp);

echo get_api_data($id);
?>