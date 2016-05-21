////////////////// ADD ATTRACTION to database///////////////////////////

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


$('.yelp-results-btn').click(addAttraction);

////////////////// ADD EVENT to database ///////////////////////////

function addEventSuccess (result) {
  alert("YAY");
}

function addEvent (evt) {
  var eventId = $(this).data('id');
  var nameId = $(this).data('name');
  var startId = $(this).data('start');
  var statusId = $(this).data('status');
  var urlId = $(this).data('url');
  var localeId = $(this).data('locale');
 
  
  var evt = {'id': eventId,
            'name': nameId,
            'start': startId,
            'status':statusId,
            'url': urlId,
            'locale': localeId}
  
  $.post('/add_to_events', evt, addEventSuccess)
}

$('.eventbrite-results-btn').click(addEvent);



////////////////// DEL event from database ///////////////////////////
function removeAttrSuccess (result) {
  console.log('removed');
  alert('gone girl');
}

function delAttr (evt) {
  var attrId = $(this).data('id');
  var attr = {
    'attraction_id': attrId}

  console.log(attr)
  $.post('/delete_attr', attr, removeAttrSuccess)
  }

$('#delatt').click(delAttr);




