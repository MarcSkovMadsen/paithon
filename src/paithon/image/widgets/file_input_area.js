// Inspiration
// https://github.com/bokeh/bokeh/blob/branch-3.0/bokehjs/src/lib/models/widgets/file_input.ts
render=()=>{
  self.configureFakeInput()
  
  dropRegion.addEventListener('click', function() {
    if (data.enable_click_upload){
      state.fakeInput.click();
    }
  });
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
        data.message="Please don't upload more than one file at the time!"
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
  const dt=data
  function setDataUri(uri){
    data.progress=50
    data.uri=uri;
    const [, mime_type="",, value=""] = uri.split(/[:;,]/, 4)
    data.mime_type=mime_type
    data.progress=0
  }
  function validateImage(image) {
    // check the type
    var validTypes = Array.from(dt.accept, (x)=>{return "image/"+x});
    if (validTypes.indexOf( image.type ) === -1 && false) {
      data.message = "File type '" + image.type + "' is  not accepted!"
      return false;
    }

    // check the size
    if (image.size > dt.max_size_in_mega_bytes*1000000) {
      data.message = "File too large. Max is " + String(dt.max_size_in_mega_bytes) + "MB"
      return false;
    }

    return true;
  }
  function previewAnduploadImage(image) {
    var reader = new FileReader();
    reader.onload = function(e) {
      setDataUri(e.target.result);
    }
    reader.readAsDataURL(image);
    data.filename=image.name
  }
  dropRegion.addEventListener('drop', handleDrop, false);

  self.setActiveView()
}
fit=()=>{
  objectRegion.style.objectFit=data.fit
  objectRegion.style.display="inline"
}
accept=()=>{
  state.fakeInput.accept = Array.from(data.accept, (x)=>{return "."+x}).toString();
}
message=()=>{
  drop_message.innerHTML=data.message
  data.active_view = "message"
  self.active_view()
}
uri=()=>{
  if (data.uri==="" || data.uri===null){
    self.resetUri()
  } else {
    const [, mime_type="",, value=""] = data.uri.split(/[:;,]/, 4)
    if (mime_type.startsWith("image")){
      previewRegion.innerHTML=`<img src="${data.uri}" style="object-fit:${data.fit};height:100%;width:100%;margin:5px"></img>`
    } else if (mime_type.startsWith("audio")){
      previewRegion.innerHTML=`<audio controls autoplay src="${data.uri}" style="object-fit:${data.fit};height:50%;max-width:500px;margin:5px"></audio>`
    } else if (mime_type.startsWith("video")){
      previewRegion.innerHTML=`<video controls style="margin:5px;height: calc(100% - 10px);object-fit:${data.fit};"><source type="${mime_type}" src="${data.uri}"></source></video>`
    } else if (mime_type==="application/pdf") {
      previewRegion.innerHTML=`<iframe src="${data.uri}" style="object-fit:${data.fit};height:calc(100% - 10px);width:calc(100% - 10%)">`
    } else if (mime_type==="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" || mime_type==="application/vnd.ms-excel") {
      // See https://oss.sheetjs.com/sheetjs/ for inspiration
      const [,,, value=""] = data.uri.split(/[:;,]/, 4)
      workbook = XLSX.read(value, {type:'base64', WTF: false});
      window.workbook=workbook // Todo: REMOVE. ONLY FOR DEVELOPMENT
      function to_json(workbook) {
        var result = {};
        workbook.SheetNames.forEach(function(sheetName) {
          var roa = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], {header:0});
          if(roa.length) result[sheetName] = roa;
        });
        return JSON.stringify(result, 2, 2);
      };
      console.log(to_json(workbook))
      to_html = function to_html(workbook) {
        html = "";
        workbook.SheetNames.forEach(function(sheetName) {
          var htmlstr = XLSX.write(workbook, {sheet:sheetName, type:'string', bookType:'html'});
          html += htmlstr;
        });
        return html;
      };
      grid = canvasDatagrid({
        parentNode: previewRegion
      });
      grid.style.height = '100%';
      grid.style.width = '100%';
      grid.data = [
        { col1: 'row 1 column 1', col2: 'row 1 column 2', col3: 'row 1 column 3' },
        { col1: 'row 2 column 1', col2: 'row 2 column 2', col3: 'row 2 column 3' },
      ];
    } else {
      previewRegion.innerHTML=`<div style="display:flex;align-items:center;justify-content:center;margin:25px;height:100%"><p style="white-space: break-spaces;max-width:500px">Preview of mime type ${mime_type} is not supported. File a Feature Request on <a href="https://github.com/holoviz/panel/issues" target="_blank">Github</a> if you need it.<p></div>`
    }
  }

  self.setActiveView()
}
configureFakeInput=()=>{
  var fakeInput = document.createElement("input");
  
  fakeInput.type = "file";
  fakeInput.accept = Array.from(data.accept, (x)=>{return "."+x}).toString();
  fakeInput.multiple = data.multiple;
  fakeInput.addEventListener("change", function() {
    var files = fakeInput.files;
    handleFiles(files);
  });
  state.fakeInput = fakeInput
}
active_view=()=>{
  if (data.active_view=="preview"){
    previewRegion.style.display="inline"
    objectRegion.style.display="none"
    drop_message.style.display="none"
    helper.style.display="none"
  } else if (data.active_view=="object"){
    previewRegion.style.display="none"
    objectRegion.style.display="inline"
    drop_message.style.display="none"
    helper.style.display="none"
  } else {
    previewRegion.style.display="none"
    objectRegion.style.display="none"
    drop_message.style.display="inline"
    helper.style.display="inline-block"
  }
}
setActiveView=()=>{
  if (data.uri){
    data.active_view=data.default_view
    self.active_view()
  } else {
    if (data.enable_click_upload){
      data.message="<em>Drag & Drop</em> files or <em>click</em> to upload"
    } else {
      data.message="<em>Drag & Drop</em> files to upload"
    }
  }
}
reset=()=>{
  data.filename=""
  data.mime_type=""
  data.uri=""

  previewRegion.innerHTML="Nothing to preview"
}