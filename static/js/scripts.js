/*
 * M-Store | Modern E-Commerce Template
 * Copyright 2016 rokaux
 * Theme Custom Scripts
 */

jQuery(document).ready(function($) {
	'use strict';

	// Check if Page Scrollbar is visible
	//------------------------------------------------------------------------------
	var hasScrollbar = function() {
	  // The Modern solution
	  if (typeof window.innerWidth === 'number') {
	    return window.innerWidth > document.documentElement.clientWidth;
		}

	  // rootElem for quirksmode
	  var rootElem = document.documentElement || document.body;

	  // Check overflow style property on body for fauxscrollbars
	  var overflowStyle;

	  if (typeof rootElem.currentStyle !== 'undefined') {
			overflowStyle = rootElem.currentStyle.overflow;
		}

	  overflowStyle = overflowStyle || window.getComputedStyle(rootElem, '').overflow;

	    // Also need to check the Y axis overflow
	  var overflowYStyle;

	  if (typeof rootElem.currentStyle !== 'undefined') {
			overflowYStyle = rootElem.currentStyle.overflowY;
		}

	  overflowYStyle = overflowYStyle || window.getComputedStyle(rootElem, '').overflowY;

	  var contentOverflows = rootElem.scrollHeight > rootElem.clientHeight;
	  var overflowShown    = /^(visible|auto)$/.test(overflowStyle) || /^(visible|auto)$/.test(overflowYStyle);
	  var alwaysShowScroll = overflowStyle === 'scroll' || overflowYStyle === 'scroll';

	  return (contentOverflows && overflowShown) || (alwaysShowScroll);
	};
	if (hasScrollbar()) {
		$('body').addClass('hasScrollbar');
	}


	// Disable default link behavior for dummy links that have href='#'
	//------------------------------------------------------------------------------
	var $emptyLink = $('a[href=#]');
	$emptyLink.on('click', function(e){
		e.preventDefault();
	});


	// Page Transitions
	if($('.page-preloading').length) {
		$('a:not([href^="#"])').on('click', function(e) {
	    if($(this).attr('class') !== 'video-popup-btn' && $(this).attr('class') !== 'ajax-post-link' && $(this).attr('class') !== 'read-more ajax-post-link') {
				console.log($(this).attr('class'));
	      e.preventDefault();
	      var linkUrl = $(this).attr('href');
	      $('.page-preloading').addClass('link-clicked');
	      setTimeout(function(){
	        window.open(linkUrl , '_self');
	      }, 550);
	    }
	  });
	}


	// Animated Scroll to Top Button
	//------------------------------------------------------------------------------
	var $scrollTop = $('.scroll-to-top-btn');
	if ($scrollTop.length > 0) {
		$(window).on('scroll', function(){
	    if ($(window).scrollTop() > 600) {
	      $scrollTop.addClass('visible');
	    } else {
	      $scrollTop.removeClass('visible');
	    }
		});
		$scrollTop.on('click', function(e){
			e.preventDefault();
			$('html').velocity("scroll", { offset: 0, duration: 1000, easing:'easeOutExpo', mobileHA: false });
		});
	}


	// Smooth scroll to element
	//------------------------------------------------------------------------------
	var $scrollTo = $('.scroll-to');
	$scrollTo.on('click', function(event) {
		var $elemOffsetTop = $(this).data('offset-top');
		$('html').velocity("scroll", { offset:$(this.hash).offset().top-$elemOffsetTop, duration: 1000, easing:'easeOutExpo', mobileHA: false});
		event.preventDefault();
	});


	// Language Dropdown
	//------------------------------------------------------------------------------
	var langSwitcher = $('.lang-switcher'),
			langToggle = $('.lang-toggle');
	langToggle.on('click', function() {
		$(this).parent().toggleClass('open');
	});
	langSwitcher.on('click', function(e) {
    e.stopPropagation();
	});
	$(document).on('click', function(e) {
		langSwitcher.removeClass('open');
	});


	// Toggle Mobile Menu
	//------------------------------------------------------------------------------
	var menuToggle = $('.mobile-menu-toggle'),
			mobileMenu = $('.main-navigation');
	menuToggle.on('click', function() {
		$(this).toggleClass('active');
		mobileMenu.toggleClass('open');
	});


	// Toggle Submenu
	//------------------------------------------------------------------------------
	var $hasSubmenu = $('.menu-item-has-children > a');

	function closeSubmenu() {
		$hasSubmenu.parent().removeClass('active');
	}
	$hasSubmenu.on('click', function(e) {
		if($(e.target).parent().is('.active')) {
			closeSubmenu();
		} else {
			closeSubmenu();
			$(this).parent().addClass('active');
		}
	});


	// Shop Filters Toggle
	//------------------------------------------------------------------------------
	var filtersToggle = $('[data-toggle="filters"]'),
			filtersWrap = $('.filters'),
			filtersPane = $('.filters-pane');
	function closeFilterPane() {
		filtersToggle.removeClass('active');
		filtersPane.removeClass('open');
		filtersWrap.css('height', 0);
	}
	filtersToggle.on('click', function(e) {
		var currentFilter = $(this).attr('href');
		if($(this).is('.active')) {
			closeFilterPane();
		} else {
			closeFilterPane();
			$(this).addClass('active');
			filtersWrap.css('height', $(currentFilter).outerHeight());
			$(currentFilter).addClass('open');
		}
		e.preventDefault();
	});
	if(typeof window.Modernizr !== "undefined" && !Modernizr.touch) {
		$(window).on('resize', function() {
			closeFilterPane();
		});
	}

	// Sidebar Toggle on Mobile
	//------------------------------------------------------------------------------
	var sidebar = $('.sidebar'),
			sidebarToggle = $('.sidebar-toggle');
	sidebarToggle.on('click', function() {
		$(this).addClass('sidebar-open');
		sidebar.addClass('open');
	});
	$('.sidebar-close').on('click', function() {
		sidebarToggle.removeClass('sidebar-open');
		sidebar.removeClass('open');
	});


	// Count Input (Quantity)
	//------------------------------------------------------------------------------
	$(".incr-btn").on("click", function(e) {
		var $button = $(this);
		var oldValue = $button.parent().find('.quantity').val();
		$button.parent().find('.incr-btn[data-action="decrease"]').removeClass('inactive');
		if ($button.data('action') == "increase") {
			var newVal = parseFloat(oldValue) + 1;
		} else {
		 // Don't allow decrementing below 1
			if (oldValue > 1) {
				var newVal = parseFloat(oldValue) - 1;
			} else {
				newVal = 1;
				$button.addClass('inactive');
			}
		}
		$button.parent().find('.quantity').val(newVal);
		e.preventDefault();
	});

	// Waves Effect (on Buttons)
	//------------------------------------------------------------------------------
	if($('.waves-effect').length) {
		Waves.displayEffect( { duration: 600 } );
	}

	// Add to Cart Button Effect
	//------------------------------------------------------------------------------
	var animating = false;
	$('.shop-item').each(function() {
		var addToCartBtn = $(this).find('.add-to-cart');
		addToCartBtn.on('click', function() {
			if(!animating) {
				//animate if not already animating
				animating =  true;
				// resetCustomization(addToCartBtn);

				addToCartBtn.addClass('is-added').find('path').eq(0).animate({
					//draw the check icon
					'stroke-dashoffset':0
				}, 300, function(){
					setTimeout(function(){
						// updateCart();
						addToCartBtn.removeClass('is-added').find('em').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
							//wait for the end of the transition to reset the check icon
							addToCartBtn.find('path').eq(0).css('stroke-dashoffset', '19.79');
							animating =  false;
						});

						if( $('.no-csstransitions').length > 0 ) {
							// check if browser doesn't support css transitions
							addToCartBtn.find('path').eq(0).css('stroke-dashoffset', '19.79');
							animating =  false;
						}
					}, 600);
				});
			}
		});
	});


	// Product Gallery
	//------------------------------------------------------------------------------
	var galleryThumb = $('.product-gallery-thumblist a'),
			galleryPreview = $('.product-gallery-preview > li');

	// Thumbnails
	//------------------------------------------------------------------------------
	galleryThumb.on('click', function(e) {
		var target = $(this).attr('href');

		galleryThumb.parent().removeClass('active');
		$(this).parent().addClass('active');
		galleryPreview.removeClass('current');
		$(target).addClass('current');

		e.preventDefault();
	});


	// Color Select
	//------------------------------------------------------------------------------
	$('.color-select').on('change', function() {
		var target = $(this).find(':selected').data('image');
		$('[href="#' + target + '"]').trigger('click');
	});


	
	

	// Tooltips
	//------------------------------------------------------------------------------
	var $tooltip = $('[data-toggle="tooltip"]');
	if ( $tooltip.length > 0 ) {
		$tooltip.tooltip();
	}


	// Custom checkboxes and radios
	//------------------------------------------------------------------------------
	var $checkbox = $('input[type="checkbox"], input[type="radio"]');
	if($checkbox.length) {
		$('input').iCheck();
	}


	// Countdown Function
	//------------------------------------------------------------------------------
	function countDownFunc( items, trigger ) {
		items.each( function() {
			var countDown = $(this),
					dateTime = $(this).data('date-time');

			var countDownTrigger = ( trigger ) ? trigger : countDown;
			countDownTrigger.downCount({
		      date: dateTime,
		      offset: +10
		  });
		});
	}
	countDownFunc( $('.countdown') );
    
    // Range Slider
	//------------------------------------------------------------------------------
	var rangeSlider  = document.querySelector('.ui-range-slider');
	if(typeof rangeSlider !== 'undefined' && rangeSlider !== null) {
		var dataStartMin = parseInt(rangeSlider.parentNode.getAttribute( 'data-start-min' ), 10),
				dataStartMax = parseInt(rangeSlider.parentNode.getAttribute( 'data-start-max' ), 10),
				dataMin 		 = parseInt(rangeSlider.parentNode.getAttribute( 'data-min' ), 10),
				dataMax   	 = parseInt(rangeSlider.parentNode.getAttribute( 'data-max' ), 10),
				dataStep  	 = parseInt(rangeSlider.parentNode.getAttribute( 'data-step' ), 10);
		var valueMin 			= document.querySelector('.ui-range-value-min span'),
				valueMax 			= document.querySelector('.ui-range-value-max span'),
				valueMinInput = document.querySelector('.ui-range-value-min input'),
				valueMaxInput = document.querySelector('.ui-range-value-max input');
		noUiSlider.create(rangeSlider, {
			start: [ dataStartMin, dataStartMax ],
			connect: true,
			step: dataStep,
			range: {
				'min': dataMin,
				'max': dataMax
			}
		});
		rangeSlider.noUiSlider.on('update', function(values, handle) {
			var value = values[handle];
			if ( handle ) {
				valueMax.innerHTML  = Math.round(value);
				valueMaxInput.value = Math.round(value);
//                console.log('Max '+valueMaxInput.value )
//                console.log('Min '+valueMinInput.value )
			} else {
				valueMin.innerHTML  = Math.round(value);
				valueMinInput.value = Math.round(value);
			}
		});
        

	}

});/*Document Ready End*/
