// get all 'add to cart' buttons

let btns_update_cart = document.querySelectorAll(".update-cart");

// loop through buttons
for(let i = 0; i < btns_update_cart.length; i++) {
    // define variables
    let product_id;
    let action

    // add click event
    btns_update_cart[i].addEventListener("click", function() {
        product_id = this.dataset.product;
        action = this.dataset.action;
        quantity = this.dataset.quantity;

        // check if user is logged in
        update_user_order(product_id, action, quantity);
        // if(user === 'AnonymousUser') {
        //     console.log('Not logged in');
        // }
        // else {
        // }
    });

    
}

/**
 * 
 * @param {*} product_id 
 * @param {*} action 
 */
function update_user_order(product_id, action) {

    let url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'product_id': product_id,
            'action': action,
            'quantity': quantity
        }),
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        alert(data['redirect']);
        alert(data['product_id']);
        alert(data['action']);
        alert(data['quantity']);
        if(data['redirect']) {
            
            window.location.reload();
        }
    })
}