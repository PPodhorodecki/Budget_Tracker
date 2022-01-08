let formContinuity = document.getElementById('continuity_attributes')
let check = document.getElementById('contonuity')
formContinuity.style.display = 'none'

check.addEventListener('click', functn(event){
    if (check.value == 'yes') {
    formContinuity.style.display = 'block'
    } else {
    formContinuity.style.display = 'none'}
})