<?php
    // getting all the variables from the url link
    $country_id = $_REQUEST["country_id"];
    $state_id = $_REQUEST["state_id"];

    // vars
    $path_to_db = "../db/master.db";
    $item_separator = "||";

    // initializing connection to DB
    $db = new SQLite3($path_to_db, SQLITE3_OPEN_READONLY);

    // if connection
    if(!$db) {
        echo $db->lastErrorMsg();
    } else {
        if ($state_id){
            // if there is a state is the URL then do this

            // preparing statement
            $db_stmt = "SELECT DISTINCT * FROM cities WHERE country_id IS :country_id AND state_id IS :state_id GROUP BY city_name";
            $stmt = $db->prepare($db_stmt);
            $stmt->bindParam(":state_id", $state_id, SQLITE3_INTEGER);
            $stmt->bindParam(":country_id", $country_id, SQLITE3_INTEGER);
            
            // executing statement
            if ($result = $stmt->execute()){
                while($row = $result->fetchArray(SQLITE3_ASSOC)){
                    echo $row['city_id'].$item_separator.$row['city_name']."\n";
                }
            }

        }else{
            // if there is no state in the URL then do this

            // preparing statement
            $db_stmt = "SELECT DISTINCT * FROM cities WHERE country_id IS :country_id GROUP BY city_name";
            $stmt = $db->prepare($db_stmt);
            $stmt->bindParam(":country_id", $country_id, SQLITE3_INTEGER);
            
            // executing statement
            if ($result = $stmt->execute()){
                while($row = $result->fetchArray(SQLITE3_ASSOC)){
                    echo $row['city_id'].$item_separator.$row['city_name']."\n";
                }
            }
        }
    }

    // closing the database after the transactions
    $db->close();
?>