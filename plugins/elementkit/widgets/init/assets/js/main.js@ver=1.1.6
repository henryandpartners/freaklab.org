(function ($) {
	"use strict";
	/*------------------------------------------------------------------
	[Table of contents]



	-------------------------------------------------------------------*/

	$.fn.myChart = function (options) {
		var settings = $.extend({
			barColor: '#666666',
			gradientColor1: '',
			gradientColor2: '',
			scaleColor: 'transparent',
			lineWidth: 20,
			size: 150,
			trackColor: '#f7f7f7',
			lineCap: 'round',
			gradientChart: false,
		}, options);

		return this.easyPieChart({
			barColor: settings.gradientChart === true ? function (percent) {
				var ctx = this.renderer.getCtx();
				var canvas = this.renderer.getCanvas();
				var gradient = ctx.createLinearGradient(0, 0, canvas.width, 0);
				gradient.addColorStop(0, settings.gradientColor1);
				gradient.addColorStop(1, settings.gradientColor2);
				return gradient;
			} : settings.barColor,
			scaleColor: settings.scaleColor,
			trackColor: settings.trackColor,
			lineCap: settings.lineCap,
			size: settings.size,
			lineWidth: settings.lineWidth
		});
	}

	$.fn.tab = function (options) {
		var opts = $.extend({}, $.fn.tab.defaults, options);
		return this.each(function () {
			var obj = $(this);
			$(obj).find('.tabHeader > .tab__list > .tab__list__item').on(opts.trigger_event_type, function () {
				$(obj).find('.tabHeader > .tab__list > .tab__list__item').removeClass('active');
				$(this).addClass('active');
				$('.tabContent > .tabItem').removeClass('active');
				$(obj).find('.tabContent > .tabItem').eq($(this).index()).addClass('active');
				$(obj).find('.tabContent > .tabItem').hide();
				$(obj).find('.tabContent > .tabItem').eq($(this).index()).show();
			})
		});
	}
	$.fn.tab.defaults = {
		trigger_event_type: 'click', //mouseover | click 默认是click
	};

	$(window).on('load', function () {

	}); // END load Function

	$(document).ready(function () {
		if ($('.ekit-video-popup').length > 0) {
			$('.ekit-video-popup').magnificPopup({
				disableOn: 700,
				type: 'iframe',
				mainClass: 'mfp-fade',
				removalDelay: 160,
				preloader: true,
				fixedContentPos: false,
			});
		}

		if ($('.btn-link').length > 0) {
			$(document).on('click', '.btn-link', function (e) {
				if (!$(this).parents().eq(1).hasClass('active')) {
					$(this).parents().eq(1).prevAll().removeClass('active');
					$(this).parents().eq(1).nextAll().removeClass('active');
					$(this).parents().eq(1).addClass('active');
				}
			});
		}

		if ($('.elementskit-single-image-accordion').length > 0) {
			$('.elementskit-single-image-accordion').on('click', function (e) {
				e.preventDefault();
				if (!($(this).hasClass('active'))) {
					$(this).nextAll().removeClass('active');
					$(this).prevAll().removeClass('active');
					$(this).addClass('active');
				}
			})
		}

		/*=============================================================
					29. wow function init
		=========================================================================*/
		var wow = new WOW({
			boxClass: 'wow',
			animateClass: 'animated'
		});
		wow.init();

		if ($('img').length > 0) {
			$('img').each(function () {
				$(this).attr('draggable', 'false');
				$(this).on('mousedown', function (event) {
					if (event.preventDefault) {
						event.preventDefault();
					}
				});
			});
		}


		/*==========================================================
				skill bar and number counter
		=======================================================================*/

		$.fn.animateNumbers = function (stop, commas, duration, ease) {
			return this.each(function () {
				var $this = $(this);
				var start = parseInt($this.text().replace(/,/g, ""), 10);
				commas = (commas === undefined) ? true : commas;
				$({
					value: start
				}).animate({
					value: stop
				}, {
						duration: duration == undefined ? 500 : duration,
						easing: ease == undefined ? "swing" : ease,
						step: function () {
							$this.text(Math.floor(this.value));
							if (commas) {
								$this.text($this.text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
							}
						},
						complete: function () {
							if (parseInt($this.text(), 10) !== stop) {
								$this.text(stop);
								if (commas) {
									$this.text($this.text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
								}
							}
						}
					});
			});
		};

		var colorfulchart = $('.colorful-chart');
		if ($(colorfulchart).length > 0) {
			$(colorfulchart).each(function (__, e) {
				var myColors = $(e).data('color');
				var datalineWidth = $(e).data('linewidth');
				var piechartsize = $(e).data('size');
				var color_type = $(e).data('pie_color_style');
				var gradentColor1 = $(e).data('gradientcolor1');
				var gradentColor2 = $(e).data('gradientcolor2');
				var barbg = $(e).data('barbg');

				var obj;

				if (color_type === 'gradient') {

					obj = {
						gradientChart: true,
						barColor: gradentColor1,
						gradientColor1: gradentColor2,
						gradientColor2: gradentColor1,
						lineWidth: datalineWidth,
						trackColor: barbg,
						size: piechartsize,
					};

				} else {
					obj = {
						lineWidth: datalineWidth,
						barColor: myColors,
						trackColor: barbg,
						size: piechartsize,
					};
				}


				$(e).myChart(obj);
			})
		}


		if ($('.nav-search-form .form-control').length > 0) {
			var $this = $('.nav-search-form .form-control');
			$this.on('blur', function () {
				$(this).parent().removeClass('focus')
			})
			$this.on('focus', function () {
				$(this).parent().addClass('focus')
			})
		}

		if ($(".flatpickr").length > 0) {
			$(".flatpickr").flatpickr();
		}

		if ($('#wp-admin-bar-elementor_edit_page-default').length > 0) {
			var elements = $('#wp-admin-bar-elementor_edit_page-default').children('li');
			$(elements).map(function (__, element) {
				var target = $(element).find(".elementor-edit-link-title");
				if (target.text().indexOf('dynamic-content-') !== -1) {
					target.parent().parent().remove();
				}
			});
		}

        $('[data-toggle="tooltip"]').tooltip()

	}); // end ready function

	$(window).on('scroll', function () {
		/*==========================================================
							65. shuffle letters
		======================================================================*/
		if ($('.shuffle-letter-title-wraper').length > 0) {
			$('.shuffle-letter-title-wraper').each(function (e) {
				if ($(this).onScreen() && !$(this).hasClass('shuffle-title')) {
					setTimeout(function () {
						$(this).find('.shuufle-letter-title').shuffleLetters();
						$(this).addClass('shuffle-title');
					}.bind(this), 400);
				}
			});
		}
	}); // END Scroll Function
})(jQuery);