"use strict";
////////////////// ADD ATTRACTION to database///////////////////////////
console.log("JS Connected");
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

$('#delete-att').click(delAttr);

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



///////////////////Modal Details/Map Attraction /////////////////////////////

// function makeAttModalMap(evt){
//   var resultId = $(this).data('attractionId');
//   initMap(resultId);
// }

// function populateAttModal(evt){
//   var attractionId = $(this).data('attractionId');
//   var modalToModalize = $('#attractionModal'+attractionId);
//   modalToModalize.on('shown.bs.modal', makeAttModalMap).modal('show');
//   //map things
// }

// $('.triggerAttModal').on('click', populateAttModal);


// ///////////////////Modal Details/Map Attraction /////////////////////////////

// function makeEvModalMap(evt){
//   var resultId = $(this).data('eventId');
//   initMap(resultId);
// }

// function populateEvModal(evt){
//   var eventId = $(this).data('eventId');
//   var modalToModalize = $('#eventModal'+eventId);
//   modalToModalize.on('shown.bs.modal', makeEvModalMap).modal('show');
//   //map things
// }

// $('.triggerEvModal').on('click', populateEvModal);

// ///////////// Google Maps in Modals ///////////////////////////////////////////

// var map;
// var myLatLng = new google.maps.LatLng(37.788668, -122.411499);

// function initMap(resultId, yelp_results) {
//   map = new google.maps.Map(document.getElementById('map'+resultId), {
//     center: myLatLng,
//     zoom: 5,
//   });

//   for (place in responses) {

//   var markers = new google.maps.Marker({
//       position: {
//         lat: business['location']['coordinate']['latitude']
//         lng: business['location']['coordinate']['longitude']
//       }
//       map: map
//    });

//   google.maps.event.trigger(map, 'resize');
//   map.setCenter(myLatLng);
//   google.maps.visualRefresh = true;
// }

// };

function makeAttModalMap(evt){
  var resultId = $(this).data('attractionId');
  initMap(resultId);
}

function populateAttModal(evt){
  var attractionId = $(this).data('attractionId');
  var modalToModalize = $('#attractionModal'+attractionId);
  modalToModalize.on('shown.bs.modal', makeAttModalMap).modal('show');
  //map things
}

$('.triggerAttModal').on('click', populateAttModal);


///////////////////Modal Details/Map Attraction /////////////////////////////

function makeEvModalMap(evt){
  var resultId = $(this).data('eventId');
  initMap(resultId);
}

function populateEvModal(evt){
  var eventId = $(this).data('eventId');
  var modalToModalize = $('#eventModal'+eventId);
  modalToModalize.on('shown.bs.modal', makeEvModalMap).modal('show');
  //map things
}

$('.triggerEvModal').on('click', populateEvModal);



