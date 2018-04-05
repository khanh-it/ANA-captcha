(function($){
	/**
	 | 
	 */
	function captchaResolve(filename, callback) {
		let opts = {
			'cwd': path.join(__dirname)
		};
		let proc = exec('python pyocr/index.py "' + filename + '"', opts, function(err, stdout, stderr){
			if (err) {
				return callback(new Error(stderr));
			}
			callback(null, stdout.trim());
		});
	}
	
	/**
	 | Helper: get image data
	 | @see https://davidwalsh.name/convert-image-data-uri-javascript
	 | @see https://stackoverflow.com/questions/1977871/check-if-an-image-is-loaded-no-errors-in-javascript
	 | @see https://stackoverflow.com/questions/22710627/tainted-canvases-may-not-be-exported
	 */
	function getImgDataBase64(img, callback) {
		// Dealing with cross domain images
		let imgSrc = img.src;
		img = new Image();
		img.src = imgSrc;
		img.crossOrigin = 'anonymous';
		img.onload = function imgOnload() {
			// Create an empty canvas element
			var canvas = document.createElement("canvas");
			canvas.width = img.width;
			canvas.height = img.height;

			// Copy the image contents to the canvas
			var ctx = canvas.getContext("2d");
			ctx.drawImage(img, 0, 0);

			// Get the data-URL formatted image
			// Firefox supports PNG and JPEG. You could check img.src to
			// guess the original format, but be aware the using "image/jpg"
			// will re-encode the image.
			var dataURL = canvas.toDataURL("image/png");
			// var dataURL = dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
			callback(dataURL);
			// Return?
			return dataURL;
		};
		// imgOnload();
	}
	// Re assign!
	window.getImgDataBase64 = getImgDataBase64;
	
	// 
	var $body = $('#body');
	var $img = $('#captcha');
	var $digits = $('#digits');
	//
	var $btnReload = $('#btn-reload').on('click', function(){
		$.post('?cmd=dlkaptcha', {}, function(data){
			$img.attr('src', data);
			$digits.val('');
			//
			$.post('?cmd=rskaptcha', { imgfile: data}, function(digits){
				$digits.val(digits);
			});
		});
	});
	// $btnReload.trigger('click');
	//
	var $btnFailed = $('#btn-failed').on('click', function(){
		var imgfile = $.trim($img.attr('src'));
		$.post('?cmd=fbkaptcha', { imgfile: imgfile}, function(data){
			alert(data);
		});
	});
})(Zepto);