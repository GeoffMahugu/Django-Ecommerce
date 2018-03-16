$(document).ready(function(){
    
    $(".callout").show().delay(5000).fadeOut(3000);
    
    var price = $('#vari_select option:selected').attr('data-price');
    var new_price = $('#price_change').text(price);
    $('#vari_select').change(function(){
        var price = $('#vari_select option:selected').attr('data-price');
        var new_price = $('#price_change').text(price);
    });
    
    $('li.thumb_select').click(function(){
        var tp = $(this).attr('data-price')
        var new_p = $('#price_change').text(tp);
    });
   
    inlinetot = 0;
    $('.item-price').each(function(){
        if(parseFloat( $(this).attr('data-inline')) != 'NaN'){
            inlinetot += parseFloat( $(this).attr('data-inline'));    
//            console.log(inlinetot)
        }
        
//        console.log($(this).attr('data-inline'));
    });
    var sub_cart = $('#drop_amt').text('Ksh '+inlinetot);
    
//    $(document).on('change keyup keydown blur click','.incr-btn',function(){
//    });

    $(document).on('change keyup keydown blur click','.incr-btn',function(){
        accInline = 0;
        $('.quantity').each(function(){
            var new_inline = (parseFloat( $(this).attr('data-p')))*(parseFloat( $(this).val())); 
            accInline +=new_inline
        });
        var tot = $('#total').text('Ksh '+accInline);       
    });

    $('#add_cart').click(function(event){
        event.preventDefault()
        var item = $('#vari_select option:selected').val();
        var qnt = $('#qnt').val();
//        console.log('item: '+item)
//        console.log('qnt: '+qnt)
        $.ajax({
            url: '/Cart/add/',
            type: 'post',
            data: { 'csrfmiddlewaretoken' : csrftoken, 'item':item,'qnt':qnt},
            
//            success : function(data) {
//                alert('Cart item Added');
//                console.log('success'); 
//            },
            success: function(data){
                BudgeUpdate();
                alert('Cart item Added');
            },

            error : function() {
                alert('Failed Adding Item to cart');
            }

        });
    });
    
    $('.item-remove').click(function(event){
        event.preventDefault()
        $(this).attr('data-delete','True');
        $(this).parent().hide();
    });
 
    
    $('.update').click(function(event){
        event.preventDefault()
        $(this).fadeOut(300);
        
        send_ = []
        $('.count-input').each(function(){
            send = {}
            //console.log('Div object: ', $(this).children())
//            console.log('flag value: ', $(this).parent().next().attr('data-delete'))
            input = $(this).children()[1]
            qnt = $(input).val()
            id_value = $(input).prop('id')
            del = $(this).parent().next().attr('data-delete')
//            console.log('value, id_value, del', qnt, id_value, del)
            send.id = id_value
            send.qnt = qnt
            send.del = del
            send_.push(send)
        })
//        console.log(send_)
        $.ajax({
            url: '/Cart/mycart/edit/',
            type: 'post',
            data: { 'csrfmiddlewaretoken' : csrftoken, 'send':JSON.stringify(send_)},
            
            success : function(data) {
                
                alert('Cart items Updated');
//                console.log('success'); 
            },

            error : function() {
                alert('Failed Adding Item to cart');
            }

        });
    });
    
    $('#checkout').click(function(event){
        event.preventDefault()
//        console.log('Hello')
        var fname = $('#firstname').val();
        var lname = $('#lname').val();
        var email = $('#em').val();
        var add1 = $('#add1').val();
        var add2 = $('#add2').val();
        var ph = $('#phone').val();
        var co = $('#co').val();
        var county = $('#county').val();
        var state = $('#state').val();
        var city = $('#ci').val();
        var zip = $('#zip').val();
        
        $.ajax({
            url: '/Cart/mycart/checkout/commit/',
            type: 'post',
            data: { 'csrfmiddlewaretoken' : csrftoken, 'firstname' : fname, 'lastname' : lname, 'email' : email, 'phone' : ph, 'address1' : add1, 'address2' : add2, 'company' : co, 'country' : county, 'state' : state, 'city' : city, 'zip' : zip },
//            
            success : function(data) {
//                console.log(data)
//                console.log('fname'+fname)
//                console.log('lname'+lname)
//                console.log('email'+em)
//                console.log('add1'+add1)
//                console.log('add2'+add2)
//                console.log('phone'+phone)
//                console.log('company'+co)
//                console.log('county'+county)
//                console.log('city'+city)
//                console.log('zipcode'+zip)
//                
                alert('Proccede to payment');
                window.location = "/Cart/mycart/checkout/payment/";
//                console.log('success'); 
            },

            error : function() {
                alert('Failed Adding Item to cart');
            }

        });
    });
    
    function BudgeUpdate(){
        $.ajax({
            url: '/Products/supdate/',
            type: 'get',
            data: {},
//            // handle a successful response
            success : function(data) {
//                console.log(data)
                sc = data.length
                $("#scount").text(sc)
//                console.log('The Number'+s)

                $('#cart-dropdown').html('')

            },
            error : function() {
                console.log('Not yet'); // provide a bit more info about the error to the console
            }
        });
    };
    $(document).on('change keyup keydown blur click','#search',function(e){

        ths = $("#search").val()
        console.log(ths)
        var q = e.target.value.toUpperCase();
        console.log(q)
        var self = this
        $('div.item_search').each(function(){
            var name = this.children[0].children[1].children[0].textContent.toUpperCase();
            if(name.search(q) < 0) {
                $(this).fadeOut();
            }else{
                $(this).fadeIn();
            }

        });
    });
    
    $(document).on('change keyup keydown blur click','.ui-range-slider',function(e){
        mi =  $("#min").val();
        mx =  $("#max").val();
        min = Math.round(mi);
        max = Math.round(mx);
        
        $('div.item_search').each(function(){
            var no = this.children[0].children[1].children[1].children[1].textContent;
            var number = Math.round(no);
//            console.log(number)
            if( number < min || number > max ){
                $(this).fadeOut();
            }else{
                $(this).fadeIn();
                
            }

        });
    });
    
    $(document).on('click','#first',function(e){
        max = 1000
        min = 0
        PriceFilter(max,min);
    });
    
    $(document).on('click','#sec',function(e){
        max = 10000
        min = 1000
        PriceFilter(max,min);
    });
    
    $(document).on('click','#third',function(e){
        max = 25000
        min = 10000
        PriceFilter(max,min);
    });
    
    $(document).on('click','#fourth',function(e){
        max = 50000
        min = 25000
        PriceFilter(max,min);
    });
    
    $(document).on('click','#fifth',function(e){
        max = 100000
        min = 50000
        PriceFilter(max,min);
    });
    $(document).on('click','#sixth',function(e){
        max = 250000
        min = 100000
        PriceFilter(max,min);
    });
    
    function PriceFilter(min,max){
        $('div.item_search').each(function(){
            var no = this.children[0].children[1].children[1].children[1].textContent;
            var number = Math.round(no);
//            console.log(number)
            if( number < max || number > min ){
                $(this).fadeOut();
            }else{
                $(this).fadeIn();
                
            }

        });
    };
    
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
    var csrftoken = getCookie('csrftoken');
    
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});