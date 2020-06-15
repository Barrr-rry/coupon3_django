/**
 * ResponsiveMenu
 * HeaderFixed
 * SlideTeam
 * SearchButton
 * CountDown
 * GoogleMap
 * SlideSearch
 * LoadMore
 * LoadMore_s2
 * LoadMore_s3
 * LoadMore_s4
 * LoadMore_comment
 * Parallax
 * GoTop
 * RemovePreloader
 */

;(function ($) {

  'use strict'
  var isMobile = {
    Android: function () {
      return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function () {
      return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function () {
      return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function () {
      return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function () {
      return navigator.userAgent.match(/IEMobile/i);
    },
    any: function () {
      return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
    }
  }; // is Mobile

  var responsiveMenu = function () {
    var menuType = 'desktop';

    $(window).on('load resize', function () {
      var currMenuType = 'desktop';

      if (matchMedia('only screen and (max-width: 991px)').matches) {
        currMenuType = 'mobile';
      }

      if (currMenuType !== menuType) {
        menuType = currMenuType;

        if (currMenuType === 'mobile') {
          var $mobileMenu = $('#mainnav').attr('id', 'mainnav-mobi').hide();
          var hasChildMenu = $('#mainnav-mobi').find('li:has(ul)');

          $('.header').after($mobileMenu);
          hasChildMenu.children('ul').hide();
          hasChildMenu.children('a').after('<span class="btn-submenu"></span>');
          $('.btn-menu').removeClass('active');
        } else {
          var $desktopMenu = $('#mainnav-mobi').attr('id', 'mainnav').removeAttr('style');

          $desktopMenu.find('.submenu').removeAttr('style');
          $('.header').find('.button-header').before($desktopMenu);
          $('.btn-submenu').remove();
        }
      }
    });

    $('.btn-menu').on('click', function () {
      $('#mainnav-mobi').slideToggle(300);
      $(this).toggleClass('active');
      return false;
    });

    $(document).on('click', '#mainnav-mobi li .btn-submenu', function (e) {
      $(this).toggleClass('active').next('ul').slideToggle(300);
      e.stopImmediatePropagation();
      return false;
    });
  }; // Responsive Menu

  var headerFixed = function () {
    if ($('body').hasClass('header_sticky')) {
      var nav = $('.header');
      if (nav.size() != 0) {

        var offsetTop = $('.header').offset().top,
          headerHeight = $('.header').height(),
          injectSpace = $('<div />', {height: headerHeight}).insertAfter(nav);
        injectSpace.hide();

        $(window).on('load scroll', function () {
          if ($(window).scrollTop() > offsetTop + 100) {
            injectSpace.show();
            $('.header').addClass('downscrolled');

          } else {
            $('.header').removeClass('downscrolled');
            injectSpace.hide();
          }

          if ($(window).scrollTop() > 500) {
            $('.header').addClass('upscrolled');
          } else {
            $('.header').removeClass('upscrolled');
          }
        })
      }
    }
  }; // Header Fixed

  var slideTeam = function () {
    $(".owl-carousel").owlCarousel({
      autoplay: true,
      dots: false,
      nav: true,
      margin: 27,
      loop: true,
      items: 4,
      responsive: {
        0: {
          items: 1
        },

        479: {
          items: 2
        },
        768: {
          items: 3
        },
        991: {
          items: 4
        },
        1200: {
          items: 4
        }
      }
    });
  }; // Slide Team

  var searchButton = function () {
    var showsearch = $('.show-search button');
    showsearch.on('click', function () {
      $('.show-search .top-search').toggleClass('active');
      showsearch.toggleClass('active');
      if (showsearch.hasClass('active')) {
        $(this).children('span').removeClass('ti-search');
        showsearch.children('span').addClass('ti-close');
      } else {
        showsearch.removeClass('active');
        $(this).children('span').addClass('ti-search');
        $(this).children('span').removeClass('ti-close');
      }
    });
  }; // Search Button

  var CountDown = function () {
    var before = '<div class="square"><div class="numb">',
      textday = '</div><div class="text">/ DAY',
      texthour = '</div><div class="text">/ HOURS',
      textmin = '</div><div class="text">/ MINS',
      textsec = '</div><div class="text">/ SECS';
    if ($().countdown) {
      $(".countdown").countdown('2017/09/17', function (event) {
        $(this).html(event.strftime(before + '%D' + textday + '</div></div>' + before + '%H' + texthour + '</div></div>' + before + '%M' + textmin + '</div></div>' + before + '%S' + textsec + '</div>'));
      });
    }
  }; // Count Down

  var filterToggle = function () {
    $('.filter').each(function () {
      $(this).find('.filter-title').children('.ti-angle-down').on('click', function () {
        $(this).closest('.filter').children('.select-filter').slideToggle(400);
      });
    });
  }; // Filter Toggle

  var googleMap = function () {
    var data = JSON.parse('[{"address":"8/178 Nguyễn Lương Bằng, Quang Trung, Đống Đa, Hà Nội, Việt Nam","content":"","status":"live"},{"address":"ngõ 19 phố Trần Quang Diệu, Ô Chợ Dừa, Đống Đa, Hà Nội, Việt Nam","content":""},{"address":"The Life School, Tầng 6, nhà D1, ngõ, 161 Nguyễn Lương Bằng, Quang Trung, Đống Đa, Hà Nội, Việt Nam","content":""}]');
    var data1 = JSON.parse('[{"address1":"3818 Fort Hamilton Pkwy, Brooklyn, NY 11218","content":"","status":"live"},{"address2":"Brooklyn, Tiểu bang New York 11230","content":""}]');
    var data2 = JSON.parse('[{"address":"84 Trần Quang Diệu, Ô Chợ Dừa, Đống Đa, Hà Nội, Việt Nam","content":"","status":"live"}]');
    var data3 = JSON.parse('[{"address":"Thành phố New York, Tiểu bang New York","content":""}]');
    var data4 = JSON.parse('[{"address":"8/178 Nguyễn Lương Bằng, Chợ Dừa, Đống Đa, Hà Nội, Việt Nam","content":""}]');

    // Gmap Defaults
    $('.map').gmap3({
      map: {
        options: {
          center: [21.016760, 105.826886],
          mapTypeId: 'themesflat_style',
          mapTypeControlOptions: {
            mapTypeIds: ['themesflat_style', google.maps.MapTypeId.SATELLITE, google.maps.MapTypeId.HYBRID]
          },
          zoom: 17
        },
        navigationControl: true,
        scrollwheel: false,
        streetViewControl: true
      }
    });

    $('.map-1').gmap3({
      map: {
        options: {
          center: [40.636429, -73.980047],
          zoom: 14
        }
      }
    });

    $('.map-2').gmap3({
      map: {
        options: {
          center: [21.015396, 105.824299],
          mapTypeId: 'themesflat_style',
          mapTypeControlOptions: {
            mapTypeIds: ['themesflat_style', google.maps.MapTypeId.SATELLITE, google.maps.MapTypeId.HYBRID]
          },
          zoom: 17,
          animation: google.maps.Animation.BOUNCE
        },
        navigationControl: true,
        scrollwheel: false,
        streetViewControl: true
      }
    });

    $('.map-3').gmap3({
      map: {
        options: {
          center: [40.719625, -74.004715],
          mapTypeId: 'themesflat_style',
          mapTypeControlOptions: {
            mapTypeIds: ['themesflat_style', google.maps.MapTypeId.SATELLITE, google.maps.MapTypeId.HYBRID]
          },
          zoom: 13
        }
      }
    });

    $('.map-4').gmap3({
      map: {
        options: {
          center: [21.017114, 105.826939],
          mapTypeId: 'themesflat_style',
          mapTypeControlOptions: {
            mapTypeIds: ['themesflat_style', google.maps.MapTypeId.SATELLITE, google.maps.MapTypeId.HYBRID]
          },
          zoom: 17
        }
      }
    });

    // Json Loop
    $.each(data, function (key, val) {
      $('.map').gmap3({
        marker: {
          values: [{
            address: val.address,
            options: {icon: "images/icon/map.png"},
            events: {
              mouseover: function () {
                $(this).gmap3({
                  overlay: {
                    address: val.address,
                    options: {
                      content: "<div class='infobox style2'><div class='img-box'><img src='images/icon/icon-map-01.png'></div><div class='text'><h3>AN Restaurant</h3><p>2/51 Hoang Cau Street,<br />Ha Noi, Viet Nam</p></div><div class='clearfix'></div></div>",
                      offset: {
                        y: -200,
                        x: -115
                      }
                    }
                  }
                });
              },
              mouseout: function () {
                $('.infobox').each(function () {
                  $(this).remove();
                });
              }
            }
          }]
        },
        styledmaptype: {
          id: "themesflat_style",
          options: {
            name: "Themesflat Map"
          },
          styles: [
            {
              "featureType": "administrative",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "landscape",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#efebe2"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "all",
              "stylers": [
                {
                  "saturation": -100
                },
                {
                  "lightness": 45
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "simplified"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.icon",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "administrative.locality",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#bad294"
                },
                {
                  "visibility": "on"
                }
              ]
            },
            {
              "featureType": "transit",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#a5d7e0"
                },
                {
                  "visibility": "on"
                }
              ]
            }
          ]
        }
      });
    });

    $.each(data1, function (key, val) {
      $('.map-1').gmap3({
        marker: {
          values: [{
            address: val.address1,
            options: {icon: "images/icon/map-02.png"}
          },
            {
              address: val.address2,
              options: {icon: "images/icon/map-03.png"}
            }]
        },
        styledmaptype: {
          id: "themesflat_style",
          options: {
            name: "Themesflat Map"
          },
          styles: [
            {
              "featureType": "administrative",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "landscape",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#efebe2"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "all",
              "stylers": [
                {
                  "saturation": -100
                },
                {
                  "lightness": 45
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "simplified"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.icon",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "administrative.locality",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#bad294"
                },
                {
                  "visibility": "on"
                }
              ]
            },
            {
              "featureType": "transit",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#a5d7e0"
                },
                {
                  "visibility": "on"
                }
              ]
            }
          ]
        }
      });
    });

    // Json Loop
    $.each(data2, function (key, val) {
      $('.map-2').gmap3({
        marker: {
          values: [{
            address: val.address,
            options: {icon: "images/icon/map.png"},
            events: {
              mouseover: function () {
                $(this).gmap3({
                  overlay: {
                    address: val.address,
                    options: {
                      content: "<div class='infobox'><div class='logo'>D</div><div class='text'><h3>Dailist</h3><p>31 Ven HoVan Chuong Street,<br />Ha Noi, Viet Nam</p></div><div class='clearfix'></div></div>",
                      offset: {
                        y: -200,
                        x: -115
                      }
                    }
                  }
                });
              },
              mouseout: function () {
                $('.infobox').each(function () {
                  $(this).remove();
                });
              }
            }
          }]
        },
        styledmaptype: {
          id: "themesflat_style",
          options: {
            name: "Themesflat Map"
          },
          styles: [
            {
              "featureType": "administrative",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "landscape",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#efebe2"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#2c3e50"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "all",
              "stylers": [
                {
                  "saturation": -100
                },
                {
                  "lightness": 45
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "simplified"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.icon",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#2c3e50"
                }
              ]
            },
            {
              "featureType": "administrative.locality",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#bad294"
                },
                {
                  "visibility": "on"
                }
              ]
            },
            {
              "featureType": "transit",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#a5d7e0"
                },
                {
                  "visibility": "on"
                }
              ]
            }
          ]
        }
      });
    });

    // Json Loop
    $.each(data3, function (key, val) {
      $('.map-3').gmap3({
        styledmaptype: {
          id: "themesflat_style",
          options: {
            name: "Themesflat Map"
          },
          styles: [
            {
              "featureType": "administrative",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "landscape",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#efebe2"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "all",
              "stylers": [
                {
                  "saturation": -100
                },
                {
                  "lightness": 45
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "simplified"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.icon",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "administrative.locality",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "visibility": "on"
                },
                {
                  "color": "#222222"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#bad294"
                },
                {
                  "visibility": "on"
                }
              ]
            },
            {
              "featureType": "transit",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#a5d7e0"
                },
                {
                  "visibility": "on"
                }
              ]
            }
          ]
        }
      });
    });

    // Json Loop
    $.each(data4, function (key, val) {
      $('.map-4').gmap3({
        marker: {
          values: [{
            address: val.address,
            options: {icon: "images/icon/map.png"},
            events: {
              mouseover: function () {
                $(this).gmap3({
                  overlay: {
                    address: val.address,
                    options: {
                      content: "<div class='infobox style2'><div class='img-box'><img src='images/icon/icon-map-01.png'></div><div class='text'><h3>AN Restaurant</h3><p>2/51 Hoang Cau Street,<br />Ha Noi, Viet Nam</p></div><div class='clearfix'></div></div>",
                      offset: {
                        y: -200,
                        x: -115
                      }
                    }
                  }
                });
              },
              mouseout: function () {
                $('.infobox').each(function () {
                  $(this).remove();
                });
              }
            }
          }]
        },
        styledmaptype: {
          id: "themesflat_style",
          options: {
            name: "Themesflat Map"
          },
          styles: [
            {
              "featureType": "administrative",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "landscape",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#efebe2"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#2c3e50"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "all",
              "stylers": [
                {
                  "saturation": -100
                },
                {
                  "lightness": 45
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "simplified"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.icon",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#ffffff"
                }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#2c3e50"
                }
              ]
            },
            {
              "featureType": "administrative.locality",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#bad294"
                },
                {
                  "visibility": "on"
                }
              ]
            },
            {
              "featureType": "transit",
              "elementType": "all",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "all",
              "stylers": [
                {
                  "color": "#a5d7e0"
                },
                {
                  "visibility": "on"
                }
              ]
            }
          ]
        }
      });
    });

    // Function Clear Markers
    function gmap_clear_markers() {
      $('.infobox').each(function () {
        $(this).slideToggle(400).remove();
      });
    }
  }; // Google Map

  var slideSearch = function () {
    if ($('body').hasClass('slider')) {
      $("#ex8").slider({
        tooltip: 'always'
      });

      // Without JQuery
      var slider = new Slider("#ex8", {
        tooltip: 'always'
      });
    }
  }; // Slide Search

  var loadMore = function () {
    $(".wrap-imagebox.style1 .imagebox.style3").slice(0, 4).show();
    $(".wrap-imagebox.style1 .btn-more").on('click', function (e) {
      e.preventDefault();
      $(".wrap-imagebox.style1 .imagebox.style3:hidden").slice(0, 2).slideDown(600);
      if ($(".wrap-imagebox.style1 .imagebox.style3:hidden").length == 0) {
        $(".wrap-imagebox.style1 .btn-more").fadeOut('slow');
      }
      $('html,body').animate({
        scrollTop: $(this).offset().top - 150
      }, 1000);
    });
  }; // Load More

  var loadMore_s2 = function () {
    $(".wrap-imagebox.style2 .imagebox.style4").slice(0, 4).show();
    $(".wrap-imagebox.style2 .btn-more").on('click', function (e) {
      e.preventDefault();
      $(".wrap-imagebox.style2 .imagebox.style4:hidden").slice(0, 2).slideDown(600);
      if ($(".wrap-imagebox.style2 .imagebox.style4:hidden").length == 0) {
        $(".wrap-imagebox.style2 .btn-more").fadeOut('slow');
      }
      $('html,body').animate({
        scrollTop: $(this).offset().top - 150
      }, 1000);
    });
  }; // Load More S2

  var loadMore_s3 = function () {
    $(".wrap-imagebox.style3 .imagebox.style1").slice(0, 6).show();
    $(".wrap-imagebox.style3 .btn-more").on('click', function (e) {
      e.preventDefault();
      $(".wrap-imagebox.style3 .imagebox.style1:hidden").slice(0, 2).slideDown(600);
      if ($(".wrap-imagebox.style3 .imagebox.style1:hidden").length == 0) {
        $(".wrap-imagebox.style3 .btn-more").fadeOut('slow');
      }
      $('html,body').animate({
        scrollTop: $(this).offset().top - 150
      }, 1000);
    });
  }; // Load More S3

  var loadMore_s4 = function () {
    $(".wrap-imagebox.style3 .imagebox.style2").slice(0, 3).show();
    $(".wrap-imagebox.style3 .btn-more").on('click', function (e) {
      e.preventDefault();
      $(".wrap-imagebox.style3 .imagebox.style2:hidden").slice(0, 2).slideDown(600);
      if ($(".wrap-imagebox.style3 .imagebox.style2:hidden").length == 0) {
        $(".wrap-imagebox.style3 .btn-more").fadeOut('slow');
      }
      $('html,body').animate({
        scrollTop: $(this).offset().top - 150
      }, 1000);
    });
  }; // Load More S4

  var loadMore_comment = function () {
    $(".comment-area .comment-list .comment").slice(0, 2).show();
    $(".comment-area .load-more").on('click', function (e) {
      e.preventDefault();
      $(".comment-area .comment-list .comment:hidden").slice(0, 2).slideDown(600);
      if ($(".comment-area .comment-list .comment:hidden").length == 0) {
        $(".comment-area .load-more").fadeOut('slow');
      }
      $('html,body').animate({
        scrollTop: $(this).offset().top - 100
      }, 1000);
    });
  }; // Load More Comment

  var parallax = function () {
    if ($().parallax && isMobile.any() == null) {
      $('.parallax1').parallax("50%", 0.5);
    }
  }; // Parallax

  var goTop = function () {
    var gotop = $('.go-top');
    $(window).scroll(function () {
      if ($(this).scrollTop() > 500) {
        gotop.addClass('show');
      } else {
        gotop.removeClass('show');
      }
    });
    gotop.on('click', function () {
      $('html, body').animate({scrollTop: 0}, 800, 'easeInOutExpo');
      return false;
    });
  }; // Go Top

  var removePreloader = function () {
    $(window).load(function () {
      setTimeout(function () {
          $('.preloader').hide();
        }, 500
      );
    });
  }; // Remove Preloader

  let formSerailize = (data) => {
    let ret = {}
    for (let el of data) {
      if (ret.hasOwnProperty(el.name)) {
        let temp = ret[el.name]
        if (!Array.isArray(temp)) {
          temp = [temp]
        }
        temp.push(el.value)
        ret[el.name] = temp
      } else {
        ret[el.name] = el.value
      }
    }
    return ret
  }

  let storeCreatePage = () => {
    let files = []
    let discount_id = 0
    let discount_type_list = []
    $.ajax({
      url: '/api/discounttype/',
      method: 'get'
    }).done(res => {
      discount_type_list = res
    })

    // 活動折扣
    let appendDiscount = () => {
      discount_id += 1
      let options = ''
      for (let el of discount_type_list) {
        options += `<option value="${el.id}">${el.name}</option>`
      }
      $('.store-disocunt-area').append(`
      <div class="store-discount d-flex" data-id="${discount_id}">
        <div class="store-discount-content col">
          <div class="wrap-listing your-name">
            <label>活動名稱</label>
            <input type="text" name="store_discount_name" placeholder="請輸入活動名稱（20個字內）">
            <label>活動類型</label>
            <select name="discount_type" placeholder="請選擇活動類型">
              ${options}
            </select>
          </div><!-- /.wrap-listing -->
          <div class="wrap-listing your-name">
            <label>活動內容</label>
            <textarea rows="4" cols="5" name="description" placeholder="請輸入活動內容與注意事項"></textarea>
          </div><!-- /.wrap-listing -->
        </div>
        <div class="col-auto d-flex align-items-center">
        <i class="fa fa-times pointer close-image" aria-hidden="true"
        data-id="${discount_id}"
        ></i>
        </div>
      </div>
      `)
    }
    $('.store-discount-btn').on('click', () => {
      appendDiscount()
      $('.close-image').off('click')
      $('.close-image').on('click', function () {
        let _id = $(this).attr('data-id')
        $(`.store-discount[data-id=${_id}]`).remove()
      })

    })

    // image
    let appendImage = (res) => {
      $('.upload-images').append(`
        <div class="imgbox d-flex align-items-start" data-id="${res.id}">
          <img src="/media/${res.filename}" alt="">
          <i class="fa fa-times pointer close-image" aria-hidden="true"
          data-id="${res.id}"
          ></i>
        </div>
        `)
    }
    let setImageClick = () => {
      $('.close-image').off('click')
      $('.close-image').on('click', function () {
        let _id = $(this).attr('data-id')
        $(`.imgbox[data-id="${_id}"]`).remove()
        files = files.filter(x => parseInt(x.id) !== parseInt(_id))
      })
    }
    $('input[name="upload-file"]').change((e) => {
      let form = new FormData()
      form.append("file", e.target.files[0])
      $.ajax({
        method: 'POST',
        url: '/api/file/',
        processData: false,
        data: form,
        contentType: false, //required
      }).done((res) => {
        files.push(res)
        appendImage(res)
        setImageClick()
      })
    })
    $("#createStore").validate({
      rules: {
        name: "required",
        address: "required",
        phone: "required",
        store_discount_name: "required",
      },
      messages: {
        name: "請输入商家名字",
        address: "請输入地址",
        phone: "請输入電話",
        store_discount_name: "請输入活動名稱",
      },
      submitHandler(form) {
        let data = $(form).serializeArray()
        // let ret = {}
        let ret = {
          ...(formSerailize(data)),
          county: 1,
          district: 1,
          latitude: 0.23,
          longitude: 0.22
        }
        let storediscount = []
        if (ret.store_discount_name) {
          if (Array.isArray(ret.store_discount_name)) {
            for (let i = 0; i < ret.store_discount_name.length; i++) {
              storediscount.push({
                name: ret.store_discount_name[i],
                description: ret.description[i],
                discount_type: ret.discount_type[i],
              })
            }
          } else {
            storediscount.push({
              name: ret.store_discount_name,
              description: ret.description,
              discount_type: ret.discount_type,
            })
          }


          delete ret.store_discount_name
          delete ret.description
          delete ret.discount_type
        }
        ret.storediscount_data = storediscount
        ret.storeimage_data = files.map(x => x.filename)
        console.log(ret)
        $.ajax({
          url: '/api/store/',
          type: "POST",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(ret),
          dataType: "json",
        }).done(res => {
          window.location.href = `/store/${res.id}/`
        })
      }
    });

  }
  let contactUs = () => {
    $('.contact-btn').on('click', (e) => {
      let data = $('.contact-form-self').serializeArray()
      let ret = formSerailize(data)
      $.ajax({
        url: '/api/contact/',
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(ret),
        dataType: "json",
      }).done(res => {
        window.location.reload()
      })
    })
  }
  let storePage = () => {
    // store activity
    $('.list-filter li').on('click', function () {
      let $self = $(this)
      let $span = $self.find('span')
      if ($span.hasClass('ti-check-box')) {
        $span.removeClass('ti-check-box')
        $span.addClass('ti-layout-width-full')
      } else {
        $span.removeClass('ti-layout-width-full')
        $span.addClass('ti-check-box')
      }
    })
    $('#search-btn').on('click', () => {
      $('#search-form')
      let data = $('#search-form').serializeArray()
      data = formSerailize(data)
      let querys = []

      for (let key in data) {
        querys.push(`${key}=${data[key]}`)
      }

      if ($('.filter li').length === $('.ti-check-box').length) {
        querys.push('storediscount_discount_type=all')
      } else {
        let ids = []
        $('.ti-check-box').each(function () {
          ids.push($(this).attr('data-id'))
        })
        if (ids.length) {
          querys.push(`storediscount_discount_type=${ids.join(',')}`)
        }
      }
      window.location.href = `/store/?${querys.join('&')}`
    })

    // add store
    let appendStore = (data) => {
      let html = `
      <div class="mb-50px col-md-4 store">
        <div class="imagebox style1">
          <div class="box-imagebox">
            <div class="box-header">
              <div class="box-image">
                <img src="/media/${data.image_1}" alt="">
                <a href="/store/${data.id}" title="">Preview</a>
                <div class="overlay"></div>
              </div>
            </div><!-- /.box-header -->
            <div class="box-content">
              <div class="box-title ad">
                <a href="/store/${data.id}" title="">${data.name}</a><i class="fa fa-check-circle" aria-hidden="true"></i>
              </div>
              <ul class="rating">
                <li>${data.county_name}</li>
                <li>${data.district_name}</li>
                <li>${data.store_type_name}</li>
              </ul>
              <div class="box-desc">
                ${data.storediscount_names}
              </div>
            </div><!-- /.box-content -->
            <ul class="location">
              <li class="address"><span class="ti-location-pin"></span>電話: ${data.phone}</li>
              <li class="closed">刪除</li>
            </ul><!-- /.location -->
          </div><!-- /.box-imagebox -->
        </div><!-- /.imagebox style1 -->
      </div><!-- /.col-md-4 -->
      `
      $('.store-box').append(html)
    }
    let filter_href = window.location.href.split('?')
    if (filter_href.length > 1) {
      $(".more-click").on('click', () => {
        let offset = $('.store').length
        $.ajax({
          url: `/api/store/?limit=6&offset=${offset}&${filter_href[1]}`,
          method: 'get'
        }).done(res => {
          for (let data of res.results) {
            appendStore(data)
          }
          // close more
          if (!res.next) {
            $(".more-click").remove()
          }
        })
      })
    } else {
      $(".more-click").on('click', () => {
        let offset = $('.store').length
        $.ajax({
          url: `/api/store/?limit=6&offset=${offset}`,
          method: 'get'
        }).done(res => {
          for (let data of res.results) {
            appendStore(data)
          }
          // close more
          if (!res.next) {
            $(".more-click").remove()
          }
        })
      })
    }
  }
  $(function () {
    responsiveMenu();
    headerFixed();
    slideTeam();
    searchButton();
    filterToggle();
    CountDown();
    // googleMap();
    slideSearch();
    loadMore();
    loadMore_s2();
    loadMore_s3();
    loadMore_s4();
    loadMore_comment();
    parallax();
    goTop();
    removePreloader();
    storeCreatePage();
    contactUs();
    storePage();
  });

})(jQuery);