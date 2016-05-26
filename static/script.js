"use strict";
////////////////// ADD ATTRACTION to database///////////////////////////
console.log("JS Connected")
function addAttractionSuccess (result) {
  alert("YAY");
}

function addAttraction (evt) {
  var attractionId = $(this).data('id');
  var nameId = $(this).data('name');
  var locationId = $(this).data('location');
  var latitudeId = $(this).data('latitude');
  var longitudeId = $(this).data('longitude');
  var ratingId = $(this).data('rating');
  var reviewId = $(this).data('review-count');
  var urlId = $(this).data('url');
  var imageurlId = $(this).data('img');
  var phoneId = $(this).data('phone');
  

  var attr = {'id': attractionId,
              'name': nameId,
              'location': locationId,
              'latitude:': latitudeId,
              'longitude': longitudeId,
              'rating': ratingId,
              'review_count': reviewId,
              'url': urlId,
              'image_url': imageurlId,
              'phone': phoneId
            }
  // console.log(addAttraction)

  $.post("/add_to_attractions", attr, addAttractionSuccess)
}


$('.saveAttractionModalBtn').click(addAttraction);

////////////////// ADD EVENT to database ///////////////////////////

function addEventSuccess (result) {
  alert("YAY");
}

function addEvent (evt) {
  console.log("JAVASCRIPT FUNCTION")
  var eventId = $(this).data('id');
  var nameId = $(this).data('name');
  var startId = $(this).data('start');
  var statusId = $(this).data('status');
  var urlId = $(this).data('url');
  var localeId = $(this).data('locale');
 
  
  var myEvent = {'id': eventId,
            'name': nameId,
            'start': startId,
            'status':statusId,
            'url': urlId,
            'locale': localeId}
  
  $.post('/add_to_events', myEvent, addEventSuccess)
}

$('#saveEventModalBtn').click(addEvent);



////////////////// DEL attraction from database ///////////////////////////
function removeAttrSuccess (result) {
  var attractionId = result;
  var divToDelete = $("div[data-id=" + attractionId + "]");
  divToDelete.remove();
  alert('gone girl');
}

function delAttr (evt) {
  var attrId = $(this).data('id');
  var attr = {
    'attraction_id': attrId}

  console.log(attr)
  $.post('/delete_attr', attr, removeAttrSuccess)
  }

$('.att-results').click(delAttr);

////////////////// DEL event from database ///////////////////////////
function removeEventSuccess (result) {
  var eventId = result
  console.log(eventId);
  var divToDelete = $("div[data-id=" + eventId + "]");
  divToDelete.remove();
}

function delEvent (evt) {
  var eventId = $(this).data('id');
  var ev = {
    'event_id': eventId}

  $.post('/delete_event', ev, removeEventSuccess)
  }

$('.event-results').click(delEvent);



///////////////////Modal Details/Save Attraction /////////////////////////////
$('#attractionModal').each(function(){
  $(this).modal(options);
});

var options = {
    "backdrop" : "static"
}

///////////////////Modal Detail/Save Event /////////////////////////////
$('#eventModal').each(function(){
  $(this).modal(options);
});

var options = {
    "backdrop" : "static"
}



///////////// Google Maps JS ///////////////////////////////////////////

// $(document).on('ready', function() {
//   $('#attractionModal').on('click', function(evt) {
//     alert('worked');
//   });
// });
var map;
var mylocation;

function initMap() {

  // Specify where the map is centered
  mylocation = {lat: 37.7, lng: 122.4};
  // Create a map object and specify the DOM element for display.
  // center and zoom are required.
  map = new google.maps.Map(document.getElementById('map'), {
    center: mylocation,
    zoom: 5,
  });
  google.maps.event.trigger(map, "resize");
}


$(".openModal").on('click', function (){
  // $(nth child which is the modal body).append("<div id="map"></div>")
  $(this).data('id');
  initMap();
  google.maps.event.trigger(map, "resize");
  map.setCenter(mylocation);
})

// google.maps.event.addDomListener(modal, 'load', initMap);





