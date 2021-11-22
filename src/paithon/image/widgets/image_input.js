// Inspiration
// https://github.com/bokeh/bokeh/blob/branch-3.0/bokehjs/src/lib/models/widgets/file_input.ts
render=()=>{
  var fakeInput = document.createElement("input");
  fakeInput.type = "file";
  fakeInput.accept = Array.from(data.accept, (x)=>{return "."+x}).toString();
  fakeInput.multiple = data.multiple;
  dropRegion.addEventListener('click', function() {
    fakeInput.click();
  });
  fakeInput.addEventListener("change", function() {
    var files = fakeInput.files;
    handleFiles(files);
  });
  state.fakeInput = fakeInput
  function preventDefault(e) {
    e.preventDefault();
    e.stopPropagation();
  }
  dropRegion.addEventListener('dragenter', preventDefault, false)
  dropRegion.addEventListener('dragleave', preventDefault, false)
  dropRegion.addEventListener('dragover', preventDefault, false)
  dropRegion.addEventListener('drop', preventDefault, false)

  function handleDrop(e) {
    var dt = e.dataTransfer,
		files = dt.files;
    if (files.length) {
      if (files.length>1 && !data.multiple){
        showMessage("Please don't upload more than one file at the time!")
      } else {
        handleFiles(files);
      }
    }
  }
  function handleFiles(files) {
    for (var i = 0, len = files.length; i < len; i++) {
      if (validateImage(files[i]))
        previewAnduploadImage(files[i]);
    }
  }
  const msgElement=drop_message
  const dt=data
  function setUri(uri){
    data.progress=50
    data.uri=uri;
    const [, mime_type="",, value=""] = uri.split(/[:;,]/, 4)
    data.mime_type=mime_type
    data.progress=0
  }
  function showMessage(msg){
    imageRegion.src = "";
    dt.uri=""
    dt.filename=""
    dt.mime_type=""

    msgElement.innerText = msg
    imageRegion.style.display="none"
    msgElement.style.display="inline"
  }
  function showImage(uri){
    if (uri){
      imageRegion.src = uri;
      msgElement.innerText = ""
      imageRegion.style.display="inline"
      msgElement.style.display="none"
    } else {
      showMessage("<em>Drag & Drop</em> images or <em>click</em> to upload")
    }
  }
  showImage(data.uri)
  state.showImage=showImage
  function validateImage(image) {
    // check the type
    var validTypes = Array.from(dt.accept, (x)=>{return "image/"+x});
    if (validTypes.indexOf( image.type ) === -1) {
      showMessage("File type '" + image.type + "' is  not accepted!");
      return false;
    }

    // check the size
    if (image.size > dt.max_size_in_mega_bytes*1000000) {
      showMessage("File too large. Max is " + String(dt.max_size_in_mega_bytes) + "MB");
      return false;
    }

    return true;
  }
  function previewAnduploadImage(image) {
    var reader = new FileReader();
    reader.onload = function(e) {
      setUri(e.target.result);
      showImage(e.target.result);
    }
    reader.readAsDataURL(image);
    data.filename=image.name
  }
  dropRegion.addEventListener('drop', handleDrop, false);
}
fit=()=>{
  imageRegion.style.objectFit=data.fit
  imageRegion.style.display="inline"
}
accept=()=>{
  state.fakeInput.accept = Array.from(data.accept, (x)=>{return "."+x}).toString();
}
uri=()=>{
  state.showImage(data.uri)
}
