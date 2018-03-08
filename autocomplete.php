<?php
header('Content-type: application/json');

$artist = filter_var($_POST["artist"], FILTER_SANITIZE_STRING);

$conn = pg_connect("host=localhost port=5432 dbname=metacritic user=postgres")
	or die('Could not connect: ' . pg_last_error());

$query = "SELECT artist from 
(SELECT artist from albums GROUP BY artist) as sub
WHERE LOWER(artist) LIKE LOWER('".$artist."%') limit 5;";

$result = pg_query($query) or die('Query failed: ' . pg_last_error());
$resultArray = pg_fetch_all($result);

$r = array('items' => $resultArray);
echo json_encode($r);

// Free resultset
pg_free_result($result);

// Closing connection
pg_close($conn);

?>