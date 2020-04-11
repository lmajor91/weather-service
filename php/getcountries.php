<?php
    $path_to_db = "../db/master.db";
    $item_separator = "||";

    // initializing connection to DB
    $db = new SQLite3($path_to_db, SQLITE3_OPEN_READONLY);

    // if connection
    if(!$db) {
        echo $db->lastErrorMsg();
    } else {
        // testing
        $db_stmt = "SELECT * FROM countries";
        $stmt = $db->prepare($db_stmt);
        
        if ($result = $stmt->execute()){
            while($row = $result->fetchArray(SQLITE3_ASSOC)){
                //var_dump($row);
                echo $row['country_id'].$item_separator.$row['country_name']."\n";
            }
        }
        $db->close();
    }
?>