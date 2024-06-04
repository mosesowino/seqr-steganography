function copyText(){
    var copy_text =document.getElementById("copy_text")
    copy_text.select()
    document.execCommand("copy")
    alert("text copied to clipboard")
}



let profile_image = document.querySelector(".links img")
let about_container = document.querySelector(".operations")


profile_image.addEventListener('click',()=>{
    let profile_pane = document.querySelector(".profile")
    profile_pane.classList.toggle('profile_visible')

})


function about(){
    fetch('http://localhost:5000/about')
        .then(response =>{
            if(!response){
                throw new Error("Server response not okay")
            }
            return response.text()
        })
        .then(html =>{
            // document.body.innerHTML = html
            about_container.innerHTML =html
        })
        .then(result =>{
            console.log(result)
        })
        .catch(error=>{
            console.error("there was a problem fetching the page: ",error)
        })
}



