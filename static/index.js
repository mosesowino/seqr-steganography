function copyText(){
    var copy_text =document.getElementById("copy_text")
    copy_text.select()
    document.execCommand("copy")
    alert("text copied to clipboard")
}


let profile_visible = document.querySelector(".links")
profile_visible.addEventListener('click',()=>{
    console.log("Clicked")
})

