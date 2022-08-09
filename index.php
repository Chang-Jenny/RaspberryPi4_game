<?php
    $host = "localhost";
    $dbuser = "root";
    $dbpasswd = "123456";
    $DBNAME = "project";
    
    $conn = mysqli_connect($host, $dbuser, $dbpasswd, $DBNAME);

    if(!$conn) {
        echo "Error: Unable to connect to MySQL." . PHP_EOL;
        echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
        echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
        die ("無法連線至資料庫");
    }
    // 設定連線編碼
    mysqli_query($conn, "SET NAMES 'utf8'");
    
    // $sql = "SELECT * FROM project.member ORDER BY \"time\" DESC;";
    $sql_1 = "SELECT * FROM project.play WHERE `level`=1 ORDER BY score DESC;";
    $sql_2 = "SELECT * FROM project.play WHERE `level`=2 ORDER BY score DESC;";
    $sql_3 = "SELECT * FROM project.play WHERE `level`=3 ORDER BY score DESC;";

    $ret_1 = mysqli_query($conn, $sql_1);
    $ret_2 = mysqli_query($conn, $sql_2);
    $ret_3 = mysqli_query($conn, $sql_3);

    // if(!$ret){
    //     echo "Error: Unable to connect to MySQL." . PHP_EOL;
    //     echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
    //     echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
    //     die("error");
    // }
    
    mysqli_close($conn);
?>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
        <title>復古遊戲街機</title>
    </head>
    <style>
        .table td {
            text-align: right;   
        }
    </style>
    <body>
        <!-- 上面的導航條 -->
        <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
            <!-- Brand -->
            <a class="navbar-brand" href="/index.php">復古遊戲街機排行榜</a>
          
            <!-- Links -->
            <ul class="navbar-nav">
                <!-- <li class="nav-item">
                    <a class="nav-link" href="/adduser.html">新增</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="/log.php">紀錄</a>
                  </li> --> -->
            </ul>
          </nav>
        <!-- 網頁本體 -->
        <div class="container">
            <h1 style="text-align: center; margin-top: 1rem;">遊戲排行榜</h1>
            <div class="row">
                <div class="col">
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th colspan="3">
                                    <h3>GAME_1</h3>
                                    </th>
                                </tr>
                                <tr>
                                    <th>玩家ID</th>
                                    <th>分數</th>
                                    <th>創造紀錄時間</th>
                                </tr>
                            </thead>
                            <!--  -->
                            <tbody>
                                <?php
                                while($row = mysqli_fetch_array($ret_1, MYSQLI_NUM)){
                                    echo "<tr>";
                                    echo "<td>".$row[0] ."</td>\n";
                                    echo "<td>".$row[2] ."</td>\n";
                                    echo "<td>".$row[3] ."</td>\n";
                                    echo "</tr>";
                                }
                                ?>
                            </tbody>
                            
                            <thead>
                            <tr>
                                <th colspan="3">
                                    <h3><br><br>GAME_2</h3>
                                </th>
                            </tr>
                                <tr>
                                    <th>玩家ID</th>
                                    <th>分數</th>
                                    <th>創造紀錄時間</th>
                                </tr>
                            </thead>
                            <!--  -->
                            <tbody>
                                <?php
                                while($row = mysqli_fetch_array($ret_2, MYSQLI_NUM)){
                                    echo "<tr>";
                                    echo "<td>".$row[0] ."</td>\n";
                                    echo "<td>".$row[2] ."</td>\n";
                                    echo "<td>".$row[3] ."</td>\n";
                                    echo "</tr>";
                                }
                                ?>
                            </tbody>
                            <thead>
                                <tr>
                                    <th colspan="3">
                                    <h3><br><br>GAME_3</h3>
                                    </th>
                                </tr>
                                <tr>
                                    <th>玩家ID</th>
                                    <th>分數</th>
                                    <th>創造紀錄時間</th>
                                </tr>
                            </thead>
                            <!--  -->
                            <tbody>
                                <?php
                                while($row = mysqli_fetch_array($ret_3, MYSQLI_NUM)){
                                    echo "<tr>";
                                    echo "<td>".$row[0] ."</td>\n";
                                    echo "<td>".$row[2] ."</td>\n";
                                    echo "<td>".$row[3] ."</td>\n";
                                    echo "</tr>";
                                }
                                ?>
                            </tbody>
                        </table>
                    </div>
                </div>
              </div>
        </div>
    </body>
</html>