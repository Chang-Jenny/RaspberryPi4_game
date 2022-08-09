<?php
    $host = "localhost";
    $dbuser = "root";
    $dbpasswd = "123456";
    $DBNAME = "project";

    if(isset($_GET['playerID'])){
        $conn = mysqli_connect($host, $dbuser, $dbpasswd, $DBNAME);
        if(!$conn) {
            echo "Error: Unable to connect to MySQL." . PHP_EOL;
            echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
            echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;    
            die ("無法連接資料庫");
        }
        // 設定連線編碼
        mysqli_query($conn, "SET NAMES 'utf8'");

        // 這筆資料存在嗎
        $sql = "SELECT `playerID` FROM `play` WHERE `playerID`='".$_GET['playerID']."' "."AND `level`='".$_GET['level']."'";
        $record = mysqli_query($conn, $sql);
        // 這筆資料存在
        if(mysqli_num_rows($record)>0) {
            // 判斷新的分數有沒有比較高
            $sql = "SELECT `playerID` FROM `play` WHERE `playerID`='".$_GET['playerID']."' "."AND `score`<".$_GET['score']." AND `level`='".$_GET['level']."'";
            $judge = mysqli_query($conn, $sql);
            // 這筆新的分數有比較高則進行更新
            if(mysqli_num_rows($judge)>0) {
            date_default_timezone_set('Asia/Taipei');
            $first = new DateTime();
            // update
            $sql = "UPDATE `play` SET ";
            $sql .= "`score`=".$_GET["score"].",";
            $sql .= "`time`='".$first->format('Y-m-d H:i:s')."' ";
            $sql .= "WHERE `playerID`= '".$_GET["playerID"]."' "."AND `level`='".$_GET['level']."'";
            mysqli_query($conn,$sql);
            }
        }
        // 若同時不存在相同的playerID及level則直接新增
        else{
            $sql = sprintf("INSERT INTO play (`playerID`,`level`,`score`,`time`) 
            VALUES ('%s', '%s', '%d', NOW());",
            $_GET['playerID'], $_GET['level'], $_GET['score']
            );
            $ret = mysqli_query($conn, $sql);
        }
        // unset($_GET['playerID'], $_GET['level'], $_GET['score']);


        if(!$ret){
            echo "Error: Unable to connect to MySQL." . PHP_EOL;
            echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
            echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;    
            die("insert error");
        }else{
            echo "Records created successfully\n";
        }
        mysqli_close($conn);
    }else{
        die("Error");
    }
?>