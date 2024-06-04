let x = document.querySelector('.x')
console.log('hello ',x)
x.addEventListener('click',()=>{
    document.querySelector('.about_body').classList.add('about_invisible')
})
