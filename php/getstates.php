<?php
    $country_id = $_REQUEST["id"];
    $path_to_db = "../db/master.db";
    $item_separator = "||";

    // initializing connection to DB
    $db = new SQLite3($path_to_db, SQLITE3_OPEN_READONLY);

    // if connection
    if(!$db) {
        echo $db->lastErrorMsg();
    } else {
        $db_stmt = "SELECT DISTINCT state, state_id FROM states WHERE country_id IS :country_id";
        $stmt = $db->prepare($db_stmt);
        $stmt->bindParam(":country_id", $country_id, SQLITE3_INTEGER);
        
        if ($result = $stmt->execute()){
            while($row = $result->fetchArray(SQLITE3_ASSOC)){
                echo $row["state"].$item_separator.$row["state_id"]."\n";
            }
        }
    }
    $db->close();
?>