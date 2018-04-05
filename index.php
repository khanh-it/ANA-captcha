<?php
/**
 * 
 */
require_once(__DIR__ . '/kaptcha.php');
?>
<!DOCTYPE html>
<html lang="en">
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ANA Kaptcha Resolver</title>
    <link href="./style.css" rel="stylesheet">
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/zepto/1.2.0/zepto.min.js"></script>
</head>
<body>
	<div id="body" class="container-fluid">
		<div id="frame">
			<img id="captcha" src="" />
		</div>
		<textarea id="digits"></textarea>
		<p>
			<button id="btn-reload">Download + resolve kaptcha</button>
			<button id="btn-failed">Resolve wrong?</button>
		</p>
	</div>
	<script type="text/javascript" src="./script.js"></script>
</body>
</html>