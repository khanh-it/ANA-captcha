<?php

define('DS', DIRECTORY_SEPARATOR);
define('DATA_DIR', __DIR__ . DS . 'data');
define('DATA_DIR_FEEDBACK', DATA_DIR . DS . 'feedback');

/**
 *
 */
class ANAKaptcha {
	/** */
	const URL = 'https://aswbe-d.ana.co.jp/9Eile48/dms/red21o/dyc/be/kaptcha.jpg';
	
	/**
	 *
	 */
	public static function getKaptchaBase64() {
		$content = file_get_contents(static::URL);
		$content = base64_encode($content);
		$content = "data:image/jpg;base64,{$content}";
		return $content;
	}
	
	/**
	 *
	 */
	public static function getFile($realpath = false) {
		$filename = strval(microtime(true)) . '.jpg';
		$realFilename = DATA_DIR . DS . $filename;
		$content = file_get_contents(static::URL);
		file_put_contents($realFilename, $content);
		return $realpath ? $realFilename : "/data/{$filename}";
	}
	
	/**
	 *
	 */
	public static function resolve($imgfile) {
		$digits = '_';
		$realFilename = realpath(__DIR__ . $imgfile);
		if ($realFilename) {
			$command = 'python'
				. (' ' . __DIR__ . DS . 'index.py')
				. (' ' . $realFilename)
			;
			$output = array();
			$return = array();
			trim(exec(escapeshellcmd($command), $output, $return));
			$digits = array_pop($output);
			// Debug
			$digits = " o digits: {$digits}" . PHP_EOL
				. " o command: {$command}" . PHP_EOL
				. " o output: " . implode(PHP_EOL, $output) . PHP_EOL
				// . " o return: {$return}" . PHP_EOL
			;
		}
		return $digits;
	}
	
	/**
	 *
	 */
	public static function feedback($imgfile) {
		$txt = 'Oh oh, something goes wrong :(';
		$realFilename = realpath(__DIR__ . $imgfile);
		if ($realFilename) {
			$filename = strval(microtime(true)) . '.jpg';
			$copyFilename = DATA_DIR_FEEDBACK . DS . $filename;
			if (copy($realFilename, $copyFilename)) {
				$txt = 'Thank you!';
			}
		}
		return $txt;
	}
}


$cmd = $_REQUEST['cmd'];
//
if ('dlkaptcha' == $cmd) {
	$kaptchaFile = ANAKaptcha::getFile();
	die($kaptchaFile);
}
//
if ('rskaptcha' == $cmd) {
	$imgfile = trim($_REQUEST['imgfile']);
	$digits = ANAKaptcha::resolve($imgfile);
	die($digits);
}
//
if ('fbkaptcha' == $cmd) {
	$imgfile = trim($_REQUEST['imgfile']);
	$txt = ANAKaptcha::feedback($imgfile);
	die($txt);
}
