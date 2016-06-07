"use strict";
////////////////// ADD ATTRACTION to database///////////////////////////
$(document).ready(function(){


console.log("JS Connected");
function addAttractionSuccess (result) {
  console.log("added");
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
  $(this).find(".glyphicon-heart").css("color", "salmon");

}

$('.saveAttractionModalBtn').click(addAttraction);

////////////////// ADD EVENT to database ///////////////////////////

function addEventSuccess (result) {
  console.log('added');
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


    $(this).find(".glyphicon-heart").css("color", "salmon");

}

$('.saveEventModalBtn').click(addEvent);



////////////////// DEL attraction from database ///////////////////////////
function removeAttrSuccess (result) {
  var attractionId = result;
  var divToDelete = $("div[data-id=" + attractionId + "]");
  var attractions = $(".att-results-agenda");
  if (attractions.length === 1) {
    console.log("YOOOOOO");
    $('#header-attraction').hide();
  }
  divToDelete.remove();
}

function delAttr (evt) {
  var attrId = $(this).data('id');
  var attr = {
    'attraction_id': attrId}

  console.log(attr)
  $.post('/delete_attr', attr, removeAttrSuccess)
  }

$('.delete-att').click(delAttr);

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
    'event_id': eventId
  }

  $.post('/delete_event', ev, removeEventSuccess)
  }

$('.delete-ev').click(delEvent);


///////////////////Modal Details/Map Attraction /////////////////////////////


function makeAttModalMap(evt){
  var resultId = $(this).data('attractionId');
  console.log(resultId);
  initMaps[resultId]();
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
  var eventId = $(this).data('eventId');
  console.log(eventId);
  initMaps[eventId]();
}

function populateEvModal(evt){
  var eventId = $(this).data('eventId');
  var modalToModalize = $('#eventModal'+eventId);
  modalToModalize.on('shown.bs.modal', makeEvModalMap).modal('show');
  //map things
}

$('.triggerEvModal').on('click', populateEvModal);

/////////////////// Change Heart Color for SAVE /////////////////////////////
});
