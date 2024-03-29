<?php
if($_POST) {
	header('Content-type: application/json');

	$artist = $_POST["artist"]; //filter_var($_POST["artist"], FILTER_SANITIZE_STRING);

	$pwd = fopen("pwd.config","r") or die("Cannot open file!");
	$pass = fgets($pwd);
	fclose($pwd);

	$conn = pg_connect("host=metacritic.czkzontdaczu.us-east-2.rds.amazonaws.com port=5432 dbname=metacritic user=mmaffei password=".$pass)
		or die('Could not connect: ' . pg_last_error());
		
	$query = 
	"WITH sub_b as (
		WITH sub_c as (
			SELECT artist, unnest(corr_vector) as items
			FROM correlations_15 WHERE LOWER(artist)=LOWER('".pg_escape_string($artist)."')
		)
		SELECT row_number() over() as rownum, artist, items FROM sub_c
		ORDER BY items DESC LIMIT 11		
	)
	SELECT sub_b.rownum, sub_b.items, correlations_15.artist FROM correlations_15
	JOIN sub_b on sub_b.rownum = correlations_15.row WHERE sub_b.items <= 0.99999999
	ORDER BY items DESC;";

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