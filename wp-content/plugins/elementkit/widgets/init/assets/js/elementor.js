(function ($, elementor) {
	"use strict";

	var Elementskit = {

		init: function () {

			var widgets = {
				'elementskit-countdown-timer.default': Elementskit.Countdown_Timer,
				'elementskit-client-logo.default': Elementskit.Client_Logo,
				'elementskit-testimonial.default': Elementskit.Testimonial_Slider,
				'elementskit-image-comparison.default': Elementskit.Image_Comparison,
				'elementskit-progressbar.default': Elementskit.Progressbar,
				'elementskit-piechart.default': Elementskit.Piechart,
				'elementskit-funfact.default': Elementskit.Funfact,
				'elementskit-gallery.default': Elementskit.Gallery,
				'elementskit-motion-text.default': Elementskit.MotionText,
				'elementskit-timeline.default': Elementskit.TimeLine,
				'elementskit-post-tab.default': Elementskit.PostTab,
				'elementskit-elementskit-hotspot.default': Elementskit.Hotspot,
				'elementskit-header-search.default': Elementskit.Header_Search,
				'elementskit-header-offcanvas.default': Elementskit.Header_Off_Canvas,
			};
			$.each(widgets, function (widget, callback) {
				elementor.hooks.addAction('frontend/element_ready/' + widget, callback);
			});

			elementor.hooks.addAction('frontend/element_ready/global', Elementskit.AnimationCallback);
		},

		AnimationCallback: function ($scope) {
			function init($scope) {

				new EkitStickyHandler({ $element: $scope });

				$scope.find('.elementskit-invisible').each(function () {
					var el = $(this);
					var settings = JSON.parse(el.attr('data-settings'));

					var isVisible = Elementskit.IsElementInView(el, false),
						animationClass = settings._animation,
						animationDelay = settings._animation_delay || 300;

					if (isVisible == true) {
						setTimeout(function () {
							//console.log('s');
							el.removeClass('elementskit-invisible').addClass('animated ' + animationClass);
						}, animationDelay);
					}
				});
			}

			init($scope);
			$(window).on('scroll', function () {
				init($scope);
			});
		},

		IsElementInView: function (element, fullyInView) {
			var pageTop = $(window).scrollTop();
			var pageBottom = pageTop + $(window).height();
			var elementTop = element.offset().top;
			var elementBottom = elementTop + element.height();

			if (fullyInView === true) {
				return ((pageTop < elementTop) && (pageBottom > elementBottom));
			} else {
				return ((elementTop <= pageBottom) && (elementBottom >= pageTop));
			}
		},


		Progressbar: function ($scope) {
			var barElement = $scope.find(".single-skill-bar");
			var percentElement = $scope.find(".number-percentage");
			var value = percentElement.attr("data-value");
			var duration = percentElement.attr("data-animation-duration");
			duration = parseInt((duration != '' ? duration : 300), 10);

			barElement.waypoint({
				handler: function () {
					percentElement.animateNumbers(value, true, duration);
					barElement.find('.skill-track').animate({
						width: value + '%'
					}, 3500);
				},
				offset: '100%'
			})
		},
		Funfact: function ($scope) {
			var barElement = $scope.find(".elementskit-funfact");
			var percentElement = $scope.find(".number-percentage");
			var value = percentElement.attr("data-value");
			var duration = percentElement.attr("data-animation-duration");
			duration = parseInt((duration != '' ? duration : 300), 10);

			barElement.waypoint({
				handler: function () {
					percentElement.animateNumbers(value, true, duration);
				},
				offset: '100%'
			})
		},
		Countdown_Timer: function ($scope) {

			var $container1 = $scope.find('.elementskit-countdown-timer[data-ekit-countdown]');
			var $container2 = $scope.find('.elementskit-countdown-timer-2[data-ekit-countdown]');
			var $container3 = $scope.find('.elementskit-countdown-timer-3[data-ekit-countdown]');
			var $container4 = $scope.find('.elementskit-countdown-timer-4[data-ekit-countdown]');
			var $container5 = $scope.find('.elementskit-flip-clock');

			$container1.each(function () {
				var $this = $(this),
					finalDate = $(this).data('ekit-countdown');
				var hour = $(this).data('date-ekit-hour'),
					minute = $(this).data('date-ekit-minute'),
					second = $(this).data('date-ekit-second'),
					day = $(this).data('date-ekit-day'),
					week = $(this).data('date-ekit-week'),
					finish_title = $(this).data('finish-title'),
					finish_content = $(this).data('finish-content');

				$this.theFinalCountdown(finalDate, function (event) {
					var $this = $(this).html(event.strftime(' ' +
						'<div class="elementskit-timer-container elementskit-days"><div class="elementskit-inner-container"><div class="elementskit-timer-content"><span class="elementskit-timer-count">%-D </span><span class="elementskit-timer-title">' + day + '</span></div></div></div>' +
						'<div class="elementskit-timer-container elementskit-hours"><div class="elementskit-inner-container"><div class="elementskit-timer-content"><span class="elementskit-timer-count">%H </span><span class="elementskit-timer-title">' + hour + '</span></div></div></div>' +
						'<div class="elementskit-timer-container elementskit-minutes"><div class="elementskit-inner-container"><div class="elementskit-timer-content"><span class="elementskit-timer-count">%M </span><span class="elementskit-timer-title">' + minute + '</span></div></div></div>' +
						'<div class="elementskit-timer-container elementskit-seconds"><div class="elementskit-inner-container"><div class="elementskit-timer-content"><span class="elementskit-timer-count">%S </span><span class="elementskit-timer-title">' + second + '</span></div></div></div>'
					));
				})
					.on('finish.countdown', function () {
						$(this).html(
							finish_title + "<br/>" + finish_content
						);
					});
			});

			$container2.each(function () {
				var $this = $(this),
					finalDate = $(this).data('ekit-countdown');
				var hour = $(this).data('date-ekit-hour'),
					minute = $(this).data('date-ekit-minute'),
					second = $(this).data('date-ekit-second'),
					day = $(this).data('date-ekit-day'),
					week = $(this).data('date-ekit-week'),
					finish_title = $(this).data('finish-title'),
					finish_content = $(this).data('finish-content');

				$this.theFinalCountdown(finalDate, function (event) {

					var $this = $(this).html(event.strftime(' ' +
						'<div class="elementskit-timer-container elementskit-days"><span class="elementskit-timer-count">%-D </span><span class="elementskit-timer-title">' + day + '</span></div>' +
						'<div class="elementskit-timer-container elementskit-hours"><span class="elementskit-timer-count">%H </span><span class="elementskit-timer-title">' + hour + '</span></div>' +
						'<div class="elementskit-timer-container elementskit-minutes"><span class="elementskit-timer-count">%M </span><span class="elementskit-timer-title">' + minute + '</span></div>' +
						'<div class="elementskit-timer-container elementskit-seconds"><span class="elementskit-timer-count">%S </span><span class="elementskit-timer-title">' + second + '</span></div>'));
				})
					.on('finish.countdown', function () {
						$(this).html(
							finish_title + "<br/>" + finish_content
						);
					});
			});

			$container3.each(function () {
				var $this = $(this),
					finalDate = $(this).data('ekit-countdown');
				var hour = $(this).data('date-ekit-hour'),
					minute = $(this).data('date-ekit-minute'),
					second = $(this).data('date-ekit-second'),
					day = $(this).data('date-ekit-day'),
					week = $(this).data('date-ekit-week'),
					finish_title = $(this).data('finish-title'),
					finish_content = $(this).data('finish-content');

				$this.theFinalCountdown(finalDate, function (event) {
					var $this = $(this).html(event.strftime(' ' +
						'<div class="elementskit-timer-container elementskit-days"><div class="elementskit-timer-content"><div class="elementskit-inner-container"><span class="elementskit-timer-count">%-D </span><span class="elementskit-timer-title">' + day + '</span></div></div></div>' +
						'<div class="elementskit-timer-container elementskit-hours"><div class="elementskit-timer-content"><div class="elementskit-inner-container"><span class="elementskit-timer-count">%H </span><span class="elementskit-timer-title">' + hour + '</span></div></div></div>' +
						'<div class="elementskit-timer-container elementskit-minutes"><div class="elementskit-timer-content"><div class="elementskit-inner-container"><span class="elementskit-timer-count">%M </span><span class="elementskit-timer-title">' + minute + '</span></div></div></div>' +
						'<div class="elementskit-timer-container elementskit-seconds"><div class="elementskit-timer-content"><div class="elementskit-inner-container"><span class="elementskit-timer-count">%S </span><span class="elementskit-timer-title">' + second + '</span></div></div></div>'));

				})
					.on('finish.countdown', function () {
						$(this).html(
							finish_title + "<br/>" + finish_content
						);
					});
			});

			$container4.each(function () {
				var $this = $(this),
					finalDate = $(this).data('ekit-countdown');
				var hour = $(this).data('date-ekit-hour'),
					minute = $(this).data('date-ekit-minute'),
					second = $(this).data('date-ekit-second'),
					day = $(this).data('date-ekit-day'),
					week = $(this).data('date-ekit-week'),
					finish_title = $(this).data('finish-title'),
					finish_content = $(this).data('finish-content');

				$this.theFinalCountdown(finalDate, function (event) {

					var $this = $(this).html(event.strftime(' ' +
						'<div class="elementskit-timer-container elementskit-days"><span class="elementskit-timer-count">%-D </span><span class="elementskit-timer-title">' + day + '</span></div>' +
						'<div class="elementskit-timer-container elementskit-hours"><span class="elementskit-timer-count">%H </span><span class="elementskit-timer-title">' + hour + '</span></div>' +
						'<div class="elementskit-timer-container elementskit-minutes"><span class="elementskit-timer-count">%M </span><span class="elementskit-timer-title">' + minute + '</span></div>' +
						'<div class="elementskit-timer-container elementskit-seconds"><span class="elementskit-timer-count">%S </span><span class="elementskit-timer-title">' + second + '</span></div>'));

				})
					.on('finish.countdown', function () {
						$(this).html(
							finish_title + "<br/>" + finish_content
						);
						$(this).addClass('elementskit-coundown-finish');
					});
			});
			$container5.each(function () {
				var hour = $(this).data('date-ekit-hour'),
					minute = $(this).data('date-ekit-minute'),
					second = $(this).data('date-ekit-second'),
					day = $(this).data('date-ekit-day'),
					week = $(this).data('date-ekit-week'),
					finalDate = $(this).data('countdown'),
					finish_title = $(this).data('finish-title'),
					finish_content = $(this).data('finish-content');

				var labelsData = { 'elementskit-wks': week, 'elementskit-days': day, 'elementskit-hrs': hour, 'elementskit-mins': minute, 'elementskit-secs': second };

				var labels = ['elementskit-wks', 'elementskit-days', 'elementskit-hrs', 'elementskit-mins', 'elementskit-secs'],

					nextYear = (new Date(finalDate)),
					template = _.template('<div class="elementskit-time <%= label %>"><span class="elementskit-count elementskit-curr elementskit-top"><%= curr %></span><span class="elementskit-count elementskit-next elementskit-top"><%= next %></span><span class="elementskit-count elementskit-next elementskit-bottom"><%= next %></span><span class="elementskit-count elementskit-curr elementskit-bottom"><%= curr %></span><span class="elementskit-label"><%= labelD.length < 6 ? labelD : labelD.substr(0, 3)  %></span></div>'),
					currDate = '00:00:00:00:00',
					nextDate = '00:00:00:00:00',
					parser = /([0-9]{2})/gi,
					$example = $container5;
				// Parse countdown string to an object
				function strfobj(str) {
					var parsed = str.match(parser),
						obj = {};
					labels.forEach(function (label, i) {
						obj[label] = parsed[i]
					});
					return obj;
				}
				// Return the time components that diffs
				function diff(obj1, obj2) {
					var diff = [];
					labels.forEach(function (key) {
						if (obj1[key] !== obj2[key]) {
							diff.push(key);
						}
					});
					return diff;
				}
				// Build the layout
				var initData = strfobj(currDate);
				labels.forEach(function (label, i) {
					$example.append(template({
						curr: initData[label],
						next: initData[label],
						label: label,
						labelD: labelsData[label]
					}));
				});
				// Starts the countdown
				$example.theFinalCountdown(nextYear, function (event) {
					var newDate = event.strftime('%w:%d:%H:%M:%S'),
						data;
					if (newDate !== nextDate) {
						currDate = nextDate;
						nextDate = newDate;
						// Setup the data
						data = {
							'curr': strfobj(currDate),
							'next': strfobj(nextDate)
						};
						// Apply the new values to each node that changed
						diff(data.curr, data.next).forEach(function (label) {
							var selector = '.%s'.replace(/%s/, label),
								$node = $example.find(selector);
							// Update the node
							$node.removeClass('elementskit-flip');
							$node.find('.elementskit-curr').text(data.curr[label]);
							$node.find('.elementskit-next').text(data.next[label]);
							// Wait for a repaint to then flip
							_.delay(function ($node) {
								$node.addClass('elementskit-flip');
							}, 50, $node);
						});
					}
				})
					.on('finish.countdown', function () {
						$(this).html(
							finish_title + "<br/>" + finish_content
						);
					});
			});

		},

		Client_Logo: function ($scope) {
			var $log_carosel = $scope.find('.elementskit-clients-slider');
			$log_carosel.each(function () {
				// //console.log($(this).data('right_icon'));
				var leftArrow = '<button type="button" class="slick-prev"><i class="icon icon-left-arrow2"></i></button>';

				var rightArrow = '<button type="button" class="slick-next"><i class="icon icon-right-arrow2"></i></button>';

				var slidestoshowtablet = $(this).data('slidestoshowtablet');
				var slidestoscroll_tablet = $(this).data('slidestoscroll_tablet');
				var slidestoshowmobile = $(this).data('slidestoshowmobile');
				var slidestoscroll_mobile = $(this).data('slidestoscroll_mobile');
				var arrow = $(this).data('show_arrow') === 'yes' ? true : false;
				var dot = $(this).data('show_dot') === 'yes' ? true : false;
				var autoPlay = $(this).data('autoplay') === 'yes' ? true : false;
				var centerMode = $(this).data('data-center_mode') === 'yes' ? true : false;

				$(this).not('.slick-initialized').slick({
					slidesToShow: ($(this).data('slidestoshow') !== 'undefined') ? $(this).data('slidestoshow') : 4,
					slidesToScroll: ($(this).data('slidestoscroll') !== 'undefined') ? $(this).data('slidestoscroll') : 4,
					autoplay: ($(this).data('autoplay') !== 'undefined') ? autoPlay : true,
					autoplaySpeed: ($(this).data('speed') !== 'undefined') ? $(this).data('speed') : 1000,
					arrows: ($(this).data('show_arrow') !== 'undefined') ? arrow : true,
					dots: ($(this).data('show_dot') !== 'undefined') ? dot : true,
					pauseOnHover: ($(this).data('pause_on_hover') == 'yes') ? true : false,
					prevArrow: ($(this).data('left_icon') !== 'undefined') ? '<button type="button" class="slick-prev"><i class="' + $(this).data('left_icon') + '"></i></button>' : leftArrow,
					nextArrow: ($(this).data('right_icon') !== 'undefined') ? '<button type="button" class="slick-next"><i class="' + $(this).data('right_icon') + '"></i></button>' : rightArrow,
					rows: ($(this).data('rows') !== 'undefined') ? $(this).data('rows') : 1,
					vertical: ($(this).data('vertical_style') == 'yes') ? true : false,
					infinite: ($(this).data('autoplay') !== 'undefined') ? autoPlay : true,
					responsive: [{
						breakpoint: 1024,
						settings: {
							slidesToShow: slidestoshowtablet,
							slidesToScroll: slidestoscroll_tablet,
						}
					},
					{
						breakpoint: 600,
						settings: {
							slidesToShow: slidestoshowtablet,
							slidesToScroll: slidestoscroll_tablet
						}
					},
					{
						breakpoint: 480,
						settings: {
							arrows: false,
							slidesToShow: slidestoshowmobile,
							slidesToScroll: slidestoscroll_mobile
						}
					}
					]

				});

			});
		},

		Testimonial_Slider: function ($scope) {
			var $testimonial_slider = $scope.find('.elementskit-testimonial-slider');
			$testimonial_slider.each(function () {
				var leftArrow = '<button type="button" class="slick-prev"><i class="icon icon-left-arrow2"></i></button>';
				var rightArrow = '<button type="button" class="slick-next"><i class="icon icon-right-arrow2"></i></button>';

				var slidestoshowtablet = $(this).data('slidestoshowtablet');
				var slidestoscroll_tablet = $(this).data('slidestoscroll_tablet');
				var slidestoshowmobile = $(this).data('slidestoshowmobile');
				var slidestoscroll_mobile = $(this).data('slidestoscroll_mobile');
				var arrow = $(this).data('show_arrow') === 'yes' ? true : false;
				var dot = $(this).data('show_dot') === 'yes' ? true : false;
				var autoPlay = $(this).data('autoplay') === 'yes' ? true : false;
				// var centerMode = $(this).data('data-center_mode') === 'yes' ? true : false;


				$(this).not('.slick-initialized').slick({
					slidesToShow: ($(this).data('slidestoshow') !== 'undefined') ? $(this).data('slidestoshow') : 1,
					slidesToScroll: ($(this).data('slidestoscroll') !== 'undefined') ? $(this).data('slidestoscroll') : 1,
					autoplay: ($(this).data('autoplay') !== 'undefined') ? autoPlay : true,
					autoplaySpeed: ($(this).data('speed') !== 'undefined') ? $(this).data('speed') : 1000,
					arrows: ($(this).data('show_arrow') !== 'undefined') ? arrow : true,
					dots: ($(this).data('show_dot') !== 'undefined') ? dot : true,
					pauseOnHover: ($(this).data('pause_on_hover') == 'yes') ? true : false,
					prevArrow: ($(this).data('left_icon') !== 'undefined') ? '<button type="button" class="slick-prev"><i class="' + $(this).data('left_icon') + '"></i></button>' : leftArrow,
					nextArrow: ($(this).data('right_icon') !== 'undefined') ? '<button type="button" class="slick-next"><i class="' + $(this).data('right_icon') + '"></i></button>' : rightArrow,
					// rows: ($(this).data('rows') !== 'undefined') ? $(this).data('rows') : 1,
					vertical: ($(this).data('vertical_style') == 'yes') ? true : false,
					infinite: ($(this).data('autoplay') !== 'undefined') ? autoPlay : true,
					responsive: [{
						breakpoint: 1024,
						settings: {
							slidesToShow: slidestoshowtablet,
							slidesToScroll: slidestoscroll_tablet,
						}
					},
					{
						breakpoint: 600,
						settings: {
							slidesToShow: slidestoshowtablet,
							slidesToScroll: slidestoscroll_tablet
						}
					},
					{
						breakpoint: 480,
						settings: {
							arrows: false,
							slidesToShow: slidestoshowmobile,
							slidesToScroll: slidestoscroll_mobile
						}
					}
					]
				});

			});
		},

		Image_Comparison: function ($scope) {

			var $image_comparison_container = $scope.find('.image-comparison-container');
			var $image_comparison_container_vertical = $scope.find('.image-comparison-container-vertical');


			var $this = $image_comparison_container,
				offset = $this.data('offset'),
				overlay = $this.data('overlay'),
				label_before = $this.data('label_before'),
				label_after = $this.data('label_after'),
				move_with_handle_only = $this.data('move_with_handle_only'),
				move_slider_on_hover = $this.data('move_slider_on_hover'),
				click_to_move = $this.data('click_to_move');



			$image_comparison_container.twentytwenty({
				before_label: label_before, // Set a custom before label
				after_label: label_after, // Set a custom after label
				default_offset_pct: offset, // How much of the before image is visible when the page loads
				no_overlay: overlay, //Do not show the overlay with before and after
				move_slider_on_hover: move_slider_on_hover, // Move slider on mouse hover?
				move_with_handle_only: move_with_handle_only, // Allow a user to swipe anywhere on the image to control slider movement.
				click_to_move: click_to_move // Allow a user to click (or tap) anywhere on the image to move the slider to that location.
			});

			var $this = $image_comparison_container_vertical,
				offset = $this.data('offset'),
				overlay = $this.data('overlay'),
				label_before = $this.data('label_before'),
				label_after = $this.data('label_after'),
				move_slider_on_hover = $this.data('move_slider_on_hover'),
				click_to_move = $this.data('click_to_move');


			$image_comparison_container_vertical.twentytwenty({
				orientation: 'vertical',
				before_label: label_before, // Set a custom before label
				after_label: label_after, // Set a custom after label
				default_offset_pct: offset, // How much of the before image is visible when the page loads
				no_overlay: overlay, //Do not show the overlay with before and after
				move_slider_on_hover: move_slider_on_hover, // Move slider on mouse hover?
				move_with_handle_only: move_with_handle_only, // Allow a user to swipe anywhere on the image to control slider movement.
				click_to_move: click_to_move // Allow a user to click (or tap) anywhere on the image to move the slider to that location.

			});


		},
		Piechart: function ($scope) {
			var colorfulchart = $scope.find('.colorful-chart');

			//console.log(colorfulchart);

			if (colorfulchart.length > 0) {

				colorfulchart.each(function (__, e) {
					var myColors = $(e).data('color');
					var datalineWidth = $(e).data('linewidth');
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
						};

					} else {
						obj = {
							lineWidth: datalineWidth,
							barColor: myColors,
							trackColor: barbg,
						};
					}

					$(e).myChart(obj);
				})
			}

		},
		Gallery: function ($scope) {
			var $container = $scope.find('.ekit_gallery_grid');
			var column = $container.data('gallerycol');
			// console.log((parseInt(column.tablet, 10)));
			if ($container.length > 0) {
				var colWidth = function colWidth() {
					var w = $container.width(),
						columnNum,
						columnWidth = 0;
					if (w > 1024) {
						columnNum = parseInt(column.desktop, 10);
					} else if (w > 768) {
						columnNum = parseInt(column.tablet, 10);
					}
					columnWidth = Math.floor(w / columnNum);
					$container.find('.ekit_gallery_grid_item').each(function () {
						var $item = $(this),
							multiplier_w = $item.attr('class').match(/ekit_gallery_grid_item-w(\d)/),
							width = multiplier_w ? columnWidth * multiplier_w[1] : columnWidth;
						$item.css({
							width: width,
						});
					});
					return columnWidth;
				},
					isotope = function isotope() {
						$container.isotope({
							resizable: false,
							itemSelector: '.ekit_gallery_grid_item',
							masonry: {
								columnWidth: colWidth(),
								gutterWidth: 0
							}
						});
					};
				isotope();
				$(window).on('resize load', isotope);
				var $optionSets = $scope.find('.filter-button-wraper .option-set'),
					$optionLinks = $optionSets.find('a');
				$optionLinks.on('click', function () {
					var $this = $(this);
					var $optionSet = $this.parents('.option-set');
					$optionSet.find('.selected').removeClass('selected');
					$this.addClass('selected');
					// make option object dynamically, i.e. { filter: '.my-filter-class' }
					var options = {},
						key = $optionSet.attr('data-option-key'),
						value = $this.attr('data-option-value');

					// parse 'false' as false boolean
					value = value === 'false' ? false : value;
					options[key] = value;
					if (key === 'layoutMode' && typeof changeLayoutMode === 'function') {
						// changes in layout modes need extra logic
						changeLayoutMode($this, options);
					} else {
						// creativewise, apply new options
						$container.isotope(options);
					}
					return false;
				});
			}
			// tilt
			var tiltContainer = $scope.find('.ekit-gallery-portfolio-tilt'),
				glare = $(tiltContainer).data('tilt-glare') === 'yes' ? true : false;
			$(tiltContainer).tilt({
				easing: "cubic-bezier(.03,.98,.52,.99)",
				transition: true,
				glare: glare,
			})
		},
		MotionText: function ($scope) {
			var texts = $scope.find('.ekit_char_based .ekit_motion_text');
			texts.each(function () {
				var text = $(this);
				for (let i = 0; i < text.length; i++) {
					var $this = text[i];
					var content = $this.innerHTML;
					content = content.trim();
					var str = '';
					var delay = parseInt(text.attr('ekit-animation-delay')),
						delayIncrement = delay;

					//console.log(delay);

					for (let l = 0; l < content.length; l++) {
						if (content[l] != '') {
							str += `<span class="ekit-letter" style="animation-delay:${delay}ms; -moz-animation-delay:${delay}ms; -webkit-animation-delay:${delay}ms;">${content[l]}</span>`;
							delay += delayIncrement;
						} else {
							str += content[i];
						}
					}
					$this.innerHTML = str;
				}
			});
		},

		TimeLine: function ($scope) {

			var horizantalTimeline = $scope.find('.horizantal-timeline');

			if (horizantalTimeline.length > 0) {
				horizantalTimeline.find('.content-group').each(function (__, e) {
					$(e).on('mouseenter', function () {
						if ($(e).parents('.single-timeline').hasClass('hover')) {
							$(e).parents('.single-timeline').removeClass('hover')
						} else {
							$(e).parents('.single-timeline').addClass('hover')
							$(e).parents('.single-timeline').nextAll().removeClass('hover')
							$(e).parents('.single-timeline').prevAll().removeClass('hover')
						}
					})
				})
			}
		},

		PostTab: function ($scope) {
			if ($scope.find('.hover--active').length > 0) {
				var event_type = $scope.find('.hover--active').attr('data-post-tab-event');
				$scope.find('.hover--active').tab({
					trigger_event_type: event_type
				});
			}
		},
        Hotspot: function ($scope) {
            if ($scope.find('[data-toggle="tooltip"]').length > 0) {
                var event_type = $scope.find('[data-toggle="tooltip"]');
                event_type.tooltip();
            }
        }
       ,
		Header_Search: function ($scope) {
			if ($scope.find('.ekit-modal-popup').length > 0) {
				$scope.find('.ekit-modal-popup').magnificPopup({
					type: 'inline',
					fixedContentPos: false,
					fixedBgPos: true,
					overflowY: 'auto',
					closeBtnInside: false,
					callbacks: {
						beforeOpen: function () {
							this.st.mainClass = "my-mfp-slide-bottom ekit-promo-popup";
						}
					}
				});
			}
		},

		Header_Off_Canvas: function ($scope) {
			if ($scope.find('.ekit-sidebar-group').length > 0) {
				$scope.find('.ekit_offcanvas-sidebar').on('click', function (e) {
					e.preventDefault();
					e.stopPropagation();
					$scope.find('.ekit-sidebar-group').addClass('ekit_isActive');
				});
				$scope.find('.ekit_close-side-widget').on('click', function (e) {
					e.preventDefault();
					$scope.find('.ekit-sidebar-group').removeClass('ekit_isActive');
				});
				$('body').on('click', function (e) {
					$scope.find('.ekit-sidebar-group').removeClass('ekit_isActive');
				});
				$scope.find('.ekit-sidebar-widget').on('click', function (e) {
					e.stopPropagation();
				});
			}
		}
	};
	$(window).on('elementor/frontend/init', Elementskit.init);

	var EkitStickyHandler = elementorFrontend.Module.extend({

		bindEvents: function bindEvents() {
			elementorFrontend.addListenerOnce(this.getUniqueHandlerID() + 'ekit_sticky', 'resize', this.run);
		},
	
		unbindEvents: function unbindEvents() {
			elementorFrontend.removeListeners(this.getUniqueHandlerID() + 'ekit_sticky', 'resize', this.run);
		},
	
		isActive: function isActive() {
			return undefined !== this.$element.data('ekit_sticky');
		},
	
		activate: function activate() {
			var elementSettings = this.getElementSettings(),
				stickyOptions = {
				to: elementSettings.ekit_sticky,
				offset: elementSettings.ekit_sticky_offset.size,
				effectsOffset: elementSettings.ekit_sticky_effect_offset.size,
				classes: {
					sticky: 'ekit-sticky',
					stickyActive: 'ekit-sticky--active ekit-section--handles-inside',
					stickyEffects: 'ekit-sticky--effects',
					spacer: 'ekit-sticky__spacer'
				}
			},
				$wpAdminBar = elementorFrontend.getElements('$wpAdminBar');
	
			if (elementSettings.ekit_sticky_parent) {
				stickyOptions.parent = '.ekit-widget-wrap';
			}
	
			if ($wpAdminBar.length && 'top' === elementSettings.ekit_sticky && 'fixed' === $wpAdminBar.css('position')) {
				stickyOptions.offset += $wpAdminBar.height();
			}
	
			this.$element.ekit_sticky(stickyOptions);
		},
	
		deactivate: function deactivate() {
			if (!this.isActive()) {
				return;
			}
	
			this.$element.ekit_sticky('destroy');
		},
	
		run: function run(refresh) {
			if (!this.getElementSettings('ekit_sticky')) {
				this.deactivate();
	
				return;
			}
	
			var currentDeviceMode = elementorFrontend.getCurrentDeviceMode(),
				activeDevices = this.getElementSettings('ekit_sticky_on');
	
			if (-1 !== activeDevices.indexOf(currentDeviceMode)) {
				if (true === refresh) {
					this.reactivate();
				} else if (!this.isActive()) {
					this.activate();
				}
			} else {
				this.deactivate();
			}
		},
	
		reactivate: function reactivate() {
			this.deactivate();
	
			this.activate();
		},
	
		onElementChange: function onElementChange(settingKey) {
			if (-1 !== ['ekit_sticky', 'ekit_sticky_on'].indexOf(settingKey)) {
				this.run(true);
			}
	
			if (-1 !== ['ekit_sticky_offset', 'ekit_sticky_effects_offset', 'ekit_sticky_parent'].indexOf(settingKey)) {
				this.reactivate();
			}
		},
	
		onInit: function onInit() {
			elementorFrontend.Module.prototype.onInit.apply(this, arguments);
	
			this.run();
		},
	
		onDestroy: function onDestroy() {
			elementorFrontend.Module.prototype.onDestroy.apply(this, arguments);
	
			this.deactivate();
		}
	});
}(jQuery, window.elementorFrontend));