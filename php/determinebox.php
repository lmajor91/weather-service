<?php
    $country_id = $_REQUEST["id"];
    $path_to_db = "../db/master.db";

    // initializing connection to DB
    $db = new SQLite3($path_to_db, SQLITE3_OPEN_READONLY);

    // if connection
    if(!$db) {
        echo $db->lastErrorMsg();
    } else {
        // preparing the DB statement to be executed
        $db_stmt = "SELECT states FROM countries WHERE country_id IS :country_id;";
        $stmt = $db->prepare($db_stmt);
        $stmt->bindParam(":country_id", $country_id, SQLITE3_INTEGER);
        
        // if there is a result
        if ($result = $stmt->execute()){
            // no while loop because there is going to be only one result
            // the only results are 0 or 1, false or true for the presence of states in the country
            $row = $result->fetchArray(SQLITE3_ASSOC);
                // if there are states in that country then return the following
                if ($row["states"]){
                    echo "STATE";
                } else {
                    echo "CITY";
                }
        }
    }
    $db->close();
?>