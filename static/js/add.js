var itemsArray = localStorage.getItem('items') ? JSON.parse(localStorage.getItem('items')) : [];
$('.block2-btn-addcart').each(function () {
    var nameProduct = $(this).parent().parent().parent().find('.block2-name').html();
    $(this).on('click', function () {
        $.getJSON(window.location.protocol + '//' + document.domain + ':' + window.location.port +
            '/add_to_cart', {
                id: this.id
            },
            function (data) {
                if (data.response === 'success') {
                    for (i = 0; i < itemsArray.length; i++) {
                        if (itemsArray[i].indexOf(data.id) !== -1) {
                            console.log('exits')
                            swal(nameProduct, "is already in cart !.");
                            return
                        }
                    }
                    itemsArray.push([data.id, data.name, data.quantity, data.price, data.image]);
                    localStorage.setItem('items', JSON.stringify(itemsArray));
                    swal(nameProduct, "is added to cart !", "success");
                }
            });
    });
});
