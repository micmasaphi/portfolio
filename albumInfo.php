<?php
if($_POST) {
	header('Content-type: application/json');

	$album = $_POST["album"];
	$artist = $_POST["artist"]; //filter_var($_POST["artist"], FILTER_SANITIZE_STRING);

	$pwd = fopen("pwd.config","r") or die("Cannot open file!");
	$pass = fgets($pwd);
	fclose($pwd);

	$conn = pg_connect("host=metacritic.czkzontdaczu.us-east-2.rds.amazonaws.com port=5432 dbname=metacritic user=mmaffei password=".$pass)
		or die('Could not connect: ' . pg_last_error());

	$query = "SELECT albums.img_link, albums.artist, albums.name, ratings.album_rating, ratings.critic_name, ratings.album_description
		FROM ratings 
		JOIN albums ON ratings.album_id = albums.id
		WHERE albums.artist='".$artist."' and albums.name='".$album."'
		ORDER BY ratings.album_rating DESC LIMIT 3;";

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