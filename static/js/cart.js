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

        // check if user is logged in
        update_user_order(product_id, action);
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
            'action': action
        }),
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        if(data['redirect']) {
            window.location.reload();
        }
    })
}