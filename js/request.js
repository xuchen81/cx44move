function MoveRequest() {
  this.requestPlaces = function(data) {
  	var day = data['first'];
  	$.ajax({
  	  type: 'POST',
  	  url: '/requestHandle',
  	  data: data,
      dataType: 'json',
  	  success: function(data) {
        var places = data;
  	    var mapLoader = new MapLoader(day);
  	    mapLoader.loadingPlaces(places);
  	  },
  	  error: function(data) {
  	  	console.log(data);
  	  }
  	});
  }
}
