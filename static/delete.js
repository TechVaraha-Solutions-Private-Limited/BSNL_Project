let cartPageUrl = '/bookings/cart' ;
$('button[name="continue_to_cart"]').on('click', function () {
    $.get('/api/v1/user/is-autherized/', function(data) {
        var is_authenticated = data.message
        if (is_authenticated) {
            window.location.replace(cartPageUrl);
            setCookie("itemsInCart", localStorage.getItem("cart"), 1);
          //  document.cookie="itemsInCart=" + localStorage.getItem("cart") ;
        }
        else {
            $('#loginSignup').click();
        }
    })
    
});

function setCookie(cName, cValue, expDays) {
    let date = new Date();
    date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = cName + "=" + cValue + "; " + expires + "; path=/";
}
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function createItemsCard(itemData) {
    var cachedCartData = JSON.parse(localStorage.getItem('cart'));
    var updateDivWithThisData = {};
    if (cachedCartData && cachedCartData.hasOwnProperty("items")) {
        if (cachedCartData["items"][itemData.id]) {
            updateDivWithThisData['class'] = 'active'
            updateDivWithThisData['qty'] = cachedCartData["items"][itemData.id]['qty']
        }
        else {
            updateDivWithThisData['class'] = '';
            updateDivWithThisData['qty'] = 1;
        }
        if (cachedCartData['estimatedTotal'] !== 0) {
            $('#total-item').text(cachedCartData['totalItems']);
            $("#estimated-total-item").text(cachedCartData['estimatedTotal']);;
            $('.sticky-cart-footer').addClass('show');
        }
    }
    else {
        updateDivWithThisData['class'] = '';
        updateDivWithThisData['qty'] = 1;
    }


    var cardTemplate = [
        '<div class="row-data active" data-tag="girls,restyling,regular,withLining">',
        '<div class="row">',
        '<div class="col-md-8">',
        '<h3 >',
        itemData.item__name || '',
        '</h3>',
        '<p id="selectedTags">',
        itemData.item__tags || "",
        '</p>',
        '<p id="priceTag">Starting Price: ₹<span class="priceValue" id="' +itemData.id + '"> ',
        itemData.item__starting_price || "",
        '</span></p>',
        '</div>',

        '<div class="col-md-4">',
        '<div class="items-add">',
        '<img  src="/media/' + itemData.item__image + '" alt="Items" onClick="myfunction(this.src)" />',
        '<button type="button" class="btn btn1 add" name="button" id="add1">Add</button>',
        '<div class="quantity-wrapper ' + updateDivWithThisData['class'] + '">',
        '<button type="button" class="btn  btn2  quantity-btn decrease" name="button">&#8722;</button>',
        '<span class="quantity-txt" data-count="' + updateDivWithThisData['qty'] + '">' + updateDivWithThisData['qty'] + '</span>',
        '<button type="button" class="btn btn2 quantity-btn increase"  name="button">&#43;</button>',
        '</div>',
        '</div>',
        '</div>',
        '</div>',
        '</div>',

      
    ];
    // a jQuery node
    return $(cardTemplate.join('')); 
}

$(document).ready(function () {
    $('#text_search').val('');
    var selectedServicecs = {
        'category': "1",
        'service': "1",
        'finishing': "2",
        'pattern': "1",
        'items': []
    }

    function populateItemsData() {
        var csrftoken = getCookie('csrftoken');

        
        $.ajax({
            type: "POST",
          //  url: "/api/v1/user/get-items/" +  jQuery.param({ page: obj.page}),
            url: "/api/v1/user/get-items/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'data' : JSON.stringify(selectedServicecs),
                'page' : 1,
                'limit' : 100
            },
            beforeSend: function(msg){
                $(".loader").addClass("show");
              },
            success: function (result) {
                if (result.message == "ok") {
                    $(".loader").removeClass("show");
                    $('.row-data').remove();
                    $('#itemCount').text(result.item_counts);
                    let cachedItems = JSON.parse(localStorage.getItem("cart"));
                    if(cachedItems == null){
                        localStorage.setItem('cart', JSON.stringify(result.itemsInCart));
                        setCookie("itemsInCart", localStorage.getItem("cart"), 1);
                    }

                    for (var i = 0; i < result.first_page_items.length; i++) {
                        itemCard = createItemsCard(result.first_page_items[i]);
                        $('#itemDataPlaceholder').append(itemCard);
                    }
                }
                else {

                }
            },
            error: function (error) {
                console.log(error.responseText);
            }
        });
    }

    $(document).on("click", '.filter-btn', function () {
        var csrftoken = getCookie('csrftoken');
        
        var filterLabel = $(this).attr('data-controls');
        var parentId = $(this).closest('ul').attr('id');
        var selectedId = $(this).attr('id');
        
        selectedServicecs[filterLabel] = selectedId;


        var sideTabsDiv = document.querySelector('.col-md-3.sideTabs');
        var ulElements = sideTabsDiv.querySelectorAll('ul');
        ulElements.forEach(function(ul) {

        var liElements = ul.querySelectorAll('li');

        var hasActiveLi = Array.from(liElements).some(function(li) {
            return li.querySelector('.nav-link').classList.contains('active');
        });

        if (hasActiveLi) {
            return;
        }

        liElements.forEach(function(li) {
            li.querySelector('.nav-link').classList.remove('active');
        });

        var firstLi = ul.querySelector('li');


        if (firstLi) {

            var firstButton = firstLi.querySelector('.nav-link');
            firstButton.classList.add('active');
        }
        });

        $('#' + parentId + " .filter-btn").removeClass('active');
        $(this).addClass('active');
        var itemCard = $()
        $.ajax({
            type: "POST",
            url: "/api/v1/user/get-items/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'data' : JSON.stringify(selectedServicecs),
                'page' : 1,
                'limit' : 10
            },
            beforeSend: function(msg){
                $(".loader").addClass("show");
              },
            // contentType: "application/json",
            // dataType: "json",
            // header: {
            //     'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            // },
            success: function (result) {
                if (result.message == "ok") {
                    $('#text_search').val('');
                    $(".loader").removeClass("show");
                    $('.row-data').remove();
                    $('#itemCount').text(result.item_counts);

                    for (var i = 0; i < result.first_page_items.length; i++) {
                        itemCard = createItemsCard(result.first_page_items[i]);
                        $('#itemDataPlaceholder').append(itemCard);
                    }
                }
                else {

                }
            },
            error: function (error) {
                console.log(error.responseText);
            }
        });
    });

    // Pagination
    $(function() {
        let now = new Date();
        let cachedItems = JSON.parse(localStorage.getItem('cart'));        
        if(cachedItems){
            if(now.getTime() > cachedItems.expiry){
                localStorage.removeItem("cart");
            }
        }      
        populateItemsData();
    });




    $(function(){

       
    $('.search-input').on("click", '.btn-danger', function () {
        
        var csrftoken = getCookie('csrftoken');
        
        var search_text = $('#text_search').val();

            var sideTabsDiv = document.querySelector('.col-md-3.sideTabs');
            var activeButtons = sideTabsDiv.querySelectorAll('.nav-link.active');
            activeButtons.forEach(function(button) {
            button.classList.remove('active');
            });

   
        var itemCard = $()
        $.ajax({
            type: "POST",
            url: "/api/v1/user/get-search-items/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'data' : search_text,
                'page' : 1,
                'limit' : 10
            },
            beforeSend: function(msg){
                $(".loader").addClass("show");
              },
            // contentType: "application/json",
            // dataType: "json",
            // header: {
            //     'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            // },
            success: function (result) {
                if (result.message == "ok") {
                    $(".loader").removeClass("show");
                    $('.row-data').remove();
                    $('#itemCount').text(result.item_counts);

                    for (var i = 0; i < result.first_page_items.length; i++) {
                        itemCard = createItemsCard(result.first_page_items[i]);
                        $('#itemDataPlaceholder').append(itemCard);
                    }
                }
                else {

                }
            },
            error: function (error) {
                console.log(error.responseText);
            }
        });
    });
        
        
        //press enter on text area..
       $('#text_search').keypress(function (e) {
       var key = e.which;
       if(key == 13)  // the enter key code
        {
          $('.btn-danger').click();
          return false; 
        }
      });
        
      });

    // Pagination
    $(function() {
        let now = new Date();

        let cachedItems = JSON.parse(localStorage.getItem('cart'));
        
        if(cachedItems){
            if(now.getTime() > cachedItems.expiry){
                localStorage.removeItem("cart");
            }
        }      
        

        populateItemsData();
        // var cachedItems = JSON.parse(localStorage.getItem('cart'));
        // cachedItems['orderId'] = $("input[name='orderId']").val();
        // localStorage.setItem('cart', JSON.stringify(cachedItems));
        // $('#page').Pagination({
        //         size: 50,
        //         pageShow: 1,
        //         page: 1,
        //         limit: 10,
        //     }, function(obj){
        //         populateItemsData(obj)
        //     });
    });

    //Cancel items in cart
    $('#customTabContent button.btn.btn25').on('click', function(){        
        $('.quantity-wrapper').each(function(){
            $(this).removeClass('active');
        });
        localStorage.removeItem("cart");
        localStorage.removeItem("estimatedTotal");
        localStorage.removeItem("totalItems");
        localStorage.removeItem("advancePayable");
        $('#total-item').text(0);
        $("#estimated-total-item").text(0);
        $('.sticky-cart-footer').removeClass('show');       
    })
});


// Zoom Image
//   function myFunction() {
//     $('.zooncon').show();
//   }
  function myfunction(val) {
    $('#zoomid').attr('src',val);
    $('.zooncon').toggle();
  }
  $("#clsbttn").on('click', function (e) {
    $(".zooncon").hide();
 });
 



