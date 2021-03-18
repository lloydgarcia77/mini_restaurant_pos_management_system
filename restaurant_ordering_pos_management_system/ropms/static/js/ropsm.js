$(document).ready(function () {


    // let data = {
    //         "id": id
    //     }
    //     data = JSON.stringify(data);

    //     $.ajax({
    //         // https://docs.djangoproject.com/en/2.2/ref/csrf/
    //         headers: { "X-CSRFToken": getCookie("csrftoken") },
    //         type: 'POST', // must be in POST
    //         url: url,
    //         data: data, // json object to be transfer
    //         dataType: 'json',
    //         success: (data) => {
    //             if (data.form_is_valid) {
    //                 location.reload();
    //             }

    //         },
    //         complete: (data) => {

    //         },
    //         error: (data) => {

    //         }

    //     });
    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
    $(".add-to-cart").on("click", function (e) {
        e.preventDefault();
        
        let url = $(this).attr('href');
        let quantity = $("#menu_item_quantity").val() ? $("#menu_item_quantity").val() : 1; 
        let data = {
            'quantity': quantity
        }
        data = JSON.stringify(data);
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: 'POST',
            data: data,
            dataType: 'json',
            url: url,
            beforeSend: () => {
                $(this).html(`<span class=" icon-shopping-cart"></span> Please wait...`);
                $("#nav-shopping-cart-summary").html(` 
                <span class="icon-shopping-cart"></span> 
                Updating... Item(s) - <span class="badge badge-warning"> Updating.. </span> 
                `)
            },
            success: (data) => {
                $("#nav-shopping-cart-summary").html(` 
                    <span class="icon-shopping-cart"></span> 
                    ${data.context.total_all_quantity} Item(s) - <span class="badge badge-warning"> ₱${data.context.total_all_amount} </span> 
                `)
                $("#menu_item_quantity").val("1");
            },
            complete: (data) => {
                $(this).html(`<span class=" icon-shopping-cart"></span> Add to cart`);
            },
            error: (data) => {

            }
        });
        return false;
    });

    $("#table-cart").on('click', '.add-value', function (e) {
        let row = $(this).closest('tr');
        let url = $(this).attr('data-url');
        let input = row.find(".item-quantity");
        let q = parseInt(input.val()) + 1;

        row.find(".delete-value").attr("disabled", false);
        input.val(q);
        update_menu_item_quantity($(this), q, url, "+");

    });
    $("#table-cart").on('click', '.delete-value', function (e) {
        let row = $(this).closest('tr');
        let url = $(this).attr('data-url');
        let input = row.find(".item-quantity");
        let q = parseInt(input.val()) - 1;
        if (q >= 1) {
            input.val(q);
            update_menu_item_quantity($(this), q, url, "-");
        } else {
            $(this).attr("disabled", true);
        }
    });

    function update_menu_item_quantity(button, quantity, url, type) {
        let data = {
            'quantity': quantity,
        }
        let row = button.closest('tr');

        data = JSON.stringify(data);

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: 'POST',
            data: data,
            dataType: 'json',
            url: url,
            beforeSend: () => {
                $(button).text("...");
                $("#total-all-quantity, #total-all-amount").text("updating...");
                $("#nav-shopping-cart-summary").html(` 
                    <span class="icon-shopping-cart"></span> 
                    Updating... Item(s) - <span class="badge badge-warning"> Updating.. </span> 
                 `)
                row.find(".total-amount").text("updating...");
            },
            success: (data) => {
                // By default json is parsed
                // var obj = JSON.parse('{ "name":"John", "age":30, "city":"New York"}');
                row.find(".total-amount").text("₱" + data.context.total_amount);
                $("#total-all-quantity").text(data.context.total_all_quantity);
                $("#total-all-amount").text("₱" + data.context.total_all_amount);
                $("#nav-shopping-cart-summary").html(` 
                    <span class="icon-shopping-cart"></span> 
                    ${data.context.total_all_quantity} Item(s) - <span class="badge badge-warning"> ₱${data.context.total_all_amount} </span> 
                `)
            },
            complete: (data) => {
                $(button).text(type);
            },
            error: (data) => {

            }
        });
    }

    $("#table-cart").on("click", ".delete-all-menu-items", function (e) {
        $(this).closest('tr').remove();
        let url = $(this).attr('data-url');
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: 'POST',
            url: url,
            beforeSend: () => {
                $("#total-all-quantity, #total-all-amount #total-items").text("updating...");
                $("#nav-shopping-cart-summary").html(` 
                   <span class="icon-shopping-cart"></span> 
                   Updating... Item(s) - <span class="badge badge-warning"> Updating.. </span> 
                `)
            },
            success: (data) => {
                $("#total-all-quantity").text(data.context.total_all_quantity);
                $("#total-all-amount").text("₱" + data.context.total_all_amount);
                $("#total-items").text(` ${data.context.count} Items are in the cart `);
                $("#nav-shopping-cart-summary").html(` 
                    <span class="icon-shopping-cart"></span> 
                    ${data.context.total_all_quantity} Item(s) - <span class="badge badge-warning"> ₱${data.context.total_all_amount} </span> 
                `)
            },
            complete: (data) => {
            },
            error: (data) => {

            }
        });
    });


    $("#form-payment").on("submit", function (e) {
        e.preventDefault();
        let payment = $("#payment").val();
        let url = $(this).attr("data-url");
        let data = {
            'payment': payment,
        }

        data = JSON.stringify(data);
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: 'POST',
            url: url,
            data: data,
            dataType: 'json',
            beforeSend: () => {
                $("#change").text("Calculating...");
                $("#cash").text("Calculating...");
            },
            success: (data) => {
                if (data.valid) {
                    $("#change").text(`₱ ${data.context.change}`);
                    $("#cash").text(`₱ ${payment}`);
                    $("#payment").css("border-color", "#468847");
                    $("#error-message").css("color", "#468847").text("Payment Successful!").show();
                    // 
                    alert("Thank you for ordering... All your transaction is now completed and all your accounts and order are now clear. please print your receipt and if your unable to print it, you cannot get another receipt please becareful.")
                    // Printing 
                    var divToPrint = document.getElementById("table-cart");
                    newWin = window.open("");
                    newWin.document.write(divToPrint.outerHTML);
                    newWin.print();
                    newWin.close();
                    
                    window.location.href = data.context.url;
                    window.history.forward();  
                } else {
                    $("#payment").css("border-color", "#b94a48");
                    $("#error-message").css("color", "#b94a48").text("Insufficient Money").show();
                    $("#change").text(`₱ 0.0`);
                    $("#cash").text("0.0");
                }

            },
            complete: (data) => {
            },
            error: (data) => {

            }
        });

        return true;
    });

    $("#printReceipt").on("click", function (e) {
        e.preventDefault();
        // var mywindow = window.open('', 'PRINT', 'height=400,width=600');
        // mywindow.document.write('<html><head><title>' + document.title  + '</title>');
        // mywindow.document.write('</head><body >');
        // mywindow.document.write('<h1>' + document.title  + '</h1>');
        // mywindow.document.write(document.getElementById("printMe").innerHTML);
        // mywindow.document.write('</body></html>');

        // mywindow.document.close(); // necessary for IE >= 10
        // mywindow.focus(); // necessary for IE >= 10*/

        // mywindow.print();
        // mywindow.close();
        var divToPrint = document.getElementById("table-cart");
        newWin = window.open("");
        newWin.document.write(divToPrint.outerHTML);
        newWin.print();
        newWin.close();
        return true;
    });
});