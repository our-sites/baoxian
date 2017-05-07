/**
 * Created by Administrator on 2017/3/21.
 */
CKEDITOR.editorConfig = function( config ) {
	var uploadUrl = '/ckfinder/core/connector/php/connector.php?command=QuickUpload';

	// Add the required plugin
	config.extraPlugins = 'simpleuploads';

	config.filebrowserUploadUrl = uploadUrl + '&type=Files';
	config.filebrowserImageUploadUrl = uploadUrl + '&type=Images';

	// Toolbar configuration
	config.toolbar =
		[
			{ name: 'document',    items : [ 'Source' ] },
			{ name: 'clipboard',   items : [ 'Undo','Redo' ] },
			{ name: 'basicstyles', items : [ 'Bold','Italic','-','RemoveFormat' ] },
			{ name: 'insert',      items : [  'Image', 'addFile', 'addImage'] },
			{ name: 'tools',       items : [ 'Maximize', 'About' ] }
		];

	config.extraAllowedContent = 'h3';

	// Limit the allowed set of file types for uploads:
	config.simpleuploads_acceptedExtensions = '7z|avi|csv|doc|docx|flv|gif|gz|gzip|jpeg|jpg|mov|mp3|mp4|mpc|mpeg|mpg|ods|odt|pdf|png|ppt|pxd|rar|rtf|tar|tgz|txt|vsd|wav|wma|wmv|xls|xml|zip';
};