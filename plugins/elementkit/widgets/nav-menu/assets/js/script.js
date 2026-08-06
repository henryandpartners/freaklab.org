jQuery(document).ready(function ($) {
	"use strict";

	function togglerAppend(el) {
		$(el).each(function () {
			$(this).before(
				'<button class="elementskit-menu-hamburger elementskit-menu-toggler">'
				+ '<span class="elementskit-menu-hamburger-icon"></span>'
				+ '<span class="elementskit-menu-hamburger-icon"></span>'
				+ '<span class="elementskit-menu-hamburger-icon"></span>'
				+ '</button>'
			);
		})
	}

	togglerAppend($('.elementskit-menu-container'));

	$('.elementskit-menu-container').each(function (__, e) {
		$(e).after('<div class="elementskit-menu-overlay elementskit-menu-offcanvas-elements elementskit-menu-toggler"></div>');
	});

	function elementskit_event_manager(_event, _selector, _fn) {
		$(document).on(_event, _selector, _fn);
	}

	elementskit_event_manager('click', '.elementskit-dropdown-has > a', function (e) {
		e.preventDefault();

		var menu = $(this).parents('.elementskit-navbar-nav');
		var li = $(this).parent();
		var dropdown = li.find('>.elementskit-dropdown, >.elementskit-megamenu-panel');

		dropdown.find('.elementskit-dropdown-open').removeClass('elementskit-dropdown-open');

		jQuery(window).on('resize', function () {
			if (jQuery(window).width() > 991) {
				jQuery(dropdown).removeClass('elementskit-dropdown-open');
			}
		})
		if (dropdown.hasClass('elementskit-dropdown-open')) {
			dropdown.removeClass('elementskit-dropdown-open');
		} else {
			dropdown.addClass('elementskit-dropdown-open');
		}

	});

	elementskit_event_manager('click', '.elementskit-menu-toggler', function (e) {
		e.preventDefault();
		var parent_conatiner = $(this).parents('.elementskit-menu-container').parent();
		if (parent_conatiner.length < 1) {
			parent_conatiner = $(this).parent();
		}
		var off_canvas_class = parent_conatiner.find('.elementskit-menu-offcanvas-elements');

		jQuery(window).on('resize', function () {
			if (jQuery(window).width() > 991) {
				off_canvas_class.removeClass('active');
			}
		})
		if (off_canvas_class.hasClass('active')) {
			off_canvas_class.removeClass('active');
		} else {
			off_canvas_class.addClass('active');
		}

	});


}); // end ready function