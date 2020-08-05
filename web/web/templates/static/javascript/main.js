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
(function (w) {

  w.URLSearchParams = w.URLSearchParams || function (searchString) {
    var self = this;
    self.searchString = searchString;
    self.get = function (name) {
      var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(self.searchString);
      if (results == null) {
        return null;
      } else {
        return decodeURI(results[1]) || 0;
      }
    };
  }

})(window)

let _map = null

let initStoreShare = () => {
  $('.share-to').off('click')
  $('share-url').off('click')

  $('.share-to').snsShare((self) => {
    let $el = $(self)
    let msg = `快來看看${$el.attr('data-name')}用三倍券的超棒優惠！`
    return msg
  }, (self) => {
    let $el = $(self)
    let url = `${window.location.origin}/${$el.attr('data-url')}`
    return url
  })
  $('.share-url').on('click', function () {
    let $el = $(this)
    let msg = `快來看看${$el.attr('data-name')}用三倍券的超棒優惠！${window.location.origin}/${$el.attr('data-url')}`
    copy(msg)
    Swal.fire({
      text: '網址已複製',
      confirmButtonText: '確定'
    })
  })
}

// append to store
let appendStore = (data) => {
  let class_name = ''
  if ($('#map').length) {
    class_name = 'mb-50px col-lg-6 col-md-12 store'
  } else {
    class_name = 'mb-50px col-md-4 store md-100'
  }
  let li = ''
  for (let el of data.activity) {
    if (el.name) {
      li += `<span class="tag"><a data-activity="${el.id}" href="">${el.name}</a></span>`
    }
  }
  let names = ''
  let store_type_disable = ''
  let i = 0
  if (data.storediscount) {
    for (let foo of data.storediscount) {
      i += 1
      if (i <= 3 && foo.name) {
        names += `
            <div class="sale-list">
              ${foo.name}
            </div>
            `
      }
    }
    if (data.store_type != 8 && data.store_type != 12 && data.store_type != 7 && data.store_type != 11 && data.district_name) {
      store_type_disable =
        `<li><span>${data.district_name}</span></li>
                  <li>
                    <img src="/media/map_gray.svg" alt="">
                    <span>${data.distance_name}</span>
                  </li>`
    }
    else {
      store_type_disable =
          `
                  <li>
                    <img src="/media/map_gray.svg" alt="">
                    <span>${data.distance_name}</span>
                  </li>`
    }

  }
  $(document).ready(() => {
    let href_split = window.location.href.split('?')
    $('.sort a').each(function () {
      let $el = $(this)
      let sort = $el.attr('data-sort')
      let newurl = setParameters(window.location.href, {sort: sort})
      $el.attr('href', newurl)
    })


    // init active sort
    let $el = $(`a[data-sort=${sort}]`)
    $el.addClass('active')


    $('.activity a').each(function () {
      let $el = $(this)
      let activity = $el.attr('data-activity')
      let newurl = setParameters(window.location.href, {activity: activity})
      $el.attr('href', newurl)
    })


    // init active activity
    $el = $(`a[data-activity=${activity}]`)
    $el.addClass('active')


  })

  let html = `
      <div class="${class_name}">
        <div class="imagebox style1">
          <div class="box-imagebox">
            <div class="link_block">
              <a href="/store/${data.id}" class="link" target="_blank"></a>
              <div class="box-header">
                <div class="box-image">
                  <img src="/media/${data.image_1}" alt="">
                  <a title="">查看詳情</a>
                  <div class="overlay"></div>
                </div>
              </div><!-- /.box-header -->
              <div class="box-content">
                <div class="box-title ad">
                  <a href="/store/${data.id}" title="">${data.name}</a>
                </div>
                <ul class="rating">
                  ${store_type_disable}
                  <li>
                    <img src="/media/gray_${data.store_type_icon}" alt="">
                    <span>${data.store_type_name}</span>
                  </li>
                </ul>
                <div class="box-desc">
                  ${names}
                </div>
              </div><!-- /.box-content -->
            </div>
            <div class="imagebox_bottom">
              <p class="tag_block activity">
                ${li}
              </p>
              <div class="right">
                <input type="checkbox" class="checkbox" id="share_${data.id}">
                <label for="share_${data.id}" class="label entypo-export">
                  <!--                      <a href="">分享</a>-->
                  分享
                </label>
                <div class="social">
                  <ul>
                    <li class="share-to entypo-line" data-sns="line" data-name="${data.name}"
                        data-url="store/${data.id}">
                      <img src="/media/share_line.svg" alt="">
                    </li>
                    <li class="share-to entypo-facebook" data-sns="facebook" data-name="${data.name}"
                        data-url="store/${data.id}">
                      <img src="/media/share_fb.svg" alt="">
                    </li>
                    <li class="share-url entypo-url" data-name="${data.name}" data-url="store/${data.id}">
                      <img src="/media/share_url.svg" alt="">
                    </li>
                  </ul>
                </div>
              </div>
              <div class="clear"></div>
            </div>
            <!--                <ul class="location">-->
            <!--                  <li class="address"><span class="ti-location-pin"></span>電話: {{ el.phone }}</li>-->
            <!--                </ul>&lt;!&ndash; /.location &ndash;&gt;-->
          </div><!-- /.box-imagebox -->
        </div><!-- /.imagebox style1 -->
      </div>
      `
  $('.store-box').append(html)
}


let dicount_count = 0
const default_position = {
  coords: {
    latitude: '23.8523405',
    longitude: '120.9009427'
  },
  zoom: 7
}

function nativeAdCallback(nadParas) {
  // 表示目前有廣告
  if (nadParas.SHORTSUBJECT) {
    let class_name = ''
    if ($('#map').length) {
      class_name = 'mb-50px col-lg-6 col-md-12 store'
    } else {
      class_name = 'mb-50px col-md-4 store md-100'
    }
    let desc = `<div class="box-desc ad-long-sub">
                ${nadParas.BODY.length > 1 ? nadParas.BODY : ''}
              </div>`
    let html = `
    <div class="${class_name}">
      <div class="imagebox style1">
        <div class="box-imagebox">
          <div class="link_block">
            <a href="${nadParas.nurl}" class="link" target="_blank"></a>
            <div class="box-header">
              <div class="box-image">
                <img src="${nadParas.IMAGE960X640}" alt="">
                <a title="" style="cursor: pointer">查看廣告詳情</a>
                <div class="overlay"></div>
              </div>
            </div><!-- /.box-header -->
            <div class="box-content">
              <div class="box-title ad">
                <a href="${nadParas.nurl}" title="">${nadParas.SHORTSUBJECT.length > 1 ? nadParas.SHORTSUBJECT : ''}</a>
              </div>
              <div class="ad-short-sub">
              ${nadParas.LONGSUBJECT.length > 1 ? nadParas.LONGSUBJECT : ''}
              </div>
              ${nadParas.BODY.length > 1 ? desc : ''}
            </div><!-- /.box-content -->
          </div>
          <div class="imagebox_bottom">
            <p class="tag_block activity">
            <span class="tag">
            <a href="javascript:void(0);">廣告</a>
            </span>
            
            </p>
            <div class="clear"></div>
          </div>
          <!--                <ul class="location">-->
          <!--                  <li class="address"><span class="ti-location-pin"></span>電話: {{ el.phone }}</li>-->
          <!--                </ul>&lt;!&ndash; /.location &ndash;&gt;-->
        </div><!-- /.box-imagebox -->
      </div><!-- /.imagebox style1 -->
    </div>
    `

    $('.store-box').append(html)
  } else {
    let index = 1
    let offset = $('.store').length
    let max_offset = Math.min(offset + index, data_count)
    let search = window.location.search
    if (search) {
      search += `&limit=${index}&&offset=${offset}`
    } else {
      search += `?limit=${index}&&offset=${offset}`
    }
    $('.preloader').show()
    $.ajax({
      url: `/api/store/${search}`,
      type: "GET",
      contentType: "application/json; charset=utf-8",
      dataType: "json",
    }).done(res => {
      for (let data of res.results) {
        appendStore(data)
      }
      if (max_offset === data_count || !res.next) {
        $(".more-click").remove()
      }
      initStoreShare()
      $('.preloader').hide()
    })
  }
}

let initPosition = () => {
  let setError = () => {
    setCookie("lat", default_position.coords.latitude, 365)
    setCookie("lon", default_position.coords.longitude, 365)
    now_position = default_position
  }
  let setPosition = (position) => {
    setCookie("lat", position.coords.latitude, 365)
    setCookie("lon", position.coords.longitude, 365)
  }
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(setPosition, setError)
  } else {
    alert('您的瀏覽器不支援定位系統')
    setError()
  }
}

function getParameters(url) {
  const searchURL = new URL(url)

  // 透過物件的解構賦值，取出 URL 物件的屬性值
  const {href, protocol, hostname, pathname, search, searchParams} = searchURL
  let ret = {}
  // 透過陣列的解構賦值，取得網址參數部分
  for (let [key, value] of searchParams.entries()) {
    ret [key] = value
  }
  return ret
}

function setParameters(url, params) {
  let old_params = getParameters(url)
  for (let key in params) {
    old_params[key] = params[key]
  }

  const searchURL = new URL(url)
  let searchParams = new URLSearchParams(old_params)
  searchURL.search = searchParams
  return searchURL.href

}

function setCookie(cname, cvalue, exdays) {
  let d = new Date()
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000))
  let expires = "expires=" + d.toGMTString()
  // document.cookie = cname + "=" + cvalue + " " + expires
  document.cookie = cname + "=" + cvalue
}

function getCookie(cname) {
  let name = cname + "="
  let ca = document.cookie.split(';')
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim()
    if (c.indexOf(name) === 0) return c.substring(name.length, c.length)
  }
  return
}


// image
let appendImage = (res, $el) => {
  $el.append(`
  <div class="imgbox d-flex align-items-start" data-id="${res.id}" data-file="${res.filename}">
    <img src="/media/${res.filename}" alt="">
    <i class="fa fa-times pointer close-image" aria-hidden="true"
    data-id="${res.id}"
    ></i>
  </div>
  `)
}

let now_position = {}

let marker = []
let clearAllMarker = (map) => {
  while (marker.length) {
    let target = marker.pop()
    map.removeLayer(target)
  }
}
let getLatLngData = (params) => {
  $.ajax({
    url: `/api/store/latlng?lat=${params.lat}&lng=${params.lng}`,
    method: 'get'
  }).done(data => {
    clearAllMarker(_map)
    initStoreDataMarker(data)
  })
}

let initStoreDataMarker = (datas) => {
  for (let el of datas) {
    let ul = ''
    let i = 0
    if (el.storediscount) {
      for (let foo of el.storediscount) {
        i += 1
        if (i <= 3 && foo.name) {
          ul += `
            <ul>
                <li><span>${foo.name}</span></li>     
            </ul>
            `
        }
      }
    }
    let html = `
        <div>${el.name}</div>
        ${ul}
        <a href="/store/${el.id}"><button type="button" class="search-btn" id="search-btn">查看詳情</button></a>
        `
    const pos = L.marker([el.latitude, el.longitude], {icon: greenIcon}).bindPopup(html).openPopup()
    marker.push(pos)
    _map.addLayer(pos)
  }
}

let share = (social) => {
  const webTitle = `振興券`,
    webUrl = window.location.href
  let shareUrl = (social === 'line') ? `振興券：${webUrl}?openExternalBrowser=1` : webUrl
  window.open('https://www.addtoany.com/add_to/' + social + '?linkurl=' + shareUrl + '&amp;linkname=' + encodeURI(shareUrl))
}
let copy = (content) => {
  function isOS() {
    return navigator.userAgent.match(/ipad|iphone/i);
  }

  let textArea = document.createElement('textArea')
  let range
  let selection
  textArea.value = content
  document.body.appendChild(textArea)
  if (isOS()) {
    range = document.createRange()
    range.selectNodeContents(textArea)
    selection = window.getSelection()
    selection.removeAllRanges()
    selection.addRange(range)
    textArea.setSelectionRange(0, 999999)
  } else {
    textArea.select()
  }
  try {
    let successful = document.execCommand('copy');
    let msg = successful ? 'successful' : 'unsuccessful';
    this.$toast.success(this.$t('copy_coupon'))
  } catch (err) {
  }
  document.body.removeChild(textArea)
}

const showError = (error) => {
  const position = {
    coords: {
      latitude: '23.8523405',
      longitude: '120.9009427'
    },
    zoom: 7
  }
  switch (error.code) {
    case error.PERMISSION_DENIED:
      alert('讀取不到您目前的位置 PERMISSION_DENIED')
      showSelfPosition(position)
      break
    case error.POSITION_UNAVAILABLE:
      alert('讀取不到您目前的位置 POSITION_UNAVAILABLE')
      showSelfPosition(position)
      break
    case error.TIMEOUT:
      alert('讀取位置逾時')
      showSelfPosition(position)
      break
    case error.UNKNOWN_ERROR:
      alert('Error')
      showSelfPosition(position)
      break
  }
}
// 創建icon圖標
const greenIcon = new L.Icon({
  iconUrl: '/media/map_pin.svg',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})
const orangeIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})
const greyIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})
const blueMarker = L.icon.pulse({iconSize: [20, 20], color: '#F25B22', fillColor: '#F25B22'})
const initMap = (position) => {
  if (!_map) {
    _map = L.map('map')
  }
  const map = _map.setView([position.coords.latitude, position.coords.longitude], position.zoom || 17)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map)
  map.on('moveend', function (e) {
    if ($('#getLatLngData').length) {
      getLatLngData(this.getCenter())
    }
  })
  return map
}

const showSelfPosition = (position) => {
    const map = initMap(position)

    let popup = L.popup()

    // function onMapClick(e) {
    //   popup
    //     .setLatLng(e.latlng)
    //     .setContent("經緯度座標：" + e.latlng.toString())
    //     .openOn(map);
    // }
    //
    // map.on('click', onMapClick)


    // 設定所在位置的icon
    const selfPos = L.marker([position.coords.latitude, position.coords.longitude], {icon: blueMarker}).bindPopup('目前位置')
    map.addLayer(selfPos)

  }

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

          $('.header .container-fluid .row').after($mobileMenu);
          hasChildMenu.children('ul').hide();
          hasChildMenu.children('a').after('<span class="btn-submenu"></span>');
          $('.btn-menu').removeClass('active');
        } else {
          var $desktopMenu = $('#mainnav-mobi').attr('id', 'mainnav').removeAttr('style');

          $desktopMenu.find('.submenu').removeAttr('style');
          $('.nav-wrap .wrap-box-search').before($desktopMenu);
          $('.btn-submenu').remove();
        }
      }
    });
    let open_menu = false
    $('.btn-menu').on('click', function () {
      open_menu = !open_menu
      $('#mainnav-mobi').slideToggle(300);
      $(this).toggleClass('active');
      return false;
    });
    $(window).on('click', function () {
      if (open_menu) {
        $('#mainnav-mobi').slideToggle(300);
        $('.btn-menu').toggleClass('active');
        open_menu = !open_menu
      }
    })
    $('.header').on('click', function (event) {
      event.stopPropagation()
    })

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
    setTimeout(function () {
        $('.preloader').hide();
      }, 5000
    );
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

  jQuery.validator.addMethod("isEmail", function (value, element) {
    var email = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return this.optional(element) || email.test(value);
  }, "請填寫正確的信箱");

  jQuery.validator.addMethod("isPhone", function (value, element) {
    var tel = /[0-9]{2}\-[0-9]{7}/
    var phone = /^09\d{8}$/
    return this.optional(element) || tel.test(value) || phone.test(value);
  }, "請填寫正確的電話");

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
    let val = $('select[name="county"]').val()
    let county_name = $(`select[name="county"] option[value="${val}"]`).text()
    val = $('select[name="district"]').val()
    let district_name = $(`select[name="district"] option[value="${val}"]`).text()
    let changeLocation = () => {
      $('input[name="address"]').val(`${county_name}${district_name}`)
    }
    if ($("#createStore").length) {
      changeLocation()
    }


    $('select[name="county"]').on('change', function (e) {
      county_name = $(`select[name="county"] option[value="${e.target.value}"]`).text()
      changeLocation()
    })

    $('select[name="district"]').on('change', function (e) {
      district_name = $(`select[name="district"] option[value="${e.target.value}"]`).text()
      changeLocation()
    })


    // 活動折扣
    let appendDiscount = () => {
      dicount_count += 1
      discount_id += 1
      let options = ''
      for (let el of discount_type_list) {
        options += `<option value="${el.id}">${el.name}</option>`
      }
      $('.store-disocunt-area').append(`
      <div class="store-discount d-flex" data-id="${discount_id}">
        <div class="store-discount-content col">
          <div class="wrap-listing phone">
            <label>活動名稱</label>
            <input type="text" onkeydown="return event.key !== 'Enter';" name="store_discount_name" placeholder="請輸入活動名稱（20個字內）">         
            <div class="discount_type">
              <label>活動類型</label>
              <span class="ti-angle-down"></span>
              <select name="discount_type" placeholder="請選擇活動類型">
                ${options}
              </select>
            </div>
          </div><!-- /.wrap-listing -->
          <div class="wrap-listing your-name">
            <label>活動內容</label>
            <textarea rows="4" cols="5" name="description" placeholder="請輸入活動內容與注意事項">
【 活動內容 】：
【 活動期間 】：2020/7/15 ~ 2020/12/31
【 活動說明 】：
＊（請輸入活動說明，記得刪除本行）
＊（請輸入活動說明，記得刪除本行）
（1）
（2）
（3）
＊（請輸入活動說明，記得刪除本行）
（1）
（2）
（3）
【 活動網址 】：
            </textarea>
          </div><!-- /.wrap-listing -->
          <div class="clearfix"></div>
          <div class="wrap-listing" style="margin-bottom: 15px">
            <label>請上傳活動照片</label>
            <div class="browse">
              <div class="row store-discount-upload-images-${dicount_count}">
                <input type="hidden" name="discount_picture">
              </div>
              <p>拖曳圖片至此，或</p>
              <div class="upload">
                <span>選取圖片</span>
                <input type="file" name="discount-upload-file" data-class="store-discount-upload-images" data-target="file-uploader" accept="image/*" multiple="multiple"/>
              </div>
              <p class="mt-4">圖片建議上傳尺寸 2000 px x 1527 px ， 格式 .jpg .png ，小於 1 MB</p>
            </div>
            <div class="clearfix"></div>
          </div>
        </div>
        <div class="col-auto d-flex align-items-center">
        <i class="fa fa-times pointer close-image" aria-hidden="true"
        data-id="${discount_id}"
        ></i>
        </div>
      </div>
      `)
      // update 重複的code
      $('input[name="discount-upload-file"]').checkFileTypeAndSize({
        allowedExtensions: ['jpg', 'jpeg', 'png'],
        maxSize: 1024,
        success: function (self, e) {
          let form = new FormData()
          form.append("file", e.target.files[0])
          $('.preloader').show()
          $.ajax({
            method: 'POST',
            url: '/api/file/',
            processData: false,
            data: form,
            contentType: false, //required
          }).done((res) => {
            $('.preloader').hide()
            let cls_$el = $(self).parent().parent().find('.row')
            $(self).parent().parent().find('.row .imgbox').remove()
            cls_$el.find('input').val(res.filename)
            appendImage(res, cls_$el)
            setImageClick()
          }).fail(e => {
            $('.preloader').hide()
            let msg = '超過 1MB，請重新上傳圖片'
            Swal.fire({
              text: msg,
              confirmButtonText: '確定'
            })
          })
        },
        extensionerror: function () {
          let msg = '允許的格式為.jpg .png'
          Swal.fire({
            text: msg,
            confirmButtonText: '確定'
          })
        },
        sizeerror: function () {
          let msg = '超過 1MB，請重新上傳圖片'
          Swal.fire({
            text: msg,
            confirmButtonText: '確定'
          })
        }
      });

    }
    $('.store-discount .close-image').on('click', function () {
      let _id = $(this).attr('data-id')
      $(`.store-discount[data-id=${_id}]`).remove()
    })

    $('.store-discount-btn').on('click', () => {
      appendDiscount()
      $('.store-discount .close-image').off('click')
      $('.store-discount .close-image').on('click', function () {
        let _id = $(this).attr('data-id')
        $(`.store-discount[data-id=${_id}]`).remove()
      })

    })

    // update 重複的code
    let setImageClick = () => {
      $('.imgbox .close-image').off('click')
      $('.imgbox .close-image').on('click', function () {
        let _id = $(this).attr('data-id')
        $(`.imgbox[data-id="${_id}"]`).remove()
        files = files.filter(x => parseInt(x.id) !== parseInt(_id))
      })
    }
    setImageClick()
    // image file 上傳前確認
    // update 重複的code
    $('input[name="upload-file"]').checkFileTypeAndSize({
      allowedExtensions: ['jpg', 'jpeg', 'png'],
      maxSize: 1024,
      success: function (self, e) {
        let form = new FormData()
        let $el = $(self)
        form.append("file", e.target.files[0])
        $('.preloader').show()
        $.ajax({
          method: 'POST',
          url: '/api/file/',
          processData: false,
          data: form,
          contentType: false, //required
        }).done((res) => {
          $('.preloader').hide()
          files.push(res)
          let cls_name = $el.attr('data-class')
          let $cls_el = $(`.${cls_name}`)
          appendImage(res, $cls_el, '')
          setImageClick()
        }).fail(e => {
          $('.preloader').hide()
          let msg = '超過 1MB，請重新上傳圖片'
          Swal.fire({
            text: msg,
            confirmButtonText: '確定'
          })
        })
      },
      extensionerror: function () {
        let msg = '允許的格式為.jpg .png'
        Swal.fire({
          text: msg,
          confirmButtonText: '確定'
        })
      },
      sizeerror: function () {
        let msg = '超過 1MB，請重新上傳圖片'
        Swal.fire({
          text: msg,
          confirmButtonText: '確定'
        })
      }
    });

    $("#createStore").validate({
      rules: {
        name: "required",
        person: "required",
        address: "required",
        phone: {
          isPhone: true
        },
        email: {
          required: true,
          isEmail: true,
        },
        website: {
          url: true
        }
      },
      messages: {
        name: "請输入商家名稱",
        person: "請输入聯絡人姓名",
        address: "請输入地址",
        phone: "請输入正確電話格式",
        email: "請输入正確信箱格式",
        website: "請输入正確url格式",
      },
      submitHandler(form) {
        let data = $(form).serializeArray()
        // let ret = {}
        let ret = formSerailize(data)
        let storediscount = []
        if (ret.store_discount_name) {
          if (Array.isArray(ret.store_discount_name)) {
            for (let i = 0; i < ret.store_discount_name.length; i++) {
              let picture = ret.discount_picture !== undefined ? ret.discount_picture[i] : null;
              if (!picture) {
                picture = null
              }
              storediscount.push({
                name: ret.store_discount_name[i],
                description: ret.description[i],
                discount_type: ret.discount_type[i],
                picture: picture,
              })
            }
          } else {
            storediscount.push({
              name: ret.store_discount_name,
              description: ret.description,
              discount_type: ret.discount_type,
              picture: ret.discount_picture,
            })
          }


          delete ret.store_discount_name
          delete ret.description
          delete ret.discount_type
        }
        ret.storediscount_data = storediscount
        ret.storeimage_data = files.map(x => x.filename)
        ret.latitude = null
        ret.longitude = null
        $.ajax({
          url: '/api/store/',
          type: "POST",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(ret),
          dataType: "json",
        }).done(res => {
          Swal.fire({
            text: '您的資料已經成功送出！審核通過後將會刊登，請耐心等候哦！',
            confirmButtonText: '確定'
          }).then(() => {
            window.location.href = `/store/${res.id}/`
          })

        })
      }
    })


    $("#updateStore").validate({
      rules: {},
      messages: {},
      submitHandler(form) {
        let data = $(form).serializeArray()
        // let ret = {}
        let ret = formSerailize(data)
        let storediscount = []
        if (ret.store_discount_name) {
          if (Array.isArray(ret.store_discount_name)) {
            for (let i = 0; i < ret.store_discount_name.length; i++) {
              let picture = ret.discount_picture !== undefined ? ret.discount_picture[i] : null;
              if (!picture) {
                picture = null
              }
              storediscount.push({
                name: ret.store_discount_name[i],
                description: ret.description[i],
                discount_type: ret.discount_type[i],
                picture: picture,
              })
            }
          } else {
            storediscount.push({
              name: ret.store_discount_name,
              description: ret.description,
              discount_type: ret.discount_type,
              picture: ret.discount_picture,
            })
          }


          delete ret.store_discount_name
          delete ret.description
          delete ret.discount_type
        }
        ret.storediscount_data = storediscount
        let storeimage_data = []
        $('.upload-images .imgbox').each(function () {
          storeimage_data.push($(this).attr('data-file'))
        })
        ret.storeimage_data = storeimage_data
        ret.latitude = null
        ret.longitude = null
        $.ajax({
          url: `/api/store/${ret.id}/`,
          type: "PUT",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(ret),
          dataType: "json",
        }).done(res => {
          window.location.href = `/store/${res.id}/`
        })
      }
    })

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
        Swal.fire({
          text: '您的意見我們已經收到，我們將儘速聯繫您！',
          confirmButtonText: '確定'
        }).then(() => {
          window.location.href = '/'
        })
      })
    })
  }
  let storePage = () => {
    // store activity
    let search = new URLSearchParams(window.location.search).get('search')
    if (search) {
      $('input[name="search"]').val(search)
    }
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
      window.location.href = `${$('#search-form').attr('action')}?${querys.join('&')}`
    })
    let sformsubmit = false
    $('#search-form').on('submit', function (e) {
      if (sformsubmit) {
        e.preventDefault()
      }
      sformsubmit = true
    })


    initStoreShare()

    // add store
    let appendStore = (data) => {
      let class_name = ''
      if ($('#map').length) {
        class_name = 'mb-50px col-lg-6 col-md-12 store'
      } else {
        class_name = 'mb-50px col-md-4 store md-100'
      }
      let li = ''
      for (let el of data.activity) {
        if (el.name) {
          li += `<span class="tag"><a data-activity="${el.id}" href="">${el.name}</a></span>`
        }
      }
      let names = ''
      let store_type_disable = ''
      let i = 0
      if (data.storediscount) {
        for (let foo of data.storediscount) {
          i += 1
          if (i <= 3 && foo.name) {
            names += `
            <div class="sale-list">
              ${foo.name}
            </div>
            `
          }
        }
        if (data.store_type != 8 && data.store_type != 12 && data.store_type != 7 && data.store_type != 11 && data.district_name) {
          store_type_disable =
            `<li><span>${data.district_name}</span></li>
              <li>
                <img src="/media/map_gray.svg" alt="">
                <span>${data.distance_name}</span>
              </li>`
        }
        else {
          store_type_disable =
              `
              <li>
                <img src="/media/map_gray.svg" alt="">
                <span>${data.distance_name}</span>
              </li>`
        }

      }
      $(document).ready(() => {
        let href_split = window.location.href.split('?')
        $('.sort a').each(function () {
          let $el = $(this)
          let sort = $el.attr('data-sort')
          let newurl = setParameters(window.location.href, {sort: sort})
          $el.attr('href', newurl)
        })


        // init active sort
        let $el = $(`a[data-sort=${sort}]`)
        $el.addClass('active')


        $('.activity a').each(function () {
          let $el = $(this)
          let activity = $el.attr('data-activity')
          let newurl = setParameters(window.location.href, {activity: activity})
          $el.attr('href', newurl)
        })


        // init active activity
        $el = $(`a[data-activity=${activity}]`)
        $el.addClass('active')


      })

      let html = `
      <div class="${class_name}">
        <div class="imagebox style1">
          <div class="box-imagebox">
            <div class="link_block">
              <a href="/store/${data.id}" class="link" target="_blank"></a>
              <div class="box-header">
                <div class="box-image">
                  <img src="/media/${data.image_1}" alt="">
                  <a title="">查看詳情</a>
                  <div class="overlay"></div>
                </div>
              </div><!-- /.box-header -->
              <div class="box-content">
                <div class="box-title ad">
                  <a href="/store/${data.id}" title="">${data.name}</a>
                </div>
                <ul class="rating">
                  ${store_type_disable}
                  <li>
                    <img src="/media/gray_${data.store_type_icon}" alt="">
                    <span>${data.store_type_name}</span>
                  </li>
                </ul>
                <div class="box-desc">
                  ${names}
                </div>
              </div><!-- /.box-content -->
            </div>
            <div class="imagebox_bottom">
              <p class="tag_block activity">
                ${li}
              </p>
              <div class="right">
                <input type="checkbox" class="checkbox" id="share_${data.id}">
                <label for="share_${data.id}" class="label entypo-export">
                  <!--                      <a href="">分享</a>-->
                  分享
                </label>
                <div class="social">
                  <ul>
                    <li class="share-to entypo-line" data-sns="line" data-name="${data.name}"
                        data-url="store/${data.id}">
                      <img src="/media/share_line.svg" alt="">
                    </li>
                    <li class="share-to entypo-facebook" data-sns="facebook" data-name="${data.name}"
                        data-url="store/${data.id}">
                      <img src="/media/share_fb.svg" alt="">
                    </li>
                    <li class="share-url entypo-url" data-name="${data.name}" data-url="store/${data.id}">
                      <img src="/media/share_url.svg" alt="">
                    </li>
                  </ul>
                </div>
              </div>
              <div class="clear"></div>
            </div>
            <!--                <ul class="location">-->
            <!--                  <li class="address"><span class="ti-location-pin"></span>電話: {{ el.phone }}</li>-->
            <!--                </ul>&lt;!&ndash; /.location &ndash;&gt;-->
          </div><!-- /.box-imagebox -->
        </div><!-- /.imagebox style1 -->
      </div>
      `
      $('.store-box').append(html)
    }
    $(".more-click").on('click', () => {
      let index = 5
      let offset = $('.store').length
      let max_offset = Math.min(offset + index, data_count)
      let search = window.location.search
      if (search) {
        search += `&limit=${index}&&offset=${offset}`
      } else {
        search += `?limit=${index}&&offset=${offset}`
      }
      $('.preloader').show()
      $.ajax({
        url: `/api/store/${search}`,
        type: "GET",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
      }).done(res => {
        for (let data of res.results) {
          appendStore(data)
        }
        getNativeAdParas('Q1594362301761yK', nativeAdCallback)
        // if ($('#map').length) {
        //   initStoreDataMarker(res.results)
        // }
        if (max_offset === data_count || !res.next) {
          $(".more-click").remove()
        }
        initStoreShare()
        $('.preloader').hide()
      })

    })

    // initStoreDataMarker(store_data)
  }
  let searchAPI = () => {
    $('.search-pin-icon, .search-pin-load').on('click', function () {
      initPosition()
      let $el = $(this)
      $el.find('svg').hide()
      let $load = $el.next().find('div')
      $load.addClass('loader')
      let msg = ''
      // 等經緯度取得到
      while (true) {
        try {
          let lat = getCookie('lat')
          let lon = getCookie('lon')
          msg = `${lat}, ${lon}`
          break
        } catch (e) {
        }
      }
      $.ajax({
        url: `/api/location/?task_type=2&msg=${msg}`,
        type: "GET",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
      }).done(res => {
        let $input = $el.prev()
        $input.val(res.data.address.replace('台', '臺'))
        $load.removeClass('loader')
        $el.find('svg').show()
      })

    })
  }
  let initPreloaderListenr = () => {
    let ignore_onbeforeunload = false;
    $('a[href^=mailto]').on('click', function () {
      ignore_onbeforeunload = true;
    })

    $(window).on('beforeunload', function (e) {
      if (!ignore_onbeforeunload) {
        $('.preloader').show()
      }
      ignore_onbeforeunload = false
    })
  }
  let initToScroll = () => {
    if ($('#toscroll') && $('#toscroll')[0]) {
      setTimeout(() => {
        $('#toscroll')[0].scrollIntoView()
      }, 1000)
    }
  }


  $.fn.checkFileTypeAndSize = function (options) {
    //默认设置
    var defaults = {
      allowedExtensions: [],
      maxSize: 1024, //单位是KB，默认最大文件尺寸1MB=1024KB
      success: function () {
      },
      extensionerror: function () {
      },
      sizeerror: function () {
      }
    }
    //合并设置
    options = $.extend(defaults, options)
    //遍历元素
    return this.each(function () {
      $(this).on('change', function (e) {
        //获取文件路径
        var filePath = $(this).val()
        if (!filePath) {
          return
        }
        //小写字母的文件路径
        var fileLowerPath = filePath.toLowerCase()
        //获取文件的后缀名
        var extension = fileLowerPath.substring(fileLowerPath.lastIndexOf('.') + 1)
        //判断后缀名是否包含在预先设置的、所允许的后缀名数组中
        if ($.inArray(extension, options.allowedExtensions) == -1) {
          options.extensionerror()
          $(this).focus()
        } else {
          try {
            var size = 0
            if (false) {//ie旧版浏览器
              var fileMgr = new ActiveXObject("Scripting.FileSystemObject")
              var fileObj = fileMgr.getFile(filePath)
              size = fileObj.size //byte
              size = size / 1024//kb
              //size = size / 1024//mb
            } else {//其它浏览器
              size = $(this)[0].files[0].size//byte
              size = size / 1024//kb
              //size = size / 1024//mb
            }
            if (size > options.maxSize) {
              options.sizeerror()
            } else {
              options.success(this, e)
            }
          } catch (e) {
            alert("错误：" + e)
          }
        }
      })
    })
  }
  let initAD = () => {
    $('#footer-ad').append(
      `
      <div class="d-none d-lg-block col-md-12" style=" position: relative; text-align: center; margin-top:80px;">
        <ins class="scupioadslot" style="display:inline-block;width:970px;height:90px;"
             data-sca-pub="lQgDGBIrQDI="
             data-sca-web="5143"
             data-sca-category="24"
             data-sca-cid="18233"
             data-sca-slot-type="STA">
        </ins>
        <script async src="https://img.scupio.com/js/ad.js"></script>
      </div><!-- /.col-md-12 -->
    `)
  }
  let checkSearch = () => {
    if ($(" #search ").val() == '' && !$(" #updateStore ").length) {
      $('.search-pin-icon').click()
      $('.search-pin-load').click()
    }
  }


  $(function () {
    initPreloaderListenr();
    responsiveMenu();
    headerFixed();
    slideTeam();
    searchButton();
    filterToggle();
    CountDown();
    // googleMap();
    // slideSearch();
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
    initToScroll();
    searchAPI();
    initAD();
    checkSearch();
  });

})(jQuery);
