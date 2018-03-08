<?php
//if($_POST) {
	header('Content-type: application/json');

	$artist = filter_var($_POST["artist"], FILTER_SANITIZE_STRING);

	$conn = pg_connect("host=localhost port=5432 dbname=metacritic user=postgres")
		or die('Could not connect: ' . pg_last_error());

	$query = "WITH b as (
	WITH c as (
		SELECT artist, unnest(corr_vector) as items
		FROM correlations WHERE artist='".$artist."'
	)
		SELECT row_number() over() as rownum, artist, items FROM c WHERE items <= 0.99999999999
		ORDER BY items DESC LIMIT 10
	)
	SELECT artist FROM correlations WHERE row in (SELECT rownum FROM b);";

	$result = pg_query($query) or die('Query failed: ' . pg_last_error());
	$resultArray = pg_fetch_all($result);

	$r = array('items' => $resultArray);
	echo json_encode($r);

	// Free resultset
	pg_free_result($result);

	// Closing connection
	pg_close($conn);
//}
?>