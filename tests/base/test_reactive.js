after_layout=()=>{
    document.addEventListener("click", function(event) {
        let container_elmnt = document.getElementById(container.id);
        if (!container_elmnt.contains(event.target) && options.style.display=="block") {
            options.style.display = "none"
        }
    });
}
click_handler=()=>{
    if (options.style.display!=="none") {
        options.style.display="none"
    } else {
        options.style.display="block"
    }
    view.resize_layout()
}
key_up_handler=(event)=>{
    if (event.key == "Enter") {
        data.value = event.target.value
        options.style.display="none"
    }
}
options_click_handler=(event)=>{
    let opt_elmnt = event.target.closest(".run_select_option")
    data.value = opt_elmnt.firstChild.innerHTML
    if (options.style.display!=="none") {
        options.style.display="none"
    } else {
        options.style.display="block"
    }
    view.resize_layout()
}
render=()=>{
    options.style.display="none"
}