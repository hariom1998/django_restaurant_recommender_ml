console.log('hello world')
var updateBtns = document.getElementsByClassName('update-cart')
console.log(updateBtns.length)
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var restid = this.dataset.restid
        var action = this.dataset.action
        console.log('Restaurant ID:', restid, 'action:', action)
        updateUserOrder(restid, action)
    })
}
function updateUserOrder(restid, action) {
    var url = '/update_item/'
    fetch(url, {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken, },
        body: JSON.stringify({ 'restid': restid, 'action': action })
    })
        .then((response) => { return response.json() })
        .then((data) => {
            window.alert(data);
            console.log('data:', data);

        })

}
