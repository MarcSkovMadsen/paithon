takes=()=>{
  var screenshotTarget=document.body;
  if (data.target==='object'){
    screenshotTarget = view.el;
  } else if (data.target==='selection' && data.selection) {
    screenshotTarget = document.querySelector(data.selection)
  }
  function filter (node) {
    return (node.tagName !== "FAST-TOOLTIP" && node.id!=="theme-switch");
  }
  var toImage = domtoimage.toPng
  if (data.format==="jpeg"){toImage = domtoimage.toJpeg}
  if (data.format==="svg"){toImage = domtoimage.toSvg}

  toImage(screenshotTarget, {filter: filter, scale: data.scale, quality: data.quality, bgcolor: data.bgcolor})
  .then(function (dataUrl) {
      function download(dataUrl){
        var el = document.createElement("a");
        el.setAttribute("href", dataUrl);
        el.setAttribute("download", data.download_file_name);
        // document.body.appendChild(el);
        el.click();
        // el.remove();
      }
      function open(dataUrl){
        if (data.open_target==="new"){
          win = window.open(null, data.open_target, "New Window")
        } else {
          win = window.open(null, data.open_target)
        }
        win.document.write('<iframe src="' + dataUrl  + '" frameborder="0" style="border:0; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%;margin:10px" allowfullscreen></iframe>');
        win.document.title = 'Hello!';
      }
      if (data.actions.includes("download")){download(dataUrl)}
      if (data.actions.includes("open")){open(dataUrl)}
      if (data.actions.includes("transfer")){data.uri = dataUrl}
  })
  .catch(function (error) {
      console.error('oops, something went wrong! Could not take screenshot', error);
  });
}