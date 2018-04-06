<?php
if($_POST) {
	header('Content-type: application/json');

	$artist = $_POST["artist"]; //filter_var($_POST["artist"], FILTER_SANITIZE_STRING);

	$conn = pg_connect("host=metacritic.czkzontdaczu.us-east-2.rds.amazonaws.com port=5432 dbname=metacritic user=mmaffei password=***REMOVED***")
		or die('Could not connect: ' . pg_last_error());

	$query = "SELECT * FROM albums WHERE artist='".pg_escape_string($artist)."' ORDER BY mc_rating DESC";

	$result = pg_query($query) or die('Query failed: ' . pg_last_error());
	$resultArray = pg_fetch_all($result);

	$resultArray;
	echo json_encode($resultArray);

	// Free resultset
	pg_free_result($result);

	// Closing connection
	pg_close($conn);
}
?>